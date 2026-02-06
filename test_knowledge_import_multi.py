#!/usr/bin/env python
"""
测试 knowledge_management 模块在各种环境下的导入
"""
import sys
import os

print("=" * 80)
print("测试 knowledge_management 模块导入")
print("=" * 80)

# 测试1: 从当前目录导入（添加 src 到路径）
print("\n测试1: 从 src 目录导入...")
try:
    sys.path.insert(0, 'src')
    from knowledge_management import show_knowledge_management_page
    print("✅ 导入成功！")
    print(f"   函数名: {show_knowledge_management_page.__name__}")
    print(f"   文档: {show_knowledge_management_page.__doc__[:50]}...")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 测试2: 使用 src 前缀导入
print("\n测试2: 使用 src.knowledge_management 导入...")
try:
    from src.knowledge_management import show_knowledge_management_page
    print("✅ 导入成功！")
    print(f"   函数名: {show_knowledge_management_page.__name__}")
except Exception as e:
    print(f"❌ 导入失败: {e}")

# 测试3: 清除路径后重新导入
print("\n测试3: 清除路径后重新导入...")
try:
    # 清除之前添加的路径
    if 'src' in sys.path:
        sys.path.remove('src')
    # 重新导入
    import importlib
    if 'knowledge_management' in sys.modules:
        del sys.modules['knowledge_management']
        del sys.modules['src.knowledge_management']

    # 添加 src 到路径
    sys.path.insert(0, 'src')
    from knowledge_management import show_knowledge_management_page
    print("✅ 导入成功！")
    print(f"   函数名: {show_knowledge_management_page.__name__}")
except Exception as e:
    print(f"❌ 导入失败: {e}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
