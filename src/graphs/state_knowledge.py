"""
知识库管理相关的数据结构定义
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================
# 知识库文件索引数据结构
# ============================================

class FileMetadata(BaseModel):
    """文件元信息"""
    file_path: str = Field(..., description="文件路径（相对于 datafiles 目录）")
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小（字节）")
    file_type: str = Field(..., description="文件类型：pdf/docx/pptx/txt")
    file_hash: str = Field(..., description="文件 SHA256 哈希值")
    created_at: str = Field(..., description="文件创建时间")
    modified_at: str = Field(..., description="文件修改时间")
    indexed_at: str = Field(default="", description="索引创建时间")
    updated_at: str = Field(default="", description="索引更新时间")


class ChapterSummary(BaseModel):
    """章节摘要"""
    chapter_title: str = Field(..., description="章节标题")
    page_range: str = Field(default="", description="页码范围")
    summary: str = Field(..., description="章节摘要")
    key_points: List[str] = Field(default=[], description="关键要点")


class DocumentSummary(BaseModel):
    """文档摘要"""
    full_summary: str = Field(..., description="全文摘要")
    key_chapters: List[ChapterSummary] = Field(default=[], description="关键章节摘要")
    technical_keywords: List[str] = Field(default=[], description="技术关键词")
    commercial_keywords: List[str] = Field(default=[], description="商务关键词")
    industry_tags: List[str] = Field(default=[], description="行业标签")


class KnowledgeIndex(BaseModel):
    """知识库索引"""
    id: str = Field(..., description="索引ID（文件hash）")
    metadata: FileMetadata = Field(..., description="文件元信息")
    content_summary: DocumentSummary = Field(..., description="内容摘要")
    search_tags: List[str] = Field(default=[], description="搜索标签")
    direction: Literal["technical", "commercial", "both"] = Field(default="both", description="知识方向")
    quality_score: float = Field(default=0.0, description="质量评分（0-1）")
    is_active: bool = Field(default=True, description="是否启用")


class KnowledgeLibrary(BaseModel):
    """知识库（所有索引的集合）"""
    indices: Dict[str, KnowledgeIndex] = Field(default={}, description="所有索引，key为文件hash")
    last_updated: str = Field(default="", description="最后更新时间")
    version: str = Field(default="1.0", description="索引版本")
    total_files: int = Field(default=0, description="总文件数")
    total_size: int = Field(default=0, description="总大小（字节）")


# ============================================
# 知识库管理节点输入输出
# ============================================

class ScanFilesInput(BaseModel):
    """扫描文件节点输入"""
    knowledge_dir: str = Field(default="datafiles", description="知识库目录")


class ScanFilesOutput(BaseModel):
    """扫描文件节点输出"""
    files: List[FileMetadata] = Field(default=[], description="扫描到的文件列表")
    new_files: List[FileMetadata] = Field(default=[], description="新增文件")
    modified_files: List[FileMetadata] = Field(default=[], description="修改的文件")
    deleted_files: List[str] = Field(default=[], description="删除的文件hash列表")


class ExtractSummaryInput(BaseModel):
    """提取摘要节点输入"""
    file_metadata: FileMetadata = Field(..., description="文件元信息")
    file_content: str = Field(..., description="文件内容")
    file_structure: str = Field(default="", description="文件结构信息")


class ExtractSummaryOutput(BaseModel):
    """提取摘要节点输出"""
    file_hash: str = Field(..., description="文件hash")
    summary: DocumentSummary = Field(..., description="文档摘要")
    direction: Literal["technical", "commercial", "both"] = Field(default="both", description="知识方向")


class UpdateIndexInput(BaseModel):
    """更新索引节点输入"""
    knowledge_index: KnowledgeIndex = Field(..., description="知识索引")


class UpdateIndexOutput(BaseModel):
    """更新索引节点输出"""
    success: bool = Field(default=True, description="是否成功")
    index_id: str = Field(..., description="索引ID")
    message: str = Field(default="", description="消息")


class EditIndexInput(BaseModel):
    """编辑索引节点输入"""
    index_id: str = Field(..., description="索引ID")
    updates: Dict[str, Any] = Field(..., description="更新内容")


class EditIndexOutput(BaseModel):
    """编辑索引节点输出"""
    success: bool = Field(default=True, description="是否成功")
    message: str = Field(default="", description="消息")


# ============================================
# 知识库检索节点输入输出（更新版）
# ============================================

class TechnicalKBSearchInputV2(BaseModel):
    """技术知识库检索节点输入（V2）"""
    technical_requirements: str = Field(..., description="技术要求内容")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")
    use_index: bool = Field(default=True, description="是否使用索引")
    top_k: int = Field(default=5, description="返回结果数量")


class TechnicalKBSearchOutputV2(BaseModel):
    """技术知识库检索节点输出（V2）"""
    technical_kb_results: List[dict] = Field(default=[], description="检索结果列表")
    has_local_knowledge: bool = Field(default=False, description="是否有本地知识库内容")


class CommercialKBSearchInputV2(BaseModel):
    """商务知识库检索节点输入（V2）"""
    commercial_requirements: str = Field(..., description="商务要求内容")
    knowledge_base_path: Optional[str] = Field(default=None, description="本地知识库路径")
    use_index: bool = Field(default=True, description="是否使用索引")
    top_k: int = Field(default=5, description="返回结果数量")


class CommercialKBSearchOutputV2(BaseModel):
    """商务知识库检索节点输出（V2）"""
    commercial_kb_results: List[dict] = Field(default=[], description="检索结果列表")
    has_local_knowledge: bool = Field(default=False, description="是否有本地知识库内容")
