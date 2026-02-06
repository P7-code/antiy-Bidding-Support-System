# 文档索引

## Markdown 文档

### 用户文档
- **README.md** - 项目介绍和快速开始指南
- **QUICK_START.md** - 快速开始教程
- **DEPLOYMENT.md** - 部署指南

### 开发文档
- **DEVELOPMENT.md** - 完整的开发文档（功能介绍、技术架构、业务流程、使用说明）
- **WORKFLOW_ARCHITECTURE.md** - 工作流完整架构图（三大流程分支详解、汇聚节点、人工节点）
- **WORKFLOW_QUICK_GUIDE.md** - 工作流快速指南（简化版流程图、核心节点说明）
- **workflow_diagram.mmd** - Mermaid 流程图（可视化工作流结构）
- **IMAGE_ANALYSIS_REPORT.md** - 流程图分析报告（基于用户提供的流程图图片）

### 配置文档
- **AGENTS.md** - 工作流节点清单和架构说明（包含用户流程图结构说明）
- **COZE_ENV_CONFIG.md** - Coze 环境配置说明
- **COZE_DEBUG_GUIDE.md** - Coze 调试指南

### 工具文档
- **REQUIREMENTS_FILES.md** - 依赖文件说明
- **VOLCENGINE_ARK_GUIDE.md** - 火山引擎方舟使用指南

### 辅助文档
- **LOCAL_SETUP_GUIDE.md** - 本地环境搭建指南
- **PUBLISH_CHECKLIST.md** - 发布检查清单
- **PUSH_TO_GITHUB.md** - GitHub 推送指南
- **QUICK_GENERATE_GUIDE.md** - 快速生成指南

## Word 文档

所有 Word 文档位于 `assets/` 目录下：

| 文档名称 | 文件名 | 大小 | 描述 |
|---------|--------|------|------|
| 用户手册 | 安天投标文件智能分析系统-用户手册.docx | 42KB | 完整的用户使用手册 |
| 开发文档 | 安天投标文件智能分析系统-开发文档.docx | 50KB | 完整的开发文档 |
| 部署指南 | 安天投标文件智能分析系统-部署指南.docx | 41KB | 部署配置指南 |
| 快速开始 | 安天投标文件智能分析系统-快速开始.docx | 38KB | 快速开始教程 |

## 转换工具

### 单文件转换
```bash
python scripts/md_to_docx.py <输入.md> <输出.docx>
```

示例：
```bash
python scripts/md_to_docx.py README.md 用户手册.docx
```

### 批量转换
```bash
cd scripts && python batch_convert_md.py
```

## 文档维护

### 更新流程
1. 更新 Markdown 源文件
2. 重新生成 Word 文档
3. 提交到 Git 仓库

### 版本控制
- Markdown 文档：直接提交到 Git
- Word 文档：建议使用 Git LFS 管理大文件

## 联系方式

如有文档相关问题，请：
- 提交 GitHub Issue
- 联系开发团队

---

**最后更新**: 2025-02-02
