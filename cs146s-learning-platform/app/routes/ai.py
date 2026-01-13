from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.ai_assistant import AIAssistant
from app.utils.security import InputValidator

ai_bp = Blueprint('ai', __name__, url_prefix='/api/v1/ai')

def get_ai_assistant():
    """获取AI助手实例（延迟初始化）"""
    if not hasattr(current_app, 'ai_assistant'):
        current_app.ai_assistant = AIAssistant()
    return current_app.ai_assistant

@ai_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """AI对话"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        message = data.get('message', '').strip()
        context = data.get('context', {})

        # 验证消息输入
        message_validation = InputValidator.validate_message(message, max_length=5000)
        if not message_validation['valid']:
            return jsonify({'success': False, 'message': message_validation['error']}), 400

        # 验证上下文数据
        context_validation = InputValidator.validate_json_data(context, max_depth=3, max_size=5000)
        if not context_validation['valid']:
            return jsonify({'success': False, 'message': f'上下文数据无效: {context_validation["error"]}'}), 400

        result = get_ai_assistant().chat(message, context)

        if result['success']:
            # 保存对话记录
            get_ai_assistant().save_conversation(
                user_id=current_user.id,
                user_message=message,
                ai_response=result,
                message_type='chat',
                exercise_id=context.get('exercise_id'),
                session_id=context.get('session_id')
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'AI对话失败', 'error': str(e)}), 500

@ai_bp.route('/explain', methods=['POST'])
@login_required
def explain_code():
    """代码解释"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()
        language = data.get('language', 'python')

        # 验证代码输入
        code_validation = InputValidator.validate_code(code, max_length=10000)
        if not code_validation['valid']:
            return jsonify({'success': False, 'message': code_validation['error']}), 400

        # 验证语言参数
        allowed_languages = ['python', 'javascript', 'java', 'cpp', 'c', 'go', 'rust']
        if language not in allowed_languages:
            return jsonify({'success': False, 'message': f'不支持的语言: {language}'}), 400

        result = get_ai_assistant().explain_code(code, language)

        if result['success']:
            # 保存对话记录
            get_ai_assistant().save_conversation(
                user_id=current_user.id,
                user_message=f"请解释以下{language}代码：\n\n{code}",
                ai_response=result,
                message_type='explain'
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '代码解释失败', 'error': str(e)}), 500

@ai_bp.route('/debug', methods=['POST'])
@login_required
def debug_code():
    """代码调试"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()
        error_message = data.get('error', '').strip()

        # 验证代码输入
        code_validation = InputValidator.validate_code(code, max_length=10000)
        if not code_validation['valid']:
            return jsonify({'success': False, 'message': code_validation['error']}), 400

        # 验证错误信息
        error_validation = InputValidator.validate_message(error_message, max_length=2000)
        if not error_validation['valid']:
            return jsonify({'success': False, 'message': f'错误信息无效: {error_validation["error"]}'}), 400

        result = get_ai_assistant().debug_code(code, error_message)

        if result['success']:
            # 保存对话记录
            get_ai_assistant().save_conversation(
                user_id=current_user.id,
                user_message=f"调试代码：\n错误：{error_message}\n代码：{code}",
                ai_response=result,
                message_type='debug'
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '代码调试失败', 'error': str(e)}), 500

@ai_bp.route('/guidance', methods=['POST'])
@login_required
def learning_guidance():
    """学习指导"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        week = data.get('week', 1)
        progress = data.get('progress', 0.0)

        result = get_ai_assistant().learning_guidance(week, progress)

        if result['success']:
            # 保存对话记录
            get_ai_assistant().save_conversation(
                user_id=current_user.id,
                user_message=f"学习指导：第{week}周，进度{progress}%",
                ai_response=result,
                message_type='guidance'
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取学习指导失败', 'error': str(e)}), 500

@ai_bp.route('/hint', methods=['POST'])
@login_required
def get_hint():
    """获取提示"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        exercise_id = data.get('exercise_id')
        current_code = data.get('current_code', '').strip()
        progress = data.get('progress', 'stuck')

        if not exercise_id:
            return jsonify({'success': False, 'message': '练习ID不能为空'}), 400

        result = get_ai_assistant().generate_hint(exercise_id, current_code, progress)

        if result['success']:
            # 保存对话记录
            get_ai_assistant().save_conversation(
                user_id=current_user.id,
                user_message=f"获取提示：练习{exercise_id}，当前进度：{progress}",
                ai_response=result,
                message_type='hint',
                exercise_id=exercise_id
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取提示失败', 'error': str(e)}), 500

@ai_bp.route('/conversations', methods=['GET'])
@login_required
def get_conversations():
    """获取对话历史"""
    try:
        session_id = request.args.get('session_id')
        exercise_id = request.args.get('exercise_id', type=int)
        limit = request.args.get('limit', 50, type=int)

        if limit < 1 or limit > 100:
            limit = 50

        conversations = get_ai_assistant().get_conversation_history(
            user_id=current_user.id,
            session_id=session_id,
            exercise_id=exercise_id,
            limit=limit
        )

        return jsonify({'success': True, 'conversations': conversations}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取对话历史失败', 'error': str(e)}), 500

@ai_bp.route('/usage', methods=['GET'])
@login_required
def get_usage():
    """获取AI使用统计"""
    try:
        days = request.args.get('days', 30, type=int)

        if days < 1 or days > 365:
            days = 30

        stats = get_ai_assistant().get_usage_stats(current_user.id, days)

        return jsonify({'success': True, 'usage': stats}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取使用统计失败', 'error': str(e)}), 500
