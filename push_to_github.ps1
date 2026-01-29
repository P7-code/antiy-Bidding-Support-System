# ==========================================
# 招标文件分析系统 - GitHub 推送脚本
# ==========================================
# 用途：将完整代码推送到 GitHub 仓库
# 使用：PowerShell ISE 或 VS Code 终端执行
# ==========================================

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  招标文件分析系统 - GitHub 推送" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Git
Write-Host "检查 Git 安装..." -ForegroundColor Yellow
$gitVersion = git --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 未安装 Git，请先安装：https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git 已安装: $gitVersion" -ForegroundColor Green
Write-Host ""

# 进入项目目录
Write-Host "进入项目目录..." -ForegroundColor Yellow
$projectPath = "C:\Users\48497\code\p7"
if (!(Test-Path $projectPath)) {
    Write-Host "❌ 项目目录不存在: $projectPath" -ForegroundColor Red
    Write-Host "请修改脚本中的项目路径为您实际的项目路径" -ForegroundColor Yellow
    exit 1
}
Set-Location $projectPath
Write-Host "✅ 当前目录: $PWD" -ForegroundColor Green
Write-Host ""

# 检查 Git 状态
Write-Host "检查 Git 状态..." -ForegroundColor Yellow
git status
Write-Host ""

# 添加所有文件
Write-Host "添加所有文件..." -ForegroundColor Yellow
git add .

# 检查是否有文件被添加
$gitStatus = git status --porcelain
if ([string]::IsNullOrEmpty($gitStatus)) {
    Write-Host "✅ 没有新的更改需要提交" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "✅ 已添加以下文件：" -ForegroundColor Green
    git status --short
    Write-Host ""
}

# 提交更改
Write-Host "提交更改..." -ForegroundColor Yellow
$commitMessage = "feat: 添加完整的招标文件分析功能代码

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

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 提交成功！" -ForegroundColor Green
} else {
    Write-Host "❌ 提交失败，可能没有新更改" -ForegroundColor Yellow
}
Write-Host ""

# 推送到 GitHub
Write-Host "推送到 GitHub..." -ForegroundColor Yellow
Write-Host "📦 仓库地址: https://github.com/P7-code/p7.git" -ForegroundColor Cyan
Write-Host ""

# 尝试推送
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Green
    Write-Host "  ✅ 推送成功！" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 访问地址：" -ForegroundColor Cyan
    Write-Host "   https://github.com/P7-code/p7" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Streamlit Cloud 会自动重新部署" -ForegroundColor Yellow
    Write-Host "   部署完成后访问：https://p7-code-p7.streamlit.app" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Red
    Write-Host "  ❌ 推送失败！" -ForegroundColor Red
    Write-Host "====================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "可能的原因：" -ForegroundColor Yellow
    Write-Host "1. 未配置 GitHub 凭证" -ForegroundColor Yellow
    Write-Host "2. 网络连接问题" -ForegroundColor Yellow
    Write-Host "3. 仓库权限问题" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "解决方案：" -ForegroundColor Yellow
    Write-Host "1. 配置 GitHub Personal Access Token (PAT)" -ForegroundColor Cyan
    Write-Host "   访问：https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host "   创建 Token 时选择 'repo' 权限" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. 使用 Git Credential Manager" -ForegroundColor Cyan
    Write-Host "   在推送时会自动弹出登录窗口" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. 手动执行以下命令：" -ForegroundColor Cyan
    Write-Host "   cd C:\Users\48497\code\p7" -ForegroundColor Cyan
    Write-Host "   git push -u origin main" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
