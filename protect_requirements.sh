#!/bin/bash
# requirementsL.txt 保护脚本
# 用于防止修改精简的 requirementsL.txt

echo "正在保护 requirementsL.txt 文件..."

# 检查文件是否存在
if [ ! -f "requirementsL.txt" ]; then
    echo "⚠️  requirementsL.txt 不存在"
    exit 1
fi

# 从 git 恢复到正确版本
git restore requirementsL.txt 2>/dev/null

# 设置为只读
chmod 444 requirementsL.txt

# 验证
LINES=$(wc -l < requirementsL.txt)
echo "✅ requirementsL.txt 已保护"
echo "📄 当前行数: $LINES"
echo "🔒 文件权限: $(ls -l requirementsL.txt | awk '{print $1}')"

# 显示前5行
echo ""
echo "文件内容预览（前5行）:"
head -5 requirementsL.txt
