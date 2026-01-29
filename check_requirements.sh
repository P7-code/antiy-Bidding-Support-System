#!/bin/bash
# requirementsL.txt 快速检查和恢复脚本
# 可以在每次操作前后运行，确保文件保持精简版本

REQUIREMENTSL_FILE="requirementsL.txt"
EXPECTED_LINES=61

echo "🔍 检查 requirementsL.txt 状态..."

if [ ! -f "$REQUIREMENTSL_FILE" ]; then
    echo "❌ requirementsL.txt 不存在"
    exit 1
fi

CURRENT_LINES=$(wc -l < "$REQUIREMENTSL_FILE")

echo "📊 当前状态:"
echo "   行数: $CURRENT_LINES"
echo "   预期: $EXPECTED_LINES"

if [ "$CURRENT_LINES" -ne "$EXPECTED_LINES" ]; then
    echo ""
    echo "⚠️  requirementsL.txt 已被修改！正在恢复..."
    
    # 从 git 恢复
    git restore "$REQUIREMENTSL_FILE" 2>/dev/null
    
    RESTORED_LINES=$(wc -l < "$REQUIREMENTSL_FILE")
    if [ "$RESTORED_LINES" -eq "$EXPECTED_LINES" ]; then
        echo "✅ requirementsL.txt 已恢复到精简版本（$RESTORED_LINES 行）"
    else
        echo "❌ requirementsL.txt 恢复失败！"
        exit 1
    fi
else
    echo "✅ requirementsL.txt 状态正常"
fi

# 设置为只读
chmod 444 "$REQUIREMENTSL_FILE"
echo "🔒 requirementsL.txt 已设置为只读"
