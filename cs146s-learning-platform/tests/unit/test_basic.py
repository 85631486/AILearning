"""基本功能测试"""

import pytest
from app import create_app, db
from app.models import User, Week

@pytest.mark.unit
class TestBasic:
    """基本功能测试"""

    def setup_method(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown_method(self):
        """测试后清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_creation(self):
        """测试应用创建"""
        assert self.app is not None
        assert self.app.config['TESTING'] == True

    def test_database_creation(self):
        """测试数据库表创建"""
        # 检查表是否创建成功
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        expected_tables = [
            'users', 'weeks', 'exercises', 'submissions',
            'user_progress', 'ai_conversations', 'system_config'
        ]

        for table in expected_tables:
            assert table in tables, f"表 {table} 未创建"

    def test_user_creation(self):
        """测试用户创建"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')

        db.session.add(user)
        db.session.commit()

        # 验证用户创建成功
        saved_user = User.query.filter_by(username='testuser').first()
        assert saved_user is not None
        assert saved_user.username == 'testuser'
        assert saved_user.email == 'test@example.com'
        assert saved_user.check_password('password123')

    def test_week_creation(self):
        """测试周创建"""
        week = Week(
            week_number=1,
            title='测试周',
            description='这是一个测试周',
            content_path='week1/README.md'
        )

        db.session.add(week)
        db.session.commit()

        # 验证周创建成功
        saved_week = Week.query.filter_by(week_number=1).first()
        assert saved_week is not None
        assert saved_week.title == '测试周'
        assert saved_week.week_number == 1

    def test_health_endpoint(self):
        """测试健康检查端点"""
        with self.app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200

            data = response.get_json()
            assert data['status'] == 'ok'
            assert 'service' in data

    def test_homepage(self):
        """测试主页"""
        with self.app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
