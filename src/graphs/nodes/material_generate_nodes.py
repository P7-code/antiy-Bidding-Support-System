"""
投标材料生成节点
包含：招标文件解析、知识库检索、互联网搜索、材料生成等节点
"""
import os
import json
import re
import logging
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_dev_sdk import SearchClient

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建文件处理器（使用绝对路径，确保目录存在）
log_dir = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), "app/work/logs/bypass")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

log_handler = logging.FileHandler(log_file, encoding='utf-8')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(log_handler)

from graphs.state import GlobalState
from graphs.state_materials import (
    TenderRequirementsParseInput,
    TenderRequirementsParseOutput,
    KnowledgeBaseSearchInput,
    KnowledgeBaseSearchOutput,
    CommercialKBSearchInput,
    CommercialKBSearchOutput,
    TechnicalKBSearchInput,
    TechnicalKBSearchOutput,
    WebSearchInput,
    WebSearchOutput,
    CommercialWebSearchOutput,
    TechnicalWebSearchOutput,
    CommercialMaterialGenerateInput,
    CommercialMaterialGenerateOutput,
    TechnicalMaterialGenerateInput,
    TechnicalMaterialGenerateOutput
)
from tools.knowledge_base_tool import KnowledgeBaseTool
from tools.knowledge_indexer import KnowledgeIndexer
from graphs.node import call_llm


def get_config_file_path(config_name: str) -> str:
    """获取配置文件路径"""
    return os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config_name)


def generate_reference_list(kb_results: list) -> str:
    """
    生成引用文件清单

    Args:
        kb_results: 知识库检索结果列表

    Returns:
        格式化的引用文件清单字符串
    """
    if not kb_results:
        return ""

    # 收集引用的文件信息
    referenced_files = []
    for idx, result in enumerate(kb_results, 1):
        source = result.get('source', {})
        file_name = source.get('file_name', '未知文件')
        file_path = source.get('file_path', '未知路径')
        file_type = source.get('file_type', '未知')
        citation = result.get('citation', '')

        # 获取章节信息
        chapters = result.get('chapters', [])
        chapter_info = []
        if chapters:
            for ch in chapters[:5]:  # 最多显示5个章节
                chapter_title = ch.get('chapter_title', '未知章节')
                page_range = ch.get('page_range', 'N/A')
                chapter_info.append(f"    - {chapter_title} (页码: {page_range})")

        referenced_files.append({
            'idx': idx,
            'file_name': file_name,
            'file_path': file_path,
            'file_type': file_type,
            'citation': citation,
            'chapter_info': chapter_info
        })

    # 生成引用文件清单
    reference_list = f"""
# 引用文件清单

本材料引用了以下本地知识库文件：

"""

    for file_info in referenced_files:
        reference_list += f"""
## {file_info['idx']}. {file_info['file_name']}

- **文件路径**: {file_info['file_path']}
- **文件类型**: {file_info['file_type'].upper()}
- **引用标识**: {file_info['citation']}
- **引用章节**:
"""

        if file_info['chapter_info']:
            for ch_info in file_info['chapter_info']:
                reference_list += f"{ch_info}\n"
        else:
            reference_list += "    - 全文引用\n"

    reference_list += "\n" + "="*80 + "\n\n"

    return reference_list


