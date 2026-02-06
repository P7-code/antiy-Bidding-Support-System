"""
知识库管理页面模块
提供知识库文件查看、索引编辑、手动扫描等功能
"""
import streamlit as st
import os
import sys
from datetime import datetime

# 添加 src 到路径（如果还没有）
# 支持多种部署环境
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from tools.knowledge_indexer import KnowledgeIndexer
    from tools.knowledge_scheduler import get_scheduler, start_scheduler, stop_scheduler
except ImportError:
    # 如果上面的导入失败，尝试从 src.tools 导入
    try:
        from src.tools.knowledge_indexer import KnowledgeIndexer
        from src.tools.knowledge_scheduler import get_scheduler, start_scheduler, stop_scheduler
    except ImportError:
        # 最后的尝试：直接从项目根目录导入
        import sys
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        from tools.knowledge_indexer import KnowledgeIndexer
        from tools.knowledge_scheduler import get_scheduler, start_scheduler, stop_scheduler


def show_knowledge_management_page(kb_path: str):
    """
    显示知识库管理页面
    
    Args:
        kb_path: 知识库路径
    """
    st.markdown('<h1 class="main-header">📚 知识库管理</h1>', unsafe_allow_html=True)

    # 初始化知识库索引器
    indexer = KnowledgeIndexer(kb_path)

    # 显示选项卡
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 知识库概览",
        "📄 文件索引",
        "✏️ 编辑索引",
        "⚙️ 定时任务"
    ])

    # Tab 1: 知识库概览
    with tab1:
        render_overview_tab(indexer)

    # Tab 2: 文件索引
    with tab2:
        render_files_tab(indexer, kb_path)

    # Tab 3: 编辑索引
    with tab3:
        render_edit_tab(indexer)

    # Tab 4: 定时任务
    with tab4:
        render_scheduler_tab(indexer, kb_path)


