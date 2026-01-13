from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Week
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """用户面板"""
    return render_template('learning/dashboard.html')

@main_bp.route('/weeks')
@login_required
def weeks():
    """周学习页面"""
    weeks = Week.query.filter_by(is_active=True).order_by(Week.week_number).all()
    return render_template('learning/weeks.html', weeks=weeks)

@main_bp.route('/weeks/<int:week_number>')
@login_required
def week_detail(week_number):
    """周详情页面"""
    week = Week.query.filter_by(week_number=week_number, is_active=True).first()
    if not week:
        flash('周内容不存在', 'error')
        return redirect(url_for('main.weeks'))

    return render_template('learning/week_detail.html', week=week)

@main_bp.route('/exercises/<int:exercise_id>')
@login_required
def exercise_detail(exercise_id):
    """练习详情页面"""
    from app.models import Exercise
    exercise = Exercise.query.options(db.joinedload(Exercise.week)).filter_by(id=exercise_id, is_active=True).first()

    if not exercise:
        flash('练习不存在', 'error')
        return redirect(url_for('main.weeks'))

    return render_template('exercises/exercise_detail.html', exercise=exercise)

@main_bp.route('/ai-assistant')
@login_required
def ai_assistant():
    """AI助手页面"""
    return render_template('ai/assistant.html')

@main_bp.route('/profile')
@login_required
def profile():
    """个人中心"""
    return render_template('auth/profile.html')

@main_bp.route('/progress')
@login_required
def progress():
    """学习进度页面"""
    return render_template('learning/progress.html')

# 认证相关页面路由
@main_bp.route('/login')
def login():
    """登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@main_bp.route('/register')
def register():
    """注册页面"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/register.html')

# 健康检查端点
@main_bp.route('/health')
def health():
    """健康检查"""
    return {'status': 'ok', 'service': 'cs146s-learning-platform'}
