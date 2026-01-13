from flask import current_app
from app.models import Exercise, Submission, UserProgress, AssignmentFile
from app import db
from app.services.code_executor import SecureCodeExecutor
from app.services.assignment_manager import AssignmentFileManager
import json
import ast
from datetime import datetime

class ExerciseService:
    """练习服务"""

    def __init__(self):
        self.code_executor = SecureCodeExecutor()
        self.assignment_manager = AssignmentFileManager()

    def get_exercises(self, week_id=None, exercise_type=None, difficulty=None,
                     page=1, per_page=20):
        """获取练习列表"""
        try:
            query = Exercise.query.filter_by(is_active=True)

            if week_id:
                query = query.filter_by(week_id=week_id)
            if exercise_type:
                query = query.filter_by(exercise_type=exercise_type)
            if difficulty:
                query = query.filter_by(difficulty=difficulty)

            # 分页
            exercises = query.order_by(Exercise.order_index).paginate(
                page=page, per_page=per_page, error_out=False
            )

            return {
                'exercises': [exercise.to_dict() for exercise in exercises.items],
                'pagination': {
                    'page': exercises.page,
                    'per_page': exercises.per_page,
                    'total': exercises.total,
                    'pages': exercises.pages,
                    'has_next': exercises.has_next,
                    'has_prev': exercises.has_prev
                }
            }

        except Exception as e:
            current_app.logger.error(f'获取练习列表失败: {str(e)}')
            return {
                'exercises': [],
                'pagination': {
                    'page': 1,
                    'per_page': per_page,
                    'total': 0,
                    'pages': 0,
                    'has_next': False,
                    'has_prev': False
                }
            }

    def get_exercise_by_id(self, exercise_id: int):
        """根据ID获取练习"""
        try:
            exercise = Exercise.query.filter_by(id=exercise_id, is_active=True).first()
            return exercise
        except Exception as e:
            current_app.logger.error(f'获取练习失败: {str(e)}')
            return None

    def submit_exercise(self, user_id: int, exercise_id: int, code: str, attempt_number: int = 1):
        """提交练习"""
        try:
            exercise = self.get_exercise_by_id(exercise_id)
            if not exercise:
                return {
                    'success': False,
                    'message': '练习不存在'
                }

            # 执行代码
            execution_result = self.code_executor.execute_code(code)

            # 验证测试用例
            test_results = self._run_tests(exercise, execution_result)

            # 计算分数
            score = self._calculate_score(test_results)

            # 创建提交记录
            submission = Submission(
                user_id=user_id,
                exercise_id=exercise_id,
                submitted_code=code,
                execution_result=json.dumps(execution_result),
                test_results=json.dumps(test_results),
                score=score,
                is_correct=score >= exercise.points,
                status='completed',
                attempts_count=attempt_number
            )

            db.session.add(submission)
            db.session.commit()

            # 更新用户进度
            self._update_user_progress(user_id, exercise.week_id)

            return {
                'success': True,
                'message': '提交成功',
                'submission': submission.to_dict(),
                'score': score,
                'is_correct': submission.is_correct
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'提交练习失败: {str(e)}')
            return {
                'success': False,
                'message': '提交失败，请稍后重试'
            }

    def get_user_submissions(self, user_id: int, exercise_id: int):
        """获取用户的提交历史"""
        try:
            submissions = Submission.query.filter_by(
                user_id=user_id,
                exercise_id=exercise_id
            ).order_by(Submission.submitted_at.desc()).all()

            return [submission.to_dict() for submission in submissions]

        except Exception as e:
            current_app.logger.error(f'获取提交历史失败: {str(e)}')
            return []

    def get_leaderboard(self, exercise_id: int, limit: int = 10):
        """获取练习排行榜"""
        try:
            # 获取每个用户的最高分提交
            from sqlalchemy import func

            leaderboard = db.session.query(
                Submission.user_id,
                User.username,
                func.max(Submission.score).label('best_score'),
                func.min(Submission.attempts_count).label('attempts'),
                func.min(Submission.submitted_at).label('first_submit')
            ).join(User, Submission.user_id == User.id)\
             .filter(Submission.exercise_id == exercise_id)\
             .group_by(Submission.user_id, User.username)\
             .order_by(func.max(Submission.score).desc(), func.min(Submission.attempts_count))\
             .limit(limit).all()

            return [{
                'user_id': item.user_id,
                'username': item.username,
                'best_score': float(item.best_score) if item.best_score else 0,
                'attempts': item.attempts,
                'first_submit': item.first_submit.isoformat() if item.first_submit else None
            } for item in leaderboard]

        except Exception as e:
            current_app.logger.error(f'获取排行榜失败: {str(e)}')
            return []

    def _run_tests(self, exercise, execution_result):
        """运行测试用例"""
        try:
            if not exercise.test_code:
                return {'passed': 0, 'total': 0, 'results': []}

            # 这里应该实现具体的测试运行逻辑
            # 简单起见，返回模拟结果
            return {
                'passed': 1 if execution_result['success'] else 0,
                'total': 1,
                'results': [{
                    'test_name': '基本功能测试',
                    'passed': execution_result['success'],
                    'output': execution_result.get('stdout', ''),
                    'error': execution_result.get('stderr', '')
                }]
            }

        except Exception as e:
            current_app.logger.error(f'运行测试失败: {str(e)}')
            return {'passed': 0, 'total': 1, 'results': []}

    def _calculate_score(self, test_results):
        """计算分数"""
        try:
            if not test_results or test_results.get('total', 0) == 0:
                return 0.0

            passed = test_results.get('passed', 0)
            total = test_results.get('total', 1)
            return round((passed / total) * 10, 2)

        except Exception as e:
            current_app.logger.error(f'计算分数失败: {str(e)}')
            return 0.0

    def _update_user_progress(self, user_id: int, week_id: int):
        """更新用户学习进度"""
        try:
            # 获取或创建进度记录
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

            # 更新进度统计
            completed_count = db.session.query(Submission)\
                .join(Exercise)\
                .filter(
                    Submission.user_id == user_id,
                    Exercise.week_id == week_id,
                    Submission.is_correct == True
                ).distinct(Submission.exercise_id).count()

            total_count = Exercise.query.filter_by(week_id=week_id, is_active=True).count()

            progress.completed_exercises = completed_count
            progress.total_exercises = total_count
            progress.progress_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
            progress.last_accessed = datetime.utcnow()

            if progress.progress_percentage >= 100:
                progress.status = 'completed'
                progress.completed_at = datetime.utcnow()

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'更新用户进度失败: {str(e)}')

    def autosave_exercise(self, user_id: int, exercise_id: int, code: str, metadata: dict = None):
        """自动保存练习代码"""
        try:
            # 验证练习存在
            exercise = self.get_exercise_by_id(exercise_id)
            if not exercise:
                return {
                    'success': False,
                    'message': '练习不存在'
                }

            # 检查是否已有自动保存记录
            from app.models import AutoSave
            autosave = AutoSave.query.filter_by(
                user_id=user_id,
                exercise_id=exercise_id
            ).first()

            if not autosave:
                # 创建新的自动保存记录
                autosave = AutoSave(
                    user_id=user_id,
                    exercise_id=exercise_id,
                    code=code,
                    metadata=json.dumps(metadata or {}),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(autosave)
            else:
                # 更新现有记录
                autosave.code = code
                autosave.metadata = json.dumps(metadata or {})
                autosave.updated_at = datetime.utcnow()

            db.session.commit()

            return {
                'success': True,
                'message': '自动保存成功',
                'saved_at': autosave.updated_at.isoformat()
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'自动保存失败: {str(e)}')
            return {
                'success': False,
                'message': '自动保存失败，请稍后重试'
            }

    def get_autosave_draft(self, user_id: int, exercise_id: int):
        """获取自动保存的草稿"""
        try:
            from app.models import AutoSave
            autosave = AutoSave.query.filter_by(
                user_id=user_id,
                exercise_id=exercise_id
            ).first()

            if autosave:
                return {
                    'success': True,
                    'code': autosave.code,
                    'metadata': json.loads(autosave.metadata or '{}'),
                    'saved_at': autosave.updated_at.isoformat()
                }
            else:
                return {
                    'success': False,
                    'message': '没有找到自动保存的草稿'
                }

        except Exception as e:
            current_app.logger.error(f'获取自动保存草稿失败: {str(e)}')
            return {
                'success': False,
                'message': '获取草稿失败'
            }

    def get_exercise_files(self, exercise_id: int, user_id: int = None):
        """获取练习的文件列表"""
        try:
            exercise = self.get_exercise_by_id(exercise_id)
            if not exercise:
                return {
                    'success': False,
                    'message': '练习不存在'
                }

            # 获取数据库中存储的文件列表
            db_files = AssignmentFile.query.filter_by(exercise_id=exercise_id)\
                                          .order_by(AssignmentFile.order_index)\
                                          .all()

            files = []
            if db_files:
                # 使用数据库中的文件
                for db_file in db_files:
                    content = self.assignment_manager.get_file_content_for_user(
                        user_id, exercise_id, db_file.file_path
                    ) if user_id else db_file.content

                    files.append({
                        'file_path': db_file.file_path,
                        'file_type': db_file.file_type,
                        'content': content,
                        'is_template': db_file.is_template,
                        'is_editable': db_file.is_editable,
                        'order_index': db_file.order_index
                    })
            else:
                # 从文件系统加载（向后兼容）
                week_files = self.assignment_manager.get_exercise_files(
                    exercise.week_id, exercise.title
                )

                for file_info in week_files:
                    content = self.assignment_manager.load_file_content(
                        exercise.week_id, file_info['file_path']
                    ) or ''

                    files.append({
                        'file_path': file_info['file_path'],
                        'file_type': file_info['file_type'],
                        'content': content,
                        'is_template': file_info['is_template'],
                        'is_editable': file_info['is_editable'],
                        'order_index': file_info['order_index']
                    })

            return {
                'success': True,
                'files': files,
                'exercise': exercise.to_dict()
            }

        except Exception as e:
            current_app.logger.error(f'获取练习文件失败: {str(e)}')
            return {
                'success': False,
                'message': '获取练习文件失败'
            }

    def save_exercise_file(self, user_id: int, exercise_id: int, file_path: str, content: str):
        """保存用户修改的练习文件"""
        try:
            exercise = self.get_exercise_by_id(exercise_id)
            if not exercise:
                return {
                    'success': False,
                    'message': '练习不存在'
                }

            success = self.assignment_manager.save_user_file(
                user_id, exercise_id, file_path, content
            )

            if success:
                return {
                    'success': True,
                    'message': '文件保存成功'
                }
            else:
                return {
                    'success': False,
                    'message': '文件保存失败'
                }

        except Exception as e:
            current_app.logger.error(f'保存练习文件失败: {str(e)}')
            return {
                'success': False,
                'message': '文件保存失败'
            }

    def get_exercise_with_files(self, exercise_id: int, user_id: int = None):
        """获取包含文件的完整练习信息"""
        try:
            exercise = self.get_exercise_by_id(exercise_id)
            if not exercise:
                return None

            # 获取文件列表
            files_result = self.get_exercise_files(exercise_id, user_id)
            if not files_result['success']:
                return None

            exercise_data = exercise.to_dict()
            exercise_data['files'] = files_result['files']

            return exercise_data

        except Exception as e:
            current_app.logger.error(f'获取完整练习信息失败: {str(e)}')
            return None

    def lint_code(self, code: str) -> dict:
        """代码检查和语法分析"""
        try:
            from app.utils.security import CodeSecurityChecker

            # 使用现有的安全检查器进行代码分析
            checker = CodeSecurityChecker()
            result = checker.check_code(code)

            issues = []

            # 处理AST和语法错误
            if not result['is_safe']:
                for issue in result['issues']:
                    issues.append({
                        'line': issue.get('line', 1),
                        'column': issue.get('column', 1),
                        'message': issue['message'],
                        'severity': self._map_issue_severity(issue['type']),
                        'source': 'security'
                    })

            # 尝试执行基本的语法检查和静态分析
            try:
                import ast
                tree = ast.parse(code)

                # 简单的静态分析
                analyzer = CodeAnalyzer()
                analyzer.visit(tree)
                issues.extend(analyzer.issues)

            except SyntaxError as e:
                issues.append({
                    'line': e.lineno or 1,
                    'column': e.offset or 1,
                    'message': f'语法错误: {e.msg}',
                    'severity': 'error',
                    'source': 'syntax'
                })
            except Exception as e:
                # 如果AST分析失败，至少报告基本信息
                issues.append({
                    'line': 1,
                    'column': 1,
                    'message': f'代码分析失败: {str(e)}',
                    'severity': 'warning',
                    'source': 'analysis'
                })

            return {
                'success': True,
                'issues': issues
            }

        except Exception as e:
            current_app.logger.error(f'代码检查失败: {str(e)}')
            return {
                'success': False,
                'message': '代码检查失败',
                'issues': [{
                    'line': 1,
                    'column': 1,
                    'message': f'代码检查服务暂时不可用: {str(e)}',
                    'severity': 'error',
                    'source': 'system'
                }]
            }

    def format_code(self, code: str) -> dict:
        """代码格式化"""
        try:
            # 检查是否启用格式化功能
            format_enabled = current_app.config.get('CODE_FORMAT_ENABLED', False)

            if not format_enabled:
                return {
                    'success': False,
                    'message': '代码格式化功能未启用'
                }

            # 验证代码长度
            if len(code) > 50000:
                return {
                    'success': False,
                    'message': '代码长度超过格式化限制'
                }

            # 首先尝试使用 black 进行格式化
            try:
                import subprocess
                import tempfile
                import os

                # 创建临时文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                    temp_file.write(code)
                    temp_file_path = temp_file.name

                try:
                    # 运行 black 格式化
                    result = subprocess.run(
                        ['black', '--line-length', '88', '--target-version', 'py38', temp_file_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    if result.returncode == 0:
                        # 读取格式化后的代码
                        with open(temp_file_path, 'r') as f:
                            formatted_code = f.read()

                        return {
                            'success': True,
                            'code': formatted_code,
                            'formatter': 'black'
                        }
                    else:
                        # black 失败，尝试简单的格式化
                        current_app.logger.warning(f'Black formatting failed: {result.stderr}')
                        return self._simple_format_fallback(code)

                finally:
                    # 清理临时文件
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass

            except ImportError:
                # black 未安装，使用简单格式化
                current_app.logger.info('Black not available, using simple formatting')
                return self._simple_format_fallback(code)
            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'message': '代码格式化超时'
                }
            except Exception as e:
                current_app.logger.error(f'Black formatting error: {str(e)}')
                return self._simple_format_fallback(code)

        except Exception as e:
            current_app.logger.error(f'代码格式化失败: {str(e)}')
            return {
                'success': False,
                'message': '代码格式化失败，请稍后重试'
            }

    def _simple_format_fallback(self, code: str) -> dict:
        """简单的代码格式化回退方案"""
        try:
            import ast

            # 解析并重新格式化代码
            tree = ast.parse(code)

            # 使用简单的格式化逻辑
            formatted_code = self._format_ast_node(tree, code)

            return {
                'success': True,
                'code': formatted_code,
                'formatter': 'simple'
            }

        except Exception as e:
            current_app.logger.error(f'Simple formatting failed: {str(e)}')
            return {
                'success': False,
                'message': '无法格式化代码，请检查语法'
            }

    def _format_ast_node(self, node, source_code):
        """简单的AST节点格式化"""
        # 这是一个简化的格式化器
        # 对于生产环境，建议使用专业的代码格式化工具
        lines = source_code.split('\n')
        formatted_lines = []

        for line in lines:
            # 移除行尾空格
            line = line.rstrip()
            # 确保行不为空（除非是空行）
            if line.strip() or line == '':
                formatted_lines.append(line)

        # 移除末尾的空行
        while formatted_lines and formatted_lines[-1].strip() == '':
            formatted_lines.pop()

        return '\n'.join(formatted_lines) + '\n'

    def _map_issue_severity(self, issue_type: str) -> str:
        """映射问题类型到严重程度"""
        severity_map = {
            'syntax_error': 'error',
            'dangerous_import': 'error',
            'forbidden_function': 'error',
            'forbidden_function_call': 'error',
            'dangerous_method_call': 'warning',
            'private_attribute_access': 'info',
            'restricted_import': 'warning',
            'dangerous_pattern': 'warning'
        }
        return severity_map.get(issue_type, 'info')


class CodeAnalyzer(ast.NodeVisitor):
    """简单的代码静态分析器"""

    def __init__(self):
        self.issues = []
        self.defined_vars = set()
        self.used_vars = set()
        self.functions = {}

    def visit_FunctionDef(self, node):
        """访问函数定义"""
        self.functions[node.name] = node
        self.generic_visit(node)

    def visit_Assign(self, node):
        """访问赋值语句"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        """访问变量名"""
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        """访问函数调用"""
        # 检查未定义的函数调用
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in self.functions and func_name not in ['print', 'len', 'str', 'int', 'float', 'input', 'range', 'sum', 'max', 'min', 'abs', 'round', 'sorted', 'reversed', 'enumerate', 'zip', 'dict', 'list', 'set', 'tuple']:
                # 这里可以添加更复杂的检查，但保持简单
                pass
        self.generic_visit(node)