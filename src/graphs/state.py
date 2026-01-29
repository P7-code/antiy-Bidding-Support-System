from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from utils.file.file import File

# ============================================
# 全局状态定义 (GlobalState)
# ============================================
class GlobalState(BaseModel):
    """工作流全局状态，用于在各节点间传递数据"""
    tender_file: File = Field(..., description="招标文件")
    bid_file: Optional[File] = Field(default=None, description="投标文件（检查功能需要）")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")
    tender_doc_content: str = Field(default="", description="招标文件文本内容")
    tender_doc_structure: str = Field(default="", description="招标文件章节结构（JSON格式）")
    bid_doc_content: str = Field(default="", description="投标文件文本内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")
    invalid_items_check: str = Field(default="", description="废标项检查结果")
    commercial_score_check: str = Field(default="", description="商务得分点检查结果")
    technical_plan_check: str = Field(default="", description="技术方案检查结果")
    indicator_response_check: str = Field(default="", description="指标与应答检查结果")
    technical_score_check: str = Field(default="", description="技术得分点检测结果")
    bid_structure_check: str = Field(default="", description="投标文件结构检查结果")
    final_modification_suggestions: str = Field(default="", description="最终修改建议汇总")

    # 投标材料生成相关状态
    workflow_type: Literal["check", "generate"] = Field(default="check", description="工作流类型：check=检查，generate=生成材料")
    commercial_requirements: str = Field(default="", description="商务要求内容")
    technical_requirements: str = Field(default="", description="技术要求内容")
    commercial_template: str = Field(default="", description="商务材料模板（如果有）")
    technical_template: str = Field(default="", description="技术材料模板（如果有）")
    commercial_kb_results: List[dict] = Field(default=[], description="商务知识库检索结果")
    commercial_web_results: List[dict] = Field(default=[], description="商务互联网搜索结果")
    technical_kb_results: List[dict] = Field(default=[], description="技术知识库检索结果")
    technical_web_results: List[dict] = Field(default=[], description="技术互联网搜索结果")
    commercial_material: str = Field(default="", description="生成的商务投标材料")
    technical_material: str = Field(default="", description="生成的技术投标材料")

# ============================================
# 图输入输出定义 (Graph Input/Output)
# ============================================
class GraphInput(BaseModel):
    """工作流输入"""
    tender_file: File = Field(..., description="招标文件（PDF、Word等文档格式）")
    bid_file: Optional[File] = Field(default=None, description="投标文件（PDF、Word等文档格式），检查模式需要")
    workflow_type: Literal["check", "generate"] = Field(default="check", description="工作流类型：check=投标文件检查，generate=投标材料生成")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径，材料生成模式下使用")

class GraphOutput(BaseModel):
    """工作流输出"""
    final_modification_suggestions: str = Field(..., description="详细的投标文件修改清单和修改意见")
    invalid_items_check: str = Field(..., description="废标项检查结果")
    commercial_score_check: str = Field(..., description="商务得分点检查结果")
    technical_plan_check: str = Field(..., description="技术方案检查结果")
    indicator_response_check: str = Field(..., description="指标与应答检查结果")
    technical_score_check: str = Field(..., description="技术得分点检测结果")
    bid_structure_check: str = Field(..., description="投标文件结构检查结果")

# ============================================
# 各节点输入输出定义 (Node Input/Output)
# ============================================

# 招标文件解析节点
class TenderDocParseInput(BaseModel):
    """招标文件解析节点输入"""
    tender_file: File = Field(..., description="招标文件")

class TenderDocParseOutput(BaseModel):
    """招标文件解析节点输出"""
    tender_doc_content: str = Field(..., description="招标文件提取的文本内容")
    tender_doc_structure: str = Field(default="", description="招标文件章节结构（JSON格式）")

# 投标文件解析节点
class BidDocParseInput(BaseModel):
    """投标文件解析节点输入"""
    bid_file: Optional[File] = Field(default=None, description="投标文件")

class BidDocParseOutput(BaseModel):
    """投标文件解析节点输出"""
    bid_doc_content: str = Field(..., description="投标文件提取的文本内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

# 废标项检查节点 (Agent)
class InvalidItemsCheckInput(BaseModel):
    """废标项检查节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

class InvalidItemsCheckOutput(BaseModel):
    """废标项检查节点输出"""
    invalid_items_check: str = Field(..., description="废标项检查结果，列出是否存在废标风险及具体原因")

# 商务得分点检查节点 (Agent)
class CommercialScoreCheckInput(BaseModel):
    """商务得分点检查节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

class CommercialScoreCheckOutput(BaseModel):
    """商务得分点检查节点输出"""
    commercial_score_check: str = Field(..., description="商务得分点检查结果，包括预计得分、失分点及改进建议")

# 技术方案检查节点 (Agent)
class TechnicalPlanCheckInput(BaseModel):
    """技术方案检查节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

class TechnicalPlanCheckOutput(BaseModel):
    """技术方案检查节点输出"""
    technical_plan_check: str = Field(..., description="技术方案检查结果，包括技术方案完整性、创新性、可行性评估及改进建议")

# 指标与应答检查节点 (Agent)
class IndicatorResponseCheckInput(BaseModel):
    """指标与应答检查节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

class IndicatorResponseCheckOutput(BaseModel):
    """指标与应答检查节点输出"""
    indicator_response_check: str = Field(..., description="指标与应答检查结果，检查是否逐条响应招标文件要求")

# 修改建议汇总节点 (Agent)
class ModificationSummaryInput(BaseModel):
    """修改建议汇总节点输入"""
    invalid_items_check: str = Field(..., description="废标项检查结果")
    commercial_score_check: str = Field(..., description="商务得分点检查结果")
    technical_plan_check: str = Field(..., description="技术方案检查结果")
    indicator_response_check: str = Field(..., description="指标与应答检查结果")
    technical_score_check: str = Field(..., description="技术得分点检测结果")
    bid_structure_check: str = Field(..., description="投标文件结构检查结果")

class ModificationSummaryOutput(BaseModel):
    """修改建议汇总节点输出"""
    final_modification_suggestions: str = Field(..., description="最终修改建议清单，整合所有检查结果，按优先级排序")

# 技术得分点检测节点 (Agent)
class TechnicalScoreCheckInput(BaseModel):
    """技术得分点检测节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")
    indicator_response_check: str = Field(default="", description="指标与应答检查结果，作为参考")

class TechnicalScoreCheckOutput(BaseModel):
    """技术得分点检测节点输出"""
    technical_score_check: str = Field(..., description="技术得分点检测结果，包括覆盖率、遗漏项、应答不充分项、错误项及改进建议")

# 投标文件结构检查节点 (Agent)
class BidStructureCheckInput(BaseModel):
    """投标文件结构检查节点输入"""
    tender_doc_content: str = Field(..., description="招标文件内容，提取投标文件模板要求")
    bid_doc_content: str = Field(..., description="投标文件内容")
    bid_doc_structure: str = Field(default="", description="投标文件章节结构（JSON格式）")

class BidStructureCheckOutput(BaseModel):
    """投标文件结构检查节点输出"""
    bid_structure_check: str = Field(..., description="投标文件结构检查结果，包括目录完整性、缺失项、排布问题及优化建议")
