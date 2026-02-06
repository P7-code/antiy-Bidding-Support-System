#!/usr/bin/env python
"""
测试知识库管理页面导入
"""
import sys
sys.path.insert(0, 'src')

try:
    from knowledge_management import show_knowledge_management_page
    print("✅ 导入成功！")
    print(f"✅ 函数名: {show_knowledge_management_page.__name__}")
    print(f"✅ 文档: {show_knowledge_management_page.__doc__}")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
