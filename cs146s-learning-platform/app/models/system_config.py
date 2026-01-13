from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class SystemConfig(db.Model):
    """系统配置模型"""
    __tablename__ = 'system_config'

    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False)
    config_value = db.Column(db.Text)
    config_type = db.Column(db.String(50), default='string')  # 'string', 'int', 'float', 'bool', 'json'
    description = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=False)  # 是否公开配置
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'config_type': self.config_type,
            'description': self.description,
            'is_public': self.is_public,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by
        }
