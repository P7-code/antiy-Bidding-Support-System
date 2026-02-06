"""
大文件检查工具
用于检查项目中的大文件并生成报告
"""
import os
from pathlib import Path


def format_size(size_bytes):
    """
    格式化文件大小

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        格式化后的文件大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def find_large_files(root_path='.', min_size_mb=5, exclude_dirs=None):
    """
    查找大文件

    Args:
        root_path: 根目录路径
        min_size_mb: 最小文件大小（MB）
        exclude_dirs: 排除的目录列表

    Returns:
        大文件列表，每个元素为 (文件路径, 大小MB)
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'venv', 'env', 'node_modules',
                       '.pytest_cache', '.tox', 'dist', 'build', '*.egg-info']

    large_files = []
    min_size_bytes = min_size_mb * 1024 * 1024

    for root, dirs, files in os.walk(root_path):
        # 排除指定目录
        dirs[:] = [d for d in dirs if not any(
            excluded in d for excluded in exclude_dirs
        )]

        for file in files:
            file_path = Path(root) / file
            if file_path.is_file():
                try:
                    size_bytes = file_path.stat().st_size
                    if size_bytes >= min_size_bytes:
                        size_mb = size_bytes / (1024 * 1024)
                        large_files.append((file_path, size_mb))
                except (OSError, PermissionError):
                    continue

    # 按大小排序
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files


def analyze_project_structure(root_path='.'):
    """
    分析项目结构

    Args:
        root_path: 根目录路径

    Returns:
        目录大小字典
    """
    dir_sizes = {}
    important_dirs = [
        '.git',
        'assets',
        'assets/knowledge_base',
        'datafiles',
        'config',
        'src',
        'docs',
        'scripts',
    ]

    for dir_name in important_dirs:
        dir_path = Path(root_path) / dir_name
        if dir_path.exists() and dir_path.is_dir():
            total_size = 0
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.is_file():
                        try:
                            total_size += file_path.stat().st_size
                        except (OSError, PermissionError):
                            continue
            dir_sizes[dir_name] = total_size

    return dir_sizes


def generate_report(large_files, dir_sizes, min_size_mb=5):
    """
    生成报告

    Args:
        large_files: 大文件列表
        dir_sizes: 目录大小字典
        min_size_mb: 最小文件大小（MB）

    Returns:
        报告字符串
    """
    report = []
    report.append("=" * 80)
    report.append("  大文件检查报告")
    report.append("=" * 80)
    report.append("")

    # 项目结构分析
    report.append("📊 项目结构分析")
    report.append("-" * 80)
    for dir_name, size_bytes in sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True):
        size_str = format_size(size_bytes)
        report.append(f"  {dir_name:30s} {size_str:>10s}")
    report.append("")

    # 大文件列表
    if large_files:
        report.append(f"📁 大文件列表（> {min_size_mb}MB）")
        report.append("-" * 80)
        total_size = 0
        for i, (file_path, size_mb) in enumerate(large_files, 1):
            size_str = format_size(size_mb * 1024 * 1024)
            relative_path = str(file_path.relative_to(Path.cwd()))
            report.append(f"  {i:3d}. {relative_path}")
            report.append(f"      大小: {size_str}")
            total_size += size_mb

        report.append("")
        report.append(f"  总计: {len(large_files)} 个文件，总大小: {format_size(total_size * 1024 * 1024)}")
        report.append("")
    else:
        report.append(f"✅ 未发现超过 {min_size_mb}MB 的文件")
        report.append("")

    # 建议
    report.append("💡 建议")
    report.append("-" * 80)

    if large_files:
        report.append("  1. 大文件建议使用 Git LFS 管理")
        report.append("     运行: ./scripts/setup_git_lfs.sh")
        report.append("")
        report.append("  2. 或者将大文件放到外部对象存储")
        report.append("     - 阿里云 OSS")
        report.append("     - 腾讯云 COS")
        report.append("     - AWS S3")
        report.append("")

        # 检查是否有知识库文件
        kb_files = [f for f, s in large_files if 'knowledge_base' in str(f) or 'datafiles' in str(f)]
        if kb_files:
            report.append("  3. 检测到知识库文件，建议：")
            report.append("     - 压缩文件后再上传")
            report.append("     - 分批上传")
            report.append("     - 使用外部存储服务")
            report.append("")

    report.append("  详细说明请查看: docs/LARGE_FILES_GUIDE.md")
    report.append("")

    report.append("=" * 80)
    report.append("")

    return "\n".join(report)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='检查项目中的大文件')
    parser.add_argument(
        '--min-size',
        type=int,
        default=5,
        help='最小文件大小（MB），默认 5MB'
    )
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='项目根目录路径，默认当前目录'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出报告到文件'
    )

    args = parser.parse_args()

    print(f"🔍 正在扫描项目: {args.path}")
    print(f"📏 最小文件大小: {args.min_size}MB")
    print("")

    # 查找大文件
    large_files = find_large_files(args.path, args.min_size)

    # 分析项目结构
    dir_sizes = analyze_project_structure(args.path)

    # 生成报告
    report = generate_report(large_files, dir_sizes, args.min_size)

    # 输出报告
    print(report)

    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")


if __name__ == '__main__':
    main()
