# CS146S 在线学习系统 - 详细技术开发方案

## 📋 项目概述

### 项目背景
基于斯坦福CS146S现代软件开发者课程，构建轻量级在线学习平台，专注于核心教学功能：在线编程练习、用户管理、课程文档展示和AI学习助理。

### 项目目标
- **轻量级部署**：单体Flask应用，简化部署和维护
- **核心功能聚焦**：在线练习 + 课程文档 + AI助手
- **实用性优先**：解决实际教学需求，避免过度设计
- **易于扩展**：模块化设计，便于后续功能扩展

### 核心价值
- **教学效率提升**：结构化练习 + AI即时辅导
- **学习体验优化**：在线代码练习 + 进度追踪
- **成本控制**：轻量级架构，降低部署和维护成本
- **快速上线**：简化技术栈，缩短开发周期

### 技术栈总览
- **后端**：Flask + SQLAlchemy + SQLite
- **前端**：Bootstrap 5 + JavaScript (ES6+) + Monaco Editor
- **AI服务**：阿里云千问API (Qwen)
- **部署**：Gunicorn + Nginx (生产环境)
- **版本控制**：Git

## 🏗️ 技术架构设计

### 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                    用户浏览器 (Browser)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  登录页面 │ 课程主页 │ 练习页面 │ 文档页面 │ AI助手页面 │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                 │ HTTP/HTTPS
                    ┌────────────────────┐
                    │   Flask Web应用     │
                    │   (Python + Jinja2) │
                    │                    │
                    │ • 用户认证模块     │
                    │ • 课程内容模块     │
                    │ • 练习执行模块     │
                    │ • AI交互模块       │
                    └────────────────────┘
                                 │
                    ┌────────────────────┐
                    │   数据存储层       │
                    │                    │
                    │ • SQLite数据库     │
                    │ • 本地文件存储     │
                    └────────────────────┘
                                 │
                    ┌────────────────────┐
                    │   外部服务         │
                    │                    │
                    │ • 阿里云千问API    │
                    │ • 代码执行环境     │
                    └────────────────────┘
```

### 目录结构设计
```
cs146s-learning-platform/
├── app/                          # Flask应用主目录
│   ├── __init__.py              # 应用初始化
│   ├── models.py                # 数据模型定义
│   ├── routes/                  # 路由模块
│   │   ├── __init__.py
│   │   ├── auth.py             # 用户认证路由
│   │   ├── learning.py         # 学习模块路由
│   │   ├── exercises.py        # 练习模块路由
│   │   └── api.py              # API路由
│   ├── services/                # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── code_executor.py    # 代码执行服务
│   │   ├── ai_assistant.py     # AI助手服务
│   │   └── progress_tracker.py # 进度追踪服务
│   ├── static/                  # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/               # HTML模板
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── learning/
│   │   └── exercises/
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       ├── security.py         # 安全检查工具
│       └── helpers.py          # 辅助函数
├── data/                        # 数据文件
│   ├── seed_data.py            # 初始化数据
│   ├── course_content/         # 课程内容
│   │   ├── week1/
│   │   ├── week2/
│   │   └── ...
│   └── exercises/              # 练习数据
├── tests/                       # 测试文件
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_exercises.py
│   ├── test_code_executor.py
│   └── test_ai_assistant.py
├── config.py                    # 配置文件
├── requirements.txt             # Python依赖
├── Dockerfile                   # Docker配置
├── docker-compose.yml          # Docker Compose配置
├── run.py                       # 应用启动脚本
├── Makefile                     # 构建脚本
└── README.md                    # 项目文档
```

## 🔧 开发环境搭建

### 系统要求
- **Python版本**：3.8+
- **操作系统**：Windows 10+ / macOS 10.15+ / Ubuntu 18.04+
- **内存**：至少4GB RAM
- **磁盘空间**：至少2GB可用空间

### 环境依赖安装

#### 1. Python环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 升级pip
pip install --upgrade pip
```

#### 2. 核心依赖包
```txt
# requirements.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.1.1
Flask-Login==0.6.3
Flask-Session==0.5.0
Werkzeug==2.3.7
python-dotenv==1.0.0
openai==1.3.0
markdown==3.5.1
pygments==2.16.1
requests==2.31.0
psutil==5.9.6
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 前端依赖
```bash
# Monaco Editor (通过CDN引入)
# Bootstrap 5 (通过CDN引入)
# Chart.js (通过CDN引入)
# jQuery (通过CDN引入)
```

### 环境变量配置
```bash
# .env 文件
# Flask配置
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=sqlite:///app.db

# AI服务配置
QWEN_API_KEY=your-qwen-api-key
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL=qwen-turbo

# 代码执行配置
CODE_EXECUTION_TIMEOUT=30
MAX_MEMORY_MB=100
MAX_CPU_TIME=10
```

### 数据库初始化
```bash
# 创建数据库表
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 填充初始数据
python data/seed_data.py
```

## 💾 数据模型设计

### 核心数据表结构

#### 用户表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    avatar VARCHAR(200),
    bio TEXT,
    role VARCHAR(20) DEFAULT 'student',  -- 'student', 'instructor', 'admin'
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    login_count INTEGER DEFAULT 0
);
```