def tender_requirements_parse_node(
    state: TenderRequirementsParseInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TenderRequirementsParseOutput:
    """
    title: 招标文件要求解析
    desc: 解析招标文件，识别商务要求和技术要求，提取投标材料模板
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "tender_doc_structure": state.tender_doc_structure
    })

    # 调用LLM进行解析
    result = call_llm(sp, user_prompt_content, llm_config)

    # 解析LLM返回的结果（LLM应该返回JSON格式）
    # 简化处理，直接返回LLM的结果
    # 实际应用中应该使用正则表达式或JSON解析器提取结构化数据
    commercial_requirements = result
    technical_requirements = result
    commercial_template = ""
    technical_template = ""

    return TenderRequirementsParseOutput(
        commercial_requirements=commercial_requirements,
        technical_requirements=technical_requirements,
        commercial_template=commercial_template,
        technical_template=technical_template
    )


def knowledge_base_search_node(
    state: KnowledgeBaseSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> KnowledgeBaseSearchOutput:
    """
    title: 知识库检索
    desc: 在本地知识库中检索相关素材，根据索引与摘要内容快速匹配知识信息，引用索引摘要对应文档中的相关内容
    integrations: 本地知识库
    """
    ctx = runtime.context

    # 初始化知识库索引工具
    indexer = KnowledgeIndexer(state.knowledge_base_path)

    # 执行搜索
    search_indices = indexer.search_indices(state.query, direction="both", top_k=5)

    # 格式化搜索结果，增强信息内容
    formatted_results = []
    for index in search_indices:
        # 构建章节引用信息
        chapter_references = []
        for chapter in index.content_summary.key_chapters:
            chapter_ref = {
                'chapter_title': chapter.chapter_title,
                'page_range': chapter.page_range if chapter.page_range else "N/A",
                'summary': chapter.summary,
                'key_points': chapter.key_points
            }
            chapter_references.append(chapter_ref)

        # 构建完整的结果对象
        formatted_result = {
            # 核心内容
            'full_summary': index.content_summary.full_summary,
            'chapters': chapter_references,

            # 关键词和标签
            'technical_keywords': index.content_summary.technical_keywords,
            'commercial_keywords': index.content_summary.commercial_keywords,
            'industry_tags': index.content_summary.industry_tags,
            'search_tags': index.search_tags,

            # 来源信息（用于在生成材料中标注）
            'source': {
                'file_path': index.metadata.file_path,
                'file_name': index.metadata.file_name,
                'file_type': index.metadata.file_type,
                'file_size_kb': round(index.metadata.file_size / 1024, 2),
                'created_at': index.metadata.created_at,
                'modified_at': index.metadata.modified_at,
                'indexed_at': index.metadata.indexed_at
            },

            # 质量信息
            'quality_score': index.quality_score,
            'direction': index.direction,

            # 元数据（用于追溯和验证）
            'metadata': {
                'file_hash': index.id,
                'is_active': index.is_active,
                'updated_at': index.metadata.updated_at
            },

            # 引用格式（用于在生成材料中显示）
            'citation': f"[{index.metadata.file_name} - {index.metadata.file_type.upper()}]"
        }

        formatted_results.append(formatted_result)

    return KnowledgeBaseSearchOutput(
        search_results=formatted_results,
        has_local_knowledge=len(formatted_results) > 0
    )


def commercial_kb_search_node(
    state: CommercialKBSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialKBSearchOutput:
    """
    title: 商务知识库检索
    desc: 在本地知识库中检索商务相关素材，根据索引与摘要内容快速匹配知识信息，引用索引摘要对应文档中的相关内容
    integrations: 本地知识库
    """
    ctx = runtime.context

    logger.info("="*80)
    logger.info("【商务知识库检索节点】开始执行")
    logger.info("="*80)

    # 初始化知识库索引工具
    indexer = KnowledgeIndexer(state.knowledge_base_path)
    logger.info(f"知识库路径: {state.knowledge_base_path}")
    logger.info(f"知识库索引文件: {indexer.index_file}")

    # 检查索引文件是否存在
    if not indexer.index_file.exists():
        logger.warning(f"⚠️ 索引文件不存在: {indexer.index_file}")
        logger.info("请先在知识库管理页面扫描文件并创建索引")
        return CommercialKBSearchOutput(
            commercial_kb_results=[],
            has_local_knowledge=False
        )

    # 获取索引统计信息
    stats = indexer.get_statistics()
    logger.info(f"知识库统计: 总文件数={stats['total_files']}, 总大小={stats['total_size']/1024/1024:.2f}MB")
    logger.info(f"技术文档数={stats['technical_count']}, 商务文档数={stats['commercial_count']}")

    # 执行搜索（使用商务要求作为查询）
    logger.info(f"搜索查询词: {state.commercial_requirements[:200]}...")
    logger.info(f"搜索方向: commercial, 返回结果数: top_k=5")

    search_indices = indexer.search_indices(state.commercial_requirements, direction="commercial", top_k=5)

    logger.info(f"搜索完成，找到 {len(search_indices)} 个匹配结果")

    # 格式化搜索结果，增强信息内容
    formatted_results = []
    for idx, index in enumerate(search_indices, 1):
        logger.info(f"\n--- 结果 {idx} ---")
        logger.info(f"文件名: {index.metadata.file_name}")
        logger.info(f"文件路径: {index.metadata.file_path}")
        logger.info(f"方向: {index.direction}, 质量评分: {index.quality_score}")
        logger.info(f"商务关键词: {', '.join(index.content_summary.commercial_keywords[:5])}")
        logger.info(f"搜索标签: {', '.join(index.search_tags[:5])}")
        logger.info(f"全文摘要长度: {len(index.content_summary.full_summary)} 字符")
        logger.info(f"章节数量: {len(index.content_summary.key_chapters)}")
        if index.content_summary.key_chapters:
            logger.info(f"章节标题: {', '.join([ch.chapter_title for ch in index.content_summary.key_chapters[:3]])}")
        # 构建章节引用信息
        chapter_references = []
        for chapter in index.content_summary.key_chapters:
            chapter_ref = {
                'chapter_title': chapter.chapter_title,
                'page_range': chapter.page_range if chapter.page_range else "N/A",
                'summary': chapter.summary,
                'key_points': chapter.key_points
            }
            chapter_references.append(chapter_ref)

        # 构建完整的结果对象
        formatted_result = {
            # 核心内容
            'full_summary': index.content_summary.full_summary,
            'chapters': chapter_references,

            # 关键词和标签
            'technical_keywords': index.content_summary.technical_keywords,
            'commercial_keywords': index.content_summary.commercial_keywords,
            'industry_tags': index.content_summary.industry_tags,
            'search_tags': index.search_tags,

            # 来源信息（用于在生成材料中标注）
            'source': {
                'file_path': index.metadata.file_path,
                'file_name': index.metadata.file_name,
                'file_type': index.metadata.file_type,
                'file_size_kb': round(index.metadata.file_size / 1024, 2),
                'created_at': index.metadata.created_at,
                'modified_at': index.metadata.modified_at,
                'indexed_at': index.metadata.indexed_at
            },

            # 质量信息
            'quality_score': index.quality_score,
            'direction': index.direction,

            # 元数据（用于追溯和验证）
            'metadata': {
                'file_hash': index.id,
                'is_active': index.is_active,
                'updated_at': index.metadata.updated_at
            },

            # 引用格式（用于在生成材料中显示）
            'citation': f"[{index.metadata.file_name} - {index.metadata.file_type.upper()}]"
        }

        formatted_results.append(formatted_result)

    # 总结日志
    logger.info("\n" + "="*80)
    logger.info(f"商务知识库检索完成，共返回 {len(formatted_results)} 个结果")
    logger.info(f"是否使用本地知识库: {'是' if len(formatted_results) > 0 else '否'}")
    if len(formatted_results) == 0:
        logger.warning("⚠️ 未找到匹配的知识库内容，请检查:")
        logger.warning("  1. 知识库中是否有商务方向的文档")
        logger.warning("  2. 文档是否已完成索引扫描")
        logger.warning("  3. 搜索词是否与文档内容相关")
    logger.info("="*80 + "\n")

    return CommercialKBSearchOutput(
        commercial_kb_results=formatted_results,
        has_local_knowledge=len(formatted_results) > 0
    )


def technical_kb_search_node(
    state: TechnicalKBSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalKBSearchOutput:
    """
    title: 技术知识库检索
    desc: 在本地知识库中检索技术相关素材，根据索引与摘要内容快速匹配知识信息，引用索引摘要对应文档中的相关内容
    integrations: 本地知识库
    """
    ctx = runtime.context

    logger.info("="*80)
    logger.info("【技术知识库检索节点】开始执行")
    logger.info("="*80)

    # 初始化知识库索引工具
    indexer = KnowledgeIndexer(state.knowledge_base_path)
    logger.info(f"知识库路径: {state.knowledge_base_path}")
    logger.info(f"知识库索引文件: {indexer.index_file}")

    # 检查索引文件是否存在
    if not indexer.index_file.exists():
        logger.warning(f"⚠️ 索引文件不存在: {indexer.index_file}")
        logger.info("请先在知识库管理页面扫描文件并创建索引")
        return TechnicalKBSearchOutput(
            technical_kb_results=[],
            has_local_knowledge=False
        )

    # 获取索引统计信息
    stats = indexer.get_statistics()
    logger.info(f"知识库统计: 总文件数={stats['total_files']}, 总大小={stats['total_size']/1024/1024:.2f}MB")
    logger.info(f"技术文档数={stats['technical_count']}, 商务文档数={stats['commercial_count']}")

    # 执行搜索（使用技术要求作为查询）
    logger.info(f"搜索查询词: {state.technical_requirements[:200]}...")
    logger.info(f"搜索方向: technical, 返回结果数: top_k=5")

    search_indices = indexer.search_indices(state.technical_requirements, direction="technical", top_k=5)

    logger.info(f"搜索完成，找到 {len(search_indices)} 个匹配结果")

    # 格式化搜索结果，增强信息内容
    formatted_results = []
    for idx, index in enumerate(search_indices, 1):
        logger.info(f"\n--- 结果 {idx} ---")
        logger.info(f"文件名: {index.metadata.file_name}")
        logger.info(f"文件路径: {index.metadata.file_path}")
        logger.info(f"方向: {index.direction}, 质量评分: {index.quality_score}")
        logger.info(f"技术关键词: {', '.join(index.content_summary.technical_keywords[:5])}")
        logger.info(f"搜索标签: {', '.join(index.search_tags[:5])}")
        logger.info(f"全文摘要长度: {len(index.content_summary.full_summary)} 字符")
        logger.info(f"章节数量: {len(index.content_summary.key_chapters)}")
        if index.content_summary.key_chapters:
            logger.info(f"章节标题: {', '.join([ch.chapter_title for ch in index.content_summary.key_chapters[:3]])}")
        # 构建章节引用信息
        chapter_references = []
        for chapter in index.content_summary.key_chapters:
            chapter_ref = {
                'chapter_title': chapter.chapter_title,
                'page_range': chapter.page_range if chapter.page_range else "N/A",
                'summary': chapter.summary,
                'key_points': chapter.key_points
            }
            chapter_references.append(chapter_ref)

        # 构建完整的结果对象
        formatted_result = {
            # 核心内容
            'full_summary': index.content_summary.full_summary,
            'chapters': chapter_references,

            # 关键词和标签
            'technical_keywords': index.content_summary.technical_keywords,
            'commercial_keywords': index.content_summary.commercial_keywords,
            'industry_tags': index.content_summary.industry_tags,
            'search_tags': index.search_tags,

            # 来源信息（用于在生成材料中标注）
            'source': {
                'file_path': index.metadata.file_path,
                'file_name': index.metadata.file_name,
                'file_type': index.metadata.file_type,
                'file_size_kb': round(index.metadata.file_size / 1024, 2),
                'created_at': index.metadata.created_at,
                'modified_at': index.metadata.modified_at,
                'indexed_at': index.metadata.indexed_at
            },

            # 质量信息
            'quality_score': index.quality_score,
            'direction': index.direction,

            # 元数据（用于追溯和验证）
            'metadata': {
                'file_hash': index.id,
                'is_active': index.is_active,
                'updated_at': index.metadata.updated_at
            },

            # 引用格式（用于在生成材料中显示）
            'citation': f"[{index.metadata.file_name} - {index.metadata.file_type.upper()}]"
        }

        formatted_results.append(formatted_result)

    # 总结日志
    logger.info("\n" + "="*80)
    logger.info(f"技术知识库检索完成，共返回 {len(formatted_results)} 个结果")
    logger.info(f"是否使用本地知识库: {'是' if len(formatted_results) > 0 else '否'}")
    if len(formatted_results) == 0:
        logger.warning("⚠️ 未找到匹配的知识库内容，请检查:")
        logger.warning("  1. 知识库中是否有技术方向的文档")
        logger.warning("  2. 文档是否已完成索引扫描")
        logger.warning("  3. 搜索词是否与文档内容相关")
    logger.info("="*80 + "\n")

    return TechnicalKBSearchOutput(
        technical_kb_results=formatted_results,
        has_local_knowledge=len(formatted_results) > 0
    )


def commercial_web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialWebSearchOutput:
    """
    title: 商务互联网搜索
    desc: 在互联网上搜索商务相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 获取查询词
    query = state.commercial_requirements if state.commercial_requirements else "商务资质、项目经验、服务承诺"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 只返回商务搜索结果
    return CommercialWebSearchOutput(commercial_web_results=search_results)


def technical_web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalWebSearchOutput:
    """
    title: 技术互联网搜索
    desc: 在互联网上搜索技术相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 获取查询词
    query = state.technical_requirements if state.technical_requirements else "技术方案、系统架构、实施方案"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 只返回技术搜索结果
    return TechnicalWebSearchOutput(technical_web_results=search_results)


def web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> WebSearchOutput:
    """
    title: 互联网搜索
    desc: 在互联网上搜索相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 根据输入判断是商务还是技术搜索
    # 如果有 commercial_kb_results，说明是商务搜索
    is_commercial = bool(state.commercial_kb_results or (state.commercial_requirements and not state.technical_requirements))

    if is_commercial:
        query = state.commercial_requirements if state.commercial_requirements else "商务资质、项目经验、服务承诺"
    else:
        query = state.technical_requirements if state.technical_requirements else "技术方案、系统架构、实施方案"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 根据类型返回不同的字段
    if is_commercial:
        return WebSearchOutput(commercial_web_results=search_results)
    else:
        return WebSearchOutput(technical_web_results=search_results)


def commercial_material_generate_node(
    state: CommercialMaterialGenerateInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialMaterialGenerateOutput:
    """
    title: 商务材料生成
    desc: 根据商务要求和素材生成商务投标材料，标注素材出处
    integrations: 大语言模型
    """
    ctx = runtime.context

    logger.info("="*80)
    logger.info("【商务材料生成节点】开始执行")
    logger.info("="*80)
    logger.info(f"商务要求长度: {len(state.commercial_requirements)} 字符")
    logger.info(f"本地知识库结果数: {len(state.commercial_kb_results)}")
    logger.info(f"互联网搜索结果数: {len(state.commercial_web_results)}")

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    llm_config = _cfg.get("config", {})

    # 整理素材信息
    kb_materials = ""
    if state.commercial_kb_results:
        logger.info(f"\n使用本地知识库素材:")
        for idx, result in enumerate(state.commercial_kb_results[:5], 1):
            source_name = result.get('source', {}).get('file_name', 'Unknown')
            citation = result.get('citation', 'Unknown')
            summary_len = len(result.get('full_summary', ''))
            logger.info(f"  {idx}. {citation} - 摘要长度: {summary_len} 字符")
            logger.info(f"     技术关键词: {', '.join(result.get('technical_keywords', [])[:3])}")
            logger.info(f"     商务关键词: {', '.join(result.get('commercial_keywords', [])[:3])}")

        kb_materials = "\n".join([
            f"[本地知识库 - {r.get('source', {}).get('file_name', '')}]: {r.get('full_summary', '')[:1000]}"
            for r in state.commercial_kb_results[:5]
        ])
    else:
        logger.warning("⚠️ 未使用本地知识库素材")

    web_materials = ""
    if state.commercial_web_results:
        kb_materials = "\n".join([
            f"[本地知识库 - {r.get('source_doc', '')} - {r.get('source_page', 'N/A')}]: {r.get('content', '')[:800]}"
            for r in state.commercial_kb_results[:5]
        ])

    web_materials = ""
    if state.commercial_web_results:
        web_materials = "\n".join([
            f"[互联网搜索 - {r.get('url', '')}]: {r.get('title', '')}\n{r.get('content', '')[:800]}"
            for r in state.commercial_web_results[:5]
        ])

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "requirements": state.commercial_requirements,
        "template": state.commercial_template,
        "kb_materials": kb_materials,
        "web_materials": web_materials
    })

    # 调用LLM生成内容
    commercial_material = call_llm(sp, user_prompt_content, llm_config)

    # 如果使用了本地知识库，添加引用文件清单
    if state.commercial_kb_results:
        reference_list = generate_reference_list(state.commercial_kb_results)
        commercial_material = reference_list + commercial_material
        logger.info(f"已添加引用文件清单，共引用 {len(state.commercial_kb_results)} 个文件")

    logger.info(f"\n商务材料生成完成")
    logger.info(f"生成内容长度: {len(commercial_material)} 字符")
    logger.info(f"使用本地知识库: {'是' if kb_materials else '否'}")
    logger.info(f"使用互联网搜索: {'是' if web_materials else '否'}")
    logger.info("="*80 + "\n")

    return CommercialMaterialGenerateOutput(
        commercial_material=commercial_material
    )


