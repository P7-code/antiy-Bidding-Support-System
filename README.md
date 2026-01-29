# 安天投标文件智能分析系统

基于 LangGraph 工作流的智能招标文件分析工具，专为网络安全售前工程师设计。

## ✨ 核心功能

- ✅ **废标项检测** - 自动识别可能导致废标的致命问题
- ✅ **商务得分检查** - 评估商务部分得分，找出失分点
- ✅ **技术方案评估** - 检查技术方案的完整性、创新性、可行性
- ✅ **指标应答验证** - 逐条检查技术指标响应情况
- ✅ **技术得分点分析** - 深度分析技术得分覆盖情况
- ✅ **文件结构检查** - 检查目录完整性和排布合理性

## 🚀 快速开始

### 在线访问

- **GitHub 仓库**：https://github.com/P7-code/p7
- **在线应用**：https://p7-code-p7.streamlit.app

### 本地运行

#### 1. 克隆仓库

```bash
git clone https://github.com/P7-code/p7.git
cd p7
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置 API Key（推荐）

**方式 A: 使用 secrets.toml 文件（推荐）**

复制示例文件并填写你的配置：

```bash
# 复制示例文件
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 编辑文件，填写你的 API Key
# 选择以下任一服务进行配置

# 火山引擎方舟（推荐）
# OPENAI_API_KEY = "9cebea4f-aa41-47ea-942e-4bf1324d1162"
# OPENAI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"

# DeepSeek
# OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
# OPENAI_API_BASE = "https://api.deepseek.com"

# Kimi
# OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
# OPENAI_API_BASE = "https://api.moonshot.cn/v1"

# OpenAI
# OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
# OPENAI_API_BASE = "https://api.openai.com/v1"
```

**方式 B: 使用环境变量**

```bash
# Linux/Mac - 火山引擎方舟
export OPENAI_API_KEY="9cebea4f-aa41-47ea-942e-4bf1324d1162"
export OPENAI_API_BASE="https://ark.cn-beijing.volces.com/api/v3"

# Windows - 火山引擎方舟
set OPENAI_API_KEY=9cebea4f-aa41-47ea-942e-4bf1324d1162
set OPENAI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

#### 4. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

> **提示**: 如果未配置 API Key，系统将运行在演示模式，返回模拟结果。

## 📦 部署指南

详细的部署指南请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

### 快速部署到 Streamlit Cloud

#### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "chore: 准备部署"
git push origin main
```

#### 2. 连接 Streamlit Cloud

1. 访问 https://share.streamlit.io
2. 点击 "New app"
3. 选择你的 GitHub 仓库
4. 配置：
   - Repository: `P7-code/p7`
   - Branch: `main`
   - Main file path: `app.py`
5. 点击 "Deploy"

#### 3. 配置 Secrets（关键步骤）

**方式 A: 在 Streamlit Cloud 界面配置**

1. 部署完成后，进入应用主页
2. 点击右上角 **"···"** → **"Manage app"**
3. 左侧菜单选择 **"Settings"** → **"Secrets"**
4. 点击 **"+ New secret"**
5. 添加以下环境变量：

   ```
   Name: OPENAI_API_KEY
   Value: sk-xxxxxxxxxxxxxxxx
   ```

   ```
   Name: OPENAI_API_BASE
   Value: https://api.deepseek.com
   ```

6. 点击 **"Save"**
7. 返回应用主页，点击 **"Re-deploy"**

**方式 B: 提交 secrets.toml 文件（不推荐，仅用于测试）**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# 编辑文件填写你的 API Key
git add .streamlit/secrets.toml
git commit -m "add: 添加secrets配置"
git push origin main
```

> **注意**: `.streamlit/secrets.toml` 已在 `.gitignore` 中，不会提交到 Git。仅用于测试环境。

### 支持的 LLM 服务

本系统使用 OpenAI 兼容接口，支持以下服务：