#### 周学习模块表 (weeks)
```sql
CREATE TABLE weeks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER UNIQUE NOT NULL,  -- 1-8
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content_path VARCHAR(500),  -- Markdown文档路径
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 练习题目表 (exercises)
```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    exercise_type VARCHAR(50) NOT NULL,  -- 'prompt', 'code', 'project'
    difficulty VARCHAR(20) DEFAULT 'beginner',  -- 'beginner', 'intermediate', 'advanced'
    initial_code TEXT,  -- 初始代码模板
    test_code TEXT,     -- 测试代码
    solution_code TEXT, -- 参考答案
    hints TEXT,         -- 提示信息 (JSON格式)
    points INTEGER DEFAULT 10,
    time_limit INTEGER DEFAULT 30,  -- 分钟
    order_index INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (week_id) REFERENCES weeks(id)
);
```

#### 用户提交记录表 (submissions)
```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    submitted_code TEXT NOT NULL,
    execution_result TEXT,  -- JSON格式的执行结果
    test_results TEXT,      -- JSON格式的测试结果
    score DECIMAL(5,2),
    is_correct BOOLEAN DEFAULT 0,
    status VARCHAR(20) DEFAULT 'submitted',  -- 'submitted', 'running', 'completed', 'failed'
    execution_time DECIMAL(5,2),  -- 执行时间(秒)
    memory_usage INTEGER,    -- 内存使用(KB)
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    attempts_count INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id),
    UNIQUE(user_id, exercise_id, attempts_count)
);
```

#### 学习进度表 (user_progress)
```sql
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    week_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed'
    completed_exercises INTEGER DEFAULT 0,
    total_exercises INTEGER DEFAULT 0,
    current_exercise_id INTEGER,
    started_at DATETIME,
    completed_at DATETIME,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_spent INTEGER DEFAULT 0,  -- 总学习时长(秒)
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (week_id) REFERENCES weeks(id),
    FOREIGN KEY (current_exercise_id) REFERENCES exercises(id),
    UNIQUE(user_id, week_id)
);
```

#### AI对话记录表 (ai_conversations)
```sql
CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(100),  -- 会话ID，用于分组对话
    exercise_id INTEGER,  -- 可为空，关联具体练习
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'chat',  -- 'chat', 'explain', 'debug', 'guidance'
    tokens_used INTEGER,  -- AI消耗的tokens
    response_time DECIMAL(5,2),  -- 响应时间(秒)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);
```

#### 系统配置表 (system_config)
```sql
CREATE TABLE system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(50) DEFAULT 'string',  -- 'string', 'int', 'float', 'bool', 'json'
    description VARCHAR(500),
    is_public BOOLEAN DEFAULT 0,  -- 是否公开配置
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,  -- 更新者用户ID
    FOREIGN KEY (updated_by) REFERENCES users(id)
);
```

### SQLAlchemy模型定义
```python
# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200))
    bio = db.Column(db.Text)
    role = db.Column(db.String(20), default='student')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)

    # 关联关系
    submissions = db.relationship('Submission', backref='user', lazy=True)
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    conversations = db.relationship('AIConversation', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Week(db.Model):
    __tablename__ = 'weeks'

    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content_path = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    exercises = db.relationship('Exercise', backref='week', lazy=True)
    progress = db.relationship('UserProgress', backref='week', lazy=True)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    exercise_type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), default='beginner')
    initial_code = db.Column(db.Text)
    test_code = db.Column(db.Text)
    solution_code = db.Column(db.Text)
    hints = db.Column(db.Text)  # JSON格式
    points = db.Column(db.Integer, default=10)
    time_limit = db.Column(db.Integer, default=30)
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    submissions = db.relationship('Submission', backref='exercise', lazy=True)

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    submitted_code = db.Column(db.Text, nullable=False)
    execution_result = db.Column(db.Text)  # JSON格式
    test_results = db.Column(db.Text)      # JSON格式
    score = db.Column(db.Numeric(5, 2))
    is_correct = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='submitted')
    execution_time = db.Column(db.Numeric(5, 2))
    memory_usage = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts_count = db.Column(db.Integer, default=1)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started')
    completed_exercises = db.Column(db.Integer, default=0)
    total_exercises = db.Column(db.Integer, default=0)
    current_exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, default=0)
    progress_percentage = db.Column(db.Numeric(5, 2), default=0.00)

class AIConversation(db.Model):
    __tablename__ = 'ai_conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='chat')
    tokens_used = db.Column(db.Integer)
    response_time = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemConfig(db.Model):
    __tablename__ = 'system_config'

    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False)
    config_value = db.Column(db.Text)
    config_type = db.Column(db.String(50), default='string')
    description = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
