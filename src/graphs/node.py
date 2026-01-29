import json
import os
from typing import Dict, Any, TYPE_CHECKING
from jinja2 import Template
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

# 使用公开的 LangChain 接口
from langchain_openai import ChatOpenAI

# 条件导入Context，避免在Streamlit Cloud上因私有包缺失而报错
try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    # 如果导入失败，创建一个假的Context类用于类型注解
    class Context:
        pass

from utils.file.file import FileOps
from graphs.state import (
    TenderDocParseInput, TenderDocParseOutput,
    BidDocParseInput, BidDocParseOutput,
    InvalidItemsCheckInput, InvalidItemsCheckOutput,
    CommercialScoreCheckInput, CommercialScoreCheckOutput,
    TechnicalPlanCheckInput, TechnicalPlanCheckOutput,
    IndicatorResponseCheckInput, IndicatorResponseCheckOutput,
    TechnicalScoreCheckInput, TechnicalScoreCheckOutput,
    BidStructureCheckInput, BidStructureCheckOutput,
    ModificationSummaryInput, ModificationSummaryOutput
)


# ============================================
# Coze 环境变量加载
# ============================================

def load_coze_env():
    """
    从 .coze.env 文件加载环境变量（Coze 平台备用配置方式）
    """
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        env_file = os.path.join(workspace_path, ".coze.env")

        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            return True
    except Exception as e:
        print(f"[警告] 加载 .coze.env 文件失败: {e}")
    return False


# 加载 Coze 环境变量（在模块导入时执行）
load_coze_env()


# ============================================
# 配置文件路径辅助函数
# ============================================

def get_config_file_path(config_filename: str) -> str:
    """
    获取配置文件的绝对路径
    """
    # 获取 src/graphs 目录的绝对路径
    graphs_dir = os.path.dirname(os.path.abspath(__file__))
    # 项目根目录是 src/graphs 的上一级的上一级
    project_root = os.path.dirname(os.path.dirname(graphs_dir))
    # 拼接配置文件路径
    config_path = os.path.join(project_root, "config", config_filename)
    # 规范化为绝对路径
    return os.path.abspath(config_path)


# ============================================
# 文件解析节点
# ============================================

def tender_doc_parse_node(state: TenderDocParseInput, config: RunnableConfig, runtime: Runtime[Context]) -> TenderDocParseOutput:
    """
    title: 招标文件解析
    desc: 从招标文件中提取文本内容和章节结构，为后续分析做准备
    integrations:
    """
    try:
        tender_file = state.tender_file
        if isinstance(tender_file, dict):
            from utils.file.file import File
            tender_file = File(**tender_file)

        content, structure = FileOps.extract_text_with_structure(tender_file)
        return TenderDocParseOutput(tender_doc_content=content, tender_doc_structure=structure)
    except Exception as e:
        return TenderDocParseOutput(tender_doc_content=f"解析失败: {str(e)}", tender_doc_structure="")


def bid_doc_parse_node(state: BidDocParseInput, config: RunnableConfig, runtime: Runtime[Context]) -> BidDocParseOutput:
    """
    title: 投标文件解析
    desc: 从投标文件中提取文本内容和章节结构，为后续检查做准备
    integrations:
    """
    try:
        bid_file = state.bid_file
        if isinstance(bid_file, dict):
            from utils.file.file import File
            bid_file = File(**bid_file)

        content, structure = FileOps.extract_text_with_structure(bid_file)
        return BidDocParseOutput(bid_doc_content=content, bid_doc_structure=structure)
    except Exception as e:
        return BidDocParseOutput(bid_doc_content=f"解析失败: {str(e)}", bid_doc_structure="")


# ============================================
# LLM 调用辅助函数
# ============================================

