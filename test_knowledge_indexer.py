"""
测试知识库索引管理功能
"""
import os
import sys

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.knowledge_indexer import KnowledgeIndexer

def test_knowledge_indexer():
    """测试知识库索引管理工具"""
    print("=" * 80)
    print("测试知识库索引管理工具")
    print("=" * 80)
    
    # 设置测试路径
    kb_path = "assets/knowledge_base"
    
    # 检查路径是否存在
    if not os.path.exists(kb_path):
        print(f"⚠️  知识库路径不存在: {kb_path}")
        print("   将创建测试目录...")
        os.makedirs(kb_path, exist_ok=True)
        print(f"✅ 测试目录已创建: {kb_path}")
    else:
        print(f"✅ 知识库路径存在: {kb_path}")
    
    # 初始化索引工具
    print("\n1. 初始化知识库索引工具...")
    indexer = KnowledgeIndexer(kb_path)
    print("✅ 索引工具初始化成功")
    
    # 扫描文件
    print("\n2. 扫描文件...")
    all_files, new_files, modified_files, deleted_files = indexer.scan_files()
    print(f"✅ 文件扫描完成")
    print(f"   总文件数: {len(all_files)}")
    print(f"   新增文件: {len(new_files)}")
    print(f"   修改文件: {len(modified_files)}")
    print(f"   删除文件: {len(deleted_files)}")
    
    # 获取所有索引
    print("\n3. 获取所有索引...")
    indices = indexer.get_all_indices()
    print(f"✅ 获取索引成功")
    print(f"   索引数量: {len(indices)}")
    for index_id, index in list(indices.items())[:3]:  # 显示前3个索引
        print(f"   - {index.metadata.file_name}: {index.content_summary.full_summary[:50]}...")
    
    # 测试搜索
    print("\n4. 测试搜索功能...")
    test_query = "网络安全"
    print(f"   查询词: {test_query}")
    results = indexer.search_indices(test_query, direction="both", top_k=3)
    if results:
        print(f"✅ 搜索成功，找到 {len(results)} 个结果:")
        for i, index in enumerate(results, 1):
            print(f"   {i}. {index.metadata.file_name} (分数: {index.quality_score})")
            print(f"      摘要: {index.content_summary.full_summary[:80]}...")
    else:
        print("⚠️  未找到搜索结果")
    
    # 测试统计
    print("\n5. 测试统计功能...")
    stats = indexer.get_statistics()
    print(f"✅ 统计信息:")
    print(f"   总文件数: {stats['total_files']}")
    print(f"   总大小: {stats['total_size']} 字节")
    print(f"   技术文档数: {stats['technical_count']}")
    print(f"   商务文档数: {stats['commercial_count']}")
    print(f"   文件类型分布: {stats['file_types']}")
    print(f"   最后更新: {stats['last_updated']}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_knowledge_indexer()
