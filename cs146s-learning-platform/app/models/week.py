from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class Week(db.Model):
    """周学习模块模型"""
    __tablename__ = 'weeks'

    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer, unique=True, nullable=False)  # 1-8
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content_path = db.Column(db.String(500))  # Markdown文档路径
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    exercises = db.relationship('Exercise', backref='week', lazy=True)
    progress = db.relationship('UserProgress', backref='week', lazy=True)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'week_number': self.week_number,
            'title': self.title,
            'description': self.description,
            'content_path': self.content_path,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
