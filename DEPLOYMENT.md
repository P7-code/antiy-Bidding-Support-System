# 安天投标文件智能分析系统 - 部署指南

本指南提供多种部署方式，适用于不同场景。

## 📦 部署方式概览

| 部署方式 | 难度 | 适用场景 | 推荐 |
|---------|------|---------|------|
| Streamlit Cloud | ⭐ | 快速上线、个人项目 | ✅ |
| Hugging Face Spaces | ⭐⭐ | 免费 GPU、AI 项目 | ✅ |
| Docker | ⭐⭐⭐ | 生产环境、企业部署 | - |
| 本地运行 | - | 开发测试 | - |

---

## 方式 1: Streamlit Cloud 部署（推荐）

### 优点
- ✅ 完全免费
- ✅ 自动部署
- ✅ 支持自定义域名
- ✅ 一键配置

### 步骤

#### 1. 准备 GitHub 仓库

```bash
# 克隆仓库
git clone https://github.com/P7-code/p7.git
cd p7

# 配置 secrets（参考 README.md）
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# 编辑 .streamlit/secrets.toml 填写你的 API Key

# 提交到 GitHub
git add .
git commit -m "chore: 准备部署"
git push origin main
```

#### 2. 连接 Streamlit Cloud

1. 访问 https://share.streamlit.io
2. 使用 GitHub 账号登录
3. 点击 **"New app"**
4. 填写配置：
   ```
   Repository: P7-code/p7
   Branch: main
   Main file path: app.py
   ```
5. 点击 **"Deploy"**

#### 3. 配置 Secrets（关键步骤）

**方式 A: 在 Streamlit Cloud 界面配置**

1. 部署完成后，进入应用主页
2. 点击右上角 **"···"** → **"Manage app"**
3. 左侧菜单选择 **"Settings"** → **"Secrets"**
4. 点击 **"+ New secret"**
5. 添加以下环境变量：

   **变量 1: OPENAI_API_KEY**
   ```
   Name: OPENAI_API_KEY
   Value: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   点击 **"Save"**

   **变量 2: OPENAI_API_BASE**（可选）
   ```
   Name: OPENAI_API_BASE
   Value: https://api.deepseek.com
   ```
   点击 **"Save"**

6. 返回应用主页，点击 **"Re-deploy"**
7. 等待 2-5 分钟重新部署完成

**方式 B: 使用 secrets.toml 文件（推荐）**

如果不想在 Streamlit Cloud 界面配置，可以在本地创建 `.streamlit/secrets.toml` 文件并提交到 Git（仅用于测试，不推荐生产环境使用）。

#### 4. 验证部署

访问你的应用地址：`https://[your-username]-p7.streamlit.app`

#### 5. 自定义域名（可选）

1. 进入 **"Manage app"** → **"Settings"**
2. 找到 **"Custom domains"**
3. 添加你的域名（如 `bid-analysis.yourdomain.com`）
4. 在域名 DNS 设置中添加 CNAME 记录：
   ```
   Type: CNAME
   Name: bid-analysis
   Value: your-app.streamlit.app
   ```

---

## 方式 2: Hugging Face Spaces 部署

### 优点
- ✅ 完全免费
- ✅ 支持 GPU
- ✅ 适合 AI 项目

### 步骤

#### 1. 创建 Space

1. 访问 https://huggingface.co/spaces
2. 登录后点击 **"Create new Space"**
3. 配置：
   ```
   Space Name: p7-bid-analysis
   License: MIT
   SDK: Streamlit
   Hardware: CPU basic (免费)
   Public/Private: Public
   ```
4. 点击 **"Create Space"**

#### 2. 上传代码

**方式 A: 使用 Git**

```bash
git clone https://huggingface.co/spaces/your-username/p7-bid-analysis
cd p7-bid-analysis
# 复制你的代码到当前目录
git add .
git commit -m "Initial commit"
git push
```

**方式 B: 使用 Web 界面**

在 Space 页面点击 **"Files"** → **"Add file"** → **"Upload files"**，上传所有文件。

#### 3. 配置 Secrets

1. 进入 Space 的 **"Settings"** 标签
2. 找到 **"Repository secrets"**
3. 点击 **"New secret"**
4. 添加以下环境变量：

   ```
   Name: OPENAI_API_KEY
   Value: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

   ```
   Name: OPENAI_API_BASE
   Value: https://api.deepseek.com
   ```

5. 点击 **"Create secret"**

#### 4. 重新部署

修改代码后，Space 会自动重新部署。手动重新部署：

1. 进入 **"Settings"** → **"Factory reset"**
2. 点击 **"Restart Space"**

#### 5. 访问应用

部署完成后，访问：`https://huggingface.co/spaces/your-username/p7-bid-analysis`

---

## 方式 3: Docker 部署

### 优点
- ✅ 环境隔离
- ✅ 易于管理
- ✅ 适合生产环境

### 步骤

#### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动应用
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. 构建 Docker 镜像

```bash
docker build -t p7-bid-analysis:latest .
```

#### 3. 运行容器

```bash
docker run -d \
  -p 8501:8501 \
  -e OPENAI_API_KEY="sk-xxxx" \
  -e OPENAI_API_BASE="https://api.deepseek.com" \
  --name p7-bid-analysis \
  p7-bid-analysis:latest
```

