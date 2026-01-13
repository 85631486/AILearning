from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class AutoSave(db.Model):
    """自动保存模型"""
    __tablename__ = 'autosaves'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    metadata_json = db.Column(db.Text)  # JSON格式的元数据（光标位置等）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    user = db.relationship('User', backref='autosaves', lazy=True)
    exercise = db.relationship('Exercise', backref='autosaves', lazy=True)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exercise_id': self.exercise_id,
            'code': self.code,
            'metadata': self.metadata_json,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
