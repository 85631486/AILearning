"""测试练习服务"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.exercise_service import ExerciseService
from app.models import Exercise, Submission, UserProgress

@pytest.mark.unit
@pytest.mark.service
class TestExerciseService:
    """练习服务测试"""

    def setup_method(self):
        """测试前准备"""
        self.service = ExerciseService()

    def teardown_method(self):
        """测试后清理"""
        pass

    @patch('app.models.Exercise.query')
    def test_get_exercises_basic(self, mock_query):
        """测试获取练习列表（基本情况）"""
        # 模拟练习数据
        mock_exercise1 = MagicMock()
        mock_exercise1.to_dict.return_value = {'id': 1, 'title': 'Exercise 1'}
        mock_exercise2 = MagicMock()
        mock_exercise2.to_dict.return_value = {'id': 2, 'title': 'Exercise 2'}

        # 模拟分页
        mock_paginate = MagicMock()
        mock_paginate.items = [mock_exercise1, mock_exercise2]
        mock_paginate.page = 1
        mock_paginate.per_page = 20
        mock_paginate.total = 2
        mock_paginate.pages = 1
        mock_paginate.has_next = False
        mock_paginate.has_prev = False

        mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_paginate

        result = self.service.get_exercises()

        assert 'exercises' in result
        assert 'pagination' in result
        assert len(result['exercises']) == 2
        assert result['pagination']['total'] == 2

    @patch('app.models.Exercise.query')
    def test_get_exercises_with_filters(self, mock_query):
        """测试带过滤器的练习列表"""
        mock_paginate = MagicMock()
        mock_paginate.items = []
        mock_paginate.page = 1
        mock_paginate.per_page = 20
        mock_paginate.total = 0
        mock_paginate.pages = 0
        mock_paginate.has_next = False
        mock_paginate.has_prev = False

        mock_query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_paginate

        result = self.service.get_exercises(
            week_id=1,
            exercise_type='code',
            difficulty='beginner',
            page=2,
            per_page=10
        )

        # 验证过滤器被正确应用
        filter_calls = mock_query.filter_by.call_args_list
        assert any(call[1]['week_id'] == 1 for call in filter_calls)
        assert any(call[1]['exercise_type'] == 'code' for call in filter_calls)
        assert any(call[1]['difficulty'] == 'beginner' for call in filter_calls)

        # 验证分页参数
        paginate_call = mock_query.filter_by.return_value.order_by.return_value.paginate
        paginate_call.assert_called_with(page=2, per_page=10, error_out=False)

    @patch('app.models.Exercise.query')
    def test_get_exercises_error_handling(self, mock_query):
        """测试获取练习列表的错误处理"""
        mock_query.filter_by.side_effect = Exception("DB error")

        result = self.service.get_exercises()

        # 应该返回空结果而不是抛出异常
        assert result['exercises'] == []
        assert result['pagination']['total'] == 0

    @patch('app.models.Exercise.query')
    def test_get_exercise_by_id_success(self, mock_query):
        """测试成功获取练习详情"""
        mock_exercise = MagicMock()
        mock_exercise.is_active = True
        mock_query.filter_by.return_value.first.return_value = mock_exercise

        result = self.service.get_exercise_by_id(1)

        assert result == mock_exercise
        mock_query.filter_by.assert_called_with(id=1, is_active=True)

    @patch('app.models.Exercise.query')
    def test_get_exercise_by_id_not_found(self, mock_query):
        """测试练习不存在的情况"""
        mock_query.filter_by.return_value.first.return_value = None

        result = self.service.get_exercise_by_id(999)

        assert result is None

    @patch('app.models.Exercise.query')
    def test_get_exercise_by_id_error(self, mock_query):
        """测试获取练习时的错误处理"""
        mock_query.filter_by.side_effect = Exception("DB error")

        result = self.service.get_exercise_by_id(1)

        assert result is None

    @patch('app.services.code_executor.SecureCodeExecutor')
    @patch('app.models.Submission')
    @patch('app.models.db')
    def test_submit_exercise_success(self, mock_db, mock_submission_class, mock_executor):
        """测试成功提交练习"""
        # 模拟练习
        mock_exercise = MagicMock()
        mock_exercise.id = 1
        mock_exercise.points = 10

        # 模拟代码执行
        mock_executor.return_value.execute_code.return_value = {
            'success': True,
            'stdout': 'Hello World',
            'stderr': '',
            'execution_time': 0.5
        }

        # 模拟测试运行
        with patch.object(self.service, '_run_tests') as mock_run_tests:
            mock_run_tests.return_value = {'passed': 1, 'total': 1, 'results': []}

        with patch.object(self.service, '_calculate_score') as mock_calc_score:
            mock_calc_score.return_value = 8.5

        with patch.object(self.service, '_update_user_progress') as mock_update_progress:
            mock_update_progress.return_value = None

        # 模拟数据库提交
        mock_submission = MagicMock()
        mock_submission.to_dict.return_value = {'id': 1, 'score': 8.5}
        mock_submission.is_correct = True
        mock_submission_class.return_value = mock_submission

        with patch.object(self.service, 'get_exercise_by_id', return_value=mock_exercise):
            result = self.service.submit_exercise(
                user_id=1,
                exercise_id=1,
                code="print('Hello World')",
                attempt_number=1
            )

        assert result['success'] == True
        assert result['score'] == 8.5
        assert result['is_correct'] == True

        # 验证数据库操作
        mock_db.session.add.assert_called_once_with(mock_submission)
        mock_db.session.commit.assert_called_once()

    @patch('app.services.code_executor.SecureCodeExecutor')
    def test_submit_exercise_exercise_not_found(self, mock_executor):
        """测试提交不存在的练习"""
        with patch.object(self.service, 'get_exercise_by_id', return_value=None):
            result = self.service.submit_exercise(1, 999, "code", 1)

        assert result['success'] == False
        assert '练习不存在' in result['message']
        mock_executor.return_value.execute_code.assert_not_called()

    @patch('app.services.code_executor.SecureCodeExecutor')
    @patch('app.models.db')
    def test_submit_exercise_execution_failure(self, mock_db, mock_executor):
        """测试代码执行失败的情况"""
        mock_exercise = MagicMock()
        mock_exercise.id = 1

        mock_executor.return_value.execute_code.return_value = {
            'success': False,
            'error': 'Syntax error'
        }

        with patch.object(self.service, 'get_exercise_by_id', return_value=mock_exercise):
            result = self.service.submit_exercise(1, 1, "invalid code", 1)

        assert result['success'] == False
        mock_db.session.rollback.assert_called_once()

    def test_run_tests_with_test_code(self):
        """测试有测试代码的情况"""
        mock_exercise = MagicMock()
        mock_exercise.test_code = "assert result == 42"

        execution_result = {'success': True, 'stdout': '42'}

        result = self.service._run_tests(mock_exercise, execution_result)

        # 简单实现应该返回基本结果
        assert 'passed' in result
        assert 'total' in result
        assert 'results' in result

    def test_run_tests_without_test_code(self):
        """测试无测试代码的情况"""
        mock_exercise = MagicMock()
        mock_exercise.test_code = None

        execution_result = {'success': True}

        result = self.service._run_tests(mock_exercise, execution_result)

        assert result['passed'] == 0
        assert result['total'] == 0
        assert result['results'] == []

    def test_calculate_score_valid(self):
        """测试有效分数计算"""
        test_results = {'passed': 2, 'total': 3}
        score = self.service._calculate_score(test_results)

        expected_score = round((2/3) * 10, 2)
        assert score == expected_score

    def test_calculate_score_edge_cases(self):
        """测试分数计算的边界情况"""
        # 全对
        assert self.service._calculate_score({'passed': 5, 'total': 5}) == 10.0
        # 全错
        assert self.service._calculate_score({'passed': 0, 'total': 5}) == 0.0
        # 空结果
        assert self.service._calculate_score({}) == 0.0
        # 无总数
        assert self.service._calculate_score({'passed': 1}) == 0.0

    @patch('app.models.Submission.query')
    def test_get_user_submissions(self, mock_query):
        """测试获取用户提交历史"""
        mock_submission1 = MagicMock()
        mock_submission1.to_dict.return_value = {'id': 1, 'score': 8.0}
        mock_submission2 = MagicMock()
        mock_submission2.to_dict.return_value = {'id': 2, 'score': 9.0}

        mock_query.filter_by.return_value.order_by.return_value.all.return_value = [
            mock_submission1, mock_submission2
        ]

        result = self.service.get_user_submissions(1, 1)

        assert len(result) == 2
        assert result[0]['score'] == 8.0
        assert result[1]['score'] == 9.0

    @patch('app.models.Submission.query')
    def test_get_user_submissions_empty(self, mock_query):
        """测试空提交历史"""
        mock_query.filter_by.return_value.order_by.return_value.all.return_value = []

        result = self.service.get_user_submissions(1, 1)

        assert result == []

    @patch('app.models.Submission.query')
    @patch('app.models.db.session')
    def test_get_leaderboard(self, mock_session, mock_query):
        """测试获取排行榜"""
        # 模拟复杂的排行榜查询结果
        mock_result = MagicMock()
        mock_result.user_id = 1
        mock_result.username = 'testuser'
        mock_result.total_score = 85.5
        mock_result.total_submissions = 10
        mock_result.correct_submissions = 8

        mock_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [
            mock_result
        ]

        result = self.service.get_leaderboard(limit=5)

        assert len(result) == 1
        assert result[0]['user_id'] == 1
        assert result[0]['username'] == 'testuser'
        assert result[0]['total_score'] == 85.5
        assert result[0]['accuracy_rate'] == 80.0

    @patch('app.models.Submission.query')
    @patch('app.models.db.session')
    def test_get_leaderboard_empty(self, mock_session, mock_query):
        """测试空排行榜"""
        mock_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = []

        result = self.service.get_leaderboard()

        assert result == []

    @patch('app.models.UserProgress')
    @patch('app.models.Exercise.query')
    @patch('app.models.Submission.query')
    @patch('app.models.db')
    def test_update_user_progress(self, mock_db, mock_submission_query, mock_exercise_query, mock_progress_class):
        """测试更新用户进度"""
        # 模拟现有进度
        mock_progress = MagicMock()
        mock_progress.completed_exercises = 2
        mock_progress.total_exercises = 5
        mock_progress.time_spent = 100
        mock_progress.status = 'in_progress'

        mock_progress_class.query.filter_by.return_value.first.return_value = mock_progress

        # 模拟练习计数
        mock_submission_query.join.return_value.filter.return_value.distinct.return_value.count.return_value = 3
        mock_exercise_query.filter_by.return_value.count.return_value = 5

        self.service._update_user_progress(1, 1)

        # 验证进度更新
        assert mock_progress.completed_exercises == 3
        assert mock_progress.total_exercises == 5
        assert mock_progress.progress_percentage == 60.0  # 3/5 * 100

        mock_db.session.commit.assert_called_once()

    def test_service_initialization(self):
        """测试服务初始化"""
        service = ExerciseService()
        assert hasattr(service, 'code_executor')
        assert service.code_executor is not None

    def test_method_error_handling(self):
        """测试方法错误处理"""
        # 测试_run_tests的错误处理
        with patch.object(self.service, '_run_tests') as mock_run_tests:
            mock_run_tests.side_effect = Exception("Test error")

            result = self.service._run_tests(MagicMock(), {})
            assert result['passed'] == 0

        # 测试_calculate_score的错误处理
        with patch.object(self.service, '_calculate_score') as mock_calc:
            mock_calc.side_effect = Exception("Calc error")

            result = self.service._calculate_score({})
            assert result == 0.0
