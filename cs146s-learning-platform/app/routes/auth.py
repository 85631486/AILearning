from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': '用户名、邮箱和密码不能为空'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码长度至少6位'}), 400

    result = auth_service.register_user(username, email, password)

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': '邮箱和密码不能为空'}), 400

    result = auth_service.authenticate_user(email, password)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    result = auth_service.logout_user()
    return jsonify(result), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """获取当前用户信息"""
    user = auth_service.get_current_user()
    if user:
        return jsonify({'success': True, 'user': user.to_dict()}), 200
    else:
        return jsonify({'success': False, 'message': '用户未登录'}), 401

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新用户资料"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

    result = auth_service.update_user_profile(current_user.id, data)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@auth_bp.route('/password', methods=['PUT'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请求数据不能为空'}), 400

    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not old_password or not new_password:
        return jsonify({'success': False, 'message': '原密码和新密码不能为空'}), 400

    if len(new_password) < 6:
        return jsonify({'success': False, 'message': '新密码长度至少6位'}), 400

    result = auth_service.change_password(current_user.id, old_password, new_password)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400
