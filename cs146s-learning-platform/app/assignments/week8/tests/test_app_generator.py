#!/usr/bin/env python3
"""
Week 8: 应用生成器测试
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# 添加generator目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generator'))

from app_generator import AppGenerator, AppSpecification


class TestAppGenerator:
    """测试应用生成器"""

    def setup_method(self):
        """测试前设置"""
        self.generator = AppGenerator()

    def test_generator_initialization(self):
        """测试生成器初始化"""
        assert self.generator.templates is not None
        assert len(self.generator.templates) > 0
        assert 'react-flask' in self.generator.templates

    def test_list_available_templates(self):
        """测试获取可用模板"""
        templates = self.generator.list_available_templates()
        assert isinstance(templates, dict)
        assert 'react-flask' in templates
        assert 'description' in templates['react-flask']

    def test_get_template_info(self):
        """测试获取模板信息"""
        info = self.generator.get_template_info('react-flask')
        assert info is not None
        assert 'description' in info
        assert 'frontend' in info

    def test_get_template_info_not_found(self):
        """测试获取不存在的模板信息"""
        info = self.generator.get_template_info('nonexistent-template')
        assert info is None

    def test_app_specification_creation(self):
        """测试应用规格创建"""
        spec = AppSpecification(
            name='TestApp',
            description='Test application',
            tech_stack='react-flask',
            features=['feature1', 'feature2'],
            entities=[{'name': 'user', 'fields': ['name', 'email']}],
            frontend_framework='react',
            backend_framework='flask',
            database='sqlite'
        )

        assert spec.name == 'TestApp'
        assert spec.tech_stack == 'react-flask'
        assert len(spec.features) == 2
        assert len(spec.entities) == 1

    def test_directory_structure_creation(self):
        """测试目录结构创建"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test',
                tech_stack='react-flask',
                features=[],
                entities=[],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            self.generator._create_directory_structure(spec, temp_dir)

            # 检查目录是否创建
            assert os.path.exists(os.path.join(temp_dir, 'backend'))
            assert os.path.exists(os.path.join(temp_dir, 'backend', 'app'))
            assert os.path.exists(os.path.join(temp_dir, 'frontend'))
            assert os.path.exists(os.path.join(temp_dir, 'frontend', 'src'))

    def test_flask_backend_generation(self):
        """测试Flask后端生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test',
                tech_stack='react-flask',
                features=[],
                entities=[{'name': 'user', 'fields': ['name', 'email']}],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            files = self.generator._generate_flask_backend(spec, temp_dir)

            # 检查生成的文件
            assert len(files) > 0
            assert any('__init__.py' in f for f in files)
            assert any('models.py' in f for f in files)
            assert any('run.py' in f for f in files)

            # 检查文件内容
            init_file = os.path.join(temp_dir, 'backend', 'app', '__init__.py')
            assert os.path.exists(init_file)

            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert 'create_app' in content
                assert 'register_routes' in content

    def test_react_frontend_generation(self):
        """测试React前端生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test',
                tech_stack='react-flask',
                features=[],
                entities=[{'name': 'user', 'fields': ['name', 'email']}],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            files = self.generator._generate_react_frontend(spec, temp_dir)

            # 检查生成的文件
            assert len(files) > 0
            assert any('package.json' in f for f in files)
            assert any('App.js' in f for f in files)

            # 检查package.json内容
            package_file = os.path.join(temp_dir, 'frontend', 'package.json')
            assert os.path.exists(package_file)

            with open(package_file, 'r', encoding='utf-8') as f:
                import json
                package_data = json.load(f)
                assert 'react' in package_data.get('dependencies', {})
                assert 'axios' in package_data.get('dependencies', {})

    def test_config_files_generation(self):
        """测试配置文件生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test',
                tech_stack='react-flask',
                features=[],
                entities=[],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            files = self.generator._generate_config_files(spec, temp_dir)

            # 检查生成的文件
            assert len(files) > 0
            assert any('Dockerfile' in f for f in files)
            assert any('docker-compose.yml' in f for f in files)
            assert any('.env.example' in f for f in files)

    def test_documentation_generation(self):
        """测试文档生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test application',
                tech_stack='react-flask',
                features=['Feature 1', 'Feature 2'],
                entities=[],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            files = self.generator._generate_documentation(spec, temp_dir)

            # 检查生成的文件
            assert len(files) > 0
            assert any('README.md' in f for f in files)

            # 检查README内容
            readme_file = os.path.join(temp_dir, 'README.md')
            assert os.path.exists(readme_file)

            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '# TestApp' in content
                assert 'Test application' in content
                assert '- Feature 1' in content

    def test_full_app_generation(self):
        """测试完整应用生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = AppSpecification(
                name='TestApp',
                description='Test application',
                tech_stack='react-flask',
                features=['Basic CRUD'],
                entities=[{'name': 'item', 'fields': ['name', 'description']}],
                frontend_framework='react',
                backend_framework='flask',
                database='sqlite'
            )

            result = self.generator.generate_app(spec, temp_dir)

            # 检查结果
            assert result['success'] is True
            assert result['app_path'] == temp_dir
            assert len(result['files_generated']) > 0
            assert 'next_steps' in result

            # 检查关键文件是否存在
            assert os.path.exists(os.path.join(temp_dir, 'README.md'))
            assert os.path.exists(os.path.join(temp_dir, 'Dockerfile'))
            assert os.path.exists(os.path.join(temp_dir, 'backend', 'run.py'))
            assert os.path.exists(os.path.join(temp_dir, 'frontend', 'package.json'))

    def test_get_setup_instructions(self):
        """测试获取设置说明"""
        spec = AppSpecification(
            name='TestApp',
            description='Test',
            tech_stack='react-flask',
            features=[],
            entities=[],
            frontend_framework='react',
            backend_framework='flask',
            database='sqlite'
        )

        instructions = self.generator._get_setup_instructions(spec)

        assert len(instructions) > 0
        assert any('backend' in step for step in instructions)
        assert any('frontend' in step for step in instructions)
        assert any('requirements.txt' in step for step in instructions)


def test_generate_app_from_prompt():
    """测试从提示生成应用"""
    from app_generator import generate_app_from_prompt

    with tempfile.TemporaryDirectory() as temp_dir:
        result = generate_app_from_prompt(
            "创建一个简单的任务管理应用",
            "react-flask"
        )

        # 即使是模拟生成，也应该返回结果结构
        assert 'success' in result
        assert 'app_path' in result
        assert 'files_generated' in result
        assert 'next_steps' in result


def test_template_validation():
    """测试模板验证"""
    generator = AppGenerator()

    # 有效的模板
    assert generator.get_template_info('react-flask') is not None

    # 无效的模板
    assert generator.get_template_info('invalid-template') is None


def test_app_spec_validation():
    """测试应用规格验证"""
    # 有效的规格
    spec = AppSpecification(
        name='ValidApp',
        description='Valid description',
        tech_stack='react-flask',
        features=['feature1'],
        entities=[{'name': 'entity1', 'fields': ['field1']}],
        frontend_framework='react',
        backend_framework='flask',
        database='sqlite'
    )

    assert spec.name == 'ValidApp'
    assert len(spec.features) > 0
    assert len(spec.entities) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
