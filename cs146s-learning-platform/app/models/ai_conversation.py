from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class AIConversation(db.Model):
    """AI对话记录模型"""
    __tablename__ = 'ai_conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100))  # 会话ID，用于分组对话
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))  # 可为空，关联具体练习
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), default='chat')  # 'chat', 'explain', 'debug', 'guidance'
    tokens_used = db.Column(db.Integer)  # AI消耗的tokens
    response_time = db.Column(db.Numeric(5, 2))  # 响应时间(秒)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'exercise_id': self.exercise_id,
            'user_message': self.user_message,
            'ai_response': self.ai_response,
            'message_type': self.message_type,
            'tokens_used': self.tokens_used,
            'response_time': float(self.response_time) if self.response_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
