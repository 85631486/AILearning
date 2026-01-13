"""
作业文件管理器
负责管理作业文件的加载、保存和验证
"""

import os
import json
from typing import List, Dict, Any, Optional
from flask import current_app
from app import db


class AssignmentFileManager:
    """作业文件管理器"""

    def __init__(self, base_path: str = None):
        self._base_path = base_path

    @property
    def base_path(self):
        """获取基础路径，延迟初始化以避免应用上下文问题"""
        if self._base_path is None:
            self._base_path = os.path.join(current_app.root_path, 'assignments')
        return self._base_path

    def _ensure_base_path(self):
        """确保基础路径存在"""
        path = self.base_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def get_exercise_files(self, week_num: int, exercise_title: str) -> List[Dict[str, Any]]:
        """获取练习的文件列表"""
        self._ensure_base_path()
        week_path = os.path.join(self.base_path, f'week{week_num}')
        if not os.path.exists(week_path):
            return []

        files = []
        for root, dirs, filenames in os.walk(week_path):
            # 只处理与练习相关的文件
            if exercise_title.lower().replace(' ', '_') in root.lower():
                for filename in filenames:
                    if self._is_valid_file(filename):
                        file_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(file_path, week_path)

                        files.append({
                            'file_path': rel_path,
                            'file_type': self._determine_file_type(filename, rel_path),
                            'is_template': True,
                            'is_editable': self._is_editable_file(filename),
                            'order_index': self._get_file_order(filename)
                        })

        return sorted(files, key=lambda x: x['order_index'])

    def load_file_content(self, week_num: int, file_path: str) -> Optional[str]:
        """加载文件内容"""
        self._ensure_base_path()
        full_path = os.path.join(self.base_path, f'week{week_num}', file_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (FileNotFoundError, UnicodeDecodeError):
            return None

    def save_user_file(self, user_id: int, exercise_id: int, file_path: str, content: str) -> bool:
        """保存用户修改的文件"""
        self._ensure_base_path()
        user_dir = os.path.join(self.base_path, 'user_submissions', str(user_id), str(exercise_id))
        os.makedirs(user_dir, exist_ok=True)

        full_path = os.path.join(user_dir, os.path.basename(file_path))
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            current_app.logger.error(f'保存用户文件失败: {str(e)}')
            return False

    def get_user_file_content(self, user_id: int, exercise_id: int, file_path: str) -> Optional[str]:
        """获取用户修改的文件内容"""
        self._ensure_base_path()
        user_dir = os.path.join(self.base_path, 'user_submissions', str(user_id), str(exercise_id))
        user_file = os.path.join(user_dir, os.path.basename(file_path))

        if os.path.exists(user_file):
            try:
                with open(user_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except (UnicodeDecodeError, IOError):
                pass

        return None

    def get_file_content_for_user(self, user_id: int, exercise_id: int, file_path: str) -> str:
        """获取用户使用的文件内容（优先使用用户修改的版本）"""
        # 首先尝试获取用户修改的版本
        user_content = self.get_user_file_content(user_id, exercise_id, file_path)
        if user_content is not None:
            return user_content

        # 如果没有用户版本，从模板加载
        week_num = self._get_week_num_from_exercise_id(exercise_id)
        template_content = self.load_file_content(week_num, file_path)

        return template_content or ''

    def _is_valid_file(self, filename: str) -> bool:
        """检查是否为有效的作业文件"""
        invalid_extensions = {'.pyc', '.pyo', '__pycache__', '.git', '.DS_Store'}
        invalid_files = {'README.md', '.gitignore'}

        if any(filename.endswith(ext) for ext in invalid_extensions):
            return False

        if filename in invalid_files:
            return False

        return True

    def _determine_file_type(self, filename: str, rel_path: str) -> str:
        """确定文件类型"""
        if filename.startswith('test_') or filename.endswith('_test.py'):
            return 'test'
        elif 'data' in rel_path.lower() or filename.endswith(('.txt', '.json', '.csv')):
            return 'data'
        elif filename.endswith(('.md', '.rst')):
            return 'docs'
        else:
            return 'source'

    def _is_editable_file(self, filename: str) -> bool:
        """判断文件是否可编辑"""
        # 测试文件通常不可编辑（用户只需运行）
        if filename.startswith('test_') or filename.endswith('_test.py'):
            return False

        # 数据文件通常不可编辑
        if filename.endswith(('.txt', '.json', '.csv')):
            return False

        return True

    def _get_file_order(self, filename: str) -> int:
        """获取文件排序"""
        order_map = {
            'main.py': 1,
            'app.py': 1,
            '__init__.py': 2,
            'config.py': 3,
            'models.py': 4,
            'routes.py': 5,
            'services.py': 6,
        }

        for key, order in order_map.items():
            if key in filename:
                return order

        # 测试文件排在后面
        if filename.startswith('test_'):
            return 100

        return 50

    def _get_week_num_from_exercise_id(self, exercise_id: int) -> int:
        """从练习ID推断周数"""
        # 这是一个简化的实现，实际应该从数据库查询
        # 这里假设exercise_id与week_id有对应关系
        from app.models import Exercise
        exercise = Exercise.query.get(exercise_id)
        if exercise:
            return exercise.week_id
        return 1

    def validate_exercise_structure(self, week_num: int, exercise_title: str) -> Dict[str, Any]:
        """验证练习结构完整性"""
        files = self.get_exercise_files(week_num, exercise_title)

        validation = {
            'has_source_files': any(f['file_type'] == 'source' for f in files),
            'has_test_files': any(f['file_type'] == 'test' for f in files),
            'has_readme': any(f['file_path'].lower().endswith('readme.md') for f in files),
            'total_files': len(files),
            'editable_files': len([f for f in files if f['is_editable']]),
            'issues': []
        }

        if not validation['has_source_files']:
            validation['issues'].append('缺少源代码文件')

        if not validation['has_test_files']:
            validation['issues'].append('缺少测试文件')

        return validation
