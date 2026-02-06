# 安天投标文件智能分析系统

基于 LangGraph 工作流的智能招标文件分析工具，专为网络安全售前工程师设计。提供**投标文件智能检查**和**投标材料自动生成**两大核心功能。

## ✨ 核心功能

### 📊 投标文件检查

- ✅ **废标项检测** - 自动识别可能导致废标的致命问题
- ✅ **商务得分检查** - 评估商务部分得分，找出失分点
- ✅ **技术方案评估** - 检查技术方案的完整性、创新性、可行性
- ✅ **指标应答验证** - 逐条检查技术指标响应情况
- ✅ **技术得分点分析** - 深度分析技术得分覆盖情况
- ✅ **文件结构检查** - 检查目录完整性和排布合理性
- 📋 **智能检查报告** - 自动生成详细修改清单和改进建议
- 📄 **多格式报告导出** - 支持 PDF、Word、TXT 三种格式报告下载

### 📝 投标材料生成

- ✅ **招标要求智能解析** - 自动提取商务要求和技术要求
- 📚 **本地知识库检索** - 基于历史成功案例快速匹配素材
- 🔍 **互联网智能搜索** - 实时搜索最新的行业标准和最佳实践
- 💼 **商务材料生成** - 自动生成商务资质、项目经验、服务承诺等内容
- 🔧 **技术材料生成** - 自动生成技术方案、系统架构、实施方案等内容
- 📎 **素材出处标注** - 自动标注每个内容的来源（知识库文档/互联网链接）
- 📄 **多格式材料下载** - 支持 Word 和 TXT 格式材料下载

## 🎯 适用场景

- 🔒 **网络安全行业** - 招投标文件专业分析
- 🏢 **售前投标团队** - 提高投标文件质量和响应速度
- 📊 **项目管理** - 快速检查投标文件完整性
- 🤖 **自动化流程** - 减少人工重复工作，提高效率

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

#### 3. 配置 API Key（必需）

**方式 A: 使用 .env 文件（推荐）**

复制示例文件并填写你的配置：

```bash
# 复制示例文件
cp .env.example .env

# 编辑文件，填写你的 API Key
# 火山引擎方舟（推荐）
ARK_API_KEY=your-api-key-here
ARK_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

**方式 B: 使用 secrets.toml 文件**

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 编辑文件，填写你的配置
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

**方式 C: 使用环境变量**

```bash
# Linux/Mac - 火山引擎方舟
export ARK_API_KEY="your-api-key-here"
export ARK_API_BASE="https://ark.cn-beijing.volces.com/api/v3"

# Windows PowerShell
set ARK_API_KEY=your-api-key-here
set ARK_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

#### 4. （可选）配置 Git LFS（用于大文件管理）

如果您计划上传知识库文件（PDF、Word、PPT 等），建议配置 Git LFS：

```bash
# 安装 Git LFS（如果尚未安装）
# macOS
brew install git-lfs
# Linux
sudo apt-get install git-lfs
# Windows
# 下载并安装：https://git-lfs.github.com/

# 初始化 Git LFS
git lfs install

# 运行配置脚本
./scripts/setup_git_lfs.sh
```

详细说明请查看 [大文件处理指南](docs/LARGE_FILES_GUIDE.md)

#### 5. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

> **提示**: 如果未配置 API Key，系统将无法正常工作。请务必配置有效的 API Key。

## 📦 部署指南

### Streamlit Cloud 部署（推荐）

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

#### 3. 配置环境变量（关键步骤）

1. 部署完成后，进入应用主页
2. 点击右上角 **"···"** → **"Manage app"**
3. 左侧菜单选择 **"Settings"** → **"Secrets"**
4. 添加以下环境变量：

   ```
   Name: ARK_API_KEY
   Value: your-api-key-here
   ```

5. 点击 **"Save"**
6. 返回应用主页，点击 **"Re-deploy"**

### 支持的 LLM 服务

本系统使用 OpenAI 兼容接口，支持以下服务：

| 服务 | API Base | 模型 | 价格 | 特点 |
|-----|---------|------|------|------|
| **火山引擎方舟** | https://ark.cn-beijing.volces.com/api/v3 | deepseek-v3-2-251201 | 按官方定价 | 国内访问稳定、支持多模型 |
| **DeepSeek** | https://api.deepseek.com | deepseek-chat | ¥1/百万 tokens | 高性价比、中文优化 |
| **Kimi** | https://api.moonshot.cn/v1 | moonshot-v1 | ¥12/百万 tokens | 长上下文、中文优化 |
| **OpenAI** | https://api.openai.com/v1 | gpt-4 | $2.5/百万 tokens | 最强大的通用模型 |

**当前推荐配置**：火山引擎方舟 `deepseek-v3-2-251201`

### 其他部署方式

- **Hugging Face Spaces**: 免费部署，支持 GPU
- **Docker**: 适合生产环境
- **本地运行**: 适合开发测试

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 📁 项目结构

