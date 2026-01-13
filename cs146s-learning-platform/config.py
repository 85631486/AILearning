import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""

    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI服务配置
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    QWEN_BASE_URL = os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/api/v1')
    QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-turbo')
    QWEN_MOCK_MODE = os.getenv('QWEN_MOCK_MODE', 'False').lower() == 'true'

    # 代码格式化配置
    CODE_FORMAT_ENABLED = os.getenv('CODE_FORMAT_ENABLED', 'False').lower() == 'true'

    # 代码执行配置
    CODE_EXECUTION_TIMEOUT = int(os.getenv('CODE_EXECUTION_TIMEOUT', 30))
    MAX_MEMORY_MB = int(os.getenv('MAX_MEMORY_MB', 100))
    MAX_CPU_TIME = int(os.getenv('MAX_CPU_TIME', 10))

    # 会话配置
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'False').lower() == 'true'

    # 其他配置
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = SECRET_KEY

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    WTF_CSRF_ENABLED = False  # 开发环境禁用CSRF方便测试
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
