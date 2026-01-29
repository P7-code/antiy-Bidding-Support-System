"""
本地知识库管理工具
支持本地文档的索引和检索
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re


class KnowledgeBaseTool:
    """本地知识库管理工具"""

    def __init__(self, kb_path: Optional[str] = None):
        """
        初始化知识库

        Args:
            kb_path: 知识库路径，如果为None则使用默认路径
        """
        self.kb_path = kb_path or os.path.join(os.path.dirname(__file__), "../../assets/knowledge_base")
        self.kb_path = os.path.abspath(self.kb_path)
        self.index_file = os.path.join(self.kb_path, ".kb_index.json")
        self.documents = {}
        self._load_index()

    def _load_index(self):
        """加载索引"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
            except Exception as e:
                print(f"加载知识库索引失败: {e}")
                self.documents = {}

    def _save_index(self):
        """保存索引"""
        try:
            os.makedirs(self.kb_path, exist_ok=True)
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存知识库索引失败: {e}")

    def scan_directory(self, directory: Optional[str] = None) -> int:
        """
        扫描目录，索引所有支持的文档

        Args:
            directory: 要扫描的目录，如果为None则使用kb_path

        Returns:
            新增的文档数量
        """
        scan_path = directory or self.kb_path
        if not os.path.exists(scan_path):
            print(f"目录不存在: {scan_path}")
            return 0

        new_count = 0
        # 支持的文件扩展名
        supported_extensions = {'.txt', '.md', '.pdf', '.docx', '.doc'}

        # 遍历目录
        for root, dirs, files in os.walk(scan_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                if ext in supported_extensions:
                    # 计算文件相对路径作为key
                    rel_path = os.path.relpath(file_path, scan_path)
                    
                    # 如果文档已存在且未被修改，则跳过
                    file_hash = self._get_file_hash(file_path)
                    if rel_path in self.documents and self.documents[rel_path].get('hash') == file_hash:
                        continue

                    # 提取文档内容
                    content = self._extract_content(file_path, ext)
                    if content:
                        self.documents[rel_path] = {
                            'path': file_path,
                            'hash': file_hash,
                            'content': content,
                            'title': file,
                            'type': ext
                        }
                        new_count += 1

        # 保存索引
        if new_count > 0:
            self._save_index()

        return new_count

    def _get_file_hash(self, file_path: str) -> str:
        """获取文件哈希值（简单版本，使用文件修改时间）"""
        import time
        return str(os.path.getmtime(file_path))

    def _extract_content(self, file_path: str, ext: str) -> Optional[str]:
        """
        提取文档内容

        Args:
            file_path: 文件路径
            ext: 文件扩展名

        Returns:
            文档内容
        """
        try:
            if ext in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            elif ext in ['.pdf', '.docx', '.doc']:
                # 使用FileOps提取内容
                from utils.file.file import File, FileOps
                file_obj = File(url=file_path, file_type="document")
                return FileOps.extract_text(file_obj)

            return None
        except Exception as e:
            print(f"提取文件内容失败 {file_path}: {e}")
            return None

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        在知识库中搜索

        Args:
            query: 搜索查询词
            top_k: 返回结果数量

        Returns:
            搜索结果列表，每项包含content、source、page等
        """
        results = []

        # 将查询词分解为关键词
        keywords = self._extract_keywords(query)

        # 计算每个文档的相关性分数
        for doc_key, doc in self.documents.items():
            content = doc.get('content', '')
            score = self._calculate_relevance(content, keywords)

            if score > 0:
                results.append({
                    'content': content,
                    'source': doc.get('title', doc_key),
                    'path': doc.get('path', ''),
                    'score': score,
                    'type': 'local_knowledge_base'
                })

        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)

        # 返回top_k结果
        return results[:top_k]

    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取：去除停用词，提取重要的词
        stop_words = {'的', '了', '和', '是', '在', '有', '我', '你', '他', '她', '它', '们', '这个', '那个', '和', '或', '但', '不', '也'}
        
        # 分词（简单版本，按空格和标点分割）
        words = re.split(r'[\s,，.。!！?？;；:：、]+', query)
        
        # 过滤停用词和短词
        keywords = [word.strip() for word in words if word.strip() and word.strip() not in stop_words and len(word.strip()) > 1]
        
        return keywords

    def _calculate_relevance(self, content: str, keywords: List[str]) -> float:
        """
        计算内容与查询的相关性

        Args:
            content: 文档内容
            keywords: 关键词列表

        Returns:
            相关性分数
        """
        if not keywords:
            return 0.0

        content_lower = content.lower()
        score = 0.0

        for keyword in keywords:
            keyword_lower = keyword.lower()
            # 计算关键词出现次数
            count = content_lower.count(keyword_lower)
            
            # 计算关键词长度（越长越重要）
            weight = len(keyword)
            
            # 累加分数
            score += count * weight

        # 归一化分数（除以内容长度）
        return score / (len(content) / 100 + 1)

    def get_document_count(self) -> int:
        """获取文档数量"""
        return len(self.documents)

    def get_document_list(self) -> List[Dict]:
        """获取文档列表"""
        return [
            {
                'title': doc.get('title', key),
                'path': doc.get('path', ''),
                'type': doc.get('type', ''),
                'length': len(doc.get('content', ''))
            }
            for key, doc in self.documents.items()
        ]

    def clear_index(self):
        """清空索引"""
        self.documents = {}
        self._save_index()
