"""集成测试"""

import pytest
from app import create_app, db
from app.models import User, Week, Exercise, Submission
from app.services.exercise_service import ExerciseService
from app.services.ai_assistant import AIAssistant

@pytest.mark.integration
class TestIntegration:
    """集成测试"""

    def setup_method(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # 创建测试用户
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)

        # 创建测试周
        self.week = Week(
            week_number=1,
            title='测试周',
            description='用于测试的周',
            content_path='week1/README.md'
        )
        db.session.add(self.week)

        # 创建测试练习
        self.exercise = Exercise(
            week_id=1,
            title='测试练习',
            description='用于测试的练习',
            exercise_type='code',
            difficulty='beginner',
            initial_code='print("Hello World")',
            test_code='# 测试代码',
            points=10
        )
        db.session.add(self.exercise)

        db.session.commit()

    def teardown_method(self):
        """测试后清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_complete_exercise_workflow(self):
        """测试完整的练习工作流"""
        with self.app.test_client() as client:
            # 1. 用户登录
            login_response = client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })
            assert login_response.status_code == 200
            login_data = login_response.get_json()
            assert login_data['success'] == True

            # 2. 获取练习列表
            exercises_response = client.get('/api/v1/exercises')
            assert exercises_response.status_code == 200
            exercises_data = exercises_response.get_json()
            assert exercises_data['success'] == True
            assert len(exercises_data['exercises']) > 0

            # 3. 获取练习详情
            exercise_response = client.get(f'/api/v1/exercises/{self.exercise.id}')
            assert exercise_response.status_code == 200
            exercise_data = exercise_response.get_json()
            assert exercise_data['success'] == True
            assert exercise_data['exercise']['title'] == '测试练习'

            # 4. 执行代码
            execute_response = client.post(f'/api/v1/exercises/{self.exercise.id}/execute', json={
                'code': 'print("Test execution")'
            })
            assert execute_response.status_code == 200
            execute_data = execute_response.get_json()
            assert execute_data['success'] == True
            assert 'result' in execute_data

            # 5. 提交练习答案
            submit_response = client.post(f'/api/v1/exercises/{self.exercise.id}/submit', json={
                'code': 'print("Test submission")',
                'attempt_number': 1
            })
            assert submit_response.status_code == 201
            submit_data = submit_response.get_json()
            assert submit_data['success'] == True
            assert 'submission' in submit_data

            # 6. 获取提交历史
            submissions_response = client.get(f'/api/v1/exercises/{self.exercise.id}/submissions')
            assert submissions_response.status_code == 200
            submissions_data = submissions_response.get_json()
            assert submissions_data['success'] == True
            assert len(submissions_data['submissions']) == 1

            # 7. 获取排行榜
            leaderboard_response = client.get(f'/api/v1/exercises/{self.exercise.id}/leaderboard')
            assert leaderboard_response.status_code == 200
            leaderboard_data = leaderboard_response.get_json()
            assert leaderboard_data['success'] == True
            assert 'leaderboard' in leaderboard_data

    def test_ai_assistant_integration(self):
        """测试AI助手集成"""
        with self.app.test_client() as client:
            # 登录
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            # 测试AI对话（应该使用mock客户端）
            chat_response = client.post('/api/v1/ai/chat', json={
                'message': '解释Python中的print函数',
                'context': {'type': 'explain'}
            })
            assert chat_response.status_code == 200
            chat_data = chat_response.get_json()
            assert chat_data['success'] == True
            assert 'response' in chat_data

            # 测试代码解释
            explain_response = client.post('/api/v1/ai/explain', json={
                'code': 'print("hello")',
                'language': 'python'
            })
            assert explain_response.status_code == 200
            explain_data = explain_response.get_json()
            assert explain_data['success'] == True

            # 测试代码调试
            debug_response = client.post('/api/v1/ai/debug', json={
                'code': 'print("hello"',
                'error': 'SyntaxError: EOL while scanning string literal'
            })
            assert debug_response.status_code == 200
            debug_data = debug_response.get_json()
            assert debug_data['success'] == True

            # 测试学习指导
            guidance_response = client.post('/api/v1/ai/guidance', json={
                'week': 1,
                'progress': 50.0
            })
            assert guidance_response.status_code == 200
            guidance_data = guidance_response.get_json()
            assert guidance_data['success'] == True

            # 测试获取提示
            hint_response = client.post('/api/v1/ai/hint', json={
                'exercise_id': self.exercise.id,
                'current_code': 'print("incomplete")',
                'progress': 'stuck'
            })
            assert hint_response.status_code == 200
            hint_data = hint_response.get_json()
            assert hint_data['success'] == True

    def test_progress_tracking_integration(self):
        """测试进度追踪集成"""
        with self.app.test_client() as client:
            # 登录
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            # 获取进度
            progress_response = client.get('/api/v1/learning/progress')
            assert progress_response.status_code == 200
            progress_data = progress_response.get_json()
            assert progress_data['success'] == True

            # 获取周进度
            week_progress_response = client.get('/api/v1/learning/progress/1')
            assert week_progress_response.status_code == 200
            week_progress_data = week_progress_response.get_json()
            assert week_progress_data['success'] == True

            # 更新进度
            update_response = client.put('/api/v1/learning/progress/1', json={
                'time_spent': 30,
                'current_exercise_id': self.exercise.id
            })
            assert update_response.status_code == 200
            update_data = update_response.get_json()
            assert update_data['success'] == True

            # 获取统计
            stats_response = client.get('/api/v1/learning/stats')
            assert stats_response.status_code == 200
            stats_data = stats_response.get_json()
            assert stats_data['success'] == True

    def test_error_handling_integration(self):
        """测试错误处理集成"""
        with self.app.test_client() as client:
            # 未登录访问需要认证的端点
            execute_response = client.post('/api/v1/exercises/1/execute', json={
                'code': 'print("test")'
            })
            # 应该返回401或重定向到登录页
            assert execute_response.status_code in [401, 302]

            # 登录后测试无效输入
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            # 测试无效练习ID
            invalid_exercise_response = client.post('/api/v1/exercises/999/execute', json={
                'code': 'print("test")'
            })
            assert invalid_exercise_response.status_code == 404

            # 测试空代码
            empty_code_response = client.post(f'/api/v1/exercises/{self.exercise.id}/execute', json={
                'code': ''
            })
            assert empty_code_response.status_code == 400

    def test_cross_service_integration(self):
        """测试跨服务集成"""
        with self.app.test_client() as client:
            # 登录
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            # 执行代码
            client.post(f'/api/v1/exercises/{self.exercise.id}/execute', json={
                'code': 'print("integration test")'
            })

            # 提交练习
            submit_response = client.post(f'/api/v1/exercises/{self.exercise.id}/submit', json={
                'code': 'print("integration test")',
                'attempt_number': 1
            })
            assert submit_response.status_code == 201

            # 检查进度是否更新
            progress_response = client.get('/api/v1/learning/progress/1')
            progress_data = progress_response.get_json()
            assert progress_data['success'] == True

            # 检查提交历史
            submissions_response = client.get(f'/api/v1/exercises/{self.exercise.id}/submissions')
            submissions_data = submissions_response.get_json()
            assert submissions_data['success'] == True
            assert len(submissions_data['submissions']) == 1

    def test_data_consistency_integration(self):
        """测试数据一致性集成"""
        with self.app.test_client() as client:
            # 登录
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            # 多次提交，检查数据一致性
            for i in range(3):
                submit_response = client.post(f'/api/v1/exercises/{self.exercise.id}/submit', json={
                    'code': f'print("attempt {i+1}")',
                    'attempt_number': i + 1
                })
                assert submit_response.status_code == 201

            # 检查提交历史数量
            submissions_response = client.get(f'/api/v1/exercises/{self.exercise.id}/submissions')
            submissions_data = submissions_response.get_json()
            assert len(submissions_data['submissions']) == 3

            # 检查数据库中的记录数
            submission_count = Submission.query.filter_by(
                user_id=self.user.id,
                exercise_id=self.exercise.id
            ).count()
            assert submission_count == 3

    def test_api_response_format_consistency(self):
        """测试API响应格式一致性"""
        with self.app.test_client() as client:
            # 登录
            client.post('/api/v1/auth/login', json={
                'email': 'test@example.com',
                'password': 'password123'
            })

            endpoints_to_test = [
                ('GET', '/api/v1/exercises'),
                ('GET', f'/api/v1/exercises/{self.exercise.id}'),
                ('GET', '/api/v1/learning/progress'),
                ('GET', '/api/v1/learning/stats'),
                ('POST', '/api/v1/ai/chat', {'message': 'test'}),
            ]

            for method, endpoint, *data in endpoints_to_test:
                if method == 'GET':
                    response = client.get(endpoint)
                else:
                    response = client.post(endpoint, json=data[0] if data else {})

                assert response.status_code in [200, 201, 400, 404]

                if response.status_code < 400:  # 成功响应
                    response_data = response.get_json()
                    assert 'success' in response_data
                    if response_data['success']:
                        # 检查是否有数据字段
                        data_fields = ['exercises', 'exercise', 'progress', 'stats', 'response', 'result']
                        has_data = any(field in response_data for field in data_fields)
                        assert has_data, f"成功响应缺少数据字段: {endpoint}"
