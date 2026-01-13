from flask import current_app
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from app.models import User
from app import db

class AuthService:
    """用户认证服务"""

    def register_user(self, username: str, email: str, password: str) -> dict:
        """注册新用户"""
        try:
            # 检查用户名是否已存在
            if User.query.filter_by(username=username).first():
                return {
                    'success': False,
                    'message': '用户名已存在'
                }

            # 检查邮箱是否已存在
            if User.query.filter_by(email=email).first():
                return {
                    'success': False,
                    'message': '邮箱已被注册'
                }

            # 创建新用户
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return {
                'success': True,
                'message': '注册成功',
                'user': user.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'用户注册失败: {str(e)}')
            return {
                'success': False,
                'message': '注册失败，请稍后重试'
            }

    def authenticate_user(self, email: str, password: str) -> dict:
        """用户认证"""
        try:
            user = User.query.filter_by(email=email).first()

            if not user:
                return {
                    'success': False,
                    'message': '邮箱或密码错误'
                }

            if not user.check_password(password):
                return {
                    'success': False,
                    'message': '邮箱或密码错误'
                }

            if not user.is_active:
                return {
                    'success': False,
                    'message': '账户已被禁用'
                }

            # 更新登录信息
            user.last_login = datetime.utcnow()
            user.login_count += 1
            db.session.commit()

            # 登录用户
            login_user(user)

            return {
                'success': True,
                'message': '登录成功',
                'user': user.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'用户认证失败: {str(e)}')
            return {
                'success': False,
                'message': '登录失败，请稍后重试'
            }

    def logout_user(self):
        """用户登出"""
        try:
            logout_user()
            return {
                'success': True,
                'message': '登出成功'
            }
        except Exception as e:
            current_app.logger.error(f'用户登出失败: {str(e)}')
            return {
                'success': False,
                'message': '登出失败'
            }

    def get_current_user(self):
        """获取当前用户信息"""
        if current_user.is_authenticated:
            return current_user
        return None

    def update_user_profile(self, user_id: int, data: dict) -> dict:
        """更新用户资料"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }

            # 更新允许的字段
            allowed_fields = ['avatar', 'bio']
            for field in allowed_fields:
                if field in data:
                    setattr(user, field, data[field])

            db.session.commit()

            return {
                'success': True,
                'message': '资料更新成功',
                'user': user.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'更新用户资料失败: {str(e)}')
            return {
                'success': False,
                'message': '更新失败，请稍后重试'
            }

    def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """修改密码"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {
                    'success': False,
                    'message': '用户不存在'
                }

            if not user.check_password(old_password):
                return {
                    'success': False,
                    'message': '原密码错误'
                }

            user.set_password(new_password)
            db.session.commit()

            return {
                'success': True,
                'message': '密码修改成功'
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'修改密码失败: {str(e)}')
            return {
                'success': False,
                'message': '修改失败，请稍后重试'
            }
