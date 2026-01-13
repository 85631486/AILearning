"""测试AI助手"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.ai_assistant import AIAssistant
from app.models import AIConversation


@pytest.mark.unit
class TestAIAssistant:
    """AI助手测试"""

    def setup_method(self):
        """测试前准备"""
        pass

    def teardown_method(self):
        """测试后清理"""
        pass

    @patch('app.utils.llm_client.LLMClientFactory.create_client')
    def test_mock_fallback_when_no_api_key(self, mock_factory, test_app):
        """测试无API密钥时使用mock回退"""
        with test_app.app_context():
            # 模拟无API密钥的情况
            with patch('current_app.config.get') as mock_config:
                mock_config.return_value = None  # 没有QWEN_API_KEY

                mock_client = MagicMock()
                mock_client.chat.return_value = {
                    'content': 'Mock response',
                    'tokens_used': 10,
                    'response_time': 0.1
                }
                mock_factory.return_value = mock_client

            assistant = AIAssistant()
            result = assistant.chat("Test message")

            assert result['success'] == True
            assert result['response'] == 'Mock response'
            assert result['tokens_used'] == 10
            assert result['response_time'] == 0.1

    @patch('app.utils.llm_client.LLMClientFactory.create_client')
    def test_qwen_client_when_api_key_available(self, mock_factory):
        """测试有API密钥时使用Qwen客户端"""
        with patch('current_app.config.get') as mock_config:
            mock_config.side_effect = lambda key: {
                'QWEN_API_KEY': 'test-key',
                'QWEN_BASE_URL': 'https://test.com',
                'QWEN_MODEL': 'qwen-turbo'
            }.get(key)

            mock_client = MagicMock()
            mock_client.chat.return_value = {
                'content': 'Qwen response',
                'tokens_used': 20,
                'response_time': 0.2
            }
            mock_factory.return_value = mock_client

            assistant = AIAssistant()
            result = assistant.chat("Test message")

            assert result['success'] == True
            assert result['response'] == 'Qwen response'

    def test_explain_code_functionality(self):
        """测试代码解释功能"""
        with patch.object(self.assistant, 'chat') as mock_chat:
            mock_chat.return_value = {
                'success': True,
                'response': '这是一个print函数的解释',
                'tokens_used': 15,
                'response_time': 0.1
            }

            result = self.assistant.explain_code("print('hello')", "python")

            assert result['success'] == True
            assert 'print函数' in result['response']

            # 验证chat被正确调用
            mock_chat.assert_called_once()
            call_args = mock_chat.call_args[0]
            assert '解释' in call_args[0]
            assert 'python' in call_args[0]
            assert call_args[1]['type'] == 'explain'

    def test_debug_code_functionality(self):
        """测试代码调试功能"""
        with patch.object(self.assistant, 'chat') as mock_chat:
            mock_chat.return_value = {
                'success': True,
                'response': '这是一个语法错误的修复建议',
                'tokens_used': 18,
                'response_time': 0.15
            }

            result = self.assistant.debug_code("print('hello'", "SyntaxError")

            assert result['success'] == True
            assert '语法错误' in result['response']

            mock_chat.assert_called_once()
            call_args = mock_chat.call_args[0]
            assert '调试' in call_args[0]
            assert 'SyntaxError' in call_args[0]

    def test_learning_guidance_functionality(self):
        """测试学习指导功能"""
        with patch.object(self.assistant, 'chat') as mock_chat:
            mock_chat.return_value = {
                'success': True,
                'response': '这是第1周的学习指导',
                'tokens_used': 22,
                'response_time': 0.18
            }

            result = self.assistant.learning_guidance(1, 75.5)

            assert result['success'] == True
            assert '第1周' in result['response']

            mock_chat.assert_called_once()
            call_args = mock_chat.call_args[0]
            assert '第1周' in call_args[0]
            assert '75.5%' in call_args[0]

    def test_generate_hint_functionality(self):
        """测试生成提示功能"""
        with patch.object(self.assistant, 'chat') as mock_chat:
            mock_chat.return_value = {
                'success': True,
                'response': '提示：试试用循环来解决这个问题',
                'tokens_used': 12,
                'response_time': 0.12
            }

            result = self.assistant.generate_hint(1, "for i in range(10):", "stuck")

            assert result['success'] == True
            assert '循环' in result['response']

            mock_chat.assert_called_once()
            call_args = mock_chat.call_args[0]
            assert '提示' in call_args[0]
            assert 'stuck' in call_args[0]

    @patch('app.models.db.session')
    def test_save_conversation_success(self, mock_session):
        """测试成功保存对话"""
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        result = self.assistant.save_conversation(
            user_id=1,
            user_message="Hello",
            ai_response={'success': True, 'response': 'Hi there'},
            message_type='chat'
        )

        assert result == True
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('app.models.db.session')
    def test_save_conversation_failure(self, mock_session):
        """测试保存对话失败"""
        mock_session.commit.side_effect = Exception("DB error")

        result = self.assistant.save_conversation(
            user_id=1,
            user_message="Hello",
            ai_response={'success': True, 'response': 'Hi there'}
        )

        assert result == False
        mock_session.rollback.assert_called_once()

    @patch('app.models.db.session')
    def test_save_conversation_skip_failed_response(self, mock_session):
        """测试跳过保存失败的响应"""
        result = self.assistant.save_conversation(
            user_id=1,
            user_message="Hello",
            ai_response={'success': False, 'error': 'API failed'}
        )

        assert result == False
        # 不应该调用数据库操作
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()

    @patch('app.models.AIConversation.query')
    def test_get_conversation_history(self, mock_query):
        """测试获取对话历史"""
        # 模拟查询结果
        mock_conversation = MagicMock()
        mock_conversation.to_dict.return_value = {'id': 1, 'message': 'test'}

        mock_query.filter_by.return_value.order_by.return_value.limit.return_value.all.return_value = [
            mock_conversation
        ]

        result = self.assistant.get_conversation_history(user_id=1, limit=10)

        assert len(result) == 1
        assert result[0]['id'] == 1

        mock_query.filter_by.assert_called_with(user_id=1)
        mock_query.filter_by.return_value.order_by.assert_called_once()
        mock_query.filter_by.return_value.order_by.return_value.limit.assert_called_with(10)

    @patch('app.models.AIConversation.query')
    def test_get_conversation_history_with_filters(self, mock_query):
        """测试带过滤器的对话历史"""
        mock_query.filter_by.return_value.filter_by.return_value.order_by.return_value.limit.return_value.all.return_value = []

        result = self.assistant.get_conversation_history(
            user_id=1,
            session_id='session123',
            exercise_id=5,
            limit=20
        )

        assert result == []

        # 验证过滤器被正确应用
        first_filter = mock_query.filter_by
        first_filter.assert_called_with(user_id=1)
        second_filter = first_filter.return_value.filter_by
        second_filter.assert_called_with(session_id='session123')
        third_filter = second_filter.return_value.filter_by
        third_filter.assert_called_with(exercise_id=5)

    def test_build_system_prompt_basic(self):
        """测试构建基础系统提示"""
        prompt = self.assistant._build_system_prompt()
        assert 'AI编程学习助手' in prompt
        assert '耐心、友好的教学态度' in prompt

    def test_build_system_prompt_with_context(self):
        """测试带上下文的系统提示"""
        context = {'type': 'explain', 'language': 'python'}
        prompt = self.assistant._build_system_prompt(context)
        assert 'AI编程学习助手' in prompt
        assert '解释代码' in prompt

    def test_build_system_prompt_different_types(self):
        """测试不同类型的系统提示"""
        test_cases = [
            ({'type': 'debug'}, '调试代码'),
            ({'type': 'guidance'}, '学习指导'),
            ({'type': 'hint'}, '提示'),
            ({'type': 'unknown'}, 'AI编程学习助手')  # 默认情况
        ]

        for context, expected_text in test_cases:
            prompt = self.assistant._build_system_prompt(context)
            assert expected_text in prompt

    @patch('app.models.AIConversation.query')
    @patch('app.models.db.session')
    def test_get_usage_stats(self, mock_session, mock_query):
        """测试获取使用统计"""
        # 模拟聚合查询结果
        mock_stats = MagicMock()
        mock_stats.total_conversations = 10
        mock_stats.total_tokens = 500
        mock_stats.avg_response_time = 0.5

        mock_query.with_entities.return_value.first.return_value = mock_stats

        result = self.assistant.get_usage_stats(user_id=1, days=7)

        assert result['total_conversations'] == 10
        assert result['total_tokens'] == 500
        assert result['avg_response_time'] == 0.5
        assert result['period_days'] == 7

    @patch('app.models.AIConversation.query')
    def test_get_usage_stats_no_data(self, mock_query):
        """测试无数据时的使用统计"""
        mock_query.with_entities.return_value.first.return_value = None

        result = self.assistant.get_usage_stats()

        assert result['total_conversations'] == 0
        assert result['total_tokens'] == 0
        assert result['avg_response_time'] == 0

    @patch('app.models.AIConversation.query')
    def test_get_usage_stats_error_handling(self, mock_query):
        """测试使用统计的错误处理"""
        mock_query.with_entities.side_effect = Exception("DB error")

        result = self.assistant.get_usage_stats()

        assert result['total_conversations'] == 0
        assert result['total_tokens'] == 0
        assert result['avg_response_time'] == 0

    def test_chat_error_handling(self):
        """测试chat方法的错误处理"""
        with patch.object(self.assistant, 'client') as mock_client:
            mock_client.chat.side_effect = Exception("API error")

            result = self.assistant.chat("Test message")

            assert result['success'] == False
            assert '暂时不可用' in result['message']

    def test_initialization_error_handling(self):
        """测试初始化错误处理"""
        with patch('app.utils.llm_client.LLMClientFactory.create_client') as mock_factory:
            mock_factory.side_effect = Exception("Client creation failed")

            # 这应该不会抛出异常，而是创建mock客户端
            assistant = AIAssistant()
            assert assistant.client is not None  # 应该有fallback

    def test_context_parameter_handling(self):
        """测试上下文参数处理"""
        # 测试None上下文
        result = self.assistant._build_system_prompt(None)
        assert 'AI编程学习助手' in result

        # 测试空上下文
        result = self.assistant._build_system_prompt({})
        assert 'AI编程学习助手' in result

    def test_response_format_consistency(self):
        """测试响应格式一致性"""
        expected_keys = ['success', 'response', 'tokens_used', 'response_time']

        with patch.object(self.assistant, 'chat') as mock_chat:
            mock_chat.return_value = {
                'success': True,
                'response': 'test',
                'tokens_used': 5,
                'response_time': 0.1
            }

            result = self.assistant.explain_code("print('test')")

            for key in expected_keys:
                assert key in result
