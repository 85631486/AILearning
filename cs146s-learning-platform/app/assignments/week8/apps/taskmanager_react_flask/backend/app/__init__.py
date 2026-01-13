"""
TaskManager Flask后端应用
任务管理系统API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 初始化扩展
db = SQLAlchemy()

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化扩展
    db.init_app(app)
    CORS(app)

    # 注册路由
    register_routes(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app

def register_routes(app):
    """注册API路由"""

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'TaskManager API'
        })

    # 任务路由
    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        """获取所有任务"""
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks])

    @app.route('/api/tasks', methods=['POST'])
    def create_task():
        """创建新任务"""
        data = request.get_json()

        if not data or 'title' not in data:
            return jsonify({'error': 'Task title is required'}), 400

        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date')
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify(new_task.to_dict()), 201

    @app.route('/api/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """获取特定任务"""
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict())

    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """更新任务"""
        task = Task.query.get_or_404(task_id)
        data = request.get_json()

        # 更新字段
        for field in ['title', 'description', 'status', 'priority', 'due_date']:
            if field in data:
                setattr(task, field, data[field])

        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(task.to_dict())

    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """删除任务"""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return '', 204

    # 用户路由
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """获取所有用户"""
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    @app.route('/api/users', methods=['POST'])
    def create_user():
        """创建新用户"""
        data = request.get_json()

        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400

        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 409

        new_user = User(
            name=data['name'],
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201

    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """获取特定用户"""
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @app.route('/api/users/<int:user_id>/tasks', methods=['GET'])
    def get_user_tasks(user_id):
        """获取用户的任务"""
        user = User.query.get_or_404(user_id)
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks])


# 数据库模型
class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    tasks = db.relationship('Task', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Task(db.Model):
    """任务模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
