"""
Week 4: 测试代理 - 专门负责编写和运行测试的代理
"""

import os
import subprocess
import ast
import inspect
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentMessage, Task


class TestAgent(BaseAgent):
    """测试代理 - 负责编写和执行测试"""

    def __init__(self):
        super().__init__(
            name="test_agent",
            role="测试工程师",
            capabilities=["write_tests", "run_tests", "analyze_coverage", "identify_edge_cases"]
        )

        # 添加测试工具
        self.add_tool("analyze_code", self._analyze_code_for_tests)
        self.add_tool("generate_test_cases", self._generate_test_cases)
        self.add_tool("run_pytest", self._run_pytest)
        self.add_tool("check_coverage", self._check_coverage)

    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """处理消息"""
        if message.message_type == "task_assignment":
            task_data = message.content.get("task", {})
            task_description = task_data.get("description", "")

            if "test" in task_description.lower():
                # 处理测试相关任务
                result = self._handle_test_task(task_data)
                return AgentMessage(
                    sender=self.name,
                    receiver="orchestrator",
                    message_type="task_completed",
                    content={"task_id": task_data.get("task_id"), "result": result},
                    metadata={"original_task": task_data.get("task_id")}
                )

        return None

    def generate_response(self, task: str, context: Dict) -> str:
        """生成任务响应"""
        if "write test" in task.lower():
            return self._generate_test_code(context.get("code", ""), context.get("function_name", ""))
        elif "run test" in task.lower():
            return self._run_tests_for_code(context.get("code_path", ""))
        else:
            return f"测试代理：我可以帮助编写和运行测试。任务：{task}"

    def _handle_test_task(self, task_data: Dict) -> Dict[str, Any]:
        """处理测试任务"""
        task_id = task_data.get("task_id", "")
        description = task_data.get("description", "")

        result = {
            "task_id": task_id,
            "status": "processing",
            "test_results": [],
            "coverage": None
        }

        try:
            # 分析代码并生成测试
            code_path = description.split("for file:")[-1].strip() if "for file:" in description else "sample_code.py"

            test_cases = self.use_tool("generate_test_cases", code_path=code_path)
            result["test_cases_generated"] = len(test_cases)

            # 运行测试
            test_result = self.use_tool("run_pytest", test_path=f"test_{code_path}")
            result["test_results"] = test_result

            # 检查覆盖率
            coverage = self.use_tool("check_coverage", source_path=code_path)
            result["coverage"] = coverage

            result["status"] = "completed"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    def _analyze_code_for_tests(self, code: str) -> Dict[str, Any]:
        """分析代码以确定测试需求"""
        try:
            tree = ast.parse(code)

            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'returns': node.returns is not None,
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno
                    })

            return {
                'functions': functions,
                'classes': classes,
                'total_functions': len(functions),
                'total_classes': len(classes)
            }

        except SyntaxError as e:
            return {'error': f'代码语法错误: {e}'}

    def _generate_test_cases(self, code_path: str) -> List[Dict[str, Any]]:
        """生成测试用例"""
        # 简化的测试用例生成器
        test_cases = [
            {
                'function': 'example_function',
                'test_name': 'test_example_function_basic',
                'inputs': [1, 2],
                'expected': 3,
                'description': '测试基本功能'
            },
            {
                'function': 'example_function',
                'test_name': 'test_example_function_edge_case',
                'inputs': [0, 0],
                'expected': 0,
                'description': '测试边界情况'
            },
            {
                'function': 'example_function',
                'test_name': 'test_example_function_negative',
                'inputs': [-1, 1],
                'expected': 0,
                'description': '测试负数输入'
            }
        ]

        return test_cases

    def _run_pytest(self, test_path: str) -> Dict[str, Any]:
        """运行pytest"""
        try:
            # 在学习平台环境中，我们使用模拟的测试结果
            # 实际实现中会调用subprocess运行pytest

            return {
                'passed': 8,
                'failed': 0,
                'errors': 0,
                'total': 8,
                'success': True,
                'output': '8 passed, 0 failed'
            }

        except Exception as e:
            return {
                'passed': 0,
                'failed': 1,
                'errors': 1,
                'total': 1,
                'success': False,
                'error': str(e)
            }

    def _check_coverage(self, source_path: str) -> Dict[str, Any]:
        """检查测试覆盖率"""
        # 模拟覆盖率报告
        return {
            'total_coverage': 85.5,
            'lines_covered': 123,
            'lines_total': 144,
            'missing_lines': [45, 67, 89],
            'functions_covered': 12,
            'functions_total': 14
        }

    def _generate_test_code(self, code: str, function_name: str) -> str:
        """生成测试代码"""
        test_template = f'''
import pytest
from {function_name.split(".")[0]} import {function_name.split(".")[-1]}

def test_{function_name.split(".")[-1]}_basic():
    """测试基本功能"""
    result = {function_name.split(".")[-1]}(1, 2)
    assert result == 3

def test_{function_name.split(".")[-1]}_edge_cases():
    """测试边界情况"""
    # 添加边界情况测试
    assert {function_name.split(".")[-1]}(0, 0) == 0
    assert {function_name.split(".")[-1]}(-1, 1) == 0

def test_{function_name.split(".")[-1]}_types():
    """测试类型检查"""
    with pytest.raises(TypeError):
        {function_name.split(".")[-1]}("a", 1)
'''
        return test_template.strip()
