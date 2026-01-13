#!/usr/bin/env python3
"""
CS146S 在线学习平台启动脚本
"""

from app import create_app
import os

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    print("🚀 启动 CS146S 在线学习平台...")
    print(f"🌐 应用将在 http://127.0.0.1:5000 启动")
    print("📖 API文档: http://127.0.0.1:5000/api/v1/")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)

    # 开发环境直接运行
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=app.config.get('DEBUG', True)
    )
