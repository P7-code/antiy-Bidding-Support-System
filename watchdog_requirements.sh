#!/bin/bash
# requirementsL.txt 守护脚本
# 持续监控 requirementsL.txt 文件，防止被修改

REQUIREMENTSL_FILE="requirementsL.txt"
EXPECTED_LINES=61
CHECK_INTERVAL=5

echo "🔒 启动 requirementsL.txt 守护进程..."
echo "📄 预期行数: $EXPECTED_LINES"
echo "⏱️  检查间隔: ${CHECK_INTERVAL}秒"
echo "🔄 按 Ctrl+C 停止守护进程"
echo ""

# 无限循环监控
while true; do
    # 检查文件是否存在
    if [ ! -f "$REQUIREMENTSL_FILE" ]; then
        echo "⚠️  requirementsL.txt 不存在，从 git 恢复..."
        git restore "$REQUIREMENTSL_FILE" 2>/dev/null
    fi
    
    # 检查行数
    CURRENT_LINES=$(wc -l < "$REQUIREMENTSL_FILE")
    
    if [ "$CURRENT_LINES" -ne "$EXPECTED_LINES" ]; then
        echo "⚠️  检测到 requirementsL.txt 被修改！"
        echo "   当前行数: $CURRENT_LINES"
        echo "   预期行数: $EXPECTED_LINES"
        echo "   正在恢复到精简版本..."
        
        # 从 git 恢复
        git restore "$REQUIREMENTSL_FILE" 2>/dev/null
        
        # 验证恢复结果
        RESTORED_LINES=$(wc -l < "$REQUIREMENTSL_FILE")
        if [ "$RESTORED_LINES" -eq "$EXPECTED_LINES" ]; then
            echo "✅ requirementsL.txt 已成功恢复！"
            chmod 444 "$REQUIREMENTSL_FILE"
        else
            echo "❌ requirementsL.txt 恢复失败！当前行数: $RESTORED_LINES"
        fi
    fi
    
    # 等待下一次检查
    sleep $CHECK_INTERVAL
done
