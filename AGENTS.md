## 项目概述
- **名称**: 安天投标文件智能分析系统
- **功能**: 基于 LangGraph 的智能招标文件分析系统，专为网络安全售前工程师设计。提供投标文件智能检查和投标材料自动生成两大核心功能。

### 节点清单

#### 投标文件检查流程
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| tender_doc_parse | `node.py` | task | 解析招标文件 | - | - |
| bid_doc_parse | `node.py` | task | 解析投标文件 | - | - |
| invalid_items_check | `node.py` | agent | 废标项检查 | - | `config/invalid_items_check_cfg.json` |
| commercial_score_check | `node.py` | agent | 商务得分点检查 | - | `config/commercial_score_check_cfg.json` |
| technical_plan_check | `node.py` | agent | 技术方案检查 | - | `config/technical_plan_check_cfg.json` |
| indicator_response_check | `node.py` | agent | 指标与应答检查 | - | `config/indicator_response_check_cfg.json` |
| technical_score_check | `node.py` | agent | 技术得分点检查 | - | `config/technical_score_check_cfg.json` |
| bid_structure_check | `node.py` | agent | 投标文件结构检查 | - | `config/bid_structure_check_cfg.json` |
| modification_summary | `node.py` | agent | 结果汇总与建议生成 | - | `config/modification_summary_cfg.json` |
| route_by_workflow_type | `graph.py` | condition | 工作流类型路由 | check→check_workflow, generate→tender_requirements_parse | - |

#### 投标材料生成流程
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| tender_requirements_parse | `nodes/material_generate_nodes.py` | agent | 解析招标文件，提取商务和技术要求 | - | `config/tender_requirements_parse_cfg.json` |
| commercial_kb_search | `nodes/material_generate_nodes.py` | task | 商务知识库检索（使用新的索引系统） | - | - |
| commercial_web_search | `nodes/material_generate_nodes.py` | task | 商务互联网搜索 | - | - |
| commercial_material_generate | `nodes/material_generate_nodes.py` | agent | 生成商务投标材料 | - | `config/commercial_material_generate_cfg.json` |
| technical_kb_search | `nodes/material_generate_nodes.py` | task | 技术知识库检索（使用新的索引系统） | - | - |
| technical_web_search | `nodes/material_generate_nodes.py` | task | 技术互联网搜索 | - | - |
| technical_material_generate | `nodes/material_generate_nodes.py` | agent | 生成技术投标材料 | - | `config/technical_material_generate_cfg.json` |

#### 知识库管理流程
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| scan_and_index_files | `nodes/knowledge_manager_nodes.py` | task | 扫描 datafiles 目录并更新索引 | - | - |
| create_file_index | `nodes/knowledge_manager_nodes.py` | task | 为单个文件创建索引（提取摘要、标签） | - | `config/knowledge_summary_cfg.json` |
| update_file_index | `nodes/knowledge_manager_nodes.py` | task | 更新已有文件的索引 | - | `config/knowledge_summary_cfg.json` |
| delete_file_index | `nodes/knowledge_manager_nodes.py` | task | 删除文件的索引 | - | - |
| edit_index | `nodes/knowledge_manager_nodes.py` | task | 编辑索引元数据（摘要、标签、方向等） | - | - |
| search_knowledge | `nodes/knowledge_manager_nodes.py` | task | 搜索知识库（基于关键词和摘要） | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 集成使用
- 节点`tender_doc_parse`使用集成 pypdf/docx2python
- 节点`bid_doc_parse`使用集成 pypdf/docx2python
- 节点`commercial_kb_search`使用集成 知识库（KnowledgeIndexer）
- 节点`technical_kb_search`使用集成 知识库（KnowledgeIndexer）
- 节点`create_file_index`使用集成 大语言模型
- 节点`update_file_index`使用集成 大语言模型
- 节点`commercial_web_search`使用集成 联网搜索
- 节点`technical_web_search`使用集成 联网搜索
- 节点`modification_summary`使用集成 报告生成
- 所有agent节点使用集成 大语言模型 (deepseek-v3-2-251201)

## 工作流说明

### 1. 投标文件检查流程
**入口**: `tender_doc_parse` → `bid_doc_parse`

**并行检查维度**:
- 废标项检查 (`invalid_items_check`)
- 商务得分点检查 (`commercial_score_check`)
- 技术方案检查 (`technical_plan_check`)
- 指标与应答检查 (`indicator_response_check`)
- 技术得分点检查 (`technical_score_check`)
- 投标文件结构检查 (`bid_structure_check`)

**汇聚节点**: `modification_summary` (汇总六维度检查结果，生成最终修改建议)

### 2. 投标材料生成流程
**入口**: `tender_doc_parse` → `tender_requirements_parse`

