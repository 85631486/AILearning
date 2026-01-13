from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import os
import markdown as md

from config import config

# 全局变量
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name='development'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        """加载用户"""
        from app.models import User
        return User.query.get(int(user_id))

    # 配置会话
    Session(app)

    # 注册Jinja2过滤器
    @app.template_filter('markdown')
    def markdown_filter(text):
        """Markdown过滤器"""
        if not text:
            return ''
        return md.markdown(text, extensions=['fenced_code', 'codehilite', 'tables'])

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.learning import learning_bp
    from app.routes.exercises import exercise_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(learning_bp, url_prefix='/api/v1/learning')
    app.register_blueprint(exercise_bp, url_prefix='/api/v1/exercises')
    app.register_blueprint(ai_bp, url_prefix='/api/v1/ai')

    # 注册页面路由
    from app.routes import main
    app.register_blueprint(main.main_bp)

    # 设置日志
    if not app.debug and not app.testing:
        setup_logging(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app

def setup_logging(app):
    """设置日志"""
    import logging
    from logging.handlers import RotatingFileHandler

    if not os.path.exists('logs'):
        os.mkdir('logs')

    # 文件日志
    file_handler = RotatingFileHandler(
        'logs/cs146s.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # 错误日志
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=1024 * 1024,
        backupCount=10
    )
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s'
    ))
    error_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('CS146S Learning Platform startup')
