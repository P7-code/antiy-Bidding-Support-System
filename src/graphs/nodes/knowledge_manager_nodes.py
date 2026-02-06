"""
知识库管理节点
用于管理知识库文件索引，包括扫描、摘要提取、索引更新等
"""
import os
import json
import re
from typing import Dict, Any
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass

from graphs.state_knowledge import (
    ScanFilesInput,
    ScanFilesOutput,
    ExtractSummaryInput,
    ExtractSummaryOutput,
    UpdateIndexInput,
    UpdateIndexOutput
)
from graphs.node import call_llm
from tools.knowledge_indexer import KnowledgeIndexer


def get_config_file_path(config_name: str) -> str:
    """获取配置文件路径"""
    return os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), config_name)


def scan_files_node(
    state: ScanFilesInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ScanFilesOutput:
    """
    title: 扫描知识库文件
    desc: 扫描 datafiles 目录，检测文件变化（新增、修改、删除）
    integrations:
    """
    ctx = runtime.context

    # 创建索引器
    indexer = KnowledgeIndexer(knowledge_dir=state.knowledge_dir)

    # 扫描文件
    all_files, new_files, modified_files, deleted_files = indexer.scan_files()

    return ScanFilesOutput(
        files=all_files,
        new_files=new_files,
        modified_files=modified_files,
        deleted_files=deleted_files
    )


def extract_summary_node(
    state: ExtractSummaryInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> ExtractSummaryOutput:
    """
    title: 提取文档摘要
    desc: 使用 LLM 提取文档的全文摘要、章节摘要、关键词等
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 使用 jinja2 模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "file_content": state.file_content[:10000],  # 限制内容长度
        "file_name": state.file_metadata.file_name,
        "file_structure": state.file_structure
    })

    # 调用 LLM 生成摘要
    result = call_llm(sp, user_prompt_content, llm_config)

    # 解析 LLM 返回结果（期望返回 JSON 格式）
    # 尝试提取 JSON
    json_match = re.search(r'\{[\s\S]*\}', result)
    if json_match:
        try:
            summary_data = json.loads(json_match.group())
        except json.JSONDecodeError:
            # 如果解析失败，使用默认值
            summary_data = {
                "full_summary": result[:500],
                "key_chapters": [],
                "technical_keywords": [],
                "commercial_keywords": [],
                "industry_tags": []
            }
    else:
        summary_data = {
            "full_summary": result[:500],
            "key_chapters": [],
            "technical_keywords": [],
            "commercial_keywords": [],
            "industry_tags": []
        }

    # 解析章节摘要
    chapters = []
    for chapter_data in summary_data.get("key_chapters", []):
        chapters.append({
            "chapter_title": chapter_data.get("title", ""),
            "page_range": chapter_data.get("page_range", ""),
            "summary": chapter_data.get("summary", ""),
            "key_points": chapter_data.get("key_points", [])
        })

    # 构建 DocumentSummary
    from graphs.state_knowledge import DocumentSummary, ChapterSummary

    document_summary = DocumentSummary(
        full_summary=summary_data.get("full_summary", ""),
        key_chapters=[
            ChapterSummary(
                chapter_title=ch.get("chapter_title", ""),
                page_range=ch.get("page_range", ""),
                summary=ch.get("summary", ""),
                key_points=ch.get("key_points", [])
            )
            for ch in chapters
        ],
        technical_keywords=summary_data.get("technical_keywords", []),
        commercial_keywords=summary_data.get("commercial_keywords", []),
        industry_tags=summary_data.get("industry_tags", [])
    )

    # 判断知识方向
    technical_count = len(document_summary.technical_keywords)
    commercial_count = len(document_summary.commercial_keywords)

    if technical_count > 0 and commercial_count > 0:
        direction = "both"
    elif technical_count > 0:
        direction = "technical"
    else:
        direction = "commercial"

    return ExtractSummaryOutput(
        file_hash=state.file_metadata.file_hash,
        summary=document_summary,
        direction=direction  # type: ignore
    )


def update_index_node(
    state: UpdateIndexInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> UpdateIndexOutput:
    """
    title: 更新知识索引
    desc: 将提取的摘要添加到知识库索引中
    integrations:
    """
    ctx = runtime.context

    # 创建索引器
    indexer = KnowledgeIndexer()

    # 添加或更新索引
    if state.knowledge_index.id in indexer.library.indices:
        indexer.update_index(state.knowledge_index)
        message = f"更新索引: {state.knowledge_index.metadata.file_name}"
    else:
        indexer.add_index(state.knowledge_index)
        message = f"添加索引: {state.knowledge_index.metadata.file_name}"

    return UpdateIndexOutput(
        success=True,
        index_id=state.knowledge_index.id,
        message=message
    )
