"""
批量将 Markdown 文件转换为 DOCX 格式
"""
import os
import glob

# 转换配置
CONVERSIONS = [
    ("README.md", "安天投标文件智能分析系统-用户手册.docx"),
    ("DEVELOPMENT.md", "安天投标文件智能分析系统-开发文档.docx"),
    ("DEPLOYMENT.md", "安天投标文件智能分析系统-部署指南.docx"),
    ("QUICK_START.md", "安天投标文件智能分析系统-快速开始.docx"),
]

# 输出目录
OUTPUT_DIR = "assets"


def batch_convert():
    """批量转换 Markdown 文件"""
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 导入转换函数
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    from md_to_docx import markdown_to_docx

    # 逐个转换
    for md_file, docx_file in CONVERSIONS:
        md_path = os.path.join("..", md_file)
        docx_path = os.path.join(OUTPUT_DIR, docx_file)

        if os.path.exists(md_path):
            print(f"🔄 正在转换: {md_file}")
            try:
                markdown_to_docx(md_path, docx_path)
                print(f"✅ 完成: {docx_file}")
            except Exception as e:
                print(f"❌ 失败: {md_file} - {e}")
        else:
            print(f"⚠️  跳过: {md_file} (文件不存在)")

    print("\n📝 批量转换完成！")


if __name__ == '__main__':
    batch_convert()
