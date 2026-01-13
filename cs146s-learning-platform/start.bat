@echo off
REM CS146S 在线学习平台启动脚本 (Windows)

echo 🚀 启动 CS146S 在线学习平台...

REM 激活虚拟环境
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    echo 请确保虚拟环境已正确创建
    pause
    exit /b 1
)

echo ✅ 虚拟环境已激活

REM 启动Flask应用
echo 🌐 启动Flask应用...
python start.py

REM 停留在命令行
pause