**并行生成分支**:
1. **商务材料生成**:
   - `commercial_kb_search` (知识库检索，使用新的索引系统)
   - `commercial_web_search` (互联网搜索)
   - `commercial_material_generate` (生成商务材料)

2. **技术材料生成**:
   - `technical_kb_search` (知识库检索，使用新的索引系统)
   - `technical_web_search` (互联网搜索)
   - `technical_material_generate` (生成技术材料)

**结束**: 商务和技术材料都生成完成后，工作流结束

### 3. 知识库管理流程
**功能**: 管理 datafiles 目录下的知识文档索引

**索引创建流程**:
```
扫描文件 (scan_and_index_files)
    ↓
检测文件变化（新增、修改、删除）
    ↓
为每个文件提取内容
    ↓
调用 LLM 生成摘要和关键词 (create_file_index)
    ↓
保存索引到 knowledge_index.json
```

**索引更新流程**:
```
检测文件哈希变化
    ↓
更新文件索引 (update_file_index)
    ↓
重新生成摘要和关键词
    ↓
更新索引文件
```

**知识库检索流程**:
```
接收查询词
    ↓
多维度匹配（标签、摘要、关键词）
    ↓
计算匹配分数
    ↓
返回 Top-K 结果
```

**定时扫描流程**:
- 使用 `KnowledgeScheduler` 定时扫描 datafiles 目录
- 默认间隔：15 分钟
- 自动检测文件变化并更新索引
- 记录扫描日志到 `datafiles/knowledge_scheduler.log`

### 3. 路由逻辑
通过 `route_by_workflow_type` 条件节点根据 `workflow_type` 参数路由：
- `workflow_type="check"` → 进入投标文件检查流程
- `workflow_type="generate"` → 进入投标材料生成流程

## 工作流架构

### 检查模式架构（workflow_type = "check"）

```
┌─────────────┐
│tender_doc_  │
│  parse      │ 串行
└──────┬──────┘
       │
┌──────▼──────┐
│bid_doc_     │
│  parse      │ 串行
└──────┬──────┘
       │
  ┌────┴──────────────────────────────────────────┐
  │                六维并行检测                     │
  ├──────────┬──────────┬──────────┬──────────────┤
  │          │          │          │              │
  │invalid_  │commercial│technical │indicator_    │
  │ items    │ _score   │ _plan    │ response     │
  │ _check   │ _check   │ _check   │ _check       │
  │          │          │          │              │
  ├──────────┴──────────┴──────────┴──────────────┤
  │          │          │          │              │
  │technical │bid_      │          │              │
  │_score    │ structure│          │              │
  │_check    │_check    │          │              │
  │          │          │          │              │
  └──────────┴──────────┴──────────┴──────────────┘
                          │
                  ┌───────▼────────┐
                  │modification_   │
                  │   summary      │ 串行
                  └────────────────┘
```

### 生成模式架构（workflow_type = "generate"）

```
┌─────────────────────────┐
│      tender_doc_        │
│         parse           │ 串行
└───────────┬─────────────┘
            │
    ┌───────▼──────────────────────────────────────┐
    │   tender_requirements_parse                   │ 串行
    └───────────┬──────────────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
  ┌─────▼────────┐  ┌───▼──────────┐
  │商务材料生成    │  │ 技术材料生成   │ 并行
  └─────┬────────┘  └───┬──────────┘
        │                │
  ┌─────▼──────┐  ┌─────▼──────┐
  │kb_search   │  │kb_search   │ 串行
  └─────┬──────┘  └─────┬──────┘
        │                │
  ┌─────▼──────┐  ┌─────▼──────┐
  │web_search  │  │web_search  │ 串行
  └─────┬──────┘  └─────┬──────┘
        │                │
  ┌─────▼────────────────▼──────┐
  │material_generate (汇聚)      │ 并行
  └─────────────────────────────┘
```

## 配置文件清单

### 检查模式配置文件
| 配置文件 | 用途 |
|---------|------|
| `config/invalid_items_check_cfg.json` | 废标项检查的 LLM 配置 |
| `config/commercial_score_check_cfg.json` | 商务得分检查的 LLM 配置 |
| `config/technical_plan_check_cfg.json` | 技术方案检查的 LLM 配置 |
| `config/indicator_response_check_cfg.json` | 指标应答检查的 LLM 配置 |
| `config/technical_score_check_cfg.json` | 技术得分检查的 LLM 配置 |
| `config/bid_structure_check_cfg.json` | 文件结构检查的 LLM 配置 |
| `config/modification_summary_cfg.json` | 汇总修改建议的 LLM 配置 |

### 生成模式配置文件
| 配置文件 | 用途 |
|---------|------|
| `config/tender_requirements_parse_cfg.json` | 招标要求解析的 LLM 配置 |
| `config/commercial_material_generate_cfg.json` | 商务材料生成的 LLM 配置 |
| `config/technical_material_generate_cfg.json` | 技术材料生成的 LLM 配置 |

