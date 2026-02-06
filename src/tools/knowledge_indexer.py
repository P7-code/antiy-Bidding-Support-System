"""
知识库索引工具
用于管理 datafiles 目录下的知识库文件索引
"""
import os
import json
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from utils.file.file import File, FileOps
from graphs.state_knowledge import (
    FileMetadata,
    DocumentSummary,
    ChapterSummary,
    KnowledgeIndex,
    KnowledgeLibrary
)


class KnowledgeIndexer:
    """知识库索引管理器"""

    def __init__(self, knowledge_dir: str = "datafiles", index_file: str = "datafiles/knowledge_index.json"):
        """
        初始化知识库索引管理器

        Args:
            knowledge_dir: 知识库目录
            index_file: 索引文件路径
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.index_file = Path(index_file)
        self.library: Optional[KnowledgeLibrary] = None

        # 确保目录存在
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.index_file.parent.mkdir(parents=True, exist_ok=True)

        # 加载索引
        self._load_index()

    def _load_index(self):
        """加载索引文件"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.library = KnowledgeLibrary(**data)
            except Exception as e:
                print(f"[警告] 加载索引文件失败: {e}")
                self.library = KnowledgeLibrary()
        else:
            self.library = KnowledgeLibrary()

    def _save_index(self):
        """保存索引文件"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.library.dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[错误] 保存索引文件失败: {e}")

    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算文件 SHA256 哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_file_type(self, file_path: Path) -> str:
        """获取文件类型"""
        suffix = file_path.suffix.lower()
        type_map = {
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.pptx': 'pptx',
            '.txt': 'txt'
        }
        return type_map.get(suffix, 'unknown')

    def _map_to_file_standard_type(self, file_type: str) -> str:
        """
        将具体文件类型映射到 File 类的标准类型

        Args:
            file_type: 具体文件类型 (pdf, docx, pptx, txt等)

        Returns:
            File 类标准类型 (document, default等)
        """
        # 文档类型统一映射为 'document'
        document_types = ['pdf', 'docx', 'pptx', 'txt', 'doc', 'ppt', 'xls', 'xlsx', 'md']
        if file_type.lower() in document_types:
            return 'document'
        return 'default'

    def scan_files(self) -> tuple[List[FileMetadata], List[FileMetadata], List[FileMetadata], List[str]]:
        """
        扫描知识库目录，检测文件变化

        Returns:
            (所有文件, 新增文件, 修改文件, 删除文件hash列表)
        """
        all_files = []
        new_files = []
        modified_files = []
        deleted_files = []

        # 当前索引中的文件 hash
        indexed_hashes = set(self.library.indices.keys())

        # 扫描目录
        for file_path in self.knowledge_dir.rglob('*'):
            # 跳过目录和隐藏文件
            if not file_path.is_file() or file_path.name.startswith('.'):
                continue

            # 跳过索引文件
            if file_path.name == 'knowledge_index.json':
                continue

            # 计算文件信息
            file_size = file_path.stat().st_size
            file_hash = self._calculate_file_hash(file_path)
            file_type = self._get_file_type(file_path)

            # 跳过未知文件类型
            if file_type == 'unknown':
                continue

            # 创建文件元信息
            metadata = FileMetadata(
                file_path=str(file_path.relative_to(self.knowledge_dir)),
                file_name=file_path.name,
                file_size=file_size,
                file_type=file_type,
                file_hash=file_hash,
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                modified_at=datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            )

            all_files.append(metadata)

            # 检查是否是新增或修改的文件
            if file_hash not in indexed_hashes:
                new_files.append(metadata)
            else:
                # 检查文件是否被修改（通过 hash 判断）
                indexed_metadata = self.library.indices[file_hash]
                if indexed_metadata.metadata.modified_at != metadata.modified_at:
                    modified_files.append(metadata)

            # 从待删除列表中移除
            indexed_hashes.discard(file_hash)

        # 剩余的 hash 就是删除的文件
        deleted_files = list(indexed_hashes)

        return all_files, new_files, modified_files, deleted_files

    def extract_file_content(self, file_metadata: FileMetadata) -> tuple[str, str]:
        """
        提取文件内容和结构

        Args:
            file_metadata: 文件元信息

        Returns:
            (文件内容, 文件结构)
        """
        file_path = self.knowledge_dir / file_metadata.file_path

        if not file_path.exists():
            return "", ""

        try:
            # 映射到 File 类的标准类型
            standard_file_type = self._map_to_file_standard_type(file_metadata.file_type)
            file = File(url=str(file_path), file_type=standard_file_type)
            content, structure = FileOps.extract_text_with_structure(file)
            return content, structure
        except Exception as e:
            print(f"[错误] 提取文件内容失败: {file_path}, 错误: {e}")
            return "", ""

    def create_index(
        self,
        file_metadata: FileMetadata,
        content_summary: DocumentSummary,
        search_tags: List[str],
        direction: str = "both",
        quality_score: float = 0.0
    ) -> KnowledgeIndex:
        """
        创建知识索引

        Args:
            file_metadata: 文件元信息
            content_summary: 内容摘要
            search_tags: 搜索标签
            direction: 知识方向
            quality_score: 质量评分

        Returns:
            知识索引
        """
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 更新元信息的索引时间
        file_metadata.indexed_at = now
        file_metadata.updated_at = now

        # 创建索引
        index = KnowledgeIndex(
            id=file_metadata.file_hash,
            metadata=file_metadata,
            content_summary=content_summary,
            search_tags=search_tags,
            direction=direction,  # type: ignore
            quality_score=quality_score,
            is_active=True
        )

        return index

    def add_index(self, index: KnowledgeIndex):
        """添加索引"""
        self.library.indices[index.id] = index
        self.library.total_files = len(self.library.indices)
        self.library.total_size = sum(idx.metadata.file_size for idx in self.library.indices.values())
        self.library.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._save_index()

    def update_index(self, index: KnowledgeIndex):
        """更新索引"""
        if index.id in self.library.indices:
            self.library.indices[index.id] = index
            self.library.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._save_index()

    def delete_index(self, index_id: str):
        """删除索引"""
        if index_id in self.library.indices:
            del self.library.indices[index_id]
            self.library.total_files = len(self.library.indices)
            self.library.total_size = sum(idx.metadata.file_size for idx in self.library.indices.values())
            self.library.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._save_index()

    def get_index(self, index_id: str) -> Optional[KnowledgeIndex]:
        """获取索引"""
        return self.library.indices.get(index_id)

    def get_all_indices(self) -> Dict[str, KnowledgeIndex]:
        """获取所有索引"""
        return self.library.indices

    def search_indices(
        self,
        query: str,
        direction: str = "both",
        top_k: int = 5
    ) -> List[KnowledgeIndex]:
        """
        搜索索引（基于标签和摘要的简单匹配）

        Args:
            query: 查询词
            direction: 知识方向
            top_k: 返回结果数量

        Returns:
            匹配的索引列表
        """
        results = []

        for index in self.library.indices.values():
            # 过滤不启用的索引
            if not index.is_active:
                continue

            # 过滤方向
            if direction != "both" and index.direction != direction:
                continue

            # 计算匹配分数
            score = 0.0
            query_lower = query.lower()

            # 检查标签匹配
            for tag in index.search_tags:
                if query_lower in tag.lower():
                    score += 1.0

            # 检查摘要匹配
            if query_lower in index.content_summary.full_summary.lower():
                score += 0.5

            # 检查章节匹配
            for chapter in index.content_summary.key_chapters:
                if query_lower in chapter.summary.lower():
                    score += 0.3

            # 检查关键词匹配
            for keyword in index.content_summary.technical_keywords:
                if query_lower in keyword.lower():
                    score += 0.4

            for keyword in index.content_summary.commercial_keywords:
                if query_lower in keyword.lower():
                    score += 0.4

            if score > 0:
                results.append((score, index))

        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)

        # 返回 top_k 个结果
        return [idx for score, idx in results[:top_k]]

    def edit_index(self, index_id: str, updates: Dict[str, Any]) -> bool:
        """
        编辑索引

        Args:
            index_id: 索引ID
            updates: 更新内容

        Returns:
            是否成功
        """
        index = self.get_index(index_id)
        if not index:
            return False

        try:
            # 更新摘要
            if 'summary' in updates:
                index.content_summary.full_summary = updates['summary']

            # 更新标签
            if 'tags' in updates:
                index.search_tags = updates['tags']

            # 更新方向
            if 'direction' in updates:
                index.direction = updates['direction']  # type: ignore

            # 更新启用状态
            if 'is_active' in updates:
                index.is_active = updates['is_active']

            # 更新质量评分
            if 'quality_score' in updates:
                index.quality_score = updates['quality_score']

            # 更新时间戳
            index.metadata.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.library.last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self._save_index()
            return True
        except Exception as e:
            print(f"[错误] 更新索引失败: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        indices = list(self.library.indices.values())

        technical_count = sum(1 for idx in indices if idx.direction in ['technical', 'both'])
        commercial_count = sum(1 for idx in indices if idx.direction in ['commercial', 'both'])

        file_types = {}
        for idx in indices:
            ftype = idx.metadata.file_type
            file_types[ftype] = file_types.get(ftype, 0) + 1

        return {
            "total_files": self.library.total_files,
            "total_size": self.library.total_size,
            "technical_count": technical_count,
            "commercial_count": commercial_count,
            "file_types": file_types,
            "last_updated": self.library.last_updated,
            "version": self.library.version
        }
