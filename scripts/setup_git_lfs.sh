#!/bin/bash
# Git LFS 快速设置脚本

echo "=================================="
echo "  Git LFS 快速设置工具"
echo "=================================="
echo ""

# 检查 Git LFS 是否已安装
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS 未安装"
    echo ""
    echo "请先安装 Git LFS："
    echo "  macOS:   brew install git-lfs"
    echo "  Linux:   sudo apt-get install git-lfs"
    echo "  Windows: https://git-lfs.github.com/"
    echo ""
    exit 1
fi

echo "✅ Git LFS 已安装"
echo ""

# 检查 Git LFS 是否已初始化
if git lfs env &> /dev/null; then
    echo "✅ Git LFS 已初始化"
else
    echo "🔄 初始化 Git LFS..."
    git lfs install
    echo "✅ Git LFS 初始化完成"
fi

echo ""

# 检查 .gitattributes 文件
if [ -f ".gitattributes" ]; then
    echo "✅ .gitattributes 文件已存在"
else
    echo "❌ .gitattributes 文件不存在"
    echo "请确保 .gitattributes 文件存在"
    exit 1
fi

echo ""
echo "📊 当前 Git LFS 状态："
echo ""
git lfs status

echo ""
echo "📁 大文件列表（> 5MB）："
echo ""
find . -type f -size +5M -not -path "*/.git/*" -not -path "*/venv/*" -not -path "*/env/*" -exec ls -lh {} \; | awk '{print $9, "(" $5 ")"}'

echo ""
echo "💾 当前目录大小："
echo ""
du -sh . 2>/dev/null | awk '{print "总大小: " $1}'
du -sh .git 2>/dev/null | awk '{print "Git 仓库: " $1}'
du -sh assets/knowledge_base 2>/dev/null | awk '{print "知识库: " $1}'
du -sh datafiles 2>/dev/null | awk '{print "Datafiles: " $1}'

echo ""
echo "=================================="
echo "  使用说明"
echo "=================================="
echo ""
echo "1. 添加大文件到 Git LFS："
echo "   git add <file>"
echo ""
echo "2. 提交更改："
echo "   git commit -m 'docs: 添加大文件'"
echo ""
echo "3. 推送到远程："
echo "   git push origin main"
echo ""
echo "4. 查看 Git LFS 文件："
echo "   git lfs ls-files"
echo ""
echo "5. 查看 Git LFS 状态："
echo "   git lfs status"
echo ""
