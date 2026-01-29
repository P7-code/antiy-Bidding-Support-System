# Coze 调试环境配置指南

本项目支持在 Coze 平台的调试环境中配置和使用大模型 API。

## 📋 环境变量说明

本项目需要配置以下环境变量：

| 变量名 | 说明 | 示例值 | 是否必需 |
|-------|------|--------|---------|
| `OPENAI_API_KEY` | API 密钥 | `9cebea4f-aa41-47ea-942e-4bf1324d1162` | ✅ 必需 |
| `OPENAI_API_BASE` | API 基础URL | `https://ark.cn-beijing.volces.com/api/v3` | ✅ 必需 |

## 🔧 在 Coze 平台上配置环境变量

### 步骤 1: 登录 Coze 平台

访问 Coze 平台并登录你的账号。

### 步骤 2: 进入项目设置

1. 找到你的项目
2. 进入项目设置页面
3. 找到"环境变量"或"Environment Variables"配置项

### 步骤 3: 添加环境变量

**变量 1: OPENAI_API_KEY**

- **Key**: `OPENAI_API_KEY`
- **Value**: 你的 API 密钥
  - 火山引擎方舟：`9cebea4f-aa41-47ea-942e-4bf1324d1162`
  - DeepSeek：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - Kimi：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - OpenAI：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**变量 2: OPENAI_API_BASE**

- **Key**: `OPENAI_API_BASE`
- **Value**: 你的 API 基础URL
  - 火山引擎方舟：`https://ark.cn-beijing.volces.com/api/v3`
  - DeepSeek：`https://api.deepseek.com`
  - Kimi：`https://api.moonshot.cn/v1`
  - OpenAI：`https://api.openai.com/v1`

### 步骤 4: 保存配置

保存环境变量配置。

## 🚀 在 Coze 调试环境中运行

### 自动加载环境变量

项目使用 `coze_workload_identity` 自动加载环境变量：

```python
import os
from coze_workload_identity import Client

# 获取项目环境变量
client = Client()
env_vars = client.get_project_env_vars()
client.close()

# 输出环境变量
for env_var in env_vars:
    print(f"{env_var.key}={env_var.value}")
```

### 使用环境变量

在代码中使用环境变量：

```python
import os

# 获取 API 配置
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

# 使用配置
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-v3-2-251201",
    openai_api_key=api_key,
    openai_api_base=api_base
)
```

## 📊 支持的 LLM 服务

### 1. 火山引擎方舟（推荐）

```toml
OPENAI_API_KEY = "9cebea4f-aa41-47ea-942e-4bf1324d1162"
OPENAI_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
```

- 官网：https://console.volcengine.com/ark
- 当前模型：`deepseek-v3-2-251201`
- 特点：支持多模型、国内访问稳定

### 2. DeepSeek

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.deepseek.com"
```

- 官网：https://platform.deepseek.com
- 价格：¥1/百万 tokens
- 特点：高性价比、中文优化

### 3. Kimi (Moonshot AI)

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.moonshot.cn/v1"
```

- 官网：https://platform.moonshot.cn
- 价格：¥12/百万 tokens
- 特点：长上下文、中文优化

### 4. OpenAI

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_BASE = "https://api.openai.com/v1"
```

- 官网：https://platform.openai.com
- 价格：$2.5/百万 tokens
- 特点：最强大的通用模型

## 🧪 测试配置

### 测试脚本

创建测试脚本 `test_api_config.py`：

```python
#!/usr/bin/env python3
"""
测试 API 配置是否正确
"""
import os
import sys

# 添加 src 到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langchain_openai import ChatOpenAI

# 获取环境变量
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

print(f"API Key: {'*' * (len(api_key) - 4)}{api_key[-4:] if api_key else 'None'}")
print(f"API Base: {api_base}")

if not api_key:
    print("❌ 未配置 OPENAI_API_KEY")
    sys.exit(1)

if not api_base:
    print("❌ 未配置 OPENAI_API_BASE")
    sys.exit(1)

# 测试 API 连接
try:
    llm = ChatOpenAI(
        model="deepseek-v3-2-251201",
        openai_api_key=api_key,
        openai_api_base=api_base
    )

    response = llm.invoke("你好，请介绍一下你自己")
    print(f"✅ API 配置成功！")
    print(f"LLM 响应: {response.content[:100]}...")
    
except Exception as e:
    print(f"❌ API 配置失败: {e}")
    sys.exit(1)
```

运行测试：

```bash
python test_api_config.py
```

## ⚠️ 常见问题

### 问题 1: 环境变量未生效

**症状**：
```
由于未配置 LLM API Key，系统返回演示结果。
```

**解决方案**：
1. 确认在 Coze 平台上正确配置了环境变量
2. 确认环境变量名称拼写正确（`OPENAI_API_KEY`、`OPENAI_API_BASE`）
3. 重新启动调试环境

### 问题 2: API 调用失败

**症状**：
```
Error code: 404 - ModelNotOpen
```

**解决方案**：
1. 确认模型 ID 正确（当前使用 `deepseek-v3-2-251201`）
2. 确认 API Key 有效且已激活对应模型
3. 确认 API Base 地址正确

### 问题 3: 连接超时

**症状**：
```
ConnectionError: Failed to establish a new connection
```

**解决方案**：
1. 检查网络连接
2. 确认 API Base 地址正确
3. 尝试切换网络环境

## 📖 相关文档

- **火山引擎方舟配置指南**：[VOLCENGINE_ARK_GUIDE.md](./VOLCENGINE_ARK_GUIDE.md)
- **部署指南**：[DEPLOYMENT.md](./DEPLOYMENT.md)
- **项目结构**：[AGENTS.md](./AGENTS.md)

## 🔗 Coze 平台相关

- Coze 平台文档
- `coze_workload_identity` 使用说明
- 项目配置文件：`.coze`

---

**🎉 配置完成后，就可以在 Coze 调试环境中正常使用大模型了！**