#### 4. 访问应用

访问：`http://localhost:8501`

#### 5. 停止容器

```bash
docker stop p7-bid-analysis
docker rm p7-bid-analysis
```

---

## 方式 4: 本地运行

### Windows

```powershell
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
set OPENAI_API_KEY=sk-xxxx
set OPENAI_API_BASE=https://api.deepseek.com

# 运行应用
streamlit run app.py
```

### Linux/Mac

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OPENAI_API_KEY="sk-xxxx"
export OPENAI_API_BASE="https://api.deepseek.com"

# 运行应用
streamlit run app.py
```

---

## 🔐 环境变量配置

### 必需变量

| 变量名 | 说明 | 示例值 |
|-------|------|--------|
| OPENAI_API_KEY | API 密钥 | sk-xxxxxxxxxxxxxxxx |
| OPENAI_API_BASE | API 基础URL | https://api.deepseek.com |

### 可选变量

| 变量名 | 说明 | 默认值 |
|-------|------|--------|
| MODEL_NAME | 模型名称 | gpt-4o-mini |
| TEMPERATURE | 温度参数 | 0.0 |
| MAX_TOKENS | 最大 Token 数 | 4000 |

---

## 📊 支持的 LLM 服务

### 火山引擎方舟（当前使用）

```toml
OPENAI_API_KEY = "9cebea4f-aa41-47ea-942e-4bf1324d1162"
OPENAI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
```

- 官网：https://console.volcengine.com/ark
- 价格：按官方定价
- 特点：支持多模型、国内访问稳定、API 响应快速
- 当前模型：`deepseek-v3-2-251201`

详细配置请参考：[VOLCENGINE_ARK_GUIDE.md](./VOLCENGINE_ARK_GUIDE.md)

### DeepSeek

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.deepseek.com"
```

- 官网：https://platform.deepseek.com
- 价格：¥1/百万 tokens
- 特点：高性价比、中文优化

### Kimi (Moonshot AI)

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.moonshot.cn/v1"
```

- 官网：https://platform.moonshot.cn
- 价格：¥12/百万 tokens
- 特点：长上下文、中文优化

### OpenAI

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.openai.com/v1"
```

- 官网：https://platform.openai.com
- 价格：$2.5/百万 tokens
- 特点：最强大的通用模型

### 智谱 AI (GLM)

```toml
OPENAI_API_KEY = "xxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
```

- 官网：https://open.bigmodel.cn
- 价格：¥5/百万 tokens
- 特点：中文优化、API 稳定

---

## ⚠️ 常见问题

### 1. Streamlit Cloud 部署失败

**问题**: `Error installing requirements`

**解决方案**:
- 检查 `requirements.txt` 是否包含私有包
- 移除 `coze-coding-dev-sdk` 等私有依赖
- 确保所有依赖都可以通过 `pip install` 安装

### 2. 应用启动后显示"演示模式"

**问题**: 未配置 API Key，系统运行在演示模式

**解决方案**:
- 在 Streamlit Cloud 配置 Secrets
- 添加 `OPENAI_API_KEY` 和 `OPENAI_API_BASE` 环境变量
- 重新部署应用

### 3. 文件上传失败

**问题**: 文件过大导致上传失败

**解决方案**:
- Streamlit Cloud 默认限制 200MB
- 压缩文件后再上传
- 或使用对象存储服务

### 4. LLM 调用超时

**问题**: API 调用超时

**解决方案**:
- 检查网络连接
- 增加超时时间
- 更换 API 服务提供商

---

## 🚀 性能优化

### 1. 减少 LLM 调用次数

- 合并相似的分析任务
- 使用更长的上下文窗口
- 优化 Prompt 设计

### 2. 使用缓存

```python
@st.cache_data
def load_file(file_path):
    # 文件加载逻辑
    pass
```

### 3. 异步处理

```python
import asyncio

async def analyze_file(file):
    # 异步分析逻辑
    pass
```

### 4. 使用更快的模型

- 从 `gpt-4` 切换到 `gpt-4o-mini`
- 或使用 DeepSeek、Kimi 等更便宜的模型

---

## 📈 监控与日志

### Streamlit Cloud

- 自动收集使用统计
- 可以在 "Manage app" 查看日志
- 设置告警通知

### 本地部署

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🔒 安全建议

1. **永远不要在代码中硬编码 API Key**
   - 使用环境变量或 Secrets
   - 确保 `.streamlit/secrets.toml` 在 `.gitignore` 中

2. **使用 HTTPS**
   - 确保部署在 HTTPS 环境下
   - 使用自定义域名和 SSL 证书

3. **限制访问**
   - 添加身份验证
   - 使用 IP 白名单
   - 设置访问频率限制

4. **定期更新依赖**
   - 定期运行 `pip install --upgrade -r requirements.txt`
   - 关注安全公告

---

## 📞 技术支持

- **GitHub Issues**: https://github.com/P7-code/p7/issues
- **文档**: https://github.com/P7-code/p7/blob/main/README.md
- **在线演示**: https://p7-code-p7.streamlit.app

---

## 📄 许可证

MIT License

---

**祝你部署顺利！** 🚀
