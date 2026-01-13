from flask import current_app
from app.models import AIConversation
from app import db
from app.utils.llm_client import get_llm_client, LLMClientFactory
import time
import json

class AIAssistant:
    """AI学习助手"""

    def __init__(self):
        self.api_key = current_app.config.get('QWEN_API_KEY')
        self.base_url = current_app.config.get('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/api/v1')
        self.model = current_app.config.get('QWEN_MODEL', 'qwen-turbo')

        # Create LLM client with fallback to mock
        try:
            if self.api_key:
                self.client = LLMClientFactory.create_client(
                    "qwen",
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            else:
                self.client = LLMClientFactory.create_client("mock")
                current_app.logger.info("Using mock LLM client - no QWEN_API_KEY configured")
        except Exception as e:
            current_app.logger.warning(f"Failed to create LLM client: {e}, falling back to mock")
            self.client = LLMClientFactory.create_client("mock")

    def chat(self, message: str, context: dict = None) -> dict:
        """通用AI对话"""
        try:
            # 构建系统提示
            system_prompt = self._build_system_prompt(context)

            # 调用LLM client
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                options={
                    'max_tokens': 2000,
                    'temperature': 0.7
                }
            )

            return {
                'success': True,
                'response': response['content'],
                'tokens_used': response.get('tokens_used', 0),
                'response_time': response.get('response_time', 0)
            }

        except Exception as e:
            current_app.logger.error(f'AI对话失败: {str(e)}')
            return {
                'success': False,
                'message': 'AI服务暂时不可用，请稍后重试'
            }

    def explain_code(self, code: str, language: str = 'python') -> dict:
        """代码解释"""
        prompt = f"""请详细解释以下{language}代码的功能和逻辑：

```python
{code}
```

请从以下几个方面进行解释：
1. 代码的整体功能
2. 关键步骤和逻辑流程
3. 重要的语法和概念
4. 可能的改进建议"""

        return self.chat(prompt, {'type': 'explain', 'language': language})

    def debug_code(self, code: str, error_message: str) -> dict:
        """代码调试"""
        prompt = f"""我遇到了以下代码错误：

错误信息：{error_message}

代码：
```python
{code}
```

请帮我：
1. 分析错误原因
2. 提供修复方案
3. 解释修复后的代码逻辑"""

        return self.chat(prompt, {'type': 'debug'})

    def learning_guidance(self, week: int, progress: float) -> dict:
        """学习指导"""
        prompt = f"""我正在学习CS146S第{week}周的内容，当前进度为{progress}%。


请根据我的学习进度提供：
1. 本周学习重点
2. 建议的学习方法
3. 可能遇到的难点
4. 下一步学习计划"""

        return self.chat(prompt, {'type': 'guidance', 'week': week, 'progress': progress})

    def generate_hint(self, exercise_id: int, current_code: str, progress: str) -> dict:
        """生成提示"""
        prompt = f"""我正在做练习，当前的代码是：

```python
{current_code}
```

我的进度状态：{progress}

请给我一些提示来帮助我完成这个练习，但不要直接给出答案。"""

        return self.chat(prompt, {'type': 'hint', 'exercise_id': exercise_id})

    def save_conversation(self, user_id: int, user_message: str, ai_response: dict,
                         message_type: str = 'chat', exercise_id: int = None,
                         session_id: str = None) -> bool:
        """保存对话记录"""
        try:
            if not ai_response.get('success', False):
                return False

            conversation = AIConversation(
                user_id=user_id,
                session_id=session_id,
                exercise_id=exercise_id,
                user_message=user_message,
                ai_response=ai_response.get('response', ''),
                message_type=message_type,
                tokens_used=ai_response.get('tokens_used', 0),
                response_time=ai_response.get('response_time', 0)
            )

            db.session.add(conversation)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'保存对话记录失败: {str(e)}')
            return False

    def get_conversation_history(self, user_id: int, session_id: str = None,
                               exercise_id: int = None, limit: int = 50):
        """获取对话历史"""
        try:
            query = AIConversation.query.filter_by(user_id=user_id)

            if session_id:
                query = query.filter_by(session_id=session_id)
            if exercise_id:
                query = query.filter_by(exercise_id=exercise_id)

            conversations = query.order_by(AIConversation.created_at.desc()).limit(limit).all()

            return [conv.to_dict() for conv in conversations]

        except Exception as e:
            current_app.logger.error(f'获取对话历史失败: {str(e)}')
            return []

    def _build_system_prompt(self, context: dict = None) -> str:
        """构建系统提示"""
        base_prompt = """你是一个专业的AI编程学习助手，专注于帮助学习者掌握现代软件开发技能。

你的特点：
- 耐心、友好的教学态度
- 注重概念理解而非死记硬背
- 鼓励独立思考和问题解决
- 提供循序渐进的指导
- 关注最佳实践和代码质量

你正在帮助学习CS146S（现代软件开发者）课程的学生。"""

        if not context:
            return base_prompt

        context_type = context.get('type')
        if context_type == 'explain':
            base_prompt += "\n\n现在你需要解释代码，请确保解释清晰易懂。"
        elif context_type == 'debug':
            base_prompt += "\n\n现在你需要帮助调试代码，请仔细分析错误原因并提供解决方案。"
        elif context_type == 'guidance':
            base_prompt += "\n\n现在你需要提供学习指导，请根据学生的进度给出合适的建议。"
        elif context_type == 'hint':
            base_prompt += "\n\n现在你需要提供提示，请给出适当的线索但不要直接给出答案。"

        return base_prompt

    def get_usage_stats(self, user_id: int = None, days: int = 30):
        """获取使用统计"""
        try:
            from sqlalchemy import func
            from datetime import datetime, timedelta

            query = AIConversation.query

            if user_id:
                query = query.filter_by(user_id=user_id)

            # 计算日期范围
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            query = query.filter(AIConversation.created_at.between(start_date, end_date))

            stats = query.with_entities(
                func.count(AIConversation.id).label('total_conversations'),
                func.sum(AIConversation.tokens_used).label('total_tokens'),
                func.avg(AIConversation.response_time).label('avg_response_time')
            ).first()

            return {
                'total_conversations': stats.total_conversations or 0,
                'total_tokens': stats.total_tokens or 0,
                'avg_response_time': float(stats.avg_response_time) if stats.avg_response_time else 0,
                'period_days': days
            }

        except Exception as e:
            current_app.logger.error(f'获取使用统计失败: {str(e)}')
            return {
                'total_conversations': 0,
                'total_tokens': 0,
                'avg_response_time': 0,
                'period_days': days
            }

    def run_prompt(self, user_prompt: str, system_prompt: str = None, model: str = None) -> dict:
        """运行提示工程练习"""
        try:
            # 使用指定的模型或默认模型
            model_to_use = model or self.model
            
            # 构建消息列表
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})
            
            # 调用LLM client
            response = self.client.chat(
                model=model_to_use,
                messages=messages,
                options={
                    'max_tokens': 2000,
                    'temperature': 0.7
                }
            )
            
            return {
                'success': True,
                'response': response.get('content', ''),
                'tokens': response.get('tokens', 0),
                'model': model_to_use
            }
            
        except Exception as e:
            current_app.logger.error(f'运行提示失败: {str(e)}')
            return {
                'success': False,
                'message': f'运行提示失败: {str(e)}'
            }
