#!/bin/bash

echo "=========================================="
echo "  安天投标文件智能分析系统 - 快速启动"
echo "=========================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ 已在虚拟环境中: $VIRTUAL_ENV"
else
    echo "⚠ 建议使用虚拟环境"
    echo ""
    read -p "是否创建虚拟环境? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在创建虚拟环境..."
        python3 -m venv venv
        echo "✓ 虚拟环境创建成功"
        echo "正在激活虚拟环境..."
        source venv/bin/activate
    fi
fi

# 检查依赖
echo ""
echo "检查依赖..."
if ! command -v streamlit &> /dev/null; then
    echo "正在安装依赖..."
    pip install -r requirements.txt
else
    echo "✓ 依赖已安装"
fi

# 启动应用
echo ""
echo "=========================================="
echo "  正在启动Streamlit应用..."
echo "=========================================="
echo ""
echo "访问地址: http://localhost:8501"
echo "按 Ctrl+C 停止应用"
echo ""

streamlit run app.py
