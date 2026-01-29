## 项目概述
- **名称**: 智能招标文件分析系统
- **功能**: 基于LangGraph的智能招标文件分析系统，专为网络安全售前工程师设计。支持投标文件检查和投标材料生成两大核心功能。

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
| commercial_kb_search | `nodes/material_generate_nodes.py` | task | 商务知识库检索 | - | - |
| commercial_web_search | `nodes/material_generate_nodes.py` | task | 商务互联网搜索 | - | - |
| commercial_material_generate | `nodes/material_generate_nodes.py` | agent | 生成商务投标材料 | - | `config/commercial_material_generate_cfg.json` |
| technical_kb_search | `nodes/material_generate_nodes.py` | task | 技术知识库检索 | - | - |
| technical_web_search | `nodes/material_generate_nodes.py` | task | 技术互联网搜索 | - | - |
| technical_material_generate | `nodes/material_generate_nodes.py` | agent | 生成技术投标材料 | - | `config/technical_material_generate_cfg.json` |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 集成使用
- 节点`tender_doc_parse`使用集成 pypdf/docx2python
- 节点`bid_doc_parse`使用集成 pypdf/docx2python
- 节点`commercial_kb_search`使用集成 知识库
- 节点`technical_kb_search`使用集成 知识库
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
   - `commercial_kb_search` (知识库检索)
   - `commercial_web_search` (互联网搜索)
   - `commercial_material_generate` (生成商务材料)

2. **技术材料生成**:
   - `technical_kb_search` (知识库检索)
   - `technical_web_search` (互联网搜索)
   - `technical_material_generate` (生成技术材料)

**结束**: 商务和技术材料都生成完成后，工作流结束

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

## 关键文件说明

### `src/graphs/state.py`
- 定义全局状态 `GlobalState`（包含检查和生成两种流程的所有字段）
- 定义工作流输入 `GraphInput` 和输出 `GraphOutput`
- 定义每个节点的独立输入输出类

### `src/graphs/node.py`
- 实现所有检查模式节点函数
- 包含文件解析、LLM 调用等核心逻辑

### `src/graphs/state_materials.py`
- 定义材料生成相关的状态类（已废弃，相关字段已合并到 GlobalState）

### `src/graphs/nodes/material_generate_nodes.py`
- 实现材料生成相关节点函数
- 包括招标要求解析、知识库检索、网络搜索、材料生成等节点

### `src/graphs/material_generate_graph.py`
- 投标材料生成子图（已废弃，相关节点已移至主图）

### `src/graphs/graph.py`
- 定义主图结构
- 包含检查模式和生成模式的所有节点
- 通过条件路由选择执行路径
- 所有节点都在主图中，无子图结构

### `src/tools/knowledge_base_tool.py`
- 本地知识库管理工具类
- 支持文档索引和语义检索

### `src/utils/file/file.py`
- 文件处理工具类
- 支持 PDF、Word、PPT 等格式
- 提供文本提取功能

### `app.py`
- Streamlit Web 应用主文件
- 提供文件上传和结果展示界面
- 支持工作流类型选择（检查/生成）
- 支持知识库路径配置和管理
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
