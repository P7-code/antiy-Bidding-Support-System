@echo off
chcp 65001 >nul
echo ==========================================
echo   安天投标文件智能分析系统 - 快速启动
echo ==========================================
echo.

REM 检查Python版本
python --version
echo ✓ Python已安装

REM 检查依赖
echo.
echo 检查依赖...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install -r requirements.txt
) else (
    echo ✓ 依赖已安装
)

REM 启动应用
echo.
echo ==========================================
echo   正在启动Streamlit应用...
echo ==========================================
echo.
echo 访问地址: http://localhost:8501
echo 按 Ctrl+C 停止应用
echo.

streamlit run app.py

pause
