"""
知识库定时任务调度器
每15分钟扫描 datafiles 目录，自动更新索引
"""
import time
import logging
import threading
from datetime import datetime
from typing import Callable, Optional

from tools.knowledge_indexer import KnowledgeIndexer
from graphs.state_knowledge import FileMetadata, DocumentSummary
from graphs.nodes.knowledge_manager_nodes import extract_summary_node
from utils.file.file import FileOps
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime

try:
    from coze_coding_utils.runtime_ctx.context import Context
except ImportError:
    class Context:
        pass


class KnowledgeScheduler:
    """知识库定时任务调度器"""

    def __init__(
        self,
        knowledge_dir: str = "datafiles",
        index_file: str = "datafiles/knowledge_index.json",
        interval_minutes: int = 15
    ):
        """
        初始化调度器

        Args:
            knowledge_dir: 知识库目录
            index_file: 索引文件路径
            interval_minutes: 扫描间隔（分钟）
        """
        self.knowledge_dir = knowledge_dir
        self.index_file = index_file
        self.interval_minutes = interval_minutes
        self.indexer = KnowledgeIndexer(knowledge_dir, index_file)

        self.is_running = False
        self.thread: Optional[threading.Thread] = None

        # 设置日志
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # 创建文件处理器
        handler = logging.FileHandler('datafiles/knowledge_scheduler.log', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

        # 同时输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(console_handler)

    def _extract_summary(self, file_metadata: FileMetadata) -> Optional[DocumentSummary]:
        """
        提取文件摘要

        Args:
            file_metadata: 文件元信息

        Returns:
            文档摘要，失败返回 None
        """
        try:
            # 提取文件内容
            file_path = self.knowledge_dir + '/' + file_metadata.file_path
            content, structure = FileOps.extract_text_with_structure(
                File(url=file_path, file_type=file_metadata.file_type)
            )

            if not content:
                self.logger.warning(f"文件内容为空: {file_metadata.file_name}")
                return None

            # 创建节点输入
            from graphs.state_knowledge import ExtractSummaryInput
            node_input = ExtractSummaryInput(
                file_metadata=file_metadata,
                file_content=content,
                file_structure=structure
            )

            # 读取配置
            import os
            import json
            config_path = os.path.join(
                os.getenv("COZE_WORKSPACE_PATH", "."),
                "config/knowledge_summary_cfg.json"
            )

            config = RunnableConfig(configurable={
                "llm_cfg": config_path
            })

            # 创建 runtime（简化版）
            runtime = Runtime[Context](config)

            # 调用节点提取摘要
            result = extract_summary_node(node_input, config, runtime)

            return result.summary

        except Exception as e:
            self.logger.error(f"提取摘要失败: {file_metadata.file_name}, 错误: {e}")
            return None

    def _process_file(self, file_metadata: FileMetadata):
        """
        处理单个文件

        Args:
            file_metadata: 文件元信息
        """
        try:
            self.logger.info(f"正在处理文件: {file_metadata.file_name}")

            # 提取摘要
            summary = self._extract_summary(file_metadata)

            if not summary:
                self.logger.warning(f"摘要提取失败，跳过: {file_metadata.file_name}")
                return

            # 提取标签
            search_tags = []
            search_tags.extend(summary.technical_keywords)
            search_tags.extend(summary.commercial_keywords)
            search_tags.extend(summary.industry_tags)

            # 创建索引
            from graphs.state_knowledge import KnowledgeIndex
            index = KnowledgeIndex(
                id=file_metadata.file_hash,
                metadata=file_metadata,
                content_summary=summary,
                search_tags=search_tags,
                direction=summary.direction,  # type: ignore
                quality_score=0.8,  # 默认质量评分
                is_active=True
            )

            # 添加或更新索引
            self.indexer.add_index(index)

            self.logger.info(f"✅ 成功处理文件: {file_metadata.file_name}")

        except Exception as e:
            self.logger.error(f"处理文件失败: {file_metadata.file_name}, 错误: {e}")

    def _scan_and_update(self):
        """扫描并更新索引"""
        try:
            self.logger.info("=" * 80)
            self.logger.info(f"开始扫描知识库目录: {self.knowledge_dir}")
            self.logger.info(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # 扫描文件
            all_files, new_files, modified_files, deleted_files = self.indexer.scan_files()

            self.logger.info(f"扫描结果:")
            self.logger.info(f"  总文件数: {len(all_files)}")
            self.logger.info(f"  新增文件: {len(new_files)}")
            self.logger.info(f"  修改文件: {len(modified_files)}")
            self.logger.info(f"  删除文件: {len(deleted_files)}")

            # 处理新增文件
            for file_metadata in new_files:
                self.logger.info(f"处理新增文件: {file_metadata.file_name}")
                self._process_file(file_metadata)
                time.sleep(1)  # 避免过于频繁的 API 调用

            # 处理修改文件
            for file_metadata in modified_files:
                self.logger.info(f"处理修改文件: {file_metadata.file_name}")
                self._process_file(file_metadata)
                time.sleep(1)

            # 删除文件索引
            for file_hash in deleted_files:
                index = self.indexer.get_index(file_hash)
                if index:
                    self.logger.info(f"删除索引: {index.metadata.file_name}")
                    self.indexer.delete_index(file_hash)

            # 输出统计信息
            stats = self.indexer.get_statistics()
            self.logger.info(f"知识库统计:")
            self.logger.info(f"  总文件数: {stats['total_files']}")
            self.logger.info(f"  总大小: {stats['total_size'] / 1024 / 1024:.2f} MB")
            self.logger.info(f"  技术文档: {stats['technical_count']}")
            self.logger.info(f"  商务文档: {stats['commercial_count']}")
            self.logger.info(f"  最后更新: {stats['last_updated']}")
            self.logger.info("=" * 80)

        except Exception as e:
            self.logger.error(f"扫描失败: {e}")

    def _run_loop(self):
        """运行循环"""
        while self.is_running:
            try:
                self._scan_and_update()
            except Exception as e:
                self.logger.error(f"扫描出错: {e}")

            # 等待下一次扫描
            time.sleep(self.interval_minutes * 60)

    def start(self):
        """启动调度器"""
        if self.is_running:
            self.logger.warning("调度器已在运行")
            return

        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.logger.info(f"✅ 调度器已启动，扫描间隔: {self.interval_minutes} 分钟")

    def stop(self):
        """停止调度器"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=10)
        self.logger.info("调度器已停止")

    def run_once(self):
        """立即执行一次扫描"""
        self.logger.info("手动触发扫描")
        self._scan_and_update()


# 全局调度器实例
_global_scheduler: Optional[KnowledgeScheduler] = None


def start_scheduler(
    knowledge_dir: str = "datafiles",
    index_file: str = "datafiles/knowledge_index.json",
    interval_minutes: int = 15
) -> KnowledgeScheduler:
    """
    启动全局调度器

    Args:
        knowledge_dir: 知识库目录
        index_file: 索引文件路径
        interval_minutes: 扫描间隔（分钟）

    Returns:
        调度器实例
    """
    global _global_scheduler

    if _global_scheduler is None:
        _global_scheduler = KnowledgeScheduler(
            knowledge_dir=knowledge_dir,
            index_file=index_file,
            interval_minutes=interval_minutes
        )
        _global_scheduler.start()

    return _global_scheduler


def get_scheduler() -> Optional[KnowledgeScheduler]:
    """
    获取全局调度器实例

    Returns:
        调度器实例，如果未启动则返回 None
    """
    return _global_scheduler


def stop_scheduler():
    """停止全局调度器"""
    global _global_scheduler

    if _global_scheduler:
        _global_scheduler.stop()
        _global_scheduler = None
