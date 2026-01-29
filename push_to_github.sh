#!/bin/bash
# ==========================================
# 招标文件分析系统 - GitHub 推送脚本
# ==========================================
# 用途：将完整代码推送到 GitHub 仓库
# 使用：chmod +x push_to_github.sh && ./push_to_github.sh
# ==========================================

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================${NC}"
echo -e "${CYAN}  招标文件分析系统 - GitHub 推送${NC}"
echo -e "${CYAN}====================================${NC}"
echo ""

# 检查 Git
echo -e "${YELLOW}检查 Git 安装...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ 未安装 Git，请先安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Git 已安装: $(git --version)${NC}"
echo ""

# 进入项目目录
echo -e "${YELLOW}进入项目目录...${NC}"
PROJECT_PATH="/workspace/projects"
cd "$PROJECT_PATH" || {
    echo -e "${RED}❌ 无法进入项目目录: $PROJECT_PATH${NC}"
    exit 1
}
echo -e "${GREEN}✅ 当前目录: $PWD${NC}"
echo ""

# 检查 Git 状态
echo -e "${YELLOW}检查 Git 状态...${NC}"
git status
echo ""

# 添加所有文件
echo -e "${YELLOW}添加所有文件...${NC}"
git add .

# 检查是否有文件被添加
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✅ 没有新的更改需要提交${NC}"
else
    echo -e "${GREEN}✅ 已添加以下文件：${NC}"
    git status --short
fi
echo ""

# 提交更改
echo -e "${YELLOW}提交更改...${NC}"
git commit -m "feat: 添加完整的招标文件分析功能代码

- 添加 src/graphs/state.py - 状态定义
- 添加 src/graphs/node.py - 节点函数实现
- 添加 src/graphs/graph.py - 主图编排
- 添加 src/utils/file/file.py - 文件处理工具
- 添加 config/*.json - 8个大模型配置文件
- 更新 app.py - 完整版Web应用
- 更新 requirements.txt - 完整依赖列表

实现六维并行检测：
1. 废标项检查
2. 商务得分检查
3. 技术方案评估
4. 指标应答验证
5. 技术得分点分析
6. 文件结构检查"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 提交成功！${NC}"
else
    echo -e "${YELLOW}❌ 提交失败，可能没有新更改${NC}"
fi
echo ""

# 推送到 GitHub
echo -e "${YELLOW}推送到 GitHub...${NC}"
echo -e "${CYAN}📦 仓库地址: https://github.com/P7-code/p7.git${NC}"
echo ""

# 尝试推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}====================================${NC}"
    echo -e "${GREEN}  ✅ 推送成功！${NC}"
    echo -e "${GREEN}====================================${NC}"
    echo ""
    echo -e "${CYAN}🌐 访问地址：${NC}"
    echo -e "${CYAN}   https://github.com/P7-code/p7${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Streamlit Cloud 会自动重新部署${NC}"
    echo -e "${YELLOW}   部署完成后访问：https://p7-code-p7.streamlit.app${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}====================================${NC}"
    echo -e "${RED}  ❌ 推送失败！${NC}"
    echo -e "${RED}====================================${NC}"
    echo ""
    echo -e "${YELLOW}可能的原因：${NC}"
    echo "1. 未配置 GitHub 凭证"
    echo "2. 网络连接问题"
    echo "3. 仓库权限问题"
    echo ""
    echo -e "${YELLOW}解决方案：${NC}"
    echo "1. 配置 GitHub Personal Access Token (PAT)"
    echo "   访问：https://github.com/settings/tokens"
    echo "   创建 Token 时选择 'repo' 权限"
    echo ""
    echo "2. 使用 Git Credential Helper"
    echo "   执行：git config --global credential.helper store"
    echo ""
    echo "3. 手动执行以下命令："
    echo "   cd $PROJECT_PATH"
    echo "   git push -u origin main"
    echo ""
fi