def call_llm(sp: str, up: str, llm_config: Dict[str, Any]) -> str:
    """
    调用 LLM 的公共函数
    使用 OpenAI 兼容接口
    """
    # 从环境变量获取配置
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")

    # 如果没有配置 API key，返回演示结果
    if not api_key:
        return """【演示模式结果】

由于未配置 LLM API Key，系统返回演示结果。如需使用完整功能，请配置以下环境变量：
- OPENAI_API_KEY: 你的 API 密钥
- OPENAI_API_BASE: API 基础URL（可选，默认为 https://api.openai.com/v1）

【系统提示词】
{}

【用户提示词】
{}

【配置】请先在 Streamlit Cloud 设置中添加环境变量：Settings → Environment Variables
""".format(sp[:100] + "...", up[:100] + "...")

    # 初始化 LLM
    llm = ChatOpenAI(
        model=llm_config.get("model", "gpt-4"),
        temperature=llm_config.get("temperature", 0.3),
        max_tokens=llm_config.get("max_completion_tokens", 4096),
        api_key=api_key,
        base_url=api_base
    )

    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=up)
    ]

    # 调用 LLM
    response = llm.invoke(messages)

    # 提取响应内容
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        if response.content and isinstance(response.content[0], str):
            return " ".join(response.content)
        else:
            return " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))

    return str(response.content)


# ============================================
# Agent节点函数
# ============================================

def invalid_items_check_node(state: InvalidItemsCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> InvalidItemsCheckOutput:
    """
    title: 废标项检查
    desc: 检查投标文件是否存在废标风险，对比招标文件中的废标要求，给出具体判断结果
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("invalid_items_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return InvalidItemsCheckOutput(invalid_items_check=result)


def commercial_score_check_node(state: CommercialScoreCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> CommercialScoreCheckOutput:
    """
    title: 商务得分点检查
    desc: 根据商务评分规则，检查投标文件商务部分的完整性，估算得分，找出失分点和改进机会
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("commercial_score_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return CommercialScoreCheckOutput(commercial_score_check=result)


def technical_plan_check_node(state: TechnicalPlanCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> TechnicalPlanCheckOutput:
    """
    title: 技术方案检查
    desc: 检查技术方案的完整性、创新性、可行性，评估是否符合技术评分细则，给出改进建议
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("technical_plan_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return TechnicalPlanCheckOutput(technical_plan_check=result)


def indicator_response_check_node(state: IndicatorResponseCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> IndicatorResponseCheckOutput:
    """
    title: 指标与应答检查
    desc: 检查投标文件是否逐条响应了招标文件的技术指标要求，找出遗漏或应答不充分的地方
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("indicator_response_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return IndicatorResponseCheckOutput(indicator_response_check=result)


def technical_score_check_node(state: TechnicalScoreCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> TechnicalScoreCheckOutput:
    """
    title: 技术得分点检测
    desc: 根据技术指标与应答情况，结合招标文件中的技术要求，进行技术得分点检测，检查是否覆盖全部技术应答内容，是否有遗漏缺项，是否有应答不充分或者应答错误等影响技术评分的情况
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("technical_score_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure,
        "indicator_response_check": state.indicator_response_check
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return TechnicalScoreCheckOutput(technical_score_check=result)


def bid_structure_check_node(state: BidStructureCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> BidStructureCheckOutput:
    """
    title: 投标文件结构检查
    desc: 根据投标文件中对于商务部分与技术部分的模板要求，对投标文件整体目录结构进行检查，是否有缺失项，是否存在目录与内容排布不合理等影响专家阅读标书快速对应得分点等问题
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("bid_structure_check_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "tender_doc_content": state.tender_doc_content,
        "bid_doc_content": state.bid_doc_content,
        "bid_doc_structure": state.bid_doc_structure
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return BidStructureCheckOutput(bid_structure_check=result)


def modification_summary_node(state: ModificationSummaryInput, config: RunnableConfig, runtime: Runtime[Context]) -> ModificationSummaryOutput:
    """
    title: 修改建议汇总
    desc: 汇总所有检查结果，按优先级排序，生成完整的修改清单和详细修改意见
    integrations: 大语言模型
    """
    cfg_file = get_config_file_path("modification_summary_cfg.json")
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "invalid_items_check": state.invalid_items_check,
        "commercial_score_check": state.commercial_score_check,
        "technical_plan_check": state.technical_plan_check,
        "indicator_response_check": state.indicator_response_check,
        "technical_score_check": state.technical_score_check,
        "bid_structure_check": state.bid_structure_check
    })

    result = call_llm(sp, user_prompt_content, llm_config)
    return ModificationSummaryOutput(final_modification_suggestions=result)
