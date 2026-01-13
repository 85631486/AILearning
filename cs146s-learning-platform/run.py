#!/usr/bin/env python3
"""
CS146S 在线学习平台启动脚本
"""

import os
from app import create_app

# 创建应用实例
app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    # 开发环境直接运行
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', True)
    )
