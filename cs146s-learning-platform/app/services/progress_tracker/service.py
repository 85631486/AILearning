from flask import current_app
from app.models import UserProgress, Week, Exercise, Submission
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

class ProgressTracker:
    """进度追踪服务"""

    def get_user_progress(self, user_id: int):
        """获取用户学习进度"""
        try:
            # 获取所有周的进度
            progress_records = UserProgress.query.filter_by(user_id=user_id).all()

            # 获取所有周的信息
            weeks = Week.query.filter_by(is_active=True).order_by(Week.week_number).all()

            progress_data = []
            total_progress = 0
            total_weeks = len(weeks)

            for week in weeks:
                # 查找该周的进度记录
                progress = next((p for p in progress_records if p.week_id == week.id), None)

                if not progress:
                    # 如果没有进度记录，创建默认记录
                    progress = UserProgress(
                        user_id=user_id,
                        week_id=week.id,
                        status='not_started',
                        completed_exercises=0,
                        total_exercises=0,
                        progress_percentage=0.0
                    )

                week_data = {
                    'week_id': week.id,
                    'week_number': week.week_number,
                    'title': week.title,
                    'status': progress.status,
                    'completed_exercises': progress.completed_exercises,
                    'total_exercises': progress.total_exercises,
                    'progress_percentage': float(progress.progress_percentage),
                    'last_accessed': progress.last_accessed.isoformat() if progress.last_accessed else None,
                    'time_spent': progress.time_spent
                }

                progress_data.append(week_data)
                total_progress += progress.progress_percentage

            return {
                'weeks': progress_data,
                'overall_progress': round(total_progress / total_weeks, 2) if total_weeks > 0 else 0,
                'total_weeks': total_weeks,
                'completed_weeks': len([p for p in progress_data if p['status'] == 'completed'])
            }

        except Exception as e:
            current_app.logger.error(f'获取用户进度失败: {str(e)}')
            return {
                'weeks': [],
                'overall_progress': 0,
                'total_weeks': 0,
                'completed_weeks': 0
            }

    def get_user_stats(self, user_id: int):
        """获取用户学习统计"""
        try:
            # 总提交数
            total_submissions = Submission.query.filter_by(user_id=user_id).count()

            # 正确提交数
            correct_submissions = Submission.query.filter_by(
                user_id=user_id, is_correct=True
            ).count()

            # 总分数
            total_score_result = db.session.query(func.sum(Submission.score)).filter_by(user_id=user_id).first()
            total_score = float(total_score_result[0]) if total_score_result[0] else 0

            # 平均分数
            avg_score_result = db.session.query(func.avg(Submission.score)).filter_by(user_id=user_id).first()
            avg_score = float(avg_score_result[0]) if avg_score_result[0] else 0

            # 总学习时长
            total_time_result = db.session.query(func.sum(UserProgress.time_spent)).filter_by(user_id=user_id).first()
            total_time_spent = total_time_result[0] if total_time_result[0] else 0

            # 连续学习天数
            streak_days = self._calculate_streak_days(user_id)

            # 练习完成情况
            completed_exercises = db.session.query(Submission)\
                .filter_by(user_id=user_id, is_correct=True)\
                .distinct(Submission.exercise_id)\
                .count()

            total_exercises = Exercise.query.filter_by(is_active=True).count()

            # 本周活动
            week_ago = datetime.utcnow() - timedelta(days=7)
            weekly_submissions = Submission.query.filter(
                Submission.user_id == user_id,
                Submission.submitted_at >= week_ago
            ).count()

            return {
                'total_submissions': total_submissions,
                'correct_submissions': correct_submissions,
                'accuracy_rate': round((correct_submissions / total_submissions * 100), 2) if total_submissions > 0 else 0,
                'total_score': round(total_score, 2),
                'average_score': round(avg_score, 2),
                'total_time_spent': total_time_spent,
                'completed_exercises': completed_exercises,
                'total_exercises': total_exercises,
                'completion_rate': round((completed_exercises / total_exercises * 100), 2) if total_exercises > 0 else 0,
                'streak_days': streak_days,
                'weekly_submissions': weekly_submissions
            }

        except Exception as e:
            current_app.logger.error(f'获取用户统计失败: {str(e)}')
            return {
                'total_submissions': 0,
                'correct_submissions': 0,
                'accuracy_rate': 0,
                'total_score': 0,
                'average_score': 0,
                'total_time_spent': 0,
                'completed_exercises': 0,
                'total_exercises': 0,
                'completion_rate': 0,
                'streak_days': 0,
                'weekly_submissions': 0
            }

    def update_progress(self, user_id: int, week_id: int, time_spent: int = 0,
                       current_exercise_id: int = None):
        """更新学习进度"""
        try:
            progress = UserProgress.query.filter_by(
                user_id=user_id, week_id=week_id
            ).first()

            if not progress:
                progress = UserProgress(
                    user_id=user_id,
                    week_id=week_id,
                    status='in_progress',
                    started_at=datetime.utcnow()
                )
                db.session.add(progress)

            # 更新访问时间
            progress.last_accessed = datetime.utcnow()

            # 更新当前练习
            if current_exercise_id:
                progress.current_exercise_id = current_exercise_id

            # 更新学习时长
            if time_spent > 0:
                progress.time_spent += time_spent

            # 如果是首次访问，设置开始时间
            if not progress.started_at:
                progress.started_at = datetime.utcnow()

            db.session.commit()

            return {
                'success': True,
                'progress': progress.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'更新进度失败: {str(e)}')
            return {
                'success': False,
                'message': '更新进度失败'
            }

    def get_week_progress(self, user_id: int, week_id: int):
        """获取指定周的进度详情"""
        try:
            week = Week.query.filter_by(id=week_id, is_active=True).first()
            if not week:
                return None

            progress = UserProgress.query.filter_by(
                user_id=user_id, week_id=week_id
            ).first()

            # 获取该周的所有练习
            exercises = Exercise.query.filter_by(
                week_id=week_id, is_active=True
            ).order_by(Exercise.order_index).all()

            exercise_progress = []
            for exercise in exercises:
                # 检查用户是否完成该练习
                submission = Submission.query.filter_by(
                    user_id=user_id,
                    exercise_id=exercise.id,
                    is_correct=True
                ).first()

                exercise_progress.append({
                    'exercise_id': exercise.id,
                    'title': exercise.title,
                    'difficulty': exercise.difficulty,
                    'points': exercise.points,
                    'is_completed': submission is not None,
                    'best_score': float(submission.score) if submission else 0,
                    'attempts': submission.attempts_count if submission else 0,
                    'last_attempt': submission.submitted_at.isoformat() if submission else None
                })

            return {
                'week': week.to_dict(),
                'progress': progress.to_dict() if progress else None,
                'exercises': exercise_progress,
                'summary': {
                    'total_exercises': len(exercises),
                    'completed_exercises': len([e for e in exercise_progress if e['is_completed']]),
                    'total_points': sum([e['points'] for e in exercises]),
                    'earned_points': sum([e['best_score'] for e in exercise_progress if e['is_completed']])
                }
            }

        except Exception as e:
            current_app.logger.error(f'获取周进度失败: {str(e)}')
            return None

    def get_leaderboard(self, week_id: int = None, limit: int = 10):
        """获取排行榜"""
        try:
            from app.models import User

            # 计算每个用户的总分
            query = db.session.query(
                User.id.label('user_id'),
                User.username,
                func.sum(Submission.score).label('total_score'),
                func.count(Submission.id).label('total_submissions'),
                func.count(Submission.id).filter(Submission.is_correct == True).label('correct_submissions')
            ).join(Submission, User.id == Submission.user_id)\
             .filter(Submission.is_correct == True)

            if week_id:
                query = query.join(Exercise, Submission.exercise_id == Exercise.id)\
                           .filter(Exercise.week_id == week_id)

            leaderboard = query.group_by(User.id, User.username)\
                             .order_by(func.sum(Submission.score).desc())\
                             .limit(limit).all()

            return [{
                'rank': idx + 1,
                'user_id': item.user_id,
                'username': item.username,
                'total_score': float(item.total_score) if item.total_score else 0,
                'total_submissions': item.total_submissions,
                'correct_submissions': item.correct_submissions,
                'accuracy_rate': round((item.correct_submissions / item.total_submissions * 100), 2) if item.total_submissions > 0 else 0
            } for idx, item in enumerate(leaderboard)]

        except Exception as e:
            current_app.logger.error(f'获取排行榜失败: {str(e)}')
            return []

    def _calculate_streak_days(self, user_id: int) -> int:
        """计算连续学习天数"""
        try:
            # 获取用户最近的学习活动
            recent_activities = db.session.query(
                func.date(Submission.submitted_at).label('activity_date')
            ).filter_by(user_id=user_id)\
             .distinct()\
             .order_by(Submission.submitted_at.desc())\
             .limit(30).all()

            if not recent_activities:
                return 0

            # 转换为日期集合
            activity_dates = {activity.activity_date for activity in recent_activities}
            today = datetime.utcnow().date()

            streak = 0
            current_date = today

            # 检查连续天数
            while current_date in activity_dates:
                streak += 1
                current_date -= timedelta(days=1)

            return streak

        except Exception as e:
            current_app.logger.error(f'计算连续天数失败: {str(e)}')
            return 0

    def get_user_achievements(self, user_id: int):
        """获取用户成就"""
        try:
            stats = self.get_user_stats(user_id)

            achievements = [
                {
                    'id': 'first_steps',
                    'name': '第一步',
                    'description': '完成第一个练习',
                    'icon': '👶',
                    'earned': stats['total_submissions'] > 0,
                    'earned_at': None,  # 需要从数据库获取
                    'progress': min(stats['total_submissions'], 1),
                    'max_progress': 1
                },
                {
                    'id': 'problem_solver',
                    'name': '问题解决者',
                    'description': '完成10个练习',
                    'icon': '🧠',
                    'earned': stats['completed_exercises'] >= 10,
                    'earned_at': None,
                    'progress': min(stats['completed_exercises'], 10),
                    'max_progress': 10
                },
                {
                    'id': 'perfect_score',
                    'name': '完美主义者',
                    'description': '获得满分100次',
                    'icon': '💎',
                    'earned': stats['total_score'] >= 100,
                    'earned_at': None,
                    'progress': min(int(stats['total_score']), 100),
                    'max_progress': 100
                },
                {
                    'id': 'streak_master',
                    'name': '坚持大师',
                    'description': '连续学习30天',
                    'icon': '🔥',
                    'earned': stats['streak_days'] >= 30,
                    'earned_at': None,
                    'progress': min(stats['streak_days'], 30),
                    'max_progress': 30
                },
                {
                    'id': 'accuracy_expert',
                    'name': '准确专家',
                    'description': '正确率达到95%',
                    'icon': '🎯',
                    'earned': stats['accuracy_rate'] >= 95,
                    'earned_at': None,
                    'progress': min(int(stats['accuracy_rate']), 95),
                    'max_progress': 95
                },
                {
                    'id': 'speed_demon',
                    'name': '速度之星',
                    'description': '平均每题用时少于3分钟',
                    'icon': '⚡',
                    'earned': False,  # 需要实现时间跟踪
                    'earned_at': None,
                    'progress': 0,
                    'max_progress': 1
                },
                {
                    'id': 'week_warrior',
                    'name': '周冠军',
                    'description': '完成一整周的所有练习',
                    'icon': '👑',
                    'earned': self._has_completed_full_week(user_id),
                    'earned_at': None,
                    'progress': self._get_week_completion_count(user_id),
                    'max_progress': 1
                },
                {
                    'id': 'mentor',
                    'name': '导师',
                    'description': '帮助其他学习者（预留功能）',
                    'icon': '🎓',
                    'earned': False,
                    'earned_at': None,
                    'progress': 0,
                    'max_progress': 1
                }
            ]

            return achievements

        except Exception as e:
            current_app.logger.error(f'获取用户成就失败: {str(e)}')
            return []

    def generate_study_plan(self, user_id: int):
        """生成学习计划建议"""
        try:
            progress = self.get_user_progress(user_id)
            stats = self.get_user_stats(user_id)

            plan = {
                'daily_goal': {
                    'exercises': 2,  # 每日目标练习数
                    'time': 60,  # 每日目标时间（分钟）
                },
                'weekly_goal': {
                    'exercises': 10,
                    'time': 300,  # 每周目标时间（分钟）
                },
                'recommendations': [],
                'next_steps': []
            }

            # 基于当前进度生成建议
            if progress['overall_progress'] < 25:
                plan['recommendations'].append({
                    'type': 'start',
                    'message': '建议从基础练习开始，建立编程思维',
                    'priority': 'high'
                })
                plan['next_steps'].append('完成Week 1的所有基础练习')

            elif progress['overall_progress'] < 50:
                plan['recommendations'].append({
                    'type': 'practice',
                    'message': '继续练习，巩固已学知识',
                    'priority': 'high'
                })
                plan['next_steps'].append('挑战中级难度的练习')

            elif progress['overall_progress'] < 75:
                plan['recommendations'].append({
                    'type': 'review',
                    'message': '复习之前的内容，准备进阶学习',
                    'priority': 'medium'
                })
                plan['next_steps'].append('复习错题并重新练习')

            else:
                plan['recommendations'].append({
                    'type': 'advanced',
                    'message': '尝试高级练习，提升编程技能',
                    'priority': 'medium'
                })
                plan['next_steps'].append('探索更复杂的编程问题')

            # 基于学习习惯的建议
            if stats['streak_days'] == 0:
                plan['recommendations'].append({
                    'type': 'consistency',
                    'message': '建立每日学习习惯，坚持更重要',
                    'priority': 'high'
                })

            if stats['accuracy_rate'] < 70:
                plan['recommendations'].append({
                    'type': 'accuracy',
                    'message': '关注题目理解，提高正确率',
                    'priority': 'medium'
                })

            return plan

        except Exception as e:
            current_app.logger.error(f'生成学习计划失败: {str(e)}')
            return {
                'daily_goal': {'exercises': 2, 'time': 60},
                'weekly_goal': {'exercises': 10, 'time': 300},
                'recommendations': [],
                'next_steps': ['继续学习编程基础知识']
            }

    def get_learning_reminders(self, user_id: int):
        """获取学习提醒"""
        try:
            stats = self.get_user_stats(user_id)
            reminders = []

            # 检查连续学习
            if stats['streak_days'] > 0 and stats['streak_days'] < 7:
                reminders.append({
                    'type': 'streak',
                    'title': '保持连续学习',
                    'message': f'您已经连续学习 {stats["streak_days"]} 天，不要中断！',
                    'priority': 'high',
                    'icon': '🔥'
                })

            # 检查学习频率
            if stats['weekly_submissions'] < 5:
                reminders.append({
                    'type': 'frequency',
                    'title': '增加学习频率',
                    'message': '本周学习次数较少，建议每天安排时间练习',
                    'priority': 'medium',
                    'icon': '⏰'
                })

            # 检查未完成的任务
            progress = self.get_user_progress(user_id)
            incomplete_weeks = [w for w in progress['weeks'] if w['status'] != 'completed']
            if incomplete_weeks:
                next_week = incomplete_weeks[0]
                reminders.append({
                    'type': 'progress',
                    'title': '继续学习任务',
                    'message': f'Week {next_week["week_number"]} 还有 {next_week["total_exercises"] - next_week["completed_exercises"]} 个练习未完成',
                    'priority': 'medium',
                    'icon': '📚'
                })

            # 定期复习提醒
            reminders.append({
                'type': 'review',
                'title': '定期复习',
                'message': '建议定期复习之前学过的内容，加深记忆',
                'priority': 'low',
                'icon': '🔄'
            })

            return reminders

        except Exception as e:
            current_app.logger.error(f'获取学习提醒失败: {str(e)}')
            return []

    def get_learning_analytics(self, user_id: int, days: int = 30):
        """获取学习分析数据"""
        try:
            # 获取指定天数内的数据
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            # 每日学习统计
            daily_stats = db.session.query(
                func.date(Submission.submitted_at).label('date'),
                func.count(Submission.id).label('submissions'),
                func.sum(Submission.score).label('total_score'),
                func.avg(Submission.score).label('avg_score'),
                func.sum(case((Submission.is_correct == True, 1), else_=0)).label('correct_count')
            ).filter(
                Submission.user_id == user_id,
                Submission.submitted_at >= start_date,
                Submission.submitted_at <= end_date
            ).group_by(func.date(Submission.submitted_at))\
             .order_by(func.date(Submission.submitted_at)).all()

            # 时间分布分析
            hourly_stats = db.session.query(
                func.hour(Submission.submitted_at).label('hour'),
                func.count(Submission.id).label('count')
            ).filter(
                Submission.user_id == user_id,
                Submission.submitted_at >= start_date
            ).group_by(func.hour(Submission.submitted_at))\
             .order_by(func.hour(Submission.submitted_at)).all()

            # 难度分布
            difficulty_stats = db.session.query(
                Exercise.difficulty,
                func.count(Submission.id).label('count'),
                func.avg(Submission.score).label('avg_score')
            ).join(Exercise, Submission.exercise_id == Exercise.id)\
             .filter(Submission.user_id == user_id)\
             .group_by(Exercise.difficulty).all()

            # 每周趋势
            weekly_trend = []
            for i in range(0, days, 7):
                week_start = start_date + timedelta(days=i)
                week_end = min(week_start + timedelta(days=6), end_date)

                week_data = db.session.query(
                    func.count(Submission.id).label('submissions'),
                    func.sum(Submission.score).label('total_score'),
                    func.sum(case((Submission.is_correct == True, 1), else_=0)).label('correct_count')
                ).filter(
                    Submission.user_id == user_id,
                    Submission.submitted_at >= week_start,
                    Submission.submitted_at <= week_end
                ).first()

                weekly_trend.append({
                    'week': f'Week {((end_date - week_start).days // 7) + 1}',
                    'submissions': week_data.submissions or 0,
                    'total_score': float(week_data.total_score or 0),
                    'correct_count': week_data.correct_count or 0
                })

            return {
                'daily_activity': [{
                    'date': stat.date.isoformat(),
                    'submissions': stat.submissions,
                    'total_score': float(stat.total_score or 0),
                    'avg_score': float(stat.avg_score or 0),
                    'correct_rate': (stat.correct_count / stat.submissions * 100) if stat.submissions > 0 else 0
                } for stat in daily_stats],
                'time_distribution': [{
                    'hour': stat.hour,
                    'count': stat.count
                } for stat in hourly_stats],
                'difficulty_analysis': [{
                    'difficulty': stat.difficulty,
                    'count': stat.count,
                    'avg_score': float(stat.avg_score or 0)
                } for stat in difficulty_stats],
                'weekly_trend': weekly_trend,
                'summary': {
                    'total_days_active': len(daily_stats),
                    'total_submissions': sum(s.submissions for s in daily_stats),
                    'avg_daily_submissions': sum(s.submissions for s in daily_stats) / max(len(daily_stats), 1),
                    'best_day': max(daily_stats, key=lambda x: x.submissions).date.isoformat() if daily_stats else None,
                    'most_productive_hour': max(hourly_stats, key=lambda x: x.count).hour if hourly_stats else None
                }
            }

        except Exception as e:
            current_app.logger.error(f'获取学习分析失败: {str(e)}')
            return {
                'daily_activity': [],
                'time_distribution': [],
                'difficulty_analysis': [],
                'weekly_trend': [],
                'summary': {
                    'total_days_active': 0,
                    'total_submissions': 0,
                    'avg_daily_submissions': 0,
                    'best_day': None,
                    'most_productive_hour': None
                }
            }

    def _has_completed_full_week(self, user_id: int) -> bool:
        """检查用户是否完成过整周练习"""
        try:
            # 检查是否有任何一周的所有练习都被完成
            weeks = Week.query.filter_by(is_active=True).all()
            for week in weeks:
                total_exercises = Exercise.query.filter_by(week_id=week.id, is_active=True).count()
                completed_exercises = db.session.query(Submission)\
                    .join(Exercise, Submission.exercise_id == Exercise.id)\
                    .filter(
                        Submission.user_id == user_id,
                        Exercise.week_id == week.id,
                        Submission.is_correct == True
                    ).distinct(Submission.exercise_id).count()

                if completed_exercises >= total_exercises:
                    return True
            return False
        except Exception:
            return False

    def _get_week_completion_count(self, user_id: int) -> int:
        """获取完成整周的次数"""
        try:
            count = 0
            weeks = Week.query.filter_by(is_active=True).all()
            for week in weeks:
                total_exercises = Exercise.query.filter_by(week_id=week.id, is_active=True).count()
                completed_exercises = db.session.query(Submission)\
                    .join(Exercise, Submission.exercise_id == Exercise.id)\
                    .filter(
                        Submission.user_id == user_id,
                        Exercise.week_id == week.id,
                        Submission.is_correct == True
                    ).distinct(Submission.exercise_id).count()

                if completed_exercises >= total_exercises:
                    count += 1
            return count
        except Exception:
            return 0