#!/bin/bash
# CS146S 在线学习平台启动脚本 (Unix/Linux/Mac)

echo "🚀 启动 CS146S 在线学习平台..."

# 激活虚拟环境
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ 虚拟环境激活失败"
    echo "请确保虚拟环境已正确创建"
    exit 1
fi

echo "✅ 虚拟环境已激活"

# 启动Flask应用
echo "🌐 启动Flask应用..."
python start.py