```

## 🔌 Flask API设计

### Flask RESTful API设计原则

基于Flask框架构建RESTful API，遵循以下设计原则：

1. **Flask路由设计**：使用Flask的路由装饰器 (`@app.route`) 定义API端点
2. **资源命名**：使用复数名词，如 `/api/users`, `/api/exercises`
3. **HTTP方法**：
   - `GET`：查询资源
   - `POST`：创建资源
   - `PUT`：更新整个资源
   - `PATCH`：部分更新资源
   - `DELETE`：删除资源
4. **状态码**：标准HTTP状态码
5. **版本控制**：通过URL路径，如 `/api/v1/`
6. **响应格式**：统一的JSON格式
7. **请求解析**：使用Flask的 `request` 对象处理请求数据

### Flask API端点设计

#### 用户认证API
```python
# app/routes/auth.py
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = auth_service.authenticate_user(email, password)
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    result = auth_service.register_user(username, email, password)
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    auth_service.logout_user()
    return jsonify({"success": True, "message": "登出成功"}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    user = auth_service.get_current_user()
    return jsonify({"user": user.to_dict()}), 200
```

#### 练习相关API
```python
# app/routes/exercises.py
from flask import Blueprint, request, jsonify
from app.services.exercise_service import ExerciseService
from app.services.code_executor import CodeExecutor

exercise_bp = Blueprint('exercises', __name__, url_prefix='/api/v1/exercises')
exercise_service = ExerciseService()
code_executor = CodeExecutor()

@exercise_bp.route('', methods=['GET'])
def get_exercises():
    """获取练习列表"""
    week_id = request.args.get('week_id', type=int)
    exercise_type = request.args.get('exercise_type')
    difficulty = request.args.get('difficulty')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    result = exercise_service.get_exercises(
        week_id=week_id,
        exercise_type=exercise_type,
        difficulty=difficulty,
        page=page,
        per_page=per_page
    )
    return jsonify(result), 200

@exercise_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """获取练习详情"""
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    if exercise:
        return jsonify({"exercise": exercise.to_dict()}), 200
    return jsonify({"error": "练习不存在"}), 404

@exercise_bp.route('/<int:exercise_id>/execute', methods=['POST'])
@login_required
def execute_code(exercise_id):
    """执行代码"""
    data = request.get_json()
    code = data.get('code', '')
    inputs = data.get('inputs', {})

    result = code_executor.execute_code(code, inputs)
    return jsonify(result), 200

@exercise_bp.route('/<int:exercise_id>/submit', methods=['POST'])
@login_required
def submit_exercise(exercise_id):
    """提交练习答案"""
    data = request.get_json()
    code = data.get('code', '')
    attempt_number = data.get('attempt_number', 1)

    result = exercise_service.submit_exercise(
        user_id=current_user.id,
        exercise_id=exercise_id,
        code=code,
        attempt_number=attempt_number
    )

    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400

@exercise_bp.route('/<int:exercise_id>/submissions', methods=['GET'])
@login_required
def get_submissions(exercise_id):
    """获取提交历史"""
    submissions = exercise_service.get_user_submissions(
        user_id=current_user.id,
        exercise_id=exercise_id
    )
    return jsonify({"submissions": submissions}), 200

@exercise_bp.route('/<int:exercise_id>/leaderboard', methods=['GET'])
def get_leaderboard(exercise_id):
    """获取排行榜"""
    leaderboard = exercise_service.get_leaderboard(exercise_id)
    return jsonify({"leaderboard": leaderboard}), 200
```

#### AI助手API
```python
# POST /api/v1/ai/chat
# AI对话
{
  "message": "解释Python中的装饰器",
  "context": { "exercise_id": 1, "code": "..." }
}
# Response: { "response": "...", "tokens_used": 150 }

# POST /api/v1/ai/explain
# 代码解释
{
  "code": "def hello():\n    print('Hello')",
  "language": "python"
}
# Response: { "explanation": "..." }

# POST /api/v1/ai/debug
# 代码调试
{
  "code": "def bug():\n    x = 1/0",
  "error": "ZeroDivisionError: division by zero"
}
# Response: { "suggestions": [...], "fixed_code": "..." }

# POST /api/v1/ai/hint
# 获取提示
{
  "exercise_id": 1,
  "current_code": "...",
  "progress": "stuck"
}
# Response: { "hints": [...] }
```

#### 进度追踪API
```python
# GET /api/v1/progress
# 获取用户学习进度
# Response: { "progress": [...], "stats": {...} }

# GET /api/v1/progress/{week_id}
# 获取指定周的进度
# Response: { "week_progress": {...} }

# PUT /api/v1/progress/{week_id}
# 更新学习进度
{
  "status": "in_progress",
  "current_exercise_id": 5,
  "time_spent": 3600
}
# Response: { "success": true, "progress": {...} }

# GET /api/v1/stats
# 获取学习统计
# Response: {
#   "total_exercises": 48,
#   "completed_exercises": 12,
#   "total_score": 450,
#   "average_score": 85.5,
#   "time_spent": 7200,
#   "streak_days": 7
# }
```

#### 系统管理API (管理员)
```python
# GET /api/v1/admin/users
# 用户管理
# Response: { "users": [...], "pagination": {...} }

# POST /api/v1/admin/exercises
# 创建练习
{
  "week_id": 1,
  "title": "Hello World",
  "description": "...",
  "exercise_type": "code",
  "initial_code": "print('Hello World')"
}
# Response: { "success": true, "exercise": {...} }

# GET /api/v1/admin/stats
# 系统统计
# Response: { "user_count": 100, "exercise_count": 48, "total_submissions": 500 }

# PUT /api/v1/admin/config
# 系统配置
{
  "config_key": "max_execution_time",
  "config_value": "30",
  "config_type": "int"
}
# Response: { "success": true }
```

### API错误处理

#### 统一错误响应格式
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入参数无效",
    "details": {
      "field": "email",
      "reason": "邮箱格式不正确"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 常见错误码
- `VALIDATION_ERROR`: 参数验证失败
- `AUTHENTICATION_ERROR`: 认证失败
- `AUTHORIZATION_ERROR`: 权限不足
- `NOT_FOUND`: 资源不存在
- `CONFLICT`: 资源冲突
- `RATE_LIMITED`: 请求频率限制
- `INTERNAL_ERROR`: 服务器内部错误

## 🔒 安全设计

### 代码执行安全

#### 1. 静态代码分析
```python
# app/utils/security.py
import ast
import re

class CodeSecurityChecker:
    """代码安全检查器"""

    DANGEROUS_PATTERNS = [
        r'import\s+(os|sys|subprocess|socket|urllib|http)',
        r'from\s+(os|sys|subprocess|socket|urllib|http)',
        r'__\w+__',  # 私有属性访问
        r'eval\s*\(',
        r'exec\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        r'input\s*\(',  # 防止无限等待
    ]

    FORBIDDEN_FUNCTIONS = [
        'exit', 'quit', 'system', 'popen', 'call', 'run',
        'connect', 'bind', 'listen', 'accept'
    ]

    def check_code(self, code: str) -> dict:
        """检查代码安全性"""
        issues = []

        # 检查危险模式
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'dangerous_pattern',
                    'pattern': pattern,
                    'message': f'检测到危险代码模式: {pattern}'
                })

        # 检查禁止函数
        for func in self.FORBIDDEN_FUNCTIONS:
            if re.search(r'\b' + re.escape(func) + r'\s*\(', code):
                issues.append({
                    'type': 'forbidden_function',
                    'function': func,
                    'message': f'禁止使用函数: {func}'
                })

        # AST分析
        try:
            tree = ast.parse(code)
            ast_issues = self._analyze_ast(tree)
            issues.extend(ast_issues)
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'message': f'语法错误: {e.msg}',
                'line': e.lineno
            })

        return {
            'is_safe': len(issues) == 0,
            'issues': issues
        }

    def _analyze_ast(self, tree: ast.AST) -> list:
        """AST深度分析"""
        issues = []

        class SecurityVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    if alias.name in ['os', 'sys', 'subprocess']:
                        issues.append({
                            'type': 'dangerous_import',
                            'module': alias.name,
                            'message': f'禁止导入模块: {alias.name}'
                        })
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module in ['os', 'sys', 'subprocess']:
                    issues.append({
                        'type': 'dangerous_import',
                        'module': node.module,
                        'message': f'禁止导入模块: {node.module}'
                    })
                self.generic_visit(node)

        visitor = SecurityVisitor()
        visitor.visit(tree)

        return issues
