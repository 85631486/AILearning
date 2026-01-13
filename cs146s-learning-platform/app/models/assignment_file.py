from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

class AssignmentFile(db.Model):
    """作业文件模型"""
    __tablename__ = 'assignment_files'

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # 相对于作业根目录的路径
    file_type = db.Column(db.String(50), nullable=False)  # 'source', 'test', 'data', 'docs'
    content = db.Column(db.Text, nullable=False)          # 文件内容
    is_template = db.Column(db.Boolean, default=True)     # 是否为模板文件
    is_editable = db.Column(db.Boolean, default=True)     # 用户是否可以编辑
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联关系
    exercise = db.relationship('Exercise', backref='assignment_file_objects', lazy=True)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'exercise_id': self.exercise_id,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'content': self.content,
            'is_template': self.is_template,
            'is_editable': self.is_editable,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
