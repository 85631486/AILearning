from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.services.exercise_service import ExerciseService
from app.utils.security import InputValidator

exercise_bp = Blueprint('exercises', __name__, url_prefix='/api/v1/exercises')

def get_exercise_service():
    """获取练习服务实例（延迟初始化）"""
    if not hasattr(current_app, 'exercise_service'):
        current_app.exercise_service = ExerciseService()
    return current_app.exercise_service

@exercise_bp.route('', methods=['GET'])
def get_exercises():
    """获取练习列表"""
    try:
        # 获取查询参数
        week_id = request.args.get('week_id', type=int)
        exercise_type = request.args.get('exercise_type')
        difficulty = request.args.get('difficulty')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # 验证参数
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20

        result = get_exercise_service().get_exercises(
            week_id=week_id,
            exercise_type=exercise_type,
            difficulty=difficulty,
            page=page,
            per_page=per_page
        )

        return jsonify({'success': True, **result}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取练习列表失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """获取练习详情"""
    try:
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)

        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        return jsonify({'success': True, 'exercise': exercise.to_dict()}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取练习详情失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/execute', methods=['POST'])
@login_required
def execute_code(exercise_id):
    """执行代码"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()
        inputs = data.get('inputs', {})

        # 验证代码输入
        code_validation = InputValidator.validate_code(code, max_length=10000)
        if not code_validation['valid']:
            return jsonify({'success': False, 'message': code_validation['error']}), 400

        # 验证输入数据
        inputs_validation = InputValidator.validate_json_data(inputs, max_depth=3, max_size=10000)
        if not inputs_validation['valid']:
            return jsonify({'success': False, 'message': f'输入数据无效: {inputs_validation["error"]}'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().code_executor.execute_code(code, inputs)

        return jsonify({'success': True, 'result': result}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '代码执行失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/submit', methods=['POST'])
@login_required
def submit_exercise(exercise_id):
    """提交练习答案"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()
        attempt_number = data.get('attempt_number', 1)

        # 验证代码输入
        code_validation = InputValidator.validate_code(code, max_length=50000)
        if not code_validation['valid']:
            return jsonify({'success': False, 'message': code_validation['error']}), 400

        # 验证尝试次数
        if not isinstance(attempt_number, int) or attempt_number < 1 or attempt_number > 100:
            return jsonify({'success': False, 'message': '尝试次数必须是1-100之间的整数'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().submit_exercise(
            user_id=current_user.id,
            exercise_id=exercise_id,
            code=code,
            attempt_number=attempt_number
        )

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'message': '提交练习失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/submissions', methods=['GET'])
@login_required
def get_submissions(exercise_id):
    """获取提交历史"""
    try:
        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        submissions = get_exercise_service().get_user_submissions(
            user_id=current_user.id,
            exercise_id=exercise_id
        )

        return jsonify({'success': True, 'submissions': submissions}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取提交历史失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/leaderboard', methods=['GET'])
def get_leaderboard(exercise_id):
    """获取排行榜"""
    try:
        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        limit = request.args.get('limit', 10, type=int)
        if limit < 1 or limit > 50:
            limit = 10

        leaderboard = get_exercise_service().get_leaderboard(exercise_id, limit)

        return jsonify({'success': True, 'leaderboard': leaderboard}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取排行榜失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/autosave', methods=['POST'])
@login_required
def autosave_exercise(exercise_id):
    """自动保存练习代码"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()
        metadata = data.get('metadata', {})

        # 验证代码输入（允许空代码用于清除草稿）
        if code and not InputValidator.validate_code(code, max_length=50000)['valid']:
            # 对于自动保存，我们不严格验证语法，只做基本长度检查
            if len(code) > 50000:
                return jsonify({'success': False, 'message': '代码长度超过限制'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().autosave_exercise(
            user_id=current_user.id,
            exercise_id=exercise_id,
            code=code,
            metadata=metadata
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        current_app.logger.error(f'自动保存失败: {str(e)}')
        return jsonify({'success': False, 'message': '自动保存失败', 'error': str(e)}), 500

@exercise_bp.route('/<int:exercise_id>/lint', methods=['POST'])
@login_required
def lint_code(exercise_id):
    """代码检查"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()

        # 验证代码输入（允许空代码用于检查）
        if code and not InputValidator.validate_code(code, max_length=50000)['valid']:
            return jsonify({'success': False, 'message': '代码格式无效'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().lint_code(code)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f'代码检查失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': '代码检查失败',
            'error': str(e),
            'issues': [{
                'line': 1,
                'column': 1,
                'message': '代码检查服务暂时不可用',
                'severity': 'error',
                'source': 'system'
            }]
        }), 500

@exercise_bp.route('/<int:exercise_id>/format', methods=['POST'])
@login_required
def format_code(exercise_id):
    """代码格式化"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

        code = data.get('code', '').strip()

        # 验证代码输入
        if code and not InputValidator.validate_code(code, max_length=50000)['valid']:
            return jsonify({'success': False, 'message': '代码格式无效'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().format_code(code)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f'代码格式化失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': '代码格式化失败',
            'error': str(e)
        }), 500

@exercise_bp.route('/<int:exercise_id>/files', methods=['GET'])
@login_required
def get_exercise_files(exercise_id):
    """获取练习文件列表"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().get_exercise_files(exercise_id, current_user.id)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f'获取练习文件失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': '获取练习文件失败',
            'error': str(e)
        }), 500

@exercise_bp.route('/<int:exercise_id>/files/<path:file_path>', methods=['PUT'])
@login_required
def save_exercise_file(exercise_id, file_path):
    """保存练习文件"""
    try:
        # 验证练习ID
        id_validation = InputValidator.validate_exercise_id(exercise_id)
        if not id_validation['valid']:
            return jsonify({'success': False, 'message': id_validation['error']}), 400

        data = request.get_json()

        if not data or 'content' not in data:
            return jsonify({'success': False, 'message': '请求数据无效'}), 400

        content = data['content']
        if not isinstance(content, str):
            return jsonify({'success': False, 'message': '文件内容必须是字符串'}), 400

        # 验证练习存在
        exercise = get_exercise_service().get_exercise_by_id(exercise_id)
        if not exercise:
            return jsonify({'success': False, 'message': '练习不存在'}), 404

        result = get_exercise_service().save_exercise_file(
            current_user.id, exercise_id, file_path, content
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        current_app.logger.error(f'保存练习文件失败: {str(e)}')
        return jsonify({
            'success': False,
            'message': '保存文件失败',
            'error': str(e)
        }), 500
