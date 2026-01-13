#!/usr/bin/env python3
"""
TaskManager Flask应用启动脚本
"""

import os
from app import create_app

def main():
    """主函数"""
    # 获取配置
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')

    # 创建应用
    app = create_app()

    print("🚀 启动TaskManager Flask后端...")
    print(f"📍 服务地址: http://{host}:{port}")
    print(f"🔍 调试模式: {'开启' if debug else '关闭'}")
    print(f"📊 API文档: http://{host}:{port}/api/health")

    # 启动服务器
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
