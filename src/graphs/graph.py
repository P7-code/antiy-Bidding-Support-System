from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass

from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    KnowledgeManagementInput,
    KnowledgeManagementOutput,
    RouteWorkflowInput,
    RouteWorkflowOutput
)

from graphs.node import (
    tender_doc_parse_node,
    bid_doc_parse_node,
    invalid_items_check_node,
    commercial_score_check_node,
    technical_plan_check_node,
    indicator_response_check_node,
    technical_score_check_node,
    bid_structure_check_node,
    modification_summary_node
)

# 导入材料生成节点
from graphs.nodes.material_generate_nodes import (
    tender_requirements_parse_node,
    commercial_kb_search_node,
    technical_kb_search_node,
    commercial_web_search_node,
    technical_web_search_node,
    commercial_material_generate_node,
    technical_material_generate_node
)

# 知识库管理占位节点
def knowledge_management_node(
    state: KnowledgeManagementInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> KnowledgeManagementOutput:
    """
    title: 知识库管理模块
    desc: 知识库管理是独立的功能模块，通过 Streamlit UI 提供四个功能标签页：概览、文件索引、编辑索引、定时任务
    integrations:
    """
    ctx = runtime.context
    
    # 知识库管理是独立功能，不通过工作流调用
    # 此节点仅为占位，实际功能在 app.py 中实现
    return KnowledgeManagementOutput(
        message="知识库管理是独立功能模块，请通过 Streamlit UI 访问"
    )

# 路由节点（工作流入口）
def route_workflow_node(
    state: RouteWorkflowInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> RouteWorkflowOutput:
    """
    title: 工作流路由
    desc: 根据工作流类型参数（check/generate/knowledge）路由到不同的流程分支
    """
    ctx = runtime.context
    
    # 路由节点只是传递 workflow_type，实际的分支逻辑由 add_conditional_edges 处理
    return RouteWorkflowOutput(
        workflow_type=state.workflow_type
    )

# 工作流类型选择函数
def route_by_workflow_type(state: GlobalState) -> str:
    """
    title: 工作流类型分支
    desc: 根据工作流类型参数（check/generate/knowledge）路由到不同的流程分支
    """
    if state.workflow_type == "generate":
        return "材料生成"
    elif state.workflow_type == "knowledge":
        return "知识库管理"
    else:
        return "投标文件检查"


# 创建状态图，指定入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加投标文件检查节点
builder.add_node("tender_doc_parse", tender_doc_parse_node)
builder.add_node("bid_doc_parse", bid_doc_parse_node)
builder.add_node("invalid_items_check", invalid_items_check_node,
                metadata={"type": "agent", "llm_cfg": "config/invalid_items_check_cfg.json"})
builder.add_node("commercial_score_check", commercial_score_check_node,
                metadata={"type": "agent", "llm_cfg": "config/commercial_score_check_cfg.json"})
builder.add_node("technical_plan_check", technical_plan_check_node,
                metadata={"type": "agent", "llm_cfg": "config/technical_plan_check_cfg.json"})
builder.add_node("indicator_response_check", indicator_response_check_node,
                metadata={"type": "agent", "llm_cfg": "config/indicator_response_check_cfg.json"})
builder.add_node("technical_score_check", technical_score_check_node,
                metadata={"type": "agent", "llm_cfg": "config/technical_score_check_cfg.json"})
builder.add_node("bid_structure_check", bid_structure_check_node,
                metadata={"type": "agent", "llm_cfg": "config/bid_structure_check_cfg.json"})
builder.add_node("modification_summary", modification_summary_node,
                metadata={"type": "agent", "llm_cfg": "config/modification_summary_cfg.json"})

# 添加投标材料生成节点（所有节点直接添加到主图）
builder.add_node(
    "tender_requirements_parse",
    tender_requirements_parse_node,
    metadata={"type": "agent", "llm_cfg": "config/tender_requirements_parse_cfg.json"}
)

builder.add_node("commercial_kb_search", commercial_kb_search_node)
builder.add_node("commercial_web_search", commercial_web_search_node)
builder.add_node(
    "commercial_material_generate",
    commercial_material_generate_node,
    metadata={"type": "agent", "llm_cfg": "config/commercial_material_generate_cfg.json"}
)

builder.add_node("technical_kb_search", technical_kb_search_node)
builder.add_node("technical_web_search", technical_web_search_node)
builder.add_node(
    "technical_material_generate",
    technical_material_generate_node,
    metadata={"type": "agent", "llm_cfg": "config/technical_material_generate_cfg.json"}
)

# 添加知识库管理节点（独立功能模块的占位节点）
builder.add_node("knowledge_management", knowledge_management_node)

# 添加路由节点（工作流入口）
builder.add_node("route_workflow", route_workflow_node)

# 设置入口点为路由节点
builder.set_entry_point("route_workflow")

# 添加条件边：根据工作流类型路由到各个分支的招标文件解析节点
builder.add_conditional_edges(
    source="route_workflow",
    path=route_by_workflow_type,
    path_map={
        "投标文件检查": "tender_doc_parse",
        "材料生成": "tender_doc_parse",
        "知识库管理": "knowledge_management"
    }
)

# 招标文件解析后的路由：再次根据工作流类型路由
def route_after_tender_parse(state: GlobalState) -> str:
    """
    title: 招标文件解析后路由
    desc: 根据工作流类型参数路由到下一节点
    """
    if state.workflow_type == "generate":
        return "材料生成"
    else:
        return "投标文件检查"

builder.add_conditional_edges(
    source="tender_doc_parse",
    path=route_after_tender_parse,
    path_map={
        "投标文件检查": "bid_doc_parse",
        "材料生成": "tender_requirements_parse"
    }
)

# 检查流程的边
builder.add_edge("bid_doc_parse", "invalid_items_check")
builder.add_edge("bid_doc_parse", "commercial_score_check")
builder.add_edge("bid_doc_parse", "technical_plan_check")
builder.add_edge("bid_doc_parse", "indicator_response_check")
builder.add_edge("bid_doc_parse", "technical_score_check")
builder.add_edge("bid_doc_parse", "bid_structure_check")

builder.add_edge(["invalid_items_check", "commercial_score_check", "technical_plan_check",
                "indicator_response_check", "technical_score_check", "bid_structure_check"],
                "modification_summary")

# 材料生成流程的边
builder.add_edge("tender_requirements_parse", "commercial_kb_search")
builder.add_edge("tender_requirements_parse", "technical_kb_search")

builder.add_edge("commercial_kb_search", "commercial_web_search")
builder.add_edge("technical_kb_search", "technical_web_search")

builder.add_edge("commercial_web_search", "commercial_material_generate")
builder.add_edge("technical_web_search", "technical_material_generate")

# 商务和技术材料都生成完成后结束
builder.add_edge(["commercial_material_generate", "technical_material_generate"], END)

# 检查流程结束
builder.add_edge("modification_summary", END)

# 知识库管理流程结束
builder.add_edge("knowledge_management", END)

# 编译图
main_graph = builder.compile()
