#!/bin/bash
# Git 推送脚本 - 使用 GitHub Personal Access Token
# 使用说明：
# 1. 将下面的 YOUR_TOKEN_HERE 替换为你的 GitHub Personal Access Token
# 2. 在终端执行：bash push_to_github.sh

# ============================================
# 请在这里替换你的 Personal Access Token
GITHUB_TOKEN="YOUR_TOKEN_HERE"
# ============================================

if [ "$GITHUB_TOKEN" = "YOUR_TOKEN_HERE" ]; then
    echo "❌ 错误：请先替换脚本中的 YOUR_TOKEN_HERE 为你的 GitHub Personal Access Token"
    echo ""
    echo "如何获取 token："
    echo "1. 访问：https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token' → 'Generate new token (classic)'"
    echo "3. 勾选 'repo' 权限"
    echo "4. 生成并复制 token"
    echo ""
    exit 1
fi

echo "🔧 配置 Git 远程仓库..."
git remote set-url origin https://${GITHUB_TOKEN}@github.com/P7-code/antiy-Bidding-Support-System

echo "📤 推送到 GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo ""
    echo "📊 推送的文件："
    git log -1 --stat
else
    echo "❌ 推送失败，请检查："
    echo "  - Token 是否正确"
    echo "  - Token 是否有足够的权限（需要 repo 权限）"
    echo "  - 网络连接是否正常"
    exit 1
fi