```
p7/
├── app.py                              # Streamlit Web 应用
├── requirements.txt                     # Python 依赖（完整版）
├── requirementsL.txt                    # Python 依赖（精简版，推荐）
├── README.md                            # 项目说明
├── .env.example                         # 环境变量模板
├── .streamlit/
│   ├── config.toml                      # Streamlit 配置
│   └── secrets.toml.example             # Secrets 模板
│
├── src/                                 # 源代码
│   ├── graphs/                          # LangGraph 工作流
│   │   ├── state.py                     # 全局状态定义
│   │   ├── state_materials.py           # 材料生成状态定义
│   │   ├── node.py                      # 检查功能节点
│   │   ├── nodes/                       # 节点目录
│   │   │   └── material_generate_nodes.py  # 材料生成节点
│   │   └── graph.py                     # 主图编排
│   │
│   ├── tools/                           # 工具函数
│   │   ├── knowledge_base_tool.py       # 知识库工具
│   │   └── ...
│   │
│   └── utils/                           # 工具函数
│       └── file/
│           └── file.py                  # 文件处理工具
│
├── config/                              # LLM 配置文件
│   ├── generate_checklist_cfg.json
│   ├── invalid_items_check_cfg.json
│   ├── commercial_score_check_cfg.json
│   ├── technical_plan_check_cfg.json
│   ├── indicator_response_check_cfg.json
│   ├── technical_score_check_cfg.json
│   ├── bid_structure_check_cfg.json
│   ├── modification_summary_cfg.json
│   ├── tender_requirements_parse_cfg.json
│   ├── commercial_material_generate_cfg.json
│   └── technical_material_generate_cfg.json
│
└── assets/                              # 资源目录
    ├── knowledge_base/                  # 知识库目录
    ├── tender_document.docx             # 示例招标文件
    └── bid_document.docx                # 示例投标文件
```

## 🔧 系统架构

### 工作流设计

系统采用 LangGraph 框架构建，包含两个主要工作流：

#### 1. 投标文件检查工作流

```
招标文件解析 ──┬──> 废标项检查 ──┐
               ├──> 商务得分检查 ──┤
投标文件解析 ──┼──> 技术方案检查 ──┤
               ├──> 指标应答检查 ──┤
               ├──> 技术得分检查 ──┤
               └──> 文件结构检查 ──┘
                                   │
                                   ├──> 修改建议汇总
                                   │
                                   └──> 输出检查报告
```

**特点**：
- 六个检查节点并行执行，提高效率
- 每个节点独立负责一个维度的检查
- 统一输出格式化的检查报告

#### 2. 投标材料生成工作流

```
招标文件解析 ──> 招标要求解析 ──┬──> 商务知识库检索 ──> 商务互联网搜索 ──> 商务材料生成
                                │
                                └──> 技术知识库检索 ──> 技术互联网搜索 ──> 技术材料生成
```

**特点**：
- 支持商务和技术材料并行生成
- 整合本地知识库和互联网搜索
- 自动标注素材出处

### 技术栈

- **工作流编排**: LangGraph 1.0
- **大语言模型**: 豆包（deepseek-v3-2-251201）
- **Web 框架**: Streamlit
- **文档处理**: pypdf, python-docx, python-pptx, docx2python
- **LLM 接口**: langchain-openai
- **报告生成**: reportlab
- **知识库**: 基于文件系统的向量检索

## 📖 使用指南

### 投标文件检查

1. 上传**招标文件**（PDF、Word、PPT 格式）
2. 上传**投标文件**（PDF、Word、PPT 格式）
3. 点击"开始分析"按钮
4. 等待分析完成（约 1-3 分钟）
5. 查看六维度检查结果
6. 下载检查报告（PDF/Word/TXT）

### 投标材料生成

#### 准备知识库（可选）

1. 在 `assets/knowledge_base/` 目录下放入历史成功案例
2. 支持 PDF、Word、TXT 格式
3. 系统会自动向量化并建立索引

#### 生成材料

1. 上传**招标文件**
2. 选择材料类型（商务/技术）
3. 是否使用知识库（推荐启用）
4. 输入生成要求（可选）
5. 点击"生成材料"按钮
6. 等待生成完成（约 2-5 分钟）
7. 查看生成结果
8. 下载材料（Word/TXT）

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 必填 | 默认值 |
|--------|------|------|--------|
| `ARK_API_KEY` | 火山引擎方舟 API Key | ✅ | - |
| `ARK_API_BASE` | 火山引擎方舟 API Base | ✅ | https://ark.cn-beijing.volces.com/api/v3 |
| `COZE_WORKSPACE_PATH` | 工作空间路径 | ❌ | 自动设置 |

### 知识库配置

知识库目录：`assets/knowledge_base/`

支持的文件格式：
- PDF
- Word (.docx)
- 文本 (.txt)
- PowerPoint (.pptx)

### LLM 配置

所有 LLM 配置文件位于 `config/` 目录：

- 检查功能配置：`*_check_cfg.json`
- 生成功能配置：`*_generate_cfg.json`

配置文件结构：
```json
{
  "config": {
    "model": "deepseek-v3-2-251201",
    "temperature": 0.0,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "sp": "系统提示词",
  "up": "用户提示词（支持 Jinja2 模板）"
}
```

## 🔍 常见问题

### Q: 分析需要多长时间？

A: 
- 投标文件检查：1-3 分钟（取决于文件大小）
- 材料生成：2-5 分钟（取决于生成内容长度）

### Q: 支持哪些文件格式？

A: 
- 输入：PDF、Word (.docx)、PowerPoint (.pptx)
- 输出：PDF、Word、TXT

### Q: 知识库是必需的吗？

A: 不是必需的，但强烈推荐使用。知识库可以：
- 提供更准确的素材
- 减少幻觉
- 保持内容一致性

### Q: 生成的内容可以直接使用吗？

A: 生成的内容需要人工审核和修改。系统提供：
- 初稿框架
- 素材参考
- 来源标注

请根据实际情况进行调整和补充。

### Q: 如何提高生成质量？

A: 
1. 使用高质量的知识库
2. 提供详细的生成要求
3. 多次迭代生成
4. 人工审核和修改

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 📞 联系方式

- GitHub Issues: https://github.com/P7-code/p7/issues
- Email: [your-email@example.com]

## 🙏 致谢

感谢以下开源项目：

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://github.com/streamlit/streamlit)
- [豆包大模型](https://www.volcengine.com/product/ark)

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
