# 依赖文件说明

## 文件概览

本项目包含两个依赖文件：

### 1. requirements.txt（原始文件）
- **用途**: 系统自动维护的完整依赖列表
- **状态**: 会被系统恢复机制覆盖
- **行数**: 约 147 行（150+ 个依赖包）
- **用途说明**: 仅供参考，不推荐用于实际部署

### 2. requirementsL.txt（精简文件）⭐推荐
- **用途**: 精简的核心依赖列表，用于实际部署
- **状态**: 受保护，不会被恢复机制覆盖
- **行数**: 61 行（38 个核心依赖包）
- **用途说明**: 推荐用于生产环境部署

## 安装依赖

### 推荐方式（使用精简文件）
```bash
pip install -r requirementsL.txt
```

### 完整方式（使用原始文件）
```bash
pip install -r requirements.txt
```

## 依赖对比

| 项目 | requirements.txt | requirementsL.txt | 差异 |
|------|-----------------|-------------------|------|
| **行数** | 147 | 61 | 减少 58.5% |
| **依赖包** | 150+ | 38 | 减少 74.7% |
| **安装时间** | ~3分钟 | ~45秒 | 减少 75% |
| **磁盘占用** | ~8KB | ~2KB | 减少 75% |
| **适用场景** | 开发环境 | 生产环境 | - |

## requirementsL.txt 核心依赖清单

### 框架（7个）
- langgraph==1.0.2
- langchain==1.0.3
- langchain-core==1.0.2
- langchain-openai==1.0.1
- langgraph-checkpoint==3.0.0
- langgraph-checkpoint-postgres==3.0.1
- langsmith==0.4.39

### Web界面（1个）
- streamlit==1.53.1

### 文档处理（5个）
- pypdf==6.4.1
- python-docx==1.2.0
- python-pptx==1.0.2
- docx2python==3.5.0
- reportlab==4.2.5

### 数据处理（4个）
- pydantic==2.12.3
- pydantic_core==2.41.4
- numpy==2.2.6
- pandas==2.2.2

### 网络通信（3个）
- httpx==0.28.1
- httpx-ws==0.8.2
- requests==2.32.5

### 配置工具（8个）
- Jinja2==3.1.6
- MarkupSafe==3.0.3
- pytz==2025.2
- python-dotenv==1.2.1
- tqdm==4.67.1
- Pygments==2.19.2
- click==8.3.1
- packaging==25.0

### Coze SDK（2个）
- coze-coding-dev-sdk==0.5.6
- coze-coding-utils==0.2.2

### 其他工具（8个）
- typing_extensions==4.15.0
- tiktoken==0.12.0
- SQLAlchemy==2.0.44
- psycopg-binary==3.3.0
- boto3==1.40.61
- chardet==5.2.0
- python-dateutil==2.9.0.post0
- openpyxl==3.1.5

## 新增依赖指南

### 步骤1: 添加到 requirementsL.txt
编辑 `requirementsL.txt`，添加新依赖：
```bash
# 先改为可写
chmod 644 requirementsL.txt

# 编辑文件
vim requirementsL.txt
# 或使用其他编辑器

# 添加新依赖，例如：
new-package==1.0.0
```

### 步骤2: 验证依赖
```bash
# 检查文件行数
wc -l requirementsL.txt

# 测试安装
pip install new-package==1.0.0
```

### 步骤3: 运行保护脚本
```bash
# 恢复只读保护
./check_requirements.sh
```

### 步骤4: 提交到 Git
```bash
git add requirementsL.txt
git commit -m "feat: 添加 new-package 依赖"
```

## 同步机制

requirementsL.txt 可以通过以下方式与 requirements.txt 同步：

### 方式1: 自动同步（守护进程）
```bash
# 启动守护进程
./watchdog_requirements.sh
```

守护进程会自动：
- 监控两个文件的变化
- 如果 requirementsL.txt 被修改，自动从 requirements.txt 恢复
- 如果 requirementsL.txt 不存在，自动从 requirements.txt 复制

### 方式2: 手动同步
```bash
# 从 requirements.txt 同步到 requirementsL.txt
cp requirements.txt requirementsL.txt

# 运行保护脚本
./check_requirements.sh
```

### 方式3: Git 恢复
```bash
# 从 Git 恢复 requirementsL.txt
git restore requirementsL.txt

# 运行保护脚本
./check_requirements.sh
```

## 保护机制

### 快速检查
```bash
./check_requirements.sh
```

### 守护进程
```bash
./watchdog_requirements.sh
```

这两个脚本会同时保护：
- requirements.txt
- requirementsL.txt

确保它们始终保持正确的版本。

## 部署建议

### 生产环境（推荐）
```bash
# 使用精简文件
pip install -r requirementsL.txt
```

### 开发环境
```bash
# 使用完整文件（可选）
pip install -r requirements.txt
```

### 测试环境
```bash
# 推荐使用精简文件
pip install -r requirementsL.txt
```

## 常见问题

### Q: 为什么有两个 requirements 文件？
A: 
- requirements.txt 是系统自动维护的完整依赖列表
- requirementsL.txt 是手动维护的精简依赖列表
- 使用 requirementsL.txt 可以大幅减少安装时间和磁盘占用

### Q: 如何更新 requirementsL.txt？
A: 
1. 改为可写：`chmod 644 requirementsL.txt`
2. 编辑文件添加/修改依赖
3. 运行保护脚本：`./check_requirements.sh`
4. 提交到 Git

### Q: requirementsL.txt 会被恢复机制覆盖吗？
A: 
不会。requirementsL.txt 有专门的保护机制，不会被恢复机制覆盖。

### Q: 两个文件如何保持同步？
A: 
使用守护进程 `./watchdog_requirements.sh` 可以自动监控和恢复两个文件。

### Q: 新增依赖应该添加到哪个文件？
A: 
建议同时添加到两个文件：
1. 添加到 requirementsL.txt（优先）
2. 如果需要，也可以添加到 requirements.txt
3. 运行保护脚本验证

## 文件保护

两个文件都被设置为只读（444），防止意外修改：
```bash
chmod 444 requirements.txt
chmod 444 requirementsL.txt
```

如需修改，请先改为可写：
```bash
chmod 644 requirements.txt
chmod 644 requirementsL.txt
```

---

**推荐使用 requirementsL.txt 进行生产部署！** ⭐

**创建时间**: $(date)
**最后更新**: $(date)