```

#### 2. 资源限制执行
```python
# app/services/code_executor.py
import subprocess
import tempfile
import os
import resource
import signal
import psutil
from typing import Dict, Any
from app.utils.security import CodeSecurityChecker

class SecureCodeExecutor:
    """安全代码执行器"""

    def __init__(self):
        self.security_checker = CodeSecurityChecker()
        self.max_execution_time = 30  # 秒
        self.max_memory_mb = 100     # MB
        self.max_cpu_time = 10       # 秒

    def execute_code(self, code: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        安全执行Python代码

        Args:
            code: 要执行的Python代码
            inputs: 输入数据 {"stdin": "...", "args": [...]}

        Returns:
            执行结果字典
        """
        # 1. 安全检查
        security_result = self.security_checker.check_code(code)
        if not security_result['is_safe']:
            return {
                'success': False,
                'error': '代码包含不安全的操作',
                'issues': security_result['issues']
            }

        # 2. 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # 3. 设置资源限制并执行
            result = self._execute_with_limits(temp_file, inputs or {})
            return result

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '代码执行超时',
                'timeout': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'执行失败: {str(e)}'
            }
        finally:
            # 4. 清理临时文件
            try:
                os.unlink(temp_file)
            except:
                pass

    def _execute_with_limits(self, file_path: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """带资源限制的执行"""
        def set_limits():
            """设置资源限制"""
            # CPU时间限制
            resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_time, self.max_cpu_time))
            # 内存限制
            memory_limit = self.max_memory_mb * 1024 * 1024  # 转换为字节
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))

        # 准备执行环境
        env = os.environ.copy()
        env['PYTHONPATH'] = ''  # 清理Python路径

        # 执行代码
        process = subprocess.Popen(
            ['python3', file_path],
            stdin=subprocess.PIPE if inputs.get('stdin') else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            preexec_fn=set_limits  # 设置资源限制
        )

        try:
            # 发送输入并等待结果
            stdout, stderr = process.communicate(
                input=inputs.get('stdin', ''),
                timeout=self.max_execution_time
            )

            return {
                'success': process.returncode == 0,
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode,
                'execution_time': self._measure_execution_time(process)
            }

        except subprocess.TimeoutExpired:
            process.kill()
            raise

    def _measure_execution_time(self, process) -> float:
        """测量执行时间"""
        try:
            # 获取进程信息
            ps_process = psutil.Process(process.pid)
            cpu_times = ps_process.cpu_times()
            return cpu_times.user + cpu_times.system
        except:
            return 0.0
```

### Web安全防护

#### 1. XSS防护
```python
# app/utils/helpers.py
from markupsafe import escape
import bleach

def sanitize_html(text: str) -> str:
    """清理HTML内容，防止XSS"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'code', 'pre']
    allowed_attrs = {}

    return bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs)

