from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Week
from app.services.progress_tracker import ProgressTracker

learning_bp = Blueprint('learning', __name__, url_prefix='/api/v1/learning')
progress_tracker = ProgressTracker()

@learning_bp.route('/weeks', methods=['GET'])
def get_weeks():
    """获取所有周的学习内容"""
    try:
        weeks = Week.query.filter_by(is_active=True).order_by(Week.week_number).all()
        weeks_data = [week.to_dict() for week in weeks]

        return jsonify({'success': True, 'weeks': weeks_data}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取周内容失败', 'error': str(e)}), 500

@learning_bp.route('/weeks/<int:week_id>', methods=['GET'])
def get_week(week_id):
    """获取指定周的详细信息"""
    try:
        week = Week.query.filter_by(id=week_id, is_active=True).first()

        if not week:
            return jsonify({'success': False, 'message': '周内容不存在'}), 404

        return jsonify({'success': True, 'week': week.to_dict()}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取周内容失败', 'error': str(e)}), 500

@learning_bp.route('/progress', methods=['GET'])
@login_required
def get_progress():
    """获取用户学习进度"""
    try:
        progress = progress_tracker.get_user_progress(current_user.id)
        return jsonify({'success': True, 'progress': progress}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取进度失败', 'error': str(e)}), 500

@learning_bp.route('/progress/<int:week_id>', methods=['GET'])
@login_required
def get_week_progress(week_id):
    """获取指定周的进度详情"""
    try:
        progress = progress_tracker.get_week_progress(current_user.id, week_id)

        if progress is None:
            return jsonify({'success': False, 'message': '周内容不存在'}), 404

        return jsonify({'success': True, 'progress': progress}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取周进度失败', 'error': str(e)}), 500

@learning_bp.route('/progress/<int:week_id>', methods=['PUT'])
@login_required
def update_progress(week_id):
    """更新学习进度"""
    try:
        data = request.get_json() or {}

        time_spent = data.get('time_spent', 0)
        current_exercise_id = data.get('current_exercise_id')

        # 验证周存在
        week = Week.query.filter_by(id=week_id, is_active=True).first()
        if not week:
            return jsonify({'success': False, 'message': '周内容不存在'}), 404

        result = progress_tracker.update_progress(
            user_id=current_user.id,
            week_id=week_id,
            time_spent=time_spent,
            current_exercise_id=current_exercise_id
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'message': '更新进度失败', 'error': str(e)}), 500

@learning_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """获取用户学习统计"""
    try:
        stats = progress_tracker.get_user_stats(current_user.id)
        return jsonify({'success': True, 'stats': stats}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取统计失败', 'error': str(e)}), 500

@learning_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取排行榜"""
    try:
        week_id = request.args.get('week_id', type=int)
        limit = request.args.get('limit', 10, type=int)

        if limit < 1 or limit > 50:
            limit = 10

        leaderboard = progress_tracker.get_leaderboard(week_id, limit)

        return jsonify({'success': True, 'leaderboard': leaderboard}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取排行榜失败', 'error': str(e)}), 500

@learning_bp.route('/achievements', methods=['GET'])
@login_required
def get_achievements():
    """获取用户成就"""
    try:
        achievements = progress_tracker.get_user_achievements(current_user.id)
        return jsonify({'success': True, 'achievements': achievements}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取成就失败', 'error': str(e)}), 500

@learning_bp.route('/study-plan', methods=['GET'])
@login_required
def get_study_plan():
    """获取学习计划建议"""
    try:
        plan = progress_tracker.generate_study_plan(current_user.id)
        return jsonify({'success': True, 'plan': plan}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取学习计划失败', 'error': str(e)}), 500

@learning_bp.route('/reminders', methods=['GET'])
@login_required
def get_reminders():
    """获取学习提醒"""
    try:
        reminders = progress_tracker.get_learning_reminders(current_user.id)
        return jsonify({'success': True, 'reminders': reminders}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取提醒失败', 'error': str(e)}), 500

@learning_bp.route('/analytics', methods=['GET'])
@login_required
def get_analytics():
    """获取学习分析数据"""
    try:
        days = request.args.get('days', 30, type=int)
        analytics = progress_tracker.get_learning_analytics(current_user.id, days)
        return jsonify({'success': True, 'analytics': analytics}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取分析数据失败', 'error': str(e)}), 500