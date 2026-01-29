"""
投标材料生成子图
处理商务材料和技术材料的生成流程
"""
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass

from graphs.state import GlobalState
from graphs.state_materials import (
    MaterialGenerateState,
    TenderRequirementsParseInput,
    TenderRequirementsParseOutput,
    KnowledgeBaseSearchInput,
    KnowledgeBaseSearchOutput,
    WebSearchInput,
    WebSearchOutput,
    CommercialMaterialGenerateInput,
    CommercialMaterialGenerateOutput,
    TechnicalMaterialGenerateInput,
    TechnicalMaterialGenerateOutput
)
from graphs.nodes.material_generate_nodes import (
    tender_requirements_parse_node,
    commercial_kb_search_node,
    technical_kb_search_node,
    commercial_web_search_node,
    technical_web_search_node,
    commercial_material_generate_node,
    technical_material_generate_node
)


def create_material_generate_graph() -> StateGraph:
    """
    创建投标材料生成子图

    工作流：
    1. 解析招标文件，提取商务和技术要求
    2. 并行生成商务材料和技术材料
       - 知识库检索
       - 互联网搜索（可选）
       - 材料生成
    """
    # 创建状态图，使用子图专用的 GlobalState
    builder = StateGraph(MaterialGenerateState)

    # 添加节点
    builder.add_node(
        "tender_requirements_parse",
        tender_requirements_parse_node,
        metadata={"type": "agent", "llm_cfg": "config/tender_requirements_parse_cfg.json"}
    )

    # 商务材料生成流程
    builder.add_node(
        "commercial_kb_search",
        commercial_kb_search_node
    )

    builder.add_node(
        "commercial_web_search",
        commercial_web_search_node
    )

    builder.add_node(
        "commercial_material_generate",
        commercial_material_generate_node,
        metadata={"type": "agent", "llm_cfg": "config/commercial_material_generate_cfg.json"}
    )

    # 技术材料生成流程
    builder.add_node(
        "technical_kb_search",
        technical_kb_search_node
    )

    builder.add_node(
        "technical_web_search",
        technical_web_search_node
    )

    builder.add_node(
        "technical_material_generate",
        technical_material_generate_node,
        metadata={"type": "agent", "llm_cfg": "config/technical_material_generate_cfg.json"}
    )

    # 设置入口
    builder.set_entry_point("tender_requirements_parse")

    # 添加边
    builder.add_edge("tender_requirements_parse", "commercial_kb_search")
    builder.add_edge("tender_requirements_parse", "technical_kb_search")

    builder.add_edge("commercial_kb_search", "commercial_web_search")
    builder.add_edge("technical_kb_search", "technical_web_search")

    builder.add_edge("commercial_web_search", "commercial_material_generate")
    builder.add_edge("technical_web_search", "technical_material_generate")

    # 商务和技术材料都生成完成后结束
    builder.add_edge(["commercial_material_generate", "technical_material_generate"], END)

    # 编译图
    return builder.compile()


# 创建子图实例
material_generate_graph = create_material_generate_graph()