| 服务 | API Base | 价格 | 特点 | 推荐度 |
|-----|---------|------|------|--------|
| **火山引擎方舟** | https://ark.cn-beijing.volces.com/api/v3 | 按官方定价 | 支持多模型、国内访问稳定 | ⭐⭐⭐⭐⭐ |
| **DeepSeek** | https://api.deepseek.com | ¥1/百万 tokens | 高性价比、中文优化 | ⭐⭐⭐⭐ |
| **Kimi** | https://api.moonshot.cn/v1 | ¥12/百万 tokens | 长上下文、中文优化 | ⭐⭐⭐⭐ |
| **OpenAI** | https://api.openai.com/v1 | $2.5/百万 tokens | 最强大的通用模型 | ⭐⭐⭐⭐ |
| **智谱 AI** | https://open.bigmodel.cn/api/paas/v4 | ¥5/百万 tokens | 中文优化、API 稳定 | ⭐⭐⭐⭐ |

**当前配置使用的模型**：`deepseek-v3-2-251201`（火山引擎方舟）

### 其他部署方式

- **Hugging Face Spaces**: 免费部署，支持 GPU
- **Docker**: 适合生产环境
- **本地运行**: 适合开发测试

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 项目结构

```
p7/
├── app.py                          # Streamlit Web 应用
├── requirements.txt                 # Python 依赖
├── README.md                       # 项目说明
├── .streamlit/config.toml          # Streamlit 配置
│
├── src/                            # 源代码
│   └── graphs/
│       ├── state.py               # 状态定义
│       ├── node.py                # 节点函数
│       └── graph.py               # 主图编排
│
├── src/                            # 工具
│   └── utils/
│       └── file/
│           └── file.py            # 文件处理
│
└── config/                         # LLM 配置
    ├── generate_checklist_cfg.json
    ├── invalid_items_check_cfg.json
    ├── commercial_score_check_cfg.json
    ├── technical_plan_check_cfg.json
    ├── indicator_response_check_cfg.json
    ├── technical_score_check_cfg.json
    ├── bid_structure_check_cfg.json
    └── modification_summary_cfg.json
```

## 🎯 使用流程

1. **上传招标文件**
   - 支持 PDF、Word、PPT 格式
   - 系统自动提取文件内容

2. **上传投标文件**
   - 支持 PDF、Word、PPT 格式
   - 系统自动提取文件内容

3. **点击"开始分析"**
   - 系统自动进行六维并行检测
   - 分析过程通常需要 1-3 分钟

4. **查看分析结果**
   - 废标项检测结果
   - 商务得分检查
   - 技术方案评估
   - 指标应答验证
   - 技术得分点分析
   - 文件结构检查

5. **下载分析报告**
   - 下载完整的 JSON 格式报告

## 🛠️ 技术栈

- **工作流引擎**: LangGraph
- **Web 框架**: Streamlit
- **LLM 接口**: LangChain + OpenAI API
- **文档处理**: PyPDF、python-docx、python-pptx
- **数据处理**: Pandas、OpenPyXL

## 📖 工作流架构

```
┌─────────────┐
│  文件解析   │
│ (串行)     │
└──────┬──────┘
       │
┌──────▼──────┐
│  生成清单   │
└──────┬──────┘
       │
   ┌───┴────────────────────┐
   │     六维并行检测       │
   ├─────────┬───────┬──────┤
   │         │       │      │
废标 商务 技术 指标 得分 结构
   │         │       │      │
   └─────────┴───────┴──────┘
            │
      ┌─────▼─────┐
      │  汇总建议  │
      └───────────┘
```

## ⚠️ 注意事项

1. **文件大小限制**
   - 单个文件不超过 100MB
   - 建议使用压缩后的 PDF

2. **API 配额**
   - 使用 LLM 服务会产生费用
   - 建议设置合理的配额限制

3. **隐私保护**
   - 上传的文件仅用于分析
   - 不会存储在服务器上

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- GitHub: https://github.com/P7-code/p7
- Email: 18646133221@163.com

---

**AI应用创新激励计划参赛作品** 🚀