### 知识库管理配置文件
| 配置文件 | 用途 |
|---------|------|
| `config/knowledge_summary_cfg.json` | 知识摘要生成的 LLM 配置 |

### 数据文件
| 文件路径 | 用途 |
|---------|------|
| `datafiles/knowledge_index.json` | 知识库索引文件（包含所有文档的摘要、标签、元数据） |
| `datafiles/knowledge_scheduler.log` | 定时扫描日志文件 |
| `datafiles/` | 知识文档存储目录（PDF、DOCX、PPTX、TXT） |

## 关键文件说明

### `src/graphs/state.py`
- 定义全局状态 `GlobalState`（包含检查和生成两种流程的所有字段）
- 定义工作流输入 `GraphInput` 和输出 `GraphOutput`
- 定义每个节点的独立输入输出类

### `src/graphs/node.py`
- 实现所有检查模式节点函数
- 包含文件解析、LLM 调用等核心逻辑

### `src/graphs/state_materials.py`
- 定义材料生成相关的节点输入输出类
- 包含招标要求解析、知识库检索、材料生成等节点的状态定义

### `src/graphs/nodes/material_generate_nodes.py`
- 实现材料生成相关节点函数
- 包括招标要求解析、知识库检索、网络搜索、材料生成等节点

### `src/graphs/graph.py`
- 定义主图结构
- 包含检查模式和生成模式的所有节点
- 通过条件路由 `route_by_workflow_type` 选择执行路径
- 商务材料和技术材料生成节点并行执行

### `src/tools/knowledge_indexer.py`
- 知识库索引管理工具类
- 支持文件扫描、索引创建、更新、删除
- 支持多维度搜索（标签、摘要、关键词）
- 索引持久化到 JSON 文件

### `src/tools/knowledge_scheduler.py`
- 定时任务调度器
- 支持自定义扫描间隔（1-1440 分钟）
- 自动检测文件变化并更新索引
- 记录扫描日志

### `src/knowledge_management.py`
- 知识库管理页面模块
- 提供四个标签页：概览、文件索引、编辑索引、定时任务配置
- 支持手动扫描、编辑索引、删除索引
- 支持启动/停止定时调度器

### `src/graphs/state_knowledge.py`
- 知识库相关的状态定义
- 定义 `KnowledgeIndex`、`KnowledgeLibrary`、`FileMetadata`、`DocumentSummary` 等数据结构
- 支持技术关键词、商务关键词、搜索标签、知识方向等字段

### `src/graphs/nodes/knowledge_manager_nodes.py`
- 知识库管理节点实现
- 包含索引创建、更新、删除、编辑、搜索等节点
- 集成大语言模型生成文档摘要和关键词

### `src/utils/file/file.py`
- 文件处理工具类
- 支持 PDF、Word、PPT 等格式
- 提供文本提取功能
- 提供文档结构提取功能（章节、页码）
- 用于知识库索引创建时的内容提取

### `app.py`
- Streamlit Web 应用主文件
- 提供文件上传和结果展示界面
- 支持工作流类型选择（检查/生成/知识库管理）
- 支持知识库路径配置和管理
- 支持知识库管理页面（概览、文件索引、编辑索引、定时任务配置）
- 支持 Word 和 PDF 报告下载

## 部署配置

### 环境变量
- `OPENAI_API_KEY`: API 密钥（必需）
- `OPENAI_API_BASE`: API 基础URL（必需）

### 配置文件
- `.streamlit/config.toml`: Streamlit 界面配置
- `.streamlit/secrets.toml`: API Key 配置（本地，不提交到 Git）
- `.streamlit/secrets.toml.example`: API Key 配置示例（提交到 Git）
- `.coze.env`: Coze 调试环境配置

### 依赖管理
- `requirements.txt`: Python 依赖列表
- 仅包含公开可用的包，无私有依赖

## 测试与验证

### 检查模式测试
```bash
# 需要准备两个文件
# tender_file: 招标文件
# bid_file: 投标文件
```

### 生成模式测试
```bash
# 只需要一个文件
# tender_file: 招标文件
# workflow_type: "generate"
```

### 知识库管理测试
```bash
# 准备测试文件
# 将 PDF、DOCX、PPTX、TXT 文件放入 datafiles 目录

# 测试索引创建
python test_knowledge_indexer.py

# 测试导入
python test_knowledge_import.py

# 通过 Web 界面测试
# 1. 启动应用：streamlit run app.py
# 2. 点击"知识库管理"按钮
# 3. 测试四个标签页的功能
```

