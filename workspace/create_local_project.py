#!/usr/bin/env python3
"""
一键创建项目文件脚本
运行此脚本会自动在当前目录创建完整的项目文件
"""

import os
import json
from pathlib import Path

# 定义所有文件内容
FILES = {
    "app.py": '''"""
安天投标文件智能分析系统 - Web界面
"""
import os
import sys
import json
import tempfile
from typing import Dict, Any
import streamlit as st

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from graphs.graph import main_graph
from utils.file.file import File
from pydantic import BaseModel


# 页面配置
st.set_page_config(
    page_title="安天投标文件智能分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2e7d32;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #c8e6c9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def save_uploaded_file(uploaded_file) -> str:
    """保存上传的文件到临时目录"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            return tmp_file.name
    except Exception as e:
        st.error(f"文件保存失败: {str(e)}")
        return None


def display_checklist_result(checklist: Dict[str, Any], section_title: str, color_class: str = "info-box"):
    """显示检查清单结果"""
    st.markdown(f"### {section_title}")
    st.markdown(f"<div class=\\"{color_class}\\">", unsafe_allow_html=True)

    if isinstance(checklist, dict):
        for key, value in checklist.items():
            if isinstance(value, list):
                st.markdown(f"**{key}:**")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            st.markdown(f"- {k}: {v}")
                    else:
                        st.markdown(f"- {item}")
            else:
                st.markdown(f"**{key}:** {value}")
    elif isinstance(checklist, list):
        for item in checklist:
            if isinstance(item, dict):
                for k, v in item.items():
                    st.markdown(f"**{k}:** {v}")
            else:
                st.markdown(f"- {item}")

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """主函数"""
    # 标题
    st.markdown("<h1 class=\\"main-title\\">📊 安天投标文件智能分析系统</h1>", unsafe_allow_html=True)

    # 侧边栏说明
    with st.sidebar:
        st.markdown("## 📖 使用说明")
        st.markdown("""
        1. 上传招标文件（PDF/Word）
        2. 上传投标文件（PDF/Word/PPT）
        3. 点击"开始分析"按钮
        4. 查看分析结果和修改建议
        """)

        st.markdown("---")
        st.markdown("## 💡 系统功能")
        st.markdown("""
        - ✅ 废标项检测
        - ✅ 商务得分检查
        - ✅ 技术方案评估
        - ✅ 指标应答验证
        - ✅ 技术得分点分析
        - ✅ 文件结构检查
        - ✅ 生成修改建议
        """)

        st.markdown("---")
        st.markdown("## ⚠️ 注意事项")
        st.markdown("""
        - 仅支持PDF、Word、PPT格式
        - 文件大小不超过100MB
        - 分析过程可能需要几分钟
        """)

    # 主内容区
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class=\\"section-header\\">📄 招标文件</div>", unsafe_allow_html=True)
        tender_file = st.file_uploader(
            "上传招标文件",
            type=["pdf", "docx", "doc", "pptx", "ppt"],
            key="tender_file"
        )
        if tender_file:
            st.success(f"已选择: {tender_file.name}")

    with col2:
        st.markdown("<div class=\\"section-header\\">📝 投标文件</div>", unsafe_allow_html=True)
        bid_file = st.file_uploader(
            "上传投标文件",
            type=["pdf", "docx", "doc", "pptx", "ppt"],
            key="bid_file"
        )
        if bid_file:
            st.success(f"已选择: {bid_file.name}")

    # 分析按钮
    st.markdown("---")
    analyze_button = st.button("🚀 开始分析", type="primary", use_container_width=True)

    if analyze_button:
        if not tender_file or not bid_file:
            st.error("❌ 请先上传招标文件和投标文件！")
            return

        # 保存文件
        with st.spinner("正在保存文件..."):
            tender_path = save_uploaded_file(tender_file)
            bid_path = save_uploaded_file(bid_file)

            if not tender_path or not bid_path:
                st.error("文件保存失败！")
                return

        # 准备输入
        try:
            input_data = {
                "tender_doc": {
                    "url": f"file://{tender_path}",
                    "file_type": "document"
                },
                "bid_doc": {
                    "url": f"file://{bid_path}",
                    "file_type": "document"
                }
            }

            st.success("文件准备就绪，开始分析...")

            # 运行工作流
            with st.spinner("正在进行六维分析，请稍候..."):
                result = main_graph.invoke(input_data)

            # 显示结果
            st.markdown("<h2 class=\\"section-header\\">📋 分析结果</h2>", unsafe_allow_html=True)

            # 废标项检测结果
            if result.get("invalid_items_check"):
                invalid_items = result["invalid_items_check"]
                if invalid_items.get("invalid_items"):
                    display_checklist_result(invalid_items, "❌ 废标项检测结果", "warning-box")
                else:
                    st.markdown("<div class=\\"success-box\\">✅ 未发现废标项，恭喜！</div>", unsafe_allow_html=True)

            # 商务得分检查结果
            if result.get("commercial_score_check"):
                display_checklist_result(result["commercial_score_check"], "💰 商务得分检查")

            # 技术方案评估结果
            if result.get("technical_plan_check"):
                display_checklist_result(result["technical_plan_check"], "🔧 技术方案评估")

            # 指标应答验证结果
            if result.get("indicator_response_check"):
                display_checklist_result(result["indicator_response_check"], "📊 指标应答验证")

            # 技术得分点分析结果
            if result.get("technical_score_check"):
                display_checklist_result(result["technical_score_check"], "🎯 技术得分点分析")

            # 文件结构检查结果
            if result.get("bid_structure_check"):
                display_checklist_result(result["bid_structure_check"], "📁 文件结构检查")

            # 修改建议汇总
            st.markdown("<h2 class=\\"section-header\\">💡 修改建议汇总</h2>", unsafe_allow_html=True)
            if result.get("modification_summary"):
                summary = result["modification_summary"]
                st.markdown("<div class=\\"info-box\\">", unsafe_allow_html=True)
                st.markdown(f"**总修改建议数：** {summary.get("total_modifications", 0)}")
                st.markdown(f"**优先级建议：** {summary.get("priority_modifications", 0)}")
                st.markdown(f"**详细建议：**")

                if isinstance(summary.get("modifications"), list):
                    for i, mod in enumerate(summary["modifications"], 1):
                        st.markdown(f"{i}. {mod}")
                st.markdown("</div>", unsafe_allow_html=True)

            # 下载结果按钮
            st.markdown("---")
            if st.button("📥 下载完整分析报告"):
                report_data = json.dumps(result, ensure_ascii=False, indent=2)
                st.download_button(
                    label="下载JSON报告",
                    data=report_data,
                    file_name="招标文件分析报告.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"分析过程出错: {str(e)}")
            st.error(f"错误详情: {type(e).__name__}")
            import traceback
            st.error(traceback.format_exc())

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 安天投标文件智能分析系统 | 基于LangGraph工作流引擎</p>
        <p>💡 AI应用创新激励计划参赛作品</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
''',

    "start.bat": '''@echo off
chcp 65001 >nul
echo ==========================================
echo   安天投标文件智能分析系统 - 快速启动
echo ==========================================
echo.

REM 检查Python版本
python --version
echo ✓ Python已安装

REM 检查依赖
echo.
echo 检查依赖...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install -r requirements.txt
) else (
    echo ✓ 依赖已安装
)

REM 启动应用
echo.
echo ==========================================
echo   正在启动Streamlit应用...
echo ==========================================
echo.
echo 访问地址: http://localhost:8501
echo 按 Ctrl+C 停止应用
echo.

streamlit run app.py

pause
''',

    "requirements.txt": """langgraph==1.0.2
langchain==1.0.3
langchain-core==1.0.2
langchain-openai==1.0.1
pydantic==2.12.3
pypdf==6.4.1
docx2python==3.5.0
python-docx==1.2.0
python-pptx==1.0.2
openpyxl==3.1.5
streamlit==1.28.0
coze-coding-utils==0.2.2
coze-coding-dev-sdk==0.5.6
cozeloop==0.1.21
coze-workload-identity==0.1.4
python-dotenv==1.2.1
httpx==0.28.1
httpx-ws==0.8.2
orjson==3.11.5
ormsgpack==1.12.2
uvicorn==0.38.0
fastapi==0.121.2
""",
}


def create_file(filepath: str, content: str):
    """创建文件"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✓ 创建: {filepath}")


def main():
    """主函数"""
    print("=" * 60)
    print("  安天投标文件智能分析系统 - 项目文件创建工具")
    print("=" * 60)
    print()

    # 创建文件
    for filepath, content in FILES.items():
        create_file(filepath, content)

    print()
    print("=" * 60)
    print("  ✅ 核心文件创建完成！")
    print("=" * 60)
    print()
    print("📁 已创建的文件:")
    for filepath in FILES.keys():
        print(f"   - {filepath}")
    print()
    print("🚀 下一步操作:")
    print("   1. 双击 start.bat 启动应用")
    print("   2. 或在命令行运行: start.bat")
    print("   3. 访问 http://localhost:8501")
    print()
    print("⚠️  注意:")
    print("   - 首次运行会自动安装依赖包")
    print("   - 需要确保已安装 Python 3.8+")
    print("   - 启动后不要关闭命令行窗口")
    print()


if __name__ == "__main__":
    main()
