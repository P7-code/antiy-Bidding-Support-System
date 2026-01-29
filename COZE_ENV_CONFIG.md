在 Coze 调试环境中直接执行：

```python
import os

# 设置环境变量
os.environ["OPENAI_API_KEY"] = "9cebea4f-aa41-47ea-942e-4bf1324d1162"
os.environ["OPENAI_API_BASE"] = "https://ark.cn-beijing.volces.com/api/v3"

# 然后运行你的代码
from graphs.graph import main_graph
# ... 其他代码
```

---

## 🔍 验证配置是否成功

### 方法 1: 运行测试脚本

```bash
python scripts/load_coze_env.py
```

### 方法 2: 检查环境变量

```python
import os

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', '未配置')}")
print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', '未配置')}")
```

### 方法 3: 运行工作流

```python
from graphs.graph import main_graph

# 测试工作流
result = main_graph.invoke(input_data)
print(result)
```

---

## ⚠️ 注意事项

1. **安全性**：`.coze.env` 文件已在 `.gitignore` 中，不会提交到 Git
2. **优先级**：代码会自动加载 `.coze.env` 文件
3. **备份**：建议保存 `.coze.env.example` 文件作为模板

---

## 📋 配置示例

### 火山引擎方舟（当前配置）

```bash
OPENAI_API_KEY=9cebea4f-aa41-47ea-942e-4bf1324d1162
OPENAI_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### DeepSeek

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.deepseek.com
```

### Kimi

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.moonshot.cn/v1
```

---

## 🚀 开始使用

配置完成后，直接运行你的代码即可：

```bash
# 方式 1: 运行 Streamlit 应用
streamlit run app.py

# 方式 2: 运行测试
python -m pytest

# 方式 3: 在 Coze 调试环境中运行
python src/main.py
```

---

## ❓ 常见问题

### Q1: 修改 .coze.env 后没有生效？

**A**: 需要重新启动 Python 进程或重新加载模块：

```python
import importlib
import src.graphs.node as node
importlib.reload(node)
```

### Q2: 如何查看当前加载的环境变量？

**A**: 运行以下命令：

```python
import os
print("OPENAI_API_KEY:", os.getenv('OPENAI_API_KEY'))
print("OPENAI_API_BASE:", os.getenv('OPENAI_API_BASE'))
```

### Q3: 仍然显示"演示模式"？

**A**: 检查以下几点：
1. `.coze.env` 文件是否存在
2. 文件路径是否正确（应该在项目根目录）
3. 文件格式是否正确（KEY=VALUE 格式）

---

**🎉 配置完成后，就可以在 Coze 调试环境中正常使用大模型了！**
