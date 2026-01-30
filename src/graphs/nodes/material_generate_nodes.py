"""
投标材料生成节点
包含：招标文件解析、知识库检索、互联网搜索、材料生成等节点
"""
import os
import json
import re
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_dev_sdk import SearchClient

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass

from graphs.state import GlobalState
from graphs.state_materials import (
    TenderRequirementsParseInput,
    TenderRequirementsParseOutput,
    KnowledgeBaseSearchInput,
    KnowledgeBaseSearchOutput,
    CommercialKBSearchInput,
    CommercialKBSearchOutput,
    TechnicalKBSearchInput,
    TechnicalKBSearchOutput,
    WebSearchInput,
    WebSearchOutput,
    CommercialWebSearchOutput,
    TechnicalWebSearchOutput,
    CommercialMaterialGenerateInput,
    CommercialMaterialGenerateOutput,
    TechnicalMaterialGenerateInput,
    TechnicalMaterialGenerateOutput
)
from tools.knowledge_base_tool import KnowledgeBaseTool
from graphs.node import call_llm


def get_config_file_path(config_name: str) -> str:
    """获取配置文件路径"""
    return os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config_name)


def tender_requirements_parse_node(
    state: TenderRequirementsParseInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TenderRequirementsParseOutput:
    """
    title: 招标文件要求解析
    desc: 解析招标文件，识别商务要求和技术要求，提取投标材料模板
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

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "tender_doc_structure": state.tender_doc_structure
    })

    # 调用LLM进行解析
    result = call_llm(sp, user_prompt_content, llm_config)

    # 解析LLM返回的结果（LLM应该返回JSON格式）
    # 简化处理，直接返回LLM的结果
    # 实际应用中应该使用正则表达式或JSON解析器提取结构化数据
    commercial_requirements = result
    technical_requirements = result
    commercial_template = ""
    technical_template = ""

    return TenderRequirementsParseOutput(
        commercial_requirements=commercial_requirements,
        technical_requirements=technical_requirements,
        commercial_template=commercial_template,
        technical_template=technical_template
    )


def knowledge_base_search_node(
    state: KnowledgeBaseSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> KnowledgeBaseSearchOutput:
    """
    title: 知识库检索
    desc: 在本地知识库中检索相关素材
    integrations: 本地知识库
    """
    ctx = runtime.context

    # 初始化知识库工具
    kb_tool = KnowledgeBaseTool(state.knowledge_base_path)

    # 扫描知识库目录
    kb_tool.scan_directory()

    # 执行搜索
    search_results = kb_tool.search(state.query, top_k=5)

    # 标注素材出处
    for result in search_results:
        result['source_type'] = 'local_knowledge_base'
        result['source_doc'] = result.get('source', '')

        # 尝试提取页码信息
        # 方法1：从内容中提取页码标记（如果有）
        content = result.get('content', '')
        page_match = re.search(r'第\s*(\d+)\s*页', content[:500])
        if page_match:
            result['source_page'] = page_match.group(1)
        else:
            # 方法2：从文件路径中提取（如果是PDF）
            file_path = result.get('path', '')
            if file_path.lower().endswith('.pdf'):
                # 简单的页码估算：基于内容长度
                # 假设每页约500字
                estimated_page = min(len(content) // 500 + 1, 999)
                result['source_page'] = f"约第{estimated_page}页"
            else:
                result['source_page'] = "N/A"

    return KnowledgeBaseSearchOutput(
        search_results=search_results,
        has_local_knowledge=len(search_results) > 0
    )


def commercial_kb_search_node(
    state: CommercialKBSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialKBSearchOutput:
    """
    title: 商务知识库检索
    desc: 在本地知识库中检索商务相关素材
    integrations: 本地知识库
    """
    ctx = runtime.context

    # 初始化知识库工具
    kb_tool = KnowledgeBaseTool(state.knowledge_base_path)

    # 扫描知识库目录
    kb_tool.scan_directory()

    # 执行搜索
    search_results = kb_tool.search(state.commercial_requirements, top_k=5)

    # 标注素材出处
    for result in search_results:
        result['source_type'] = 'local_knowledge_base'
        result['source_doc'] = result.get('source', '')

        # 尝试提取页码信息
        content = result.get('content', '')
        page_match = re.search(r'第\s*(\d+)\s*页', content[:500])
        if page_match:
            result['source_page'] = page_match.group(1)
        else:
            file_path = result.get('path', '')
            if file_path.lower().endswith('.pdf'):
                estimated_page = min(len(content) // 500 + 1, 999)
                result['source_page'] = f"约第{estimated_page}页"
            else:
                result['source_page'] = "N/A"

    return CommercialKBSearchOutput(
        commercial_kb_results=search_results,
        has_local_knowledge=len(search_results) > 0
    )


def technical_kb_search_node(
    state: TechnicalKBSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalKBSearchOutput:
    """
    title: 技术知识库检索
    desc: 在本地知识库中检索技术相关素材
    integrations: 本地知识库
    """
    ctx = runtime.context

    # 初始化知识库工具
    kb_tool = KnowledgeBaseTool(state.knowledge_base_path)

    # 扫描知识库目录
    kb_tool.scan_directory()

    # 执行搜索
    search_results = kb_tool.search(state.technical_requirements, top_k=5)

    # 标注素材出处
    for result in search_results:
        result['source_type'] = 'local_knowledge_base'
        result['source_doc'] = result.get('source', '')

        # 尝试提取页码信息
        content = result.get('content', '')
        page_match = re.search(r'第\s*(\d+)\s*页', content[:500])
        if page_match:
            result['source_page'] = page_match.group(1)
        else:
            file_path = result.get('path', '')
            if file_path.lower().endswith('.pdf'):
                estimated_page = min(len(content) // 500 + 1, 999)
                result['source_page'] = f"约第{estimated_page}页"
            else:
                result['source_page'] = "N/A"

    return TechnicalKBSearchOutput(
        technical_kb_results=search_results,
        has_local_knowledge=len(search_results) > 0
    )


def commercial_web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialWebSearchOutput:
    """
    title: 商务互联网搜索
    desc: 在互联网上搜索商务相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 获取查询词
    query = state.commercial_requirements if state.commercial_requirements else "商务资质、项目经验、服务承诺"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 只返回商务搜索结果
    return CommercialWebSearchOutput(commercial_web_results=search_results)


def technical_web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalWebSearchOutput:
    """
    title: 技术互联网搜索
    desc: 在互联网上搜索技术相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 获取查询词
    query = state.technical_requirements if state.technical_requirements else "技术方案、系统架构、实施方案"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 只返回技术搜索结果
    return TechnicalWebSearchOutput(technical_web_results=search_results)


def web_search_node(
    state: WebSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> WebSearchOutput:
    """
    title: 互联网搜索
    desc: 在互联网上搜索相关素材
    integrations: 联网搜索
    """
    ctx = runtime.context

    # 根据输入判断是商务还是技术搜索
    # 如果有 commercial_kb_results，说明是商务搜索
    is_commercial = bool(state.commercial_kb_results or (state.commercial_requirements and not state.technical_requirements))

    if is_commercial:
        query = state.commercial_requirements if state.commercial_requirements else "商务资质、项目经验、服务承诺"
    else:
        query = state.technical_requirements if state.technical_requirements else "技术方案、系统架构、实施方案"

    # 调用联网搜索
    try:
        client = SearchClient(ctx=ctx)
        response = client.web_search(
            query=query,
            count=5,
            need_summary=True
        )

        # 提取搜索结果
        search_results = []
        if response.web_items:
            for item in response.web_items:
                search_results.append({
                    'content': item.summary or item.snippet,
                    'url': item.url,
                    'title': item.title,
                    'site_name': item.site_name,
                    'source_type': 'web_search'
                })
    except Exception as e:
        # 如果搜索失败，返回空结果
        search_results = []

    # 根据类型返回不同的字段
    if is_commercial:
        return WebSearchOutput(commercial_web_results=search_results)
    else:
        return WebSearchOutput(technical_web_results=search_results)


def commercial_material_generate_node(
    state: CommercialMaterialGenerateInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> CommercialMaterialGenerateOutput:
    """
    title: 商务材料生成
    desc: 根据商务要求和素材生成商务投标材料，标注素材出处
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    llm_config = _cfg.get("config", {})

    # 整理素材信息
    kb_materials = ""
    if state.commercial_kb_results:
        kb_materials = "\n".join([
            f"[本地知识库 - {r.get('source_doc', '')} - {r.get('source_page', 'N/A')}]: {r.get('content', '')[:800]}"
            for r in state.commercial_kb_results[:5]
        ])

    web_materials = ""
    if state.commercial_web_results:
        web_materials = "\n".join([
            f"[互联网搜索 - {r.get('url', '')}]: {r.get('title', '')}\n{r.get('content', '')[:800]}"
            for r in state.commercial_web_results[:5]
        ])

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "requirements": state.commercial_requirements,
        "template": state.commercial_template,
        "kb_materials": kb_materials,
        "web_materials": web_materials
    })

    # 调用LLM生成内容
    commercial_material = call_llm(sp, user_prompt_content, llm_config)

    return CommercialMaterialGenerateOutput(
        commercial_material=commercial_material
    )


def technical_material_generate_node(
    state: TechnicalMaterialGenerateInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> TechnicalMaterialGenerateOutput:
    """
    title: 技术材料生成
    desc: 根据技术要求和素材生成技术投标材料，标注素材出处
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = get_config_file_path(config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    llm_config = _cfg.get("config", {})

    # 整理素材信息
    kb_materials = ""
    if state.technical_kb_results:
        kb_materials = "\n".join([
            f"[本地知识库 - {r.get('source_doc', '')} - {r.get('source_page', 'N/A')}]: {r.get('content', '')[:800]}"
            for r in state.technical_kb_results[:5]
        ])

    web_materials = ""
    if state.technical_web_results:
        web_materials = "\n".join([
            f"[互联网搜索 - {r.get('url', '')}]: {r.get('title', '')}\n{r.get('content', '')[:800]}"
            for r in state.technical_web_results[:5]
        ])

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "requirements": state.technical_requirements,
        "template": state.technical_template,
        "kb_materials": kb_materials,
        "web_materials": web_materials
    })

    # 调用LLM生成内容
    technical_material = call_llm(sp, user_prompt_content, llm_config)

    return TechnicalMaterialGenerateOutput(
        technical_material=technical_material
    )