def sanitize_markdown(text: str) -> str:
    """清理Markdown内容"""
    # 转换Markdown为HTML，然后清理
    import markdown
    html = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
    return sanitize_html(html)
```

#### 2. CSRF防护
```python
# app/__init__.py
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    # ... 其他配置 ...

    # 启用CSRF保护
    csrf.init_app(app)

    return app
```

#### 3. 速率限制
```python
# app/utils/rate_limit.py
from flask import request, g
from functools import wraps
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """检查是否允许请求"""
        now = time.time()
        self.requests[key] = [t for t in self.requests[key] if now - t < window]

        if len(self.requests[key]) >= limit:
            return False

        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter()

def rate_limit(limit: int, window: int):
    """速率限制装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"{request.remote_addr}:{request.endpoint}"
            if not rate_limiter.is_allowed(key, limit, window):
                return {"error": "请求过于频繁"}, 429
            return f(*args, **kwargs)
        return wrapped
    return decorator
```

## 🧪 测试策略

### 测试层次结构

#### 1. 单元测试
```python
# tests/test_code_executor.py
import pytest
from app.services.code_executor import SecureCodeExecutor

class TestSecureCodeExecutor:
    def setup_method(self):
        self.executor = SecureCodeExecutor()

    def test_safe_code_execution(self):
        """测试安全代码执行"""
        code = "print('Hello World')"
        result = self.executor.execute_code(code)

        assert result['success'] == True
        assert 'Hello World' in result['stdout']

    def test_dangerous_import_blocked(self):
        """测试危险导入被阻止"""
        code = "import os\nos.system('ls')"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']

    def test_timeout_handling(self):
        """测试超时处理"""
        code = "import time\ntime.sleep(60)"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert result.get('timeout') == True

    def test_memory_limit(self):
        """测试内存限制"""
        code = "data = 'x' * (50 * 1024 * 1024)"  # 50MB字符串
        result = self.executor.execute_code(code)

        assert result['success'] == False
        # 应该因为内存限制被终止

    def test_input_handling(self):
        """测试输入处理"""
        code = "name = input('Enter name: ')\nprint(f'Hello {name}')"
        inputs = {"stdin": "Alice"}
        result = self.executor.execute_code(code, inputs)

        assert result['success'] == True
        assert 'Hello Alice' in result['stdout']
```

#### 2. 集成测试
```python
# tests/test_exercise_workflow.py
import pytest
from app import create_app, db
from app.models import User, Exercise, Submission

class TestExerciseWorkflow:
    def setup_method(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_complete_exercise_flow(self):
        """测试完整的练习流程"""
        with self.app.test_client() as client:
            # 1. 用户登录
            login_response = client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password'
            })
            assert login_response.status_code == 200

            # 2. 获取练习列表
            exercises_response = client.get('/api/v1/exercises')
            assert exercises_response.status_code == 200
            exercises_data = exercises_response.get_json()

            # 3. 选择第一个练习
            exercise_id = exercises_data['exercises'][0]['id']

            # 4. 执行代码
            execute_response = client.post(f'/api/v1/exercises/{exercise_id}/execute', json={
                'code': 'print("Hello World")'
            })
            assert execute_response.status_code == 200
            execute_data = execute_response.get_json()
            assert execute_data['success'] == True

            # 5. 提交答案
            submit_response = client.post(f'/api/v1/exercises/{exercise_id}/submit', json={
                'code': 'print("Hello World")'
            })
            assert submit_response.status_code == 200

            # 6. 验证提交记录
            submissions_response = client.get(f'/api/v1/exercises/{exercise_id}/submissions')
            assert submissions_response.status_code == 200
            submissions_data = submissions_response.get_json()
            assert len(submissions_data['submissions']) > 0
```

#### 3. API测试
```python
# tests/test_api_auth.py
import pytest
from app import create_app, db
from app.models import User

class TestAuthAPI:
    def setup_method(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """测试用户注册"""
        with self.app.test_client() as client:
            response = client.post('/api/v1/auth/register', json={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'password123'
            })

            assert response.status_code == 201
            data = response.get_json()
            assert data['success'] == True
            assert 'user' in data

    def test_user_login(self):
        """测试用户登录"""
        # 先创建用户
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password'
            })

            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] == True
            assert 'token' in data

    def test_invalid_login(self):
        """测试无效登录"""
        with self.app.test_client() as client:
            response = client.post('/api/v1/auth/login', json={
                'email': 'wrong@example.com',
                'password': 'wrongpassword'
            })

            assert response.status_code == 401
            data = response.get_json()
            assert data['success'] == False
```

#### 4. 端到端测试 (E2E)
```python
# tests/test_e2e_learning_flow.py
import pytest
from playwright.sync_api import Page

class TestLearningFlow:
    def test_complete_learning_flow(self, page: Page):
        """测试完整的学习流程"""
        # 1. 访问主页
        page.goto('http://localhost:5000')

        # 2. 用户注册
        page.click('text=注册')
        page.fill('[name=username]', 'testuser')
        page.fill('[name=email]', 'test@example.com')
        page.fill('[name=password]', 'password123')
        page.click('button[type=submit]')

        # 3. 用户登录
        page.fill('[name=email]', 'test@example.com')
        page.fill('[name=password]', 'password123')
        page.click('button[type=submit]')

        # 4. 选择Week 1
        page.click('text=Week 1: 提示工程技术')

        # 5. 选择练习
        page.click('text=第一个练习')

        # 6. 在编辑器中输入代码
        editor = page.locator('.monaco-editor')
        editor.click()
        page.keyboard.type('print("Hello CS146S!")')

        # 7. 执行代码
        page.click('button:has-text("运行代码")')

        # 8. 验证输出
        output = page.locator('.code-output')
        assert 'Hello CS146S!' in output.text_content()

        # 9. 提交答案
        page.click('button:has-text("提交答案")')

        # 10. 验证提交成功
        success_message = page.locator('.success-message')
        assert '提交成功' in success_message.text_content()

        # 11. 查看进度
        page.click('text=我的进度')
        progress = page.locator('.progress-percentage')
        assert '100%' in progress.text_content()
```

### 测试覆盖率目标

- **单元测试**：80%+ 代码覆盖率
- **集成测试**：核心业务流程全覆盖
- **API测试**：所有API端点覆盖
- **E2E测试**：主要用户流程覆盖

### 持续集成

#### GitHub Actions配置
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## 📅 实施计划

### Phase 1: 基础框架搭建 (2周)

#### Week 1: 核心框架
- [ ] 项目目录结构搭建
- [ ] Flask应用初始化
- [ ] 数据库模型设计与实现
- [ ] 用户认证系统 (注册/登录/登出)
- [ ] 基础页面模板 (Bootstrap 5)
- [ ] 会话管理和权限控制
- [ ] 环境配置和配置文件

#### Week 2: 数据层和基础功能
- [ ] SQLite数据库初始化
- [ ] 数据迁移脚本
- [ ] 初始数据填充 (Week 1-8内容)
- [ ] 基础API端点实现
- [ ] 错误处理和日志系统
- [ ] 单元测试框架搭建

### Phase 2: 核心功能开发 (6周)

#### Week 3-4: 周学习模块
- [ ] Markdown文档展示功能
- [ ] 周学习页面和导航
- [ ] 练习列表展示
- [ ] 学习进度基础追踪
- [ ] 课程内容管理
- [ ] 文档搜索功能

#### Week 5-6: 在线练习系统
- [ ] Monaco Editor集成
- [ ] 代码执行安全沙箱
- [ ] 前端代码运行状态显示
- [ ] 练习提交和保存
- [ ] 测试用例验证框架
- [ ] 练习历史记录

#### Week 7-8: AI学习助理
- [ ] 阿里云千问API集成
- [ ] AI对话功能实现
- [ ] 代码解释和调试
- [ ] 学习指导功能
- [ ] AI配置管理界面
- [ ] 会话历史管理

### Phase 3: 高级功能和优化 (4周)

#### Week 9-10: 学习进度系统
- [ ] 进度数据统计和分析
- [ ] 可视化进度图表 (Chart.js)
- [ ] 个人中心页面
- [ ] 成就和徽章系统
- [ ] 学习报告生成
- [ ] 进度同步和备份

#### Week 11-12: 系统优化和部署
- [ ] 性能优化和缓存
- [ ] 用户界面优化
- [ ] Gunicorn生产部署配置
- [ ] Nginx反向代理配置
- [ ] 部署脚本编写
- [ ] 监控和日志系统
- [ ] 完整测试覆盖

### Phase 4: 测试和上线 (2周)

#### Week 13: 集成测试和修复
- [ ] 端到端测试
- [ ] 性能测试和压力测试
- [ ] 安全审计
- [ ] Bug修复和优化

#### Week 14: 部署上线
- [ ] 生产环境配置
- [ ] 数据迁移
- [ ] 用户文档编写
- [ ] 上线部署和监控

### 里程碑和交付物

#### Milestone 1: MVP版本 (Week 4)
- ✅ 用户注册登录
- ✅ Week 1-8内容展示
- ✅ 基础练习列表
- ✅ 简单的代码执行

#### Milestone 2: Beta版本 (Week 8)
- ✅ 完整的在线练习系统
- ✅ AI学习助理
- ✅ 学习进度追踪
- ✅ 基础的管理后台

#### Milestone 3: 正式版本 (Week 14)
- ✅ 完整的学习平台
- ✅ 生产级部署
- ✅ 完整的测试覆盖
- ✅ 用户文档和API文档

## 🚀 部署方案

### 开发环境部署

#### 本地开发
```bash
# 1. 克隆项目
git clone <repository-url>
cd cs146s-learning-platform

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 环境变量配置
cp .env.example .env
# 编辑 .env 文件，配置数据库和API密钥

# 5. 数据库初始化
flask db upgrade
python data/seed_data.py

# 6. 启动开发服务器
flask run
```

#### Flask开发服务器
```python
# run.py - 开发环境启动脚本
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
```

### 生产环境部署

#### 系统要求
- **操作系统**：Ubuntu 18.04+ / CentOS 7+ / macOS 10.15+
- **Python版本**：3.8+
- **内存**：至少2GB RAM
- **磁盘空间**：至少5GB可用空间
- **网络**：稳定的网络连接

#### 生产环境依赖
```txt
# requirements.txt (生产环境额外依赖)
Flask==2.3.3
gunicorn==21.2.0
gevent==23.9.1
Werkzeug==2.3.7
# ... 其他依赖
```

#### Gunicorn配置
```python
# gunicorn.conf.py
import multiprocessing

# 服务器配置
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 超时配置
timeout = 30
keepalive = 10

# 日志配置
loglevel = "info"
accesslog = "/var/log/cs146s/access.log"
errorlog = "/var/log/cs146s/error.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程配置
user = "cs146s"
group = "cs146s"
tmp_upload_dir = "/tmp"
```

#### Flask生产应用配置
```python
# run.py - 生产环境启动脚本
import os
from app import create_app

app = create_app('production')

if __name__ == '__main__':
    # 生产环境使用Gunicorn启动，不直接运行此脚本
    print("请使用 'gunicorn -c gunicorn.conf.py run:app' 启动应用")
```

#### Nginx配置
```nginx
# nginx.conf
upstream flask_app {
    server app:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # SSL配置 (生产环境)
    # listen 443 ssl;
    # ssl_certificate /etc/ssl/certs/cert.pem;
    # ssl_certificate_key /etc/ssl/certs/key.pem;

    # 静态文件
    location /static {
        alias /app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API路由
    location /api {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 主应用
    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket支持 (如果需要)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### 部署脚本
```bash
# deploy.sh
#!/bin/bash

# Flask + Gunicorn 部署脚本
set -e

echo "🚀 开始部署 CS146S 在线学习平台..."

# 检查Python版本
python3 --version

# 创建虚拟环境
echo "📦 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 创建日志目录
echo "📁 创建日志目录..."
sudo mkdir -p /var/log/cs146s
sudo chown $USER:$USER /var/log/cs146s

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p data
mkdir -p instance

# 环境配置
echo "⚙️ 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库和API密钥"
    exit 1
fi

# 数据库初始化
echo "🗄️ 初始化数据库..."
export FLASK_APP=run.py
flask db upgrade
python data/seed_data.py

# 启动应用
echo "⚡ 启动Flask应用..."
gunicorn -c gunicorn.conf.py run:app --daemon

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 健康检查
echo "🏥 运行健康检查..."
curl -f http://localhost:8000/api/health || (echo "❌ 健康检查失败" && exit 1)

echo "✅ 部署成功！"
echo "🌐 Flask应用已启动在: http://localhost:8000"
echo "🔗 API接口地址: http://localhost:8000/api/v1/"
```

#### Systemd服务配置
```ini
# /etc/systemd/system/cs146s.service
[Unit]
Description=CS146S Online Learning Platform
After=network.target

[Service]
User=cs146s
Group=cs146s
WorkingDirectory=/path/to/cs146s-learning-platform
Environment="PATH=/path/to/cs146s-learning-platform/venv/bin"
ExecStart=/path/to/cs146s-learning-platform/venv/bin/gunicorn -c gunicorn.conf.py run:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### 启动服务
```bash
# 重新加载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start cs146s

# 设置开机自启
sudo systemctl enable cs146s

# 查看服务状态
sudo systemctl status cs146s

# 查看日志
sudo journalctl -u cs146s -f
```

### 监控和维护

#### 应用监控
```python
# app/utils/monitoring.py
from flask import Flask, g
import time
import psutil
from functools import wraps

def monitor_performance(f):
    """性能监控装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        try:
            result = f(*args, **kwargs)
            execution_time = time.time() - start_time

            # 记录性能指标
            log_performance_metrics(
                endpoint=request.endpoint,
                method=request.method,
                execution_time=execution_time,
                status_code=getattr(result, 'status_code', 200) if hasattr(result, 'status_code') else 200
            )

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            log_error_metrics(
                endpoint=request.endpoint,
                method=request.method,
                execution_time=execution_time,
                error=str(e)
            )
            raise

    return decorated_function

