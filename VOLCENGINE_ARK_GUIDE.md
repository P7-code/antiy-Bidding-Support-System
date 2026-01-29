# 火山引擎方舟配置指南

本项目当前使用火山引擎方舟（Ark）的 `deepseek-v3-2-251201` 模型。

## 🔑 获取 API Key

### 1. 访问火山引擎方舟控制台

访问：https://console.volcengine.com/ark

### 2. 创建 API Key

1. 登录火山引擎账号
2. 进入"API Key 管理"页面
3. 点击"创建 API Key"
4. 复制生成的 API Key（格式如：`9cebea4f-aa41-47ea-942e-4bf1324d1162`）

### 3. 激活模型

1. 进入"模型推理"页面
2. 找到 `deepseek-v3-2-251201` 模型
3. 点击"激活模型"（如果未激活）

## ⚙️ 配置方式

### 方式 1: 在 Streamlit Cloud 中配置（推荐）

1. 访问 https://p7-code-p7.streamlit.app
2. 点击右上角 **"···"** → **"Manage app"**
3. 左侧菜单选择 **"Settings"** → **"Secrets"**
4. 添加以下环境变量：

   **变量 1: OPENAI_API_KEY**
   ```
   Name: OPENAI_API_KEY
   Value: 9cebea4f-aa41-47ea-942e-4bf1324d1162
   ```

   **变量 2: OPENAI_API_BASE**
   ```
   Name: OPENAI_API_BASE
   Value: https://ark.cn-beijing.volces.com/api/v3
   ```

5. 点击 **"Save"**
6. 返回应用主页，点击 **"Re-deploy"**

### 方式 2: 使用 secrets.toml 文件

创建 `.streamlit/secrets.toml` 文件：

```toml
OPENAI_API_KEY = "9cebea4f-aa41-47ea-942e-4bf1324d1162"
OPENAI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
```

### 方式 3: 使用环境变量（本地开发）

```bash
# Linux/Mac
export OPENAI_API_KEY="9cebea4f-aa41-47ea-942e-4bf1324d1162"
export OPENAI_API_BASE="https://ark.cn-beijing.volces.com/api/v3"

# Windows
set OPENAI_API_KEY=9cebea4f-aa41-47ea-942e-4bf1324d1162
set OPENAI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

## 📋 API 配置说明

### API Base

```
https://ark.cn-beijing.volces.com/api/v3
```

**注意**：不要在 API Base 后面添加 `/chat/completions` 或 `/responses`，langchain-openai 会自动添加正确的路径。

### 模型名称

```
deepseek-v3-2-251201
```

**注意**：模型名称已硬编码在配置文件中，无需修改。

### API Key 格式

火山引擎方舟的 API Key 格式为 UUID，例如：
```
9cebea4f-aa41-47ea-942e-4bf1324d1162
```

## 🔍 验证配置

### 测试 API 连接

```python
import os
from langchain_openai import ChatOpenAI

# 配置
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

# 创建客户端
llm = ChatOpenAI(
    model="deepseek-v3-2-251201",
    openai_api_key=api_key,
    openai_api_base=api_base
)

# 测试调用
response = llm.invoke("你好，请介绍一下你自己")
print(response.content)
```

### 常见错误

**错误 1: 404 ModelNotOpen**
```
Error code: 404 - ModelNotOpen
Your account has not activated the model deepseek-v3-2-251228
```

**解决方案**：
- 确认模型 ID 正确：`deepseek-v3-2-251201`
- 在火山引擎方舟控制台激活该模型

**错误 2: 401 Unauthorized**
```
Error code: 401 - Unauthorized
Invalid API Key
```

**解决方案**：
- 检查 API Key 是否正确
- 确认 API Key 已在控制台创建
- 确认 API Key 未过期

**错误 3: Connection Error**
```
ConnectionError: Failed to establish a new connection
```

**解决方案**：
- 检查网络连接
- 确认 API Base 地址正确
- 尝试切换网络环境

## 💰 费用说明

火山引擎方舟的定价请参考官方文档：https://www.volcengine.com/docs/82379/1263482

**注意**：
- 使用 LLM 服务会产生费用
- 建议设置配额限制
- 定期查看账单和用量

## 🔗 相关链接

- **火山引擎方舟控制台**：https://console.volcengine.com/ark
- **API 文档**：https://www.volcengine.com/docs/82379
- **定价说明**：https://www.volcengine.com/docs/82379/1263482
- **模型列表**：https://www.volcengine.com/docs/82379/1263481

## 🆘 技术支持

遇到问题可以：
1. 查看火山引擎方舟官方文档
2. 联系火山引擎技术支持
3. 提交 GitHub Issue：https://github.com/P7-code/p7/issues
