# 安天投标文件智能分析系统 - 开发文档

## 📋 目录

- [1. 文档概述](#1-文档概述)
- [2. 功能介绍](#2-功能介绍)
  - [2.1 投标文件检查功能](#21-投标文件检查功能)
  - [2.2 投标材料生成功能](#22-投标材料生成功能)
- [3. 技术架构](#3-技术架构)
  - [3.1 整体架构](#31-整体架构)
  - [3.2 技术栈](#32-技术栈)
  - [3.3 目录结构](#33-目录结构)
  - [3.4 核心组件](#34-核心组件)
- [4. 主要业务流程](#4-主要业务流程)
  - [4.1 投标文件检查流程](#41-投标文件检查流程)
  - [4.2 投标材料生成流程](#42-投标材料生成流程)
  - [4.3 工作流路由机制](#43-工作流路由机制)
- [5. 使用说明](#5-使用说明)
  - [5.1 安装部署](#51-安装部署)
  - [5.2 配置说明](#52-配置说明)
  - [5.3 开发指南](#53-开发指南)
  - [5.4 测试指南](#54-测试指南)
- [6. 附录](#6-附录)
  - [6.1 配置文件说明](#61-配置文件说明)
  - [6.2 API 接口说明](#62-api-接口说明)
  - [6.3 常见问题](#63-常见问题)

---

## 1. 文档概述

### 1.1 项目简介

安天投标文件智能分析系统是基于 LangGraph 工作流框架开发的智能招标文件分析工具，专为网络安全售前工程师设计。系统提供两大核心功能：

1. **投标文件智能检查** - 自动检查投标文件的完整性、合规性和竞争力
2. **投标材料自动生成** - 基于招标文件和历史案例自动生成投标材料

### 1.2 文档目的

本文档面向开发人员、运维人员和技术管理者，旨在：
- 详细介绍系统功能和技术架构
- 说明核心业务流程和实现原理
- 提供开发、测试、部署的完整指南
- 为二次开发和功能扩展提供参考

### 1.3 读者对象

- **开发人员**：了解系统架构、业务流程，进行功能开发和优化
- **运维人员**：掌握系统部署、配置和维护方法
- **技术管理者**：了解系统技术选型和整体设计思路

---

## 2. 功能介绍

### 2.1 投标文件检查功能

#### 2.1.1 功能概述

投标文件检查功能通过六维度并行检测，全面评估投标文件的质量和合规性，帮助售前工程师快速发现问题和改进机会。

#### 2.1.2 核心功能模块

| 模块 | 功能描述 | 输出内容 |
|------|---------|---------|
| **废标项检查** | 识别可能导致废标的致命问题 | 废标风险点、具体原因、严重程度 |
| **商务得分检查** | 评估商务部分得分情况 | 预计得分、失分点、改进建议 |
| **技术方案检查** | 评估技术方案的完整性和质量 | 方案完整性、创新性、可行性评分 |
| **指标应答检查** | 逐条检查技术指标响应情况 | 指标响应率、缺失指标、补充建议 |
| **技术得分点分析** | 分析技术得分覆盖情况 | 得分覆盖度、遗漏点、优化建议 |
| **文件结构检查** | 检查目录完整性和排布合理性 | 结构问题、缺失章节、改进方案 |

#### 2.1.3 检查流程

```
1. 用户上传招标文件和投标文件
   ↓
2. 文件解析（提取文本和结构）
   ↓
3. 六维度并行检查（AI 分析）
   ↓
4. 结果汇总与建议生成
   ↓
5. 输出检查报告（PDF/Word/TXT）
```

#### 2.1.4 输出报告

检查报告包含：
- **执行摘要** - 整体评估和关键发现
- **详细检查结果** - 六维度的检查详情
- **修改建议** - 按优先级排序的改进建议
- **得分预测** - 商务和技术部分的预计得分
- **风险提示** - 废标风险和关键问题

### 2.2 投标材料生成功能

#### 2.2.1 功能概述

投标材料生成功能基于招标文件要求，结合本地知识库和互联网搜索，自动生成高质量的商务和技术投标材料。

#### 2.2.2 核心功能模块

| 模块 | 功能描述 | 数据来源 |
|------|---------|---------|
| **招标要求解析** | 提取商务要求和技术要求 | 招标文件 |
| **知识库检索** | 从历史案例中匹配素材 | 本地知识库 |
| **互联网搜索** | 搜索最新的行业标准和实践 | 网络搜索 API |
| **商务材料生成** | 生成商务资质、项目经验等 | 知识库 + 网络搜索 + LLM |
| **技术材料生成** | 生成技术方案、系统架构等 | 知识库 + 网络搜索 + LLM |
| **素材出处标注** | 标注每个内容的来源 | 自动标注 |

#### 2.2.3 生成流程

```
1. 用户上传招标文件
   ↓
2. 解析招标文件（提取要求和结构）
   ↓
3. 招标要求智能解析（分类商务/技术要求）
   ↓
4. 并行检索素材
   ├─ 商务知识库检索
   ├─ 商务互联网搜索
   ├─ 技术知识库检索
   └─ 技术互联网搜索
   ↓
5. 并行生成材料
   ├─ 生成商务材料（标注出处）
   └─ 生成技术材料（标注出处）
   ↓
6. 输出材料（Word/TXT）
```

#### 2.2.4 生成材料内容

**商务材料包含**：
- 公司资质介绍
- 类似项目经验
- 服务承诺和质量保证
- 商务条款响应
- 资源投入承诺

**技术材料包含**：
- 整体技术方案
- 系统架构设计
- 实施方案和计划
- 关键技术说明
- 创新点和优势

---

## 3. 技术架构

### 3.1 整体架构

系统采用分层架构设计，从上到下分为：

```
┌─────────────────────────────────────────────────────┐
│                   用户界面层                          │
│           Streamlit Web Application                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   业务逻辑层                          │
│               LangGraph Workflow Engine             │
│  ┌──────────────┐      ┌──────────────┐           │
│  │  Check Flow  │      │ Generate Flow│           │
│  └──────────────┘      └──────────────┘           │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   服务层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   LLM    │  │ Knowledge│  │  Search  │         │
│  │ Service  │  │  Base    │  │  Service │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   工具层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ File     │  │  Report  │  │   Docs   │         │
│  │ Handler  │  │ Generator│  │ Handler  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### 3.2 技术栈

| 类别 | 技术选型 | 版本 | 用途 |
|------|---------|------|------|
| **工作流框架** | LangGraph | 1.0.2 | 工作流编排 |
| **LLM 框架** | LangChain | 1.0 | LLM 接口封装 |
| **Web 框架** | Streamlit | 1.x | Web 应用界面 |
| **大语言模型** | 豆包 DeepSeek | deepseek-v3-2-251201 | AI 分析和生成 |
| **文档处理** | pypdf | 3.x | PDF 解析 |
| **文档处理** | python-docx | 1.x | Word 读写 |
| **文档处理** | python-pptx | 1.x | PowerPoint 解析 |
| **文档处理** | docx2python | 1.x | Word 内容提取 |
| **报告生成** | reportlab | 4.x | PDF 报告生成 |
| **向量检索** | sentence-transformers | 2.x | 知识库向量化 |
| **HTTP 客户端** | httpx | 0.x | API 调用 |
| **模板引擎** | jinja2 | 3.x | 提示词模板 |
| **数据处理** | pandas | 2.x | 数据处理 |
| **数据处理** | numpy | 2.x | 数值计算 |

### 3.3 目录结构

```
antiy-bidding-support-system/
├── app.py                              # Streamlit Web 应用入口
├── requirements.txt                     # Python 依赖（完整版）
├── requirementsL.txt                    # Python 依赖（精简版）
├── .env.example                         # 环境变量模板
├── .streamlit/                          # Streamlit 配置目录
│   ├── config.toml                      # Streamlit 应用配置
│   └── secrets.toml.example             # Secrets 模板
│
├── src/                                 # 源代码目录
│   ├── graphs/                          # LangGraph 工作流
│   │   ├── state.py                     # 全局状态定义
│   │   ├── state_materials.py           # 材料生成节点状态
│   │   ├── node.py                      # 检查功能节点实现
│   │   ├── nodes/                       # 节点目录
│   │   │   └── material_generate_nodes.py  # 材料生成节点
│   │   └── graph.py                     # 主图编排和路由
│   │
│   ├── tools/                           # 工具函数
│   │   ├── knowledge_base_tool.py       # 知识库工具
│   │   └── ...                          # 其他工具
│   │
│   ├── utils/                           # 通用工具
│   │   ├── file/
│   │   │   └── file.py                  # 文件处理工具
│   │   └── ...                          # 其他工具
│   │
│   └── main.py                          # 主程序入口
│
├── config/                              # LLM 配置文件
│   ├── invalid_items_check_cfg.json     # 废标项检查配置
│   ├── commercial_score_check_cfg.json  # 商务得分检查配置
│   ├── technical_plan_check_cfg.json    # 技术方案检查配置
│   ├── indicator_response_check_cfg.json # 指标应答检查配置
│   ├── technical_score_check_cfg.json   # 技术得分检查配置
│   ├── bid_structure_check_cfg.json     # 文件结构检查配置
│   ├── modification_summary_cfg.json    # 修改建议汇总配置
│   ├── tender_requirements_parse_cfg.json # 招标要求解析配置
│   ├── commercial_material_generate_cfg.json # 商务材料生成配置
│   └── technical_material_generate_cfg.json  # 技术材料生成配置
│
├── assets/                              # 资源目录
│   ├── knowledge_base/                  # 本地知识库
│   │   ├── 商务案例/
│   │   ├── 技术方案/
│   │   └── ...
│   ├── tender_document.docx             # 示例招标文件
│   ├── bid_document.docx                # 示例投标文件
│   └── ...                              # 其他资源
│
├── docs/                                # 文档目录
│   └── DEVELOPMENT.md                   # 本开发文档
│
└── tests/                               # 测试目录
    ├── test_graphs.py                   # 工作流测试
    ├── test_nodes.py                    # 节点测试
    └── ...
```

### 3.4 核心组件

#### 3.4.1 LangGraph 工作流引擎

**职责**：
- 工作流编排和执行
- 状态管理和节点间数据传递
- 并行节点调度
- 条件路由和循环控制

**核心概念**：
- **GlobalState** - 全局状态，存储工作流过程中的所有数据
- **Node** - 节点，工作流的基本执行单元
- **Edge** - 边，定义节点间的执行顺序
- **Conditional Edge** - 条件边，根据状态动态路由
- **Input/Output Schema** - 工作流的输入输出定义

**实现文件**：
- `src/graphs/graph.py` - 主图定义
- `src/graphs/state.py` - 全局状态定义
- `src/graphs/node.py` - 节点实现

#### 3.4.2 大语言模型服务

**职责**：
- 统一的 LLM 调用接口
- 提示词管理（SP/UP）
- 模型配置管理
- 响应结果解析

**当前模型**：
- **Provider**: 火山引擎方舟
- **Model**: deepseek-v3-2-251201
- **API Base**: https://ark.cn-beijing.volces.com/api/v3

**配置方式**：
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

**实现文件**：
- `src/graphs/node.py` - `call_llm()` 函数

#### 3.4.3 知识库服务

**职责**：
- 文档索引和向量化
- 语义检索
- 结果排序和过滤

**技术实现**：
- 使用 sentence-transformers 进行文档向量化
- 余弦相似度匹配
- 支持增量索引

**支持格式**：
- PDF
- Word (.docx)
- 文本 (.txt)
- PowerPoint (.pptx)

**实现文件**：
- `src/tools/knowledge_base_tool.py`

#### 3.4.4 文件处理服务

**职责**：
- 文件内容提取
- 文件结构解析
- 多格式支持

**核心功能**：
- `extract_text()` - 提取文本内容
- `extract_text_with_structure()` - 提取文本和结构
- 支持章节、页码等元信息提取

**实现文件**：
- `src/utils/file/file.py`

#### 3.4.5 报告生成服务

**职责**：
- 检查报告生成
- 材料文档生成
- 多格式输出

**支持格式**：
- PDF
- Word (.docx)
- 文本 (.txt)

**实现文件**：
- `app.py` - 报告生成函数

---

## 4. 主要业务流程

### 4.1 投标文件检查流程

#### 4.1.1 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                        开始检查                               │
│              (上传招标文件 + 投标文件)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      tender_doc_parse                         │
│                    招标文件解析节点                            │
│  输入: tender_file (File)                                     │
│  输出: tender_doc_content (str), tender_doc_structure (str)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      bid_doc_parse                            │
│                    投标文件解析节点                            │
│  输入: bid_file (File)                                        │
│  输出: bid_doc_content (str), bid_doc_structure (str)        │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│   workflow_type │         │ route_by_       │
│   = "check" ?   │         │ workflow_type   │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │ 是                        │
         ▼                           │
┌─────────────────────────────────────────────────────────────┐
│                     六维并行检测                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ invalid_     │  │ commercial_  │  │ technical_   │      │
│  │ items_check  │  │ score_check  │  │ plan_check   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ indicator_   │  │ technical_   │  │ bid_         │      │
│  │ response_    │  │ score_check  │  │ structure_   │      │
│  │ check        │  │              │  │ check        │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  modification_summary                         │
│                    修改建议汇总节点                           │
│  输入: 六维度的检查结果                                        │
│  输出: final_modification_suggestions (str)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      输出检查报告                              │
│                  (PDF / Word / TXT)                           │
└─────────────────────────────────────────────────────────────┘
```

#### 4.1.2 节点说明

| 节点名称 | 类型 | 输入 | 输出 | 描述 |
|---------|------|------|------|------|
| tender_doc_parse | task | tender_file | tender_doc_content, tender_doc_structure | 解析招标文件 |
| bid_doc_parse | task | bid_file | bid_doc_content, bid_doc_structure | 解析投标文件 |
| invalid_items_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | invalid_items_check | 废标项检查 |
| commercial_score_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | commercial_score_check | 商务得分检查 |
| technical_plan_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | technical_plan_check | 技术方案检查 |
| indicator_response_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | indicator_response_check | 指标应答检查 |
| technical_score_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | technical_score_check | 技术得分检查 |
| bid_structure_check | agent | tender_doc_content, bid_doc_content, bid_doc_structure | bid_structure_check | 文件结构检查 |
| modification_summary | agent | 六维度检查结果 | final_modification_suggestions | 汇总修改建议 |

#### 4.1.3 数据流转

1. **输入阶段**：用户上传招标文件和投标文件
2. **解析阶段**：提取两个文件的文本内容和结构信息
3. **检查阶段**：六个检查节点并行执行，每个节点独立分析
4. **汇总阶段**：收集所有检查结果，生成统一的修改建议
5. **输出阶段**：生成检查报告，用户可下载

### 4.2 投标材料生成流程

#### 4.2.1 流程图

```
┌─────────────────────────────────────────────────────────────┐
│                      开始生成材料                             │
│                  (上传招标文件 + 配置)                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      tender_doc_parse                         │
│                    招标文件解析节点                            │
│  输入: tender_file (File)                                     │
│  输出: tender_doc_content (str), tender_doc_structure (str)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              route_by_workflow_type                           │
│              (workflow_type = "generate")                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              tender_requirements_parse                        │
│                招标要求解析节点                                │
│  输入: tender_doc_content, tender_doc_structure              │
│  输出: commercial_requirements, technical_requirements        │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  商务材料生成     │         │  技术材料生成     │
│      分支        │         │      分支        │
└────────┬────────┘         └────────┬────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│ commercial_kb_  │         │ technical_kb_    │
│    search       │         │    search        │
│ (知识库检索)     │         │ (知识库检索)      │
└────────┬────────┘         └────────┬────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│ commercial_web_ │         │ technical_web_   │
│    search       │         │    search        │
│ (互联网搜索)     │         │ (互联网搜索)      │
└────────┬────────┘         └────────┬────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│ commercial_     │         │ technical_      │
│ material_       │         │ material_       │
│   generate      │         │   generate      │
│ (生成商务材料)   │         │ (生成技术材料)    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └─────────────┬─────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      输出生成材料                              │
│                  (Word / TXT)                                 │
└─────────────────────────────────────────────────────────────┘
```

#### 4.2.2 节点说明

| 节点名称 | 类型 | 输入 | 输出 | 描述 |
|---------|------|------|------|------|
| tender_requirements_parse | agent | tender_doc_content, tender_doc_structure | commercial_requirements, technical_requirements, templates | 解析招标要求 |
| commercial_kb_search | task | commercial_requirements, knowledge_base_path | commercial_kb_results | 商务知识库检索 |
| commercial_web_search | task | commercial_requirements | commercial_web_results | 商务互联网搜索 |
| commercial_material_generate | agent | commercial_requirements, kb_results, web_results, template | commercial_material | 生成商务材料 |
| technical_kb_search | task | technical_requirements, knowledge_base_path | technical_kb_results | 技术知识库检索 |
| technical_web_search | task | technical_requirements | technical_web_results | 技术互联网搜索 |
| technical_material_generate | agent | technical_requirements, kb_results, web_results, template | technical_material | 生成技术材料 |

#### 4.2.3 数据流转

1. **输入阶段**：用户上传招标文件，配置生成选项
2. **解析阶段**：提取招标文件内容和结构
3. **解析要求**：LLM 分析招标文件，提取商务和技术要求
4. **检索素材**：并行检索知识库和互联网，获取相关素材
5. **生成材料**：基于要求和素材，LLM 生成商务和技术材料
6. **输出阶段**：生成材料文档，用户可下载

### 4.3 工作流路由机制

#### 4.3.1 路由逻辑

系统通过 `route_by_workflow_type` 条件节点根据 `workflow_type` 参数路由：

```python
def route_by_workflow_type(state: GlobalState) -> str:
    """
    根据工作流类型路由到不同的流程
    
    - workflow_type = "check"  → 进入投标文件检查流程
    - workflow_type = "generate" → 进入投标材料生成流程
    """
    if state.workflow_type == "generate":
        return "tender_requirements_parse"
    else:
        return "check_workflow"
```

#### 4.3.2 路由配置

```python
builder.add_conditional_edges(
    source="tender_doc_parse",
    path=route_by_workflow_type,
    path_map={
        "check_workflow": "bid_doc_parse",
        "tender_requirements_parse": "tender_requirements_parse"
    }
)
```

#### 4.3.3 路由示意

```
┌─────────────────┐
│ tender_doc_     │
│     parse       │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Route   │
    │  Node   │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────┐  ┌─────────────────┐
│check│  │   generate      │
│flow │  │      flow       │
└─────┘  └─────────────────┘
```

---

## 5. 使用说明

### 5.1 安装部署

#### 5.1.1 环境要求

- **Python**: 3.8 或更高版本
- **内存**: 建议 4GB 以上
- **磁盘**: 建议 10GB 以上可用空间
- **网络**: 需要访问 LLM API 和互联网搜索服务

#### 5.1.2 安装步骤

**1. 克隆代码仓库**

```bash
git clone https://github.com/P7-code/p7.git
cd p7
```

**2. 创建虚拟环境（推荐）**

```bash
# Python 3.8+
python -m venv venv

# 激活虚拟环境
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

**3. 安装依赖**

```bash
# 使用完整依赖（开发环境）
pip install -r requirements.txt

# 或使用精简依赖（生产环境）
pip install -r requirementsL.txt
```

**4. 配置环境变量**

复制环境变量模板并编辑：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 火山引擎方舟配置（推荐）
ARK_API_KEY=your-api-key-here
ARK_API_BASE=https://ark.cn-beijing.volces.com/api/v3

# 或使用其他 LLM 服务
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://api.deepseek.com
```

**5. 验证安装**

```bash
python -c "from graphs.graph import main_graph; print('安装成功！')"
```

#### 5.1.3 本地运行

```bash
streamlit run app.py
```

访问 http://localhost:8501

#### 5.1.4 部署到 Streamlit Cloud

**步骤**：

1. 推送代码到 GitHub
2. 访问 https://share.streamlit.io
3. 创建新应用，连接 GitHub 仓库
4. 配置环境变量（ARK_API_KEY、ARK_API_BASE）
5. 部署

详细步骤参见 [DEPLOYMENT.md](./DEPLOYMENT.md)

### 5.2 配置说明

#### 5.2.1 环境变量配置

| 变量名 | 说明 | 必填 | 示例值 |
|--------|------|------|--------|
| `ARK_API_KEY` | 火山引擎方舟 API Key | ✅ | `9cebea4f-aa41-47ea-942e-4bf1324d1162` |
| `ARK_API_BASE` | 火山引擎方舟 API Base | ✅ | `https://ark.cn-beijing.volces.com/api/v3` |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key | ❌ | `sk-xxxxxxxxxxxxxxxx` |
| `OPENAI_API_BASE` | OpenAI 兼容 API Base | ❌ | `https://api.deepseek.com` |
| `COZE_WORKSPACE_PATH` | 工作空间路径 | ❌ | 自动设置 |

#### 5.2.2 LLM 配置文件

所有 LLM 配置文件位于 `config/` 目录，格式如下：

```json
{
  "config": {
    "model": "deepseek-v3-2-251201",
    "temperature": 0.0,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "sp": "系统提示词...",
  "up": "用户提示词（支持 Jinja2 模板）..."
}
```

**配置文件说明**：

- `invalid_items_check_cfg.json` - 废标项检查
- `commercial_score_check_cfg.json` - 商务得分检查
- `technical_plan_check_cfg.json` - 技术方案检查
- `indicator_response_check_cfg.json` - 指标应答检查
- `technical_score_check_cfg.json` - 技术得分检查
- `bid_structure_check_cfg.json` - 文件结构检查
- `modification_summary_cfg.json` - 修改建议汇总
- `tender_requirements_parse_cfg.json` - 招标要求解析
- `commercial_material_generate_cfg.json` - 商务材料生成
- `technical_material_generate_cfg.json` - 技术材料生成

#### 5.2.3 知识库配置

**知识库目录**：`assets/knowledge_base/`

**支持的文件格式**：
- PDF
- Word (.docx)
- 文本 (.txt)
- PowerPoint (.pptx)

**目录结构建议**：
```
knowledge_base/
├── 商务案例/
│   ├── 公司资质.docx
│   ├── 项目经验.pdf
│   └── 服务承诺.txt
├── 技术方案/
│   ├── 网络安全方案.docx
│   ├── 系统架构设计.pdf
│   └── 实施计划.txt
└── 行业标准/
    ├── 等保2.0标准.pdf
    └── 行业规范.docx
```

#### 5.2.4 Streamlit 配置

配置文件：`.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true
maxUploadSize = 200

[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 5.3 开发指南

#### 5.3.1 代码结构

**工作流开发**：
- `src/graphs/graph.py` - 主图定义
- `src/graphs/state.py` - 全局状态定义
- `src/graphs/node.py` - 节点实现
- `src/graphs/nodes/` - 节点目录

**工具开发**：
- `src/tools/` - 工具函数
- `src/utils/` - 通用工具

**Web 开发**：
- `app.py` - Web 应用入口

#### 5.3.2 添加新节点

**步骤**：

1. **定义节点输入输出**（`src/graphs/state.py`）

```python
class NewNodeInput(BaseModel):
    """新节点输入"""
    field1: str = Field(..., description="字段1")
    field2: Optional[str] = Field(default="", description="字段2")

class NewNodeOutput(BaseModel):
    """新节点输出"""
    result: str = Field(..., description="结果")
```

2. **实现节点函数**（`src/graphs/nodes/new_node.py`）

```python
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import NewNodeInput, NewNodeOutput

def new_node(
    state: NewNodeInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewNodeOutput:
    """
    title: 新节点
    desc: 节点描述
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    # 节点逻辑
    result = "处理结果"
    
    return NewNodeOutput(result=result)
```

3. **注册节点到主图**（`src/graphs/graph.py`）

```python
from graphs.nodes.new_node import new_node

builder.add_node("new_node", new_node)
```

4. **添加边**

```python
builder.add_edge("previous_node", "new_node")
builder.add_edge("new_node", "next_node")
```

#### 5.3.3 添加新配置

**步骤**：

1. 创建配置文件（`config/new_node_cfg.json`）

```json
{
  "config": {
    "model": "deepseek-v3-2-251201",
    "temperature": 0.0,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "sp": "系统提示词...",
  "up": "用户提示词..."
}
```

2. 在节点中使用配置

```python
builder.add_node(
    "new_node",
    new_node,
    metadata={"type": "agent", "llm_cfg": "config/new_node_cfg.json"}
)
```

#### 5.3.4 调试技巧

**启用详细日志**：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**查看 LangGraph 执行图**：

```python
from IPython.display import Image, display

display(Image(main_graph.get_graph().draw_mermaid_png()))
```

**单节点测试**：

```python
from graphs.nodes.new_node import new_node
from langchain_core.runnables import RunnableConfig

input_data = NewNodeInput(field1="test", field2="test")
config = RunnableConfig(configurable={"llm_cfg": "config/new_node_cfg.json"})
runtime = main_graph.compile()
result = new_node(input_data, config, runtime)
print(result)
```

### 5.4 测试指南

#### 5.4.1 单元测试

**测试节点**：

```python
# tests/test_nodes.py
import pytest
from graphs.nodes.new_node import new_node
from graphs.state import NewNodeInput

def test_new_node():
    input_data = NewNodeInput(field1="test", field2="test")
    result = new_node(input_data, None, None)
    assert result.result is not None
```

**运行测试**：

```bash
pytest tests/test_nodes.py -v
```

#### 5.4.2 集成测试

**测试工作流**：

```python
# tests/test_graphs.py
import pytest
from graphs.graph import main_graph
from utils.file.file import File

def test_check_workflow():
    input_data = {
        "tender_file": File(url="assets/tender_document.docx"),
        "bid_file": File(url="assets/bid_document.docx"),
        "workflow_type": "check"
    }
    result = main_graph.invoke(input_data)
    assert result.final_modification_suggestions is not None

def test_generate_workflow():
    input_data = {
        "tender_file": File(url="assets/tender_document.docx"),
        "workflow_type": "generate",
        "material_type": "commercial"
    }
    result = main_graph.invoke(input_data)
    assert result.commercial_material is not None
```

**运行测试**：

```bash
pytest tests/test_graphs.py -v
```

#### 5.4.3 端到端测试

**使用 Streamlit 测试**：

1. 启动应用：`streamlit run app.py`
2. 访问 http://localhost:8501
3. 上传测试文件
4. 执行检查或生成
5. 验证输出结果

**自动化测试**：

```bash
# 安装 Playwright
pip install playwright
playwright install

# 运行 E2E 测试
pytest tests/e2e/
```

---

## 6. 附录

### 6.1 配置文件说明

#### 6.1.1 LLM 配置文件结构

```json
{
  "config": {
    "model": "deepseek-v3-2-251201",
    "temperature": 0.0,
    "top_p": 0.7,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "sp": "系统提示词...",
  "up": "用户提示词..."
}
```

**字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `model` | 模型 ID | `deepseek-v3-2-251201` |
| `temperature` | 温度参数（0-1） | `0.0`（确定性） |
| `top_p` | 核采样参数（0-1） | `0.7` |
| `max_completion_tokens` | 最大输出 token 数 | `4000` |
| `thinking` | 思维模式 | `disabled` |
| `sp` | 系统提示词 | `"你是一个投标文件分析专家..."` |
| `up` | 用户提示词 | `"请分析以下招标文件..."` |

#### 6.1.2 系统提示词（SP）生成规则

根据 [Agent SP 生成规则](#) 生成系统提示词：

```markdown
# 角色定义
[清晰定义 Agent 的身份、专业领域、能力与语气]

# 任务目标
[简明描述需解决的核心问题]

# 工作流上下文
- **Input**: [上游输入的数据类型/字段]
- **Process**: [关键处理步骤]
- **Output**: [严格定义下游所需结构与字段]

# 约束与规则
- [安全、保密、长度、禁止事项等]
- [错误处理：当输入缺失/越界时的返回结构]

# 过程
工作SOP过程

# 输出格式
仅返回如下格式的 JSON 对象：
{
  "field1": "...",
  "field2": "..."
}
```

### 6.2 API 接口说明

#### 6.2.1 工作流调用接口

**调用方式**：

```python
from graphs.graph import main_graph

input_data = {
    "tender_file": {"url": "path/to/tender.pdf", "file_type": "document"},
    "bid_file": {"url": "path/to/bid.pdf", "file_type": "document"},
    "workflow_type": "check"
}

result = main_graph.invoke(input_data)
```

**输入参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tender_file` | File | ✅ | 招标文件 |
| `bid_file` | File | ❌ | 投标文件（检查模式需要） |
| `workflow_type` | str | ✅ | 工作流类型：`check` 或 `generate` |
| `knowledge_base_path` | str | ❌ | 知识库路径（生成模式） |
| `material_type` | str | ❌ | 材料类型：`commercial`、`technical`、`both` |

**输出参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `final_modification_suggestions` | str | 修改建议汇总（检查模式） |
| `invalid_items_check` | str | 废标项检查结果 |
| `commercial_score_check` | str | 商务得分检查结果 |
| `technical_plan_check` | str | 技术方案检查结果 |
| `indicator_response_check` | str | 指标应答检查结果 |
| `technical_score_check` | str | 技术得分检查结果 |
| `bid_structure_check` | str | 文件结构检查结果 |
| `commercial_material` | str | 商务材料（生成模式） |
| `technical_material` | str | 技术材料（生成模式） |

#### 6.2.2 知识库工具接口

**初始化**：

```python
from src.tools.knowledge_base_tool import KnowledgeBaseTool

kb_tool = KnowledgeBaseTool("assets/knowledge_base/")
kb_tool.scan_directory()
```

**搜索**：

```python
results = kb_tool.search(query="网络安全方案", top_k=5)

for result in results:
    print(f"内容: {result['content']}")
    print(f"来源: {result['source']}")
    print(f"页码: {result['page']}")
```

#### 6.2.3 文件处理接口

**提取文本**：

```python
from utils.file.file import FileOps
from utils.file.file import File

file = File(url="path/to/document.pdf")
content = FileOps.extract_text(file)
```

**提取文本和结构**：

```python
content, structure = FileOps.extract_text_with_structure(file)
```

### 6.3 常见问题

#### 6.3.1 部署相关问题

**Q: Streamlit Cloud 部署失败？**

A: 检查以下几点：
1. 确认 `requirements.txt` 或 `requirementsL.txt` 存在
2. 确认环境变量已正确配置（ARK_API_KEY、ARK_API_BASE）
3. 查看部署日志，定位具体错误

**Q: 本地运行报错 "ModuleNotFoundError"？**

A: 确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

#### 6.3.2 功能相关问题

**Q: 检查结果不准确？**

A: 可以通过以下方式优化：
1. 调整 LLM 配置文件的 `temperature` 参数
2. 优化系统提示词（SP）和用户提示词（UP）
3. 提供更详细的招标文件和投标文件

**Q: 生成的材料质量不高？**

A: 可以通过以下方式优化：
1. 完善知识库，提供高质量的历史案例
2. 提供详细的生成要求
3. 调整材料生成配置文件中的提示词

#### 6.3.3 性能相关问题

**Q: 分析速度慢？**

A: 可以通过以下方式优化：
1. 减少 `max_completion_tokens` 参数
2. 使用更快的模型
3. 优化提示词，减少不必要的请求

**Q: 内存占用过高？**

A: 可以通过以下方式优化：
1. 减少知识库大小
2. 使用精简依赖（`requirementsL.txt`）
3. 分批处理大文件

#### 6.3.4 开发相关问题

**Q: 如何添加新的检查维度？**

A: 按照[添加新节点](#533-添加新节点)的步骤操作：
1. 定义节点输入输出
2. 实现节点函数
3. 注册节点到主图
4. 添加边连接节点

**Q: 如何修改 LLM 模型？**

A: 修改配置文件中的 `model` 字段：

```json
{
  "config": {
    "model": "your-new-model-id",
    ...
  }
}
```

---

## 文档版本

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| 1.0 | 2025-01-30 | 开发团队 | 初始版本 |

## 联系方式

- GitHub: https://github.com/P7-code/p7
- Issues: https://github.com/P7-code/p7/issues
- Email: [your-email@example.com]

---

**最后更新**: 2025-01-30