def log_performance_metrics(endpoint, method, execution_time, status_code):
    """记录性能指标"""
    # 这里可以集成监控服务，如 Prometheus, DataDog等
    print(f"[PERF] {method} {endpoint} - {execution_time:.3f}s - {status_code}")

def log_error_metrics(endpoint, method, execution_time, error):
    """记录错误指标"""
    print(f"[ERROR] {method} {endpoint} - {execution_time:.3f}s - {error}")

def get_system_metrics():
    """获取系统指标"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_connections': len(psutil.net_connections())
    }
```

#### 日志配置
```python
# app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app: Flask):
    """配置日志"""
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

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('CS146S Learning Platform startup')
```

## 📊 风险评估与应对策略

### 技术风险

#### 1. 代码执行安全风险
**风险等级**: 高
**描述**: 用户提交的代码可能包含恶意操作
**应对策略**:
- ✅ 实现多层安全检查 (静态分析 + AST分析 + 运行时限制)
- ✅ 使用资源限制 (CPU时间、内存、文件访问)
- ✅ 沙箱环境执行 (Docker容器隔离)
- ✅ 定期安全审计和渗透测试

#### 2. 性能扩展风险
**风险等级**: 中
**描述**: 单体应用在高并发下的性能问题
**应对策略**:
- ✅ 实现缓存机制 (Redis缓存热点数据)
- ✅ 数据库查询优化 (索引 + 分页)
- ✅ 异步任务处理 (Celery处理代码执行)
- ✅ 监控性能指标，及时扩展

#### 3. AI服务依赖风险
**风险等级**: 中
**描述**: 外部AI服务不可用或API变更
**应对策略**:
- ✅ 实现重试机制和降级策略
- ✅ 支持多个AI服务提供商
- ✅ 本地缓存常用AI响应
- ✅ 定期检查API兼容性

### 业务风险

#### 1. 用户接受度风险
**风险等级**: 中
**描述**: 学生可能不习惯在线学习模式
**应对策略**:
- ✅ 小范围试点测试，收集反馈
- ✅ 提供详细的使用教程和帮助文档
- ✅ 设计直观的用户界面
- ✅ 与教师密切合作，获取专业建议

#### 2. 内容质量风险
**风险等级**: 中
**描述**: 练习题目和教学内容质量不足
**应对策略**:
- ✅ 邀请CS146S教师参与内容审核
- ✅ 建立内容迭代机制
- ✅ 收集学生反馈，不断改进
- ✅ 参考其他优秀在线学习平台

### 运营风险

#### 1. 数据安全风险
**风险等级**: 高
**描述**: 用户数据泄露或丢失
**应对策略**:
- ✅ 数据加密存储 (密码哈希 + 敏感数据加密)
- ✅ 定期数据备份
- ✅ 访问控制和审计日志
- ✅ 符合GDPR等隐私法规要求

#### 2. 系统可用性风险
**风险等级**: 中
**描述**: 系统宕机影响教学进度
**应对策略**:
- ✅ 实施高可用部署 (负载均衡 + 多实例)
- ✅ 完善的监控和告警系统
- ✅ 灾难恢复计划
- ✅ 定期维护和更新

## 📈 成功指标

### 用户指标
- **注册用户数**: 目标 200+ 学生用户
- **活跃用户率**: 70%+ 周活跃用户
- **练习完成率**: 80%+ 练习提交率
- **用户留存率**: 60%+ 月留存率

### 技术指标
- **系统可用性**: 99.5%+ uptime
- **响应时间**: API响应 < 500ms, 页面加载 < 2s
- **错误率**: < 1% 请求错误率
- **代码执行成功率**: 95%+ 正常代码执行成功

### 教学指标
- **学习进度**: 平均每周学习进度 > 20%
- **练习通过率**: 75%+ 练习首次通过率
- **AI助手使用率**: 60%+ 用户使用AI助手
- **学生满意度**: > 4.0/5.0 平均评分

## 📚 文档和培训

### 技术文档
- **API文档**: 使用OpenAPI/Swagger自动生成
- **部署文档**: 详细的部署和维护指南
- **开发文档**: 代码规范和开发流程
- **安全文档**: 安全策略和应急响应

### 用户文档
- **学生手册**: 平台使用指南
- **教师手册**: 内容管理和学生管理
- **FAQ**: 常见问题解答
- **视频教程**: 使用演示视频

### 培训计划
- **开发者培训**: 代码规范和开发流程培训
- **运维培训**: 系统部署和维护培训
- **教师培训**: 平台功能和内容管理培训
- **学生培训**: 平台使用和学习方法培训

---

**总结**: 这个技术开发方案基于现有方案设计，提供了完整的在线学习平台实现路径。通过14周的开发周期，我们将构建一个功能完整、安全可靠、易于维护的现代化在线学习平台。方案采用轻量级架构，确保快速部署和迭代，同时保证了系统的可扩展性和安全性。
