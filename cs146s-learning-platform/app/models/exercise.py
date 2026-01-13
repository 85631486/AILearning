from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class Exercise(db.Model):
    """练习题目模型"""
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    exercise_type = db.Column(db.String(50), nullable=False)  # 'prompt', 'code', 'project'
    difficulty = db.Column(db.String(20), default='beginner')  # 'beginner', 'intermediate', 'advanced'
    initial_code = db.Column(db.Text)  # 初始代码模板
    test_code = db.Column(db.Text)     # 测试代码
    solution_code = db.Column(db.Text) # 参考答案

    # 新增字段支持复杂作业
    assignment_files = db.Column(db.Text)  # 作业文件列表 (JSON)
    test_files = db.Column(db.Text)        # 测试文件列表 (JSON)
    solution_files = db.Column(db.Text)    # 参考答案文件 (JSON)
    dependencies = db.Column(db.Text)      # 依赖包列表 (JSON)
    instructions = db.Column(db.Text)      # 详细说明 (Markdown)
    hints_sequence = db.Column(db.Text)    # 分步提示 (JSON)
    validation_rules = db.Column(db.Text)  # 验证规则 (JSON)

    hints = db.Column(db.Text)         # 提示信息 (JSON格式)
    points = db.Column(db.Integer, default=10)
    time_limit = db.Column(db.Integer, default=30)  # 分钟
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    submissions = db.relationship('Submission', backref='exercise', lazy=True)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'week_id': self.week_id,
            'title': self.title,
            'description': self.description,
            'exercise_type': self.exercise_type,
            'difficulty': self.difficulty,
            'initial_code': self.initial_code,
            'test_code': self.test_code,
            'hints': self.hints,
            'points': self.points,
            'time_limit': self.time_limit,
            'order_index': self.order_index,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
