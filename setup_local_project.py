#!/usr/bin/env python3
"""
安天投标文件智能分析系统 - 完整项目文件创建工具
在本地运行此脚本，会自动创建所有项目文件
"""

import os
from pathlib import Path

# ============ 核心文件内容 ============

PROJECT_FILES = {
    "app.py": """#!/usr/bin/env python3
\"\"\"
安天投标文件智能分析系统 - Web界面
\"\"\"
import os
import sys
import json
import tempfile
from typing import Dict, Any
import streamlit as st

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from graphs.graph import main_graph
    from utils.file.file import File
except ImportError:
    st.error("项目依赖未安装，请先运行: pip install -r requirements.txt")
    st.stop()

# 页面配置
st.set_page_config(
    page_title="安天投标文件智能分析系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown(\"\"\"
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
\"\"\", unsafe_allow_html=True)

def main():
    \"\"\"主函数\"\"\"
    st.markdown(\"<h1 class=\\"main-title\\">📊 安天投标文件智能分析系统</h1>\", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(\"## 📖 使用说明\")
        st.markdown(\"\"\"
        1. 上传招标文件（PDF/Word）
        2. 上传投标文件（PDF/Word/PPT）
        3. 点击"开始分析"按钮
        4. 查看分析结果和修改建议
        \"\"\")
        st.markdown(\"---\")
        st.markdown(\"## 💡 系统功能\")
        st.markdown(\"\"\"
        - ✅ 废标项检测
        - ✅ 商务得分检查
        - ✅ 技术方案评估
        - ✅ 指标应答验证
        - ✅ 技术得分点分析
        - ✅ 文件结构检查
        - ✅ 生成修改建议
        \"\"\")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(\"<div class=\\"section-header\\">📄 招标文件</div>\", unsafe_allow_html=True)
        tender_file = st.file_uploader(\"上传招标文件\", type=[\"pdf\", \"docx\", \"doc\", \"pptx\", \"ppt\"], key=\"tender_file\")
        if tender_file:
            st.success(f\"已选择: {tender_file.name}\")

    with col2:
        st.markdown(\"<div class=\\"section-header\\">📝 投标文件</div>\", unsafe_allow_html=True)
        bid_file = st.file_uploader(\"上传投标文件\", type=[\"pdf\", \"docx\", \"doc\", \"pptx\", \"ppt\"], key=\"bid_file\")
        if bid_file:
            st.success(f\"已选择: {bid_file.name}\")

    st.markdown(\"---\")
    analyze_button = st.button(\"🚀 开始分析\", type=\"primary\", use_container_width=True)

    if analyze_button:
        if not tender_file or not bid_file:
            st.error(\"❌ 请先上传招标文件和投标文件！\")
            return

        with st.spinner(\"正在进行六维分析，请稍候...\"):
            try:
                # 保存文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=f\"_{tender_file.name}\") as tmp_tender:
                    tmp_tender.write(tender_file.getbuffer())
                    tender_path = tmp_tender.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=f\"_{bid_file.name}\") as tmp_bid:
                    tmp_bid.write(bid_file.getbuffer())
                    bid_path = tmp_bid.name

                input_data = {
                    \"tender_doc\": {\"url\": f\"file://{tender_path}\", \"file_type\": \"document\"},
                    \"bid_doc\": {\"url\": f\"file://{bid_path}\", \"file_type\": \"document\"}
                }

                st.success(\"文件准备就绪，开始分析...\")

                with st.spinner(\"正在进行六维分析，请稍候...\"):
                    result = main_graph.invoke(input_data)

                st.markdown(\"<h2 class=\\"section-header\\">📋 分析结果</h2>\", unsafe_allow_html=True)

                if result.get(\"invalid_items_check\"):
                    invalid_items = result[\"invalid_items_check\"]
                    if invalid_items.get(\"invalid_items\"):
                        st.warning(f\"❌ 发现 {len(invalid_items['invalid_items'])} 个废标项\")
                    else:
                        st.success(\"✅ 未发现废标项，恭喜！\")

                if result.get(\"modification_summary\"):
                    summary = result[\"modification_summary\"]
                    st.info(f\"总修改建议数：{summary.get('total_modifications', 0)}\")

                st.success(\"✅ 分析完成！\")

            except Exception as e:
                st.error(f\"分析过程出错: {str(e)}\")
                st.error(f\"错误类型: {type(e).__name__}\")

    st.markdown(\"---\")
    st.markdown(\"\"\"
    <div style=\"text-align: center; color: #666; padding: 1rem;\">
        <p>🤖 安天投标文件智能分析系统 | 基于LangGraph工作流引擎</p>
        <p>💡 AI应用创新激励计划参赛作品</p>
    </div>
    \"\"\", unsafe_allow_html=True)

if __name__ == \"__main__\":
    main()
""",

    "start.bat": """@echo off
chcp 65001 >nul
echo ==========================================
echo   安天投标文件智能分析系统 - 快速启动
echo ==========================================
echo.

python --version
echo ✓ Python已安装

echo.
echo 检查依赖...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install -r requirements.txt
) else (
    echo ✓ 依赖已安装
)

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
""",

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
openai==2.15.0
tiktoken==0.12.0
jinja2==3.1.6
pyyaml==6.0.3
""",

    "README.md": """# 安天投标文件智能分析系统

## 📖 项目简介

本项目是一个基于 LangGraph 的智能招标文件分析工作流，专为网络安全售前工程师设计。通过自动化分析招标文件和投标文件，实现多维度检查与预评分，生成详细的修改建议。

## 🚀 快速开始

### 前置要求
- Python 3.8+
- 已安装项目依赖包

### 本地运行

#### Windows用户：
双击运行 `start.bat`，或在命令行执行：
```bash
start.bat
```

#### Linux/Mac用户：
```bash
chmod +x start.sh
./start.sh
```

启动后访问：http://localhost:8501

## 🌐 部署到互联网

### Streamlit Cloud（推荐，免费）
1. 推送代码到GitHub：`https://github.com/P7-code/p7`
2. 访问 https://share.streamlit.io
3. 创建应用，选择您的仓库
4. 点击Deploy

详细部署指南请查看 [DEPLOY.md](DEPLOY.md)

## 💡 主要功能

- ✅ 废标项检查
- ✅ 商务得分检查
- ✅ 技术方案评估
- ✅ 指标应答验证
- ✅ 技术得分点分析
- ✅ 文件结构检查
- ✅ 生成修改建议

## 📞 技术支持

如有问题，请查看 [DEPLOY.md](DEPLOY.md) 部署指南

---

**GitHub仓库**: https://github.com/P7-code/p7
""",

    ".streamlit/config.toml": """[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
""",

    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Streamlit
.streamlit/secrets.toml

# Environment variables
.env
.env.local

# Logs
*.log
logs/
app.log

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
*.temp

# Database
*.db
*.sqlite
*.sqlite3

# Model cache
.cache/
""",
}


def create_file(filepath: str, content: str):
    """创建文件"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {filepath}")


def main():
    """主函数"""
    print("=" * 70)
    print("  安天投标文件智能分析系统 - 项目文件创建工具")
    print("=" * 70)
    print()
    print("正在创建项目文件...")
    print()

    # 创建文件
    for filepath, content in PROJECT_FILES.items():
        create_file(filepath, content)

    print()
    print("=" * 70)
    print("  ✅ 项目文件创建完成！")
    print("=" * 70)
    print()
    print("📁 已创建的文件:")
    for filepath in PROJECT_FILES.keys():
        print(f"     • {filepath}")
    print()
    print("🚀 下一步操作:")
    print("   1. 双击 start.bat 启动应用（Windows）")
    print("   2. 或运行: python app.py")
    print("   3. 浏览器访问: http://localhost:8501")
    print()
    print("⚠️  注意事项:")
    print("   • 首次运行会自动安装依赖包（需要几分钟）")
    print("   • 确保已安装 Python 3.8 或更高版本")
    print("   • 启动后不要关闭命令行窗口")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