### 知识库检索集成测试
```python
# 测试知识库检索是否正常工作
from src.tools.knowledge_indexer import KnowledgeIndexer

# 初始化索引工具
indexer = KnowledgeIndexer("datafiles")

# 执行搜索
results = indexer.search_indices("网络安全", direction="technical", top_k=5)

# 检查结果
for result in results:
    print(f"文件: {result.metadata.file_name}")
    print(f"摘要: {result.content_summary.full_summary}")
```

## 知识库管理架构

### 知识库索引架构

```
┌─────────────────────────────────────────────────────────────┐
│                      KnowledgeLibrary                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         indices: Dict[str, KnowledgeIndex]           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐│  │
│  │  │  Index 1     │  │  Index 2     │  │  Index N    ││  │
│  │  │  (file_hash) │  │  (file_hash) │  │  (file_hash)││  │
│  │  └──────────────┘  └──────────────┘  └─────────────┘│  │
│  └──────────────────────────────────────────────────────┘  │
│  total_files, total_size, last_updated, version            │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ 每个索引包含
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      KnowledgeIndex                          │
│  ┌──────────────┐  ┌──────────────────────────────────┐    │
│  │  metadata    │  │      content_summary            │    │
│  │  ┌────────┐  │  │  ┌──────────────────────────┐   │    │
│  │  │file_name│  │  │  │  full_summary           │   │    │
│  │  │file_size│  │  │  │  key_chapters           │   │    │
│  │  │file_type│  │  │  │  technical_keywords     │   │    │
│  │  │file_hash│  │  │  │  commercial_keywords    │   │    │
│  │  └────────┘  │  │  └──────────────────────────┘   │    │
│  └──────────────┘  └──────────────────────────────────┘    │
│  search_tags, direction, quality_score, is_active            │
└─────────────────────────────────────────────────────────────┘
```

### 知识库检索流程

```
┌─────────────────┐
│   用户查询词    │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│              多维度匹配算法                        │
│  ┌──────────┬──────────┬──────────┬──────────┐  │
│  │  标签匹配 │ 摘要匹配 │ 章节匹配 │ 关键词匹配│  │
│  │  (+1.0)  │  (+0.5)  │  (+0.3)  │  (+0.4)  │  │
│  └──────────┴──────────┴──────────┴──────────┘  │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
            ┌────────────────┐
            │  计算总分并排序 │
            └────────┬───────┘
                     │
                     ▼
            ┌────────────────┐
            │  返回 Top-K 结果│
            └────────────────┘
```

### 知识库管理 Web 界面架构

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit 应用主界面                      │
│  ┌──────────┬──────────┬──────────┬──────────────────────┐  │
│  │📊 投标   │✍️ 投标   │📚 知识库 │⚙️ 配置            │  │
│  │文件检查  │材料生成  │管理      │                  │  │
│  └──────────┴──────────┴──────────┴──────────────────────┘  │
│                         │                                   │
│                    点击"知识库管理"                         │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              知识库管理页面                           │  │
│  │  ┌────────┬────────┬────────┬────────┐              │  │
│  │  │📊 概览 │📄 文件 │✏️ 编辑  │⚙️ 定时 │              │  │
│  │  │        │索引    │索引    │任务    │              │  │
│  │  └────────┴────────┴────────┴────────┘              │  │
│  │                                                       │  │
│  │  概览: 统计信息、文件类型分布                          │  │
│  │  文件索引: 搜索、过滤、查看、编辑、删除              │  │
│  │  编辑索引: 修改摘要、标签、方向、评分                 │  │
│  │  定时任务: 启动/停止调度器、查看日志                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 知识库数据结构

### FileMetadata（文件元信息）
```python
{
    "file_path": "技术知识/01 流量威胁分析服务/2.技术方案/方案.docx",
    "file_name": "方案.docx",
    "file_size": 12345,
    "file_type": "docx",
    "file_hash": "sha256_hash_value",
    "created_at": "2024-01-01 12:00:00",
    "modified_at": "2024-01-01 12:00:00",
    "indexed_at": "2024-01-01 12:00:00",
    "updated_at": "2024-01-01 12:00:00"
}
```

### DocumentSummary（文档摘要）
```python
{
    "full_summary": "本文档介绍了流量威胁分析服务的...",
    "key_chapters": [
        {"title": "第一章", "summary": "服务概述..."},
        {"title": "第二章", "summary": "技术架构..."}
    ],
    "technical_keywords": ["流量分析", "威胁检测", "实时监控"],
    "commercial_keywords": ["服务报价", "交付周期", "技术支持"]
}
```

### KnowledgeIndex（知识索引）
```python
{
    "id": "sha256_hash_value",
    "metadata": FileMetadata,
    "content_summary": DocumentSummary,
    "search_tags": ["流量分析", "威胁检测", "网络安全"],
    "direction": "technical",  # technical | commercial | both
    "quality_score": 0.9,
    "is_active": true
}
```