def technical_material_generate_node(
    state: TechnicalMaterialGenerateInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalMaterialGenerateOutput:
    """
    title: 技术材料生成
    desc: 根据技术要求和素材生成技术投标材料，标注素材出处
    integrations: 大语言模型
    """
    ctx = runtime.context

    logger.info("="*80)
    logger.info("【技术材料生成节点】开始执行")
    logger.info("="*80)
    logger.info(f"技术要求长度: {len(state.technical_requirements)} 字符")
    logger.info(f"本地知识库结果数: {len(state.technical_kb_results)}")
    logger.info(f"互联网搜索结果数: {len(state.technical_web_results)}")

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    llm_config = _cfg.get("config", {})

    # 整理素材信息
    kb_materials = ""
    if state.technical_kb_results:
        logger.info(f"\n使用本地知识库素材:")
        for idx, result in enumerate(state.technical_kb_results[:5], 1):
            source_name = result.get('source', {}).get('file_name', 'Unknown')
            citation = result.get('citation', 'Unknown')
            summary_len = len(result.get('full_summary', ''))
            logger.info(f"  {idx}. {citation} - 摘要长度: {summary_len} 字符")
            logger.info(f"     技术关键词: {', '.join(result.get('technical_keywords', [])[:3])}")
            logger.info(f"     商务关键词: {', '.join(result.get('commercial_keywords', [])[:3])}")

        kb_materials = "\n".join([
            f"[本地知识库 - {r.get('source', {}).get('file_name', '')}]: {r.get('full_summary', '')[:1000]}"
            for r in state.technical_kb_results[:5]
        ])
    else:
        logger.warning("⚠️ 未使用本地知识库素材")

    web_materials = ""
    if state.technical_web_results:
        logger.info(f"\n使用互联网搜索素材:")
        for idx, result in enumerate(state.technical_web_results[:3], 1):
            url = result.get('url', 'Unknown')
            title = result.get('title', 'Unknown')
            logger.info(f"  {idx}. {title}")
            logger.info(f"     URL: {url}")

        web_materials = "\n".join([
            f"[互联网搜索 - {r.get('url', '')}]: {r.get('title', '')}\n{r.get('content', '')[:800]}"
            for r in state.technical_web_results[:5]
        ])
    else:
        logger.info("未使用互联网搜索素材")

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "requirements": state.technical_requirements,
        "template": state.technical_template,
        "kb_materials": kb_materials,
        "web_materials": web_materials
    })

    # 调用LLM生成内容
    technical_material = call_llm(sp, user_prompt_content, llm_config)

    # 如果使用了本地知识库，添加引用文件清单
    if state.technical_kb_results:
        reference_list = generate_reference_list(state.technical_kb_results)
        technical_material = reference_list + technical_material
        logger.info(f"已添加引用文件清单，共引用 {len(state.technical_kb_results)} 个文件")

    logger.info(f"\n技术材料生成完成")
    logger.info(f"生成内容长度: {len(technical_material)} 字符")
    logger.info(f"使用本地知识库: {'是' if kb_materials else '否'}")
    logger.info(f"使用互联网搜索: {'是' if web_materials else '否'}")
    logger.info("="*80 + "\n")

    return TechnicalMaterialGenerateOutput(
        technical_material=technical_material
    )
