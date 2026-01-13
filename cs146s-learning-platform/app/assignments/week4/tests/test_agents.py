#!/usr/bin/env python3
"""
Week 4: 代理系统测试
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# 添加agents目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from base_agent import BaseAgent, AgentMessage, Task, AgentOrchestrator
from test_agent import TestAgent
from code_agent import CodeAgent


class TestBaseAgent:
    """测试基础代理功能"""

    def test_agent_initialization(self):
        """测试代理初始化"""
        agent = TestAgent()
        assert agent.name == "test_agent"
        assert agent.role == "测试工程师"
        assert "write_tests" in agent.capabilities

    def test_agent_status(self):
        """测试代理状态获取"""
        agent = TestAgent()
        status = agent.get_status()

        assert status['name'] == "test_agent"
        assert status['role'] == "测试工程师"
        assert status['tools_count'] >= 4  # 至少有4个工具

    def test_agent_memory(self):
        """测试代理记忆功能"""
        agent = TestAgent()
        message = AgentMessage("sender", "receiver", "test", "content")

        agent.remember(message)
        memories = agent.recall()

        assert len(memories) == 1
        assert memories[0].content == "content"


class TestTestAgent:
    """测试测试代理"""

    def test_test_agent_tools(self):
        """测试测试代理的工具"""
        agent = TestAgent()

        # 测试代码分析
        sample_code = '''
def add(a, b):
    return a + b

class Calculator:
    pass
'''

        analysis = agent.use_tool("analyze_code", code=sample_code)
        assert analysis['total_functions'] == 1
        assert analysis['total_classes'] == 1

    def test_generate_test_cases(self):
        """测试测试用例生成"""
        agent = TestAgent()
        test_cases = agent.use_tool("generate_test_cases", code_path="test.py")

        assert isinstance(test_cases, list)
        assert len(test_cases) > 0
        assert 'function' in test_cases[0]
        assert 'test_name' in test_cases[0]

    def test_run_pytest_simulation(self):
        """测试pytest运行模拟"""
        agent = TestAgent()
        result = agent.use_tool("run_pytest", test_path="test_sample.py")

        assert result['total'] > 0
        assert 'passed' in result
        assert 'success' in result


class TestCodeAgent:
    """测试代码代理"""

    def test_code_agent_tools(self):
        """测试代码代理的工具"""
        agent = CodeAgent()

        # 测试函数生成
        code = agent.use_tool("generate_function",
                             name="test_func",
                             params=["x", "y"],
                             description="测试函数")
        assert "def test_func(x, y):" in code
        assert '"""测试函数"""' in code

    def test_code_analysis(self):
        """测试代码分析"""
        agent = CodeAgent()
        sample_code = '''
def func1(a, b):
    return a + b

def func2(x):
    return x * 2

class MyClass:
    pass
'''

        analysis = agent.use_tool("analyze_code", code=sample_code)
        assert analysis['total_functions'] == 2
        assert analysis['total_classes'] == 1

    def test_refactor_code(self):
        """测试代码重构"""
        agent = CodeAgent()
        original_code = "x = 1\ny = 2\nz = x + y"

        refactored = agent.use_tool("refactor_code", code=original_code)
        # 简单的重构示例
        assert isinstance(refactored, str)


class TestAgentOrchestrator:
    """测试代理编排器"""

    def test_orchestrator_initialization(self):
        """测试编排器初始化"""
        orchestrator = AgentOrchestrator()
        assert len(orchestrator.agents) == 0
        assert len(orchestrator.tasks) == 0

    def test_register_agent(self):
        """测试代理注册"""
        orchestrator = AgentOrchestrator()
        agent = TestAgent()

        orchestrator.register_agent(agent)
        assert "test_agent" in orchestrator.agents
        assert orchestrator.agents["test_agent"] == agent

    def test_create_and_assign_task(self):
        """测试任务创建和分配"""
        orchestrator = AgentOrchestrator()
        agent = TestAgent()
        orchestrator.register_agent(agent)

        # 创建任务
        task = orchestrator.create_task(
            "test_task",
            "测试任务",
            ["需求1", "需求2"]
        )

        assert task.task_id == "test_task"
        assert task.status == "pending"

        # 分配任务
        orchestrator.assign_task("test_task", "test_agent")

        # 检查任务状态
        assigned_task = orchestrator.tasks["test_task"]
        assert assigned_task.status == "assigned"
        assert assigned_task.assigned_agent == "test_agent"

    def test_message_processing(self):
        """测试消息处理"""
        orchestrator = AgentOrchestrator()
        agent = TestAgent()
        orchestrator.register_agent(agent)

        # 创建任务分配消息
        message = AgentMessage(
            sender="orchestrator",
            receiver="test_agent",
            message_type="task_assignment",
            content={"task": {"task_id": "msg_test", "description": "消息测试"}}
        )

        # 发送消息
        orchestrator.send_message(message)

        # 处理队列
        orchestrator.process_message_queue()

        # 检查是否有响应消息
        assert len(orchestrator.message_queue) >= 1


class TestTask:
    """测试任务类"""

    def test_task_creation(self):
        """测试任务创建"""
        task = Task("test_id", "测试描述", ["需求1"], "high")

        assert task.task_id == "test_id"
        assert task.description == "测试描述"
        assert task.priority == "high"
        assert task.status == "pending"

    def test_task_lifecycle(self):
        """测试任务生命周期"""
        task = Task("lifecycle_test", "生命周期测试", ["需求"])

        # 初始状态
        assert task.status == "pending"

        # 分配
        task.assign_to("test_agent")
        assert task.status == "assigned"
        assert task.assigned_agent == "test_agent"

        # 完成
        task.complete("成功完成")
        assert task.status == "completed"
        assert task.result == "成功完成"
        assert task.completed_at is not None

        # 失败
        task.fail("测试失败")
        assert task.status == "failed"
        assert task.result == "测试失败"


def test_agent_collaboration():
    """测试代理协作"""
    orchestrator = AgentOrchestrator()

    # 注册代理
    test_agent = TestAgent()
    code_agent = CodeAgent()
    orchestrator.register_agent(test_agent)
    orchestrator.register_agent(code_agent)

    # 创建并分配任务
    task1 = orchestrator.create_task("collab1", "编写计算器函数", ["基本运算"])
    task2 = orchestrator.create_task("collab2", "测试计算器函数", ["单元测试"])

    orchestrator.assign_task("collab1", "code_agent")
    orchestrator.assign_task("collab2", "test_agent")

    # 处理消息
    orchestrator.process_message_queue()

    # 检查系统状态
    status = orchestrator.get_system_status()
    assert len(status['agents']) == 2
    assert status['total_tasks'] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
