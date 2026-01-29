@echo off
chcp 65001 > nul
title 招标文件分析系统 - GitHub 推送脚本

echo ====================================
echo   招标文件分析系统 - GitHub 推送
echo ====================================
echo.

echo 检查 Git 安装...
git --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 未安装 Git，请先安装：https://git-scm.com/download/win
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('git --version') do echo [成功] %%i
echo.

echo 进入项目目录...
cd /d C:\Users\48497\code\p7
if errorlevel 1 (
    echo [错误] 项目目录不存在：C:\Users\48497\code\p7
    echo 请修改脚本中的项目路径为您实际的项目路径
    pause
    exit /b 1
)
echo [成功] 当前目录：%CD%
echo.

echo 检查 Git 状态...
git status
echo.

echo 添加所有文件...
git add .
echo [成功] 已添加所有文件
echo.

echo 提交更改...
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

if errorlevel 1 (
    echo [警告] 提交失败，可能没有新更改
) else (
    echo [成功] 提交成功！
)
echo.

echo 推送到 GitHub...
echo [信息] 仓库地址: https://github.com/P7-code/p7.git
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ====================================
    echo   [错误] 推送失败！
    echo ====================================
    echo.
    echo 可能的原因：
    echo 1. 未配置 GitHub 凭证
    echo 2. 网络连接问题
    echo 3. 仓库权限问题
    echo.
    echo 解决方案：
    echo 1. 配置 GitHub Personal Access Token ^(PAT^)
    echo    访问：https://github.com/settings/tokens
    echo    创建 Token 时选择 'repo' 权限
    echo.
    echo 2. 使用 Git Credential Manager
    echo    在推送时会自动弹出登录窗口
    echo.
    echo 3. 手动执行以下命令：
    echo    cd C:\Users\48497\code\p7
    echo    git push -u origin main
    echo.
) else (
    echo.
    echo ====================================
    echo   [成功] 推送成功！
    echo ====================================
    echo.
    echo 访问地址：
    echo   https://github.com/P7-code/p7
    echo.
    echo Streamlit Cloud 会自动重新部署
    echo 部署完成后访问：https://p7-code-p7.streamlit.app
    echo.
)

pause
