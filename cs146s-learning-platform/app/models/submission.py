from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class Submission(db.Model):
    """用户提交记录模型"""
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    submitted_code = db.Column(db.Text, nullable=False)
    execution_result = db.Column(db.Text)  # JSON格式的执行结果
    test_results = db.Column(db.Text)      # JSON格式的测试结果
    score = db.Column(db.Numeric(5, 2))
    is_correct = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='submitted')  # 'submitted', 'running', 'completed', 'failed'
    execution_time = db.Column(db.Numeric(5, 2))  # 执行时间(秒)
    memory_usage = db.Column(db.Integer)    # 内存使用(KB)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts_count = db.Column(db.Integer, default=1)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exercise_id': self.exercise_id,
            'submitted_code': self.submitted_code,
            'execution_result': self.execution_result,
            'test_results': self.test_results,
            'score': float(self.score) if self.score else None,
            'is_correct': self.is_correct,
            'status': self.status,
            'execution_time': float(self.execution_time) if self.execution_time else None,
            'memory_usage': self.memory_usage,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'attempts_count': self.attempts_count
        }
