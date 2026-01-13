from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class UserProgress(db.Model):
    """学习进度模型"""
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey('weeks.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started')  # 'not_started', 'in_progress', 'completed'
    completed_exercises = db.Column(db.Integer, default=0)
    total_exercises = db.Column(db.Integer, default=0)
    current_exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, default=0)  # 总学习时长(秒)
    progress_percentage = db.Column(db.Numeric(5, 2), default=0.00)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'week_id': self.week_id,
            'status': self.status,
            'completed_exercises': self.completed_exercises,
            'total_exercises': self.total_exercises,
            'current_exercise_id': self.current_exercise_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'time_spent': self.time_spent,
            'progress_percentage': float(self.progress_percentage) if self.progress_percentage else 0.0
        }
