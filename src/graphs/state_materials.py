from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from utils.file.file import File
from graphs.state import GlobalState

# ============================================
# 材料生成子图专用的 GlobalState（包含中间状态）
# ============================================
class MaterialGenerateState(GlobalState):
    """材料生成子图的全局状态"""
    commercial_kb_results: List[dict] = Field(default=[], description="商务知识库检索结果")
    commercial_web_results: List[dict] = Field(default=[], description="商务互联网搜索结果")
    technical_kb_results: List[dict] = Field(default=[], description="技术知识库检索结果")
    technical_web_results: List[dict] = Field(default=[], description="技术互联网搜索结果")


# ============================================
# 投标材料生成相关节点定义
# ============================================

# 材料生成子图调用节点
class MaterialGenerateInvokeInput(BaseModel):
    """材料生成子图调用节点输入"""
    tender_file: File = Field(..., description="招标文件")
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    tender_doc_structure: str = Field(default="", description="招标文件章节结构")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")
    workflow_type: Literal["check", "generate"] = Field(default="generate", description="工作流类型")

class MaterialGenerateInvokeOutput(BaseModel):
    """材料生成子图调用节点输出"""
    commercial_material: str = Field(default="", description="生成的商务投标材料")
    technical_material: str = Field(default="", description="生成的技术投标材料")
    commercial_requirements: str = Field(default="", description="商务要求内容")
    technical_requirements: str = Field(default="", description="技术要求内容")

# 招标文件要求解析节点 (Agent)
class TenderRequirementsParseInput(BaseModel):
    """招标文件要求解析节点输入"""
    tender_doc_content: str = Field(..., description="招标文件文本内容")
    tender_doc_structure: str = Field(default="", description="招标文件章节结构")

class TenderRequirementsParseOutput(BaseModel):
    """招标文件要求解析节点输出"""
    commercial_requirements: str = Field(..., description="商务要求内容")
    technical_requirements: str = Field(..., description="技术要求内容")
    commercial_template: str = Field(default="", description="商务材料模板（如果有）")
    technical_template: str = Field(default="", description="技术材料模板（如果有）")

# 知识库检索节点 (Agent)
class KnowledgeBaseSearchInput(BaseModel):
    """知识库检索节点输入"""
    query: str = Field(..., description="检索查询词")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")
    section_type: Literal["commercial", "technical"] = Field(..., description="章节类型：商务或技术")

class KnowledgeBaseSearchOutput(BaseModel):
    """知识库检索节点输出"""
    search_results: List[dict] = Field(default=[], description="检索结果列表，每项包含content、source、page")
    has_local_knowledge: bool = Field(default=False, description="是否有本地知识库内容")

# 商务知识库检索节点输入
class CommercialKBSearchInput(BaseModel):
    """商务知识库检索节点输入"""
    commercial_requirements: str = Field(..., description="商务要求内容")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")

class CommercialKBSearchOutput(BaseModel):
    """商务知识库检索节点输出（自动映射到MaterialGenerateState）"""
    commercial_kb_results: List[dict] = Field(default=[], description="商务知识库检索结果")
    has_local_knowledge: bool = Field(default=False, description="是否有本地知识库内容")

# 技术知识库检索节点输入
class TechnicalKBSearchInput(BaseModel):
    """技术知识库检索节点输入"""
    technical_requirements: str = Field(..., description="技术要求内容")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")

class TechnicalKBSearchOutput(BaseModel):
    """技术知识库检索节点输出（自动映射到MaterialGenerateState）"""
    technical_kb_results: List[dict] = Field(default=[], description="技术知识库检索结果")
    has_local_knowledge: bool = Field(default=False, description="是否有本地知识库内容")

# 互联网搜索节点 (Agent)
class WebSearchInput(BaseModel):
    """互联网搜索节点输入（从MaterialGenerateState自动映射）"""
    commercial_requirements: Optional[str] = Field(default=None, description="商务要求内容")
    technical_requirements: Optional[str] = Field(default=None, description="技术要求内容")
    commercial_kb_results: List[dict] = Field(default=[], description="商务知识库检索结果（用于确定搜索类型）")
    technical_kb_results: List[dict] = Field(default=[], description="技术知识库检索结果（用于确定搜索类型）")

class WebSearchOutput(BaseModel):
    """互联网搜索节点输出（保留原字段用于兼容）"""
    search_results: List[dict] = Field(default=[], description="搜索结果列表")

class CommercialWebSearchOutput(BaseModel):
    """商务互联网搜索节点输出（自动映射到MaterialGenerateState）"""
    commercial_web_results: List[dict] = Field(default=[], description="商务互联网搜索结果")

class TechnicalWebSearchOutput(BaseModel):
    """技术互联网搜索节点输出（自动映射到MaterialGenerateState）"""
    technical_web_results: List[dict] = Field(default=[], description="技术互联网搜索结果")

# 商务材料生成节点 (Agent)
class CommercialMaterialGenerateInput(BaseModel):
    """商务材料生成节点输入（从MaterialGenerateState自动映射）"""
    commercial_requirements: str = Field(..., description="商务要求内容")
    commercial_template: str = Field(default="", description="商务材料模板")
    commercial_kb_results: List[dict] = Field(default=[], description="商务知识库检索结果")
    commercial_web_results: List[dict] = Field(default=[], description="商务互联网搜索结果")

class CommercialMaterialGenerateOutput(BaseModel):
    """商务材料生成节点输出"""
    commercial_material: str = Field(..., description="生成的商务投标材料")

# 技术材料生成节点 (Agent)
class TechnicalMaterialGenerateInput(BaseModel):
    """技术材料生成节点输入（从MaterialGenerateState自动映射）"""
    technical_requirements: str = Field(..., description="技术要求内容")
    technical_template: str = Field(default="", description="技术材料模板")
    technical_kb_results: List[dict] = Field(default=[], description="技术知识库检索结果")
    technical_web_results: List[dict] = Field(default=[], description="技术互联网搜索结果")

class TechnicalMaterialGenerateOutput(BaseModel):
    """技术材料生成节点输出"""
    technical_material: str = Field(..., description="生成的技术投标材料")

# 材料导出节点
class MaterialExportInput(BaseModel):
    """材料导出节点输入"""
    commercial_material: str = Field(..., description="商务材料")
    technical_material: str = Field(..., description="技术材料")

class MaterialExportOutput(BaseModel):
    """材料导出节点输出"""
    export_summary: str = Field(..., description="导出摘要信息")
