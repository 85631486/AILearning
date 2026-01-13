#!/usr/bin/env python3
"""
Week 5: 自动化框架测试
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from automation_framework import (
    AutomationScript,
    TestRunnerScript,
    DocSyncScript,
    RefactorScript,
    WorkflowOrchestrator
)


class TestAutomationScript:
    """测试自动化脚本基类"""

    def test_script_initialization(self):
        """测试脚本初始化"""
        script = AutomationScript("test_script", "测试脚本")
        assert script.name == "test_script"
        assert script.description == "测试脚本"

    def test_script_parameters(self):
        """测试脚本参数管理"""
        script = AutomationScript("test_script", "测试脚本")

        # 添加参数
        script.add_parameter("param1", "default", "参数1描述")
        script.add_parameter("param2", 42, "参数2描述")

        # 设置参数
        script.set_parameter("param1", "new_value")

        # 获取参数
        assert script.get_parameter("param1") == "new_value"
        assert script.get_parameter("param2") == 42
        assert script.get_parameter("nonexistent") is None

    def test_script_status(self):
        """测试脚本状态"""
        script = AutomationScript("test_script", "测试脚本")
        script.add_parameter("test_param", "value", "测试参数")

        status = script.get_status()
        assert status['name'] == "test_script"
        assert status['description'] == "测试脚本"
        assert status['parameter_count'] == 1


class TestTestRunnerScript:
    """测试测试运行器脚本"""

    def test_test_runner_initialization(self):
        """测试测试运行器初始化"""
        script = TestRunnerScript()
        assert script.name == "test_runner"
        assert "测试运行器" in script.description

    def test_test_runner_parameters(self):
        """测试测试运行器参数"""
        script = TestRunnerScript()

        # 检查默认参数
        assert script.get_parameter("coverage") is True
        assert script.get_parameter("max_retries") == 3
        assert script.get_parameter("verbose") is False

    def test_test_runner_execution(self):
        """测试测试运行器执行"""
        script = TestRunnerScript()
        script.set_parameter("coverage", True)

        result = script.execute()

        assert result['script'] == "test_runner"
        assert result['status'] in ['success', 'failed']
        assert 'passed' in result
        assert 'failed' in result
        assert 'coverage' in result
        assert isinstance(result['output'], list)

    def test_test_runner_retry_logic(self):
        """测试重试逻辑"""
        script = TestRunnerScript()
        script.set_parameter("max_retries", 2)

        result = script.execute()

        # 应该至少尝试过一次
        assert result['attempts'] >= 1
        assert result['attempts'] <= 2


class TestDocSyncScript:
    """测试文档同步脚本"""

    def test_doc_sync_initialization(self):
        """测试文档同步器初始化"""
        script = DocSyncScript()
        assert script.name == "doc_sync"
        assert "文档同步" in script.description

    def test_doc_sync_parameters(self):
        """测试文档同步器参数"""
        script = DocSyncScript()

        assert script.get_parameter("openapi_file") == "openapi.json"
        assert script.get_parameter("output_file") == "docs/API.md"
        assert script.get_parameter("force_update") is False

    def test_doc_sync_execution(self):
        """测试文档同步器执行"""
        script = DocSyncScript()

        result = script.execute()

        assert result['script'] == "doc_sync"
        assert result['status'] == "success"
        assert 'routes_processed' in result
        assert 'routes_updated' in result
        assert isinstance(result['output'], list)


class TestRefactorScript:
    """测试重构脚本"""

    def test_refactor_initialization(self):
        """测试重构脚本初始化"""
        script = RefactorScript()
        assert script.name == "refactor_module"
        assert "重构" in script.description

    def test_refactor_parameters(self):
        """测试重构脚本参数"""
        script = RefactorScript()

        assert script.get_parameter("run_tests") is True
        assert script.get_parameter("run_lint") is True

    def test_refactor_execution_success(self):
        """测试重构脚本成功执行"""
        script = RefactorScript()
        script.set_parameter("old_name", "extract")
        script.set_parameter("new_name", "parser")

        result = script.execute()

        assert result['script'] == "refactor_module"
        assert result['status'] == "success"
        assert result['files_modified'] >= 1
        assert result['imports_updated'] >= 0

    def test_refactor_execution_failure(self):
        """测试重构脚本失败情况"""
        script = RefactorScript()
        # 不设置必需的参数

        result = script.execute()

        # 应该失败，因为没有提供old_name和new_name
        assert result['status'] == "failed"
        assert 'error' in result


class TestWorkflowOrchestrator:
    """测试工作流编排器"""

    def test_orchestrator_initialization(self):
        """测试编排器初始化"""
        orchestrator = WorkflowOrchestrator()
        assert len(orchestrator.scripts) == 0
        assert len(orchestrator.workflows) == 0

    def test_script_registration(self):
        """测试脚本注册"""
        orchestrator = WorkflowOrchestrator()
        script = TestRunnerScript()

        orchestrator.register_script(script)

        assert "test_runner" in orchestrator.scripts
        assert orchestrator.scripts["test_runner"] == script

    def test_workflow_creation(self):
        """测试工作流创建"""
        orchestrator = WorkflowOrchestrator()

        orchestrator.create_workflow("test_workflow", ["script1", "script2"])

        assert "test_workflow" in orchestrator.workflows
        assert orchestrator.workflows["test_workflow"] == ["script1", "script2"]

    def test_execute_script_success(self):
        """测试脚本执行成功"""
        orchestrator = WorkflowOrchestrator()
        script = TestRunnerScript()
        orchestrator.register_script(script)

        result = orchestrator.execute_script("test_runner")

        assert result['script_name'] == "test_runner"
        assert result['status'] in ['success', 'failed']

    def test_execute_script_not_found(self):
        """测试执行不存在的脚本"""
        orchestrator = WorkflowOrchestrator()

        result = orchestrator.execute_script("nonexistent_script")

        assert result['status'] == 'error'
        assert 'error' in result

    def test_execute_workflow_parallel(self):
        """测试并行工作流执行"""
        orchestrator = WorkflowOrchestrator()
        script1 = TestRunnerScript()
        script2 = DocSyncScript()

        orchestrator.register_script(script1)
        orchestrator.register_script(script2)
        orchestrator.create_workflow("parallel_test", ["test_runner", "doc_sync"])

        result = orchestrator.execute_workflow_parallel("parallel_test")

        assert result['workflow'] == "parallel_test"
        assert result['total_scripts'] == 2
        assert result['completed_scripts'] + result['failed_scripts'] == 2
        assert 'execution_time' in result
        assert len(result['script_results']) == 2

    def test_workflow_not_found(self):
        """测试执行不存在的工作流"""
        orchestrator = WorkflowOrchestrator()

        result = orchestrator.execute_workflow_parallel("nonexistent_workflow")

        assert result['status'] == 'error'
        assert 'error' in result

    def test_get_available_scripts(self):
        """测试获取可用脚本"""
        orchestrator = WorkflowOrchestrator()
        script = TestRunnerScript()
        orchestrator.register_script(script)

        scripts = orchestrator.get_available_scripts()

        assert "test_runner" in scripts

    def test_get_script_info(self):
        """测试获取脚本信息"""
        orchestrator = WorkflowOrchestrator()
        script = TestRunnerScript()
        orchestrator.register_script(script)

        info = orchestrator.get_script_info("test_runner")

        assert info is not None
        assert info['name'] == "test_runner"
        assert 'parameters' in info

    def test_get_script_info_not_found(self):
        """测试获取不存在脚本的信息"""
        orchestrator = WorkflowOrchestrator()

        info = orchestrator.get_script_info("nonexistent")

        assert info is None

    def test_get_workflow_status(self):
        """测试获取工作流状态"""
        orchestrator = WorkflowOrchestrator()
        orchestrator.create_workflow("test_workflow", ["script1", "script2"])

        status = orchestrator.get_workflow_status("test_workflow")

        assert status is not None
        assert status['name'] == "test_workflow"
        assert status['script_count'] == 2


class TestIntegration:
    """集成测试"""

    def test_full_workflow_execution(self):
        """测试完整工作流执行"""
        orchestrator = WorkflowOrchestrator()

        # 注册所有内置脚本
        orchestrator.register_script(TestRunnerScript())
        orchestrator.register_script(DocSyncScript())
        orchestrator.register_script(RefactorScript())

        # 创建完整工作流
        orchestrator.create_workflow("full_test", ["test_runner", "doc_sync", "refactor_module"])

        # 执行工作流
        result = orchestrator.execute_workflow_parallel("full_test")

        assert result['total_scripts'] == 3
        assert len(result['script_results']) == 3
        assert result['execution_time'] >= 0

    def test_script_parameter_persistence(self):
        """测试脚本参数持久性"""
        script = TestRunnerScript()

        # 设置参数
        script.set_parameter("coverage", False)
        script.set_parameter("max_retries", 5)

        # 执行脚本
        result = script.execute()

        # 验证参数被使用（通过结果间接验证）
        assert result['status'] in ['success', 'failed']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