def render_overview_tab(indexer: KnowledgeIndexer):
    """渲染概览标签页"""
    st.markdown('<h2 class="section-header">📊 知识库概览</h2>', unsafe_allow_html=True)

    stats = indexer.get_statistics()

    # 统计卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📁 总文件数",
            value=f"{stats['total_files']}",
            delta=None
        )

    with col2:
        size_mb = stats['total_size'] / 1024 / 1024
        st.metric(
            label="💾 总大小",
            value=f"{size_mb:.2f} MB",
            delta=None
        )

    with col3:
        st.metric(
            label="🔧 技术文档",
            value=f"{stats['technical_count']}",
            delta=None
        )

    with col4:
        st.metric(
            label="💼 商务文档",
            value=f"{stats['commercial_count']}",
            delta=None
        )

    # 文件类型分布
    st.markdown('<h3 class="subsection-header">📈 文件类型分布</h3>', unsafe_allow_html=True)

    file_types = stats.get('file_types', {})
    if file_types:
        col1, col2 = st.columns(2)

        with col1:
            import plotly.express as px
            import plotly.graph_objects as go

            fig = go.Figure(data=[
                go.Bar(
                    x=list(file_types.keys()),
                    y=list(file_types.values()),
                    marker_color='#1f77b4'
                )
            ])

            fig.update_layout(
                title='文件类型统计',
                xaxis_title='文件类型',
                yaxis_title='文件数量',
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            for ftype, count in file_types.items():
                st.markdown(f"**{ftype.upper()}**: {count} 个文件")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("暂无文件")

    # 最后更新时间
    st.markdown('<h3 class="subsection-header">🕐 系统信息</h3>', unsafe_allow_html=True)
    st.markdown(f"**最后更新**: {stats.get('last_updated', '从未更新')}")
    st.markdown(f"**索引版本**: {stats.get('version', 'N/A')}")


def render_files_tab(indexer: KnowledgeIndexer, kb_path: str):
    """渲染文件索引标签页"""
    st.markdown('<h2 class="section-header">📄 文件索引列表</h2>', unsafe_allow_html=True)

    indices = indexer.get_all_indices()

    # 搜索和过滤
    col1, col2, col3 = st.columns(3)

    with col1:
        search_query = st.text_input("🔍 搜索文件", placeholder="输入文件名或关键词...")

    with col2:
        filter_direction = st.selectbox(
            "📂 知识方向",
            ["全部", "技术", "商务", "两者"]
        )

    with col3:
        filter_type = st.selectbox(
            "📄 文件类型",
            ["全部", "pdf", "docx", "pptx", "txt"]
        )

    # 过滤索引
    filtered_indices = []
    for index_id, index in indices.items():
        # 搜索过滤
        if search_query:
            query_lower = search_query.lower()
            if query_lower not in index.metadata.file_name.lower():
                # 检查标签和摘要
                found = False
                for tag in index.search_tags:
                    if query_lower in tag.lower():
                        found = True
                        break
                if not found and query_lower not in index.content_summary.full_summary.lower():
                    continue

        # 方向过滤
        if filter_direction != "全部":
            direction_map = {"技术": "technical", "商务": "commercial", "两者": "both"}
            if index.direction != direction_map[filter_direction]:
                continue

        # 类型过滤
        if filter_type != "全部":
            if index.metadata.file_type != filter_type:
                continue

        filtered_indices.append(index)

    # 显示索引列表
    if filtered_indices:
        for index in filtered_indices:
            with st.expander(
                f"📄 {index.metadata.file_name} "
                f"({index.metadata.file_type.upper()}) "
                f"- {index.direction}",
                expanded=False
            ):
                # 文件信息
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"**大小**: {index.metadata.file_size / 1024:.2f} KB")

                with col2:
                    st.markdown(f"**类型**: {index.metadata.file_type.upper()}")

                with col3:
                    status = "✅ 启用" if index.is_active else "❌ 禁用"
                    st.markdown(f"**状态**: {status}")

                # 摘要
                st.markdown('<h4 class="small-header">📝 摘要</h4>', unsafe_allow_html=True)
                st.markdown(index.content_summary.full_summary)

                # 关键词
                if index.content_summary.technical_keywords:
                    st.markdown('<h4 class="small-header">🔧 技术关键词</h4>', unsafe_allow_html=True)
                    st.markdown(", ".join([f"`{kw}`" for kw in index.content_summary.technical_keywords]))

                if index.content_summary.commercial_keywords:
                    st.markdown('<h4 class="small-header">💼 商务关键词</h4>', unsafe_allow_html=True)
                    st.markdown(", ".join([f"`{kw}`" for kw in index.content_summary.commercial_keywords]))

                # 标签
                if index.search_tags:
                    st.markdown('<h4 class="small-header">🏷️ 搜索标签</h4>', unsafe_allow_html=True)
                    st.markdown(", ".join([f"`{tag}`" for tag in index.search_tags]))

                # 操作按钮
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"编辑", key=f"edit_{index.id}"):
                        st.session_state.edit_index_id = index.id

                with col2:
                    if st.button(f"删除", key=f"delete_{index.id}"):
                        if st.session_state.get('confirm_delete', False):
                            indexer.delete_index(index.id)
                            st.success("✅ 已删除索引")
                            st.session_state.confirm_delete = False
                            st.rerun()
                        else:
                            st.session_state.confirm_delete = True
                            st.warning("⚠️ 再次点击确认删除")

                st.divider()
    else:
        st.info("🔍 未找到匹配的文件")

    # 手动扫描按钮
    st.markdown('<h3 class="subsection-header">🔄 手动操作</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 立即扫描文件", type="primary"):
            # 直接执行扫描，不依赖调度器
            try:
                with st.spinner("正在扫描文件..."):
                    # 扫描文件变化
                    all_files, new_files, modified_files, deleted_files = indexer.scan_files()

                    if not new_files and not modified_files:
                        st.info("📄 没有发现新文件或修改的文件")
                    else:
                        st.info(f"发现变化: {len(new_files)} 个新文件, {len(modified_files)} 个修改文件")

                        # 处理文件
                        processed_count = 0
                        for file_metadata in new_files + modified_files:
                            try:
                                # 提取内容
                                content, structure = indexer.extract_file_content(file_metadata)

                                if content:
                                    # 调用 LLM 提取摘要
                                    from graphs.nodes.knowledge_manager_nodes import extract_summary_node
                                    from graphs.state_knowledge import ExtractSummaryInput
                                    from langchain_core.runnables import RunnableConfig
                                    from tools.knowledge_scheduler import MockRuntime

                                    try:
                                        from coze_coding_utils.runtime_ctx.context import Context
                                    except ImportError:
                                        class Context:
                                            pass

                                    node_input = ExtractSummaryInput(
                                        file_metadata=file_metadata,
                                        file_content=content,
                                        file_structure=structure
                                    )

                                    import os
                                    import json
                                    config_path = os.path.join(
                                        os.getenv("COZE_WORKSPACE_PATH", "."),
                                        "config/knowledge_summary_cfg.json"
                                    )

                                    config = RunnableConfig(
                                        metadata={"llm_cfg": config_path}
                                    )

                                    # 创建 Mock Runtime
                                    try:
                                        runtime = MockRuntime(Context(
                                            run_id="manual_scan_run_id",
                                            space_id="manual_scan_space_id",
                                            project_id="manual_scan_project_id"
                                        ))
                                    except TypeError:
                                        # 如果 Context 不需要参数
                                        runtime = MockRuntime(Context())

                                    result = extract_summary_node(node_input, config, runtime)

                                    if result.summary:
                                        # 创建标签
                                        search_tags = []
                                        search_tags.extend(result.summary.technical_keywords)
                                        search_tags.extend(result.summary.commercial_keywords)
                                        search_tags.extend(result.summary.industry_tags)

                                        # 创建索引
                                        from graphs.state_knowledge import KnowledgeIndex
                                        index = KnowledgeIndex(
                                            id=file_metadata.file_hash,
                                            metadata=file_metadata,
                                            content_summary=result.summary,
                                            search_tags=search_tags,
                                            direction=result.direction,  # type: ignore
                                            quality_score=0.8,
                                            is_active=True
                                        )

                                        indexer.add_index(index)
                                        processed_count += 1
                                    else:
                                        st.warning(f"⚠️ 无法提取摘要: {file_metadata.file_name}")
                            except Exception as e:
                                st.error(f"❌ 处理文件失败 {file_metadata.file_name}: {e}")

                        # 删除已删除的文件索引
                        for file_hash in deleted_files:
                            indexer.delete_index(file_hash)

                        if processed_count > 0:
                            st.success(f"✅ 扫描完成，成功处理 {processed_count} 个文件")
                            st.rerun()
                        else:
                            st.warning("⚠️ 扫描完成，但没有成功处理任何文件")

            except Exception as e:
                st.error(f"❌ 扫描失败: {e}")

    with col2:
        if st.button("📥 手动上传文件"):
            st.info("请将文件上传到 datafiles 目录，然后点击扫描")


def render_edit_tab(indexer: KnowledgeIndexer):
    """渲染编辑索引标签页"""
    st.markdown('<h2 class="section-header">✏️ 编辑索引</h2>', unsafe_allow_html=True)

    indices = indexer.get_all_indices()

    # 选择要编辑的索引
    index_options = [f"{idx.metadata.file_name} ({idx.id[:8]}...)" for idx in indices.values()]
    index_options.insert(0, "请选择索引")

    selected_option = st.selectbox("选择要编辑的索引", index_options)

    if selected_option == "请选择索引":
        st.info("请先选择一个索引进行编辑")
        return

    # 获取选中的索引
    selected_index = None
    for index in indices.values():
        if f"{index.metadata.file_name} ({index.id[:8]}...)" == selected_option:
            selected_index = index
            break

    if not selected_index:
        st.error("未找到选中的索引")
        return

    # 编辑表单
    st.markdown('<h3 class="subsection-header">📝 编辑内容</h3>', unsafe_allow_html=True)

    with st.form(key="edit_index_form"):
        # 摘要
        full_summary = st.text_area(
            "全文摘要",
            value=selected_index.content_summary.full_summary,
            height=150,
            help="文档的全文摘要"
        )

        # 标签
        tags_text = st.text_area(
            "搜索标签",
            value=", ".join(selected_index.search_tags),
            height=100,
            help="用逗号分隔多个标签"
        )

        # 方向
        direction = st.selectbox(
            "知识方向",
            ["technical", "commercial", "both"],
            index=["technical", "commercial", "both"].index(selected_index.direction),
            help="文档的主要知识方向"
        )

        # 状态
        is_active = st.checkbox("启用索引", value=selected_index.is_active)

        # 质量评分
        quality_score = st.slider(
            "质量评分",
            min_value=0.0,
            max_value=1.0,
            value=selected_index.quality_score,
            step=0.1,
            help="文档的质量评分（0-1）"
        )

        # 提交按钮
        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("💾 保存更改", type="primary")

        with col2:
            cancel = st.form_submit_button("取消")

        if submit:
            # 构建更新内容
            updates = {
                'summary': full_summary,
                'tags': [tag.strip() for tag in tags_text.split(',') if tag.strip()],
                'direction': direction,
                'is_active': is_active,
                'quality_score': quality_score
            }

            # 更新索引
            success = indexer.edit_index(selected_index.id, updates)

            if success:
                st.success("✅ 索引更新成功")
                st.rerun()
            else:
                st.error("❌ 索引更新失败")


def render_scheduler_tab(indexer: KnowledgeIndexer, kb_path: str):
    """渲染定时任务标签页"""
    st.markdown('<h2 class="section-header">⚙️ 定时任务配置</h2>', unsafe_allow_html=True)

    # 显示调度器状态
    scheduler = get_scheduler()

    if scheduler:
        st.info(f"✅ 调度器正在运行")
        st.markdown(f"**扫描间隔**: {scheduler.interval_minutes} 分钟")
    else:
        st.warning("⚠️ 调度器未启动")

    # 配置选项
    st.markdown('<h3 class="subsection-header">⚙️ 配置</h3>', unsafe_allow_html=True)

    interval_minutes = st.number_input(
        "扫描间隔（分钟）",
        min_value=1,
        max_value=1440,
        value=15,
        help="自动扫描知识库目录的时间间隔"
    )

    # 操作按钮
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 启动调度器", type="primary"):
            if not scheduler:
                start_scheduler(interval_minutes=interval_minutes)
                st.success("✅ 调度器已启动")
                st.rerun()
            else:
                st.info("调度器已在运行")

    with col2:
        if st.button("⏹️ 停止调度器"):
            if scheduler:
                stop_scheduler()
                st.success("✅ 调度器已停止")
                st.rerun()
            else:
                st.info("调度器未运行")

    with col3:
        if st.button("🔄 立即扫描"):
            if scheduler:
                scheduler.run_once()
                st.success("✅ 扫描完成")
                st.rerun()
            else:
                st.warning("⚠️ 请先启动调度器")

    # 日志查看
    st.markdown('<h3 class="subsection-header">📋 运行日志</h3>', unsafe_allow_html=True)

    log_file = "datafiles/knowledge_scheduler.log"

    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()

        # 显示最近 50 行日志
        log_lines = log_content.split('\n')
        recent_logs = '\n'.join(log_lines[-50:])

        st.text_area(
            "最近日志",
            value=recent_logs,
            height=300,
            help="显示最近的运行日志"
        )
    else:
        st.info("暂无日志")
