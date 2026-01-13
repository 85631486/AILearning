#!/usr/bin/env python3
"""
Week 5: 本地终端自动化演示
展示本地脚本自动化和多任务并行处理的工作流程
"""

import sys
import os
from scripts.automation_framework import (
    default_orchestrator,
    TestRunnerScript,
    DocSyncScript,
    RefactorScript
)


def demo_individual_scripts():
    """演示单个脚本功能"""
    print("🔧 Week 5: 单个脚本演示")
    print("=" * 40)

    # 1. 测试运行器脚本
    print("\n📋 测试运行器脚本:")
    test_script = TestRunnerScript()
    test_script.set_parameter("coverage", True)
    test_script.set_parameter("verbose", True)

    result = test_script.execute()
    print(f"状态: {result['status']}")
    print(f"通过: {result['passed']}, 失败: {result['failed']}, 错误: {result['errors']}")
    if result.get('coverage'):
        print(f"覆盖率: {result['coverage']}%")
    print("输出:")
    for line in result['output']:
        print(f"  {line}")

    # 2. 文档同步脚本
    print("\n📖 文档同步脚本:")
    doc_script = DocSyncScript()
    doc_script.set_parameter("openapi_file", "sample_openapi.json")
    doc_script.set_parameter("output_file", "docs/generated_api.md")

    result = doc_script.execute()
    print(f"状态: {result['status']}")
    print(f"处理路由: {result['routes_processed']}")
    print(f"更新: {result['routes_updated']}, 新增: {result['routes_added']}, 删除: {result['routes_removed']}")
    print("输出:")
    for line in result['output']:
        print(f"  {line}")

    # 3. 重构脚本
    print("\n🔄 重构脚本:")
    refactor_script = RefactorScript()
    refactor_script.set_parameter("old_name", "extract")
    refactor_script.set_parameter("new_name", "parser")
    refactor_script.set_parameter("target_dir", "services/")

    result = refactor_script.execute()
    print(f"状态: {result['status']}")
    print(f"修改文件: {result['files_modified']}")
    print(f"更新导入: {result['imports_updated']}")
    if result.get('tests_passed') is not None:
        print(f"测试通过: {result['tests_passed']}")
    if result.get('lint_passed') is not None:
        print(f"代码检查通过: {result['lint_passed']}")
    print("输出:")
    for line in result['output']:
        print(f"  {line}")


def demo_parallel_workflows():
    """演示并行工作流"""
    print("\n⚡ 并行工作流演示")
    print("=" * 40)

    # 显示可用脚本
    print("📋 可用脚本:")
    scripts = default_orchestrator.get_available_scripts()
    for script in scripts:
        info = default_orchestrator.get_script_info(script)
        print(f"  - {script}: {info['description']}")

    # 显示可用工作流
    print("\n🔄 可用工作流:")
    workflows = ['full_ci', 'refactor_workflow']
    for workflow in workflows:
        status = default_orchestrator.get_workflow_status(workflow)
        print(f"  - {workflow}: {status['script_count']} 个脚本")

    # 执行完整CI工作流
    print("\n🚀 执行 'full_ci' 工作流:")
    result = default_orchestrator.execute_workflow_parallel("full_ci")

    print(f"工作流状态: {result['status']}")
    print(f"总脚本数: {result['total_scripts']}")
    print(f"完成脚本: {result['completed_scripts']}")
    print(f"失败脚本: {result['failed_scripts']}")
    print(".2f"
    print("脚本结果:")
    for script_result in result['script_results']:
        print(f"  {script_result['script_name']}: {script_result['status']}")
        if script_result['status'] == 'success':
            if 'passed' in script_result:
                print(f"    测试通过: {script_result['passed']}")
            if 'routes_processed' in script_result:
                print(f"    处理路由: {script_result['routes_processed']}")

    # 执行重构工作流
    print("\n🔄 执行 'refactor_workflow' 工作流:")
    result = default_orchestrator.execute_workflow_parallel("refactor_workflow")

    print(f"工作流状态: {result['status']}")
    print(f"总脚本数: {result['total_scripts']}")
    print(f"完成脚本: {result['completed_scripts']}")
    print(f"失败脚本: {result['failed_scripts']}")
    print(".2f"
    print("脚本结果:")
    for script_result in result['script_results']:
        print(f"  {script_result['script_name']}: {script_result['status']}")
        if script_result['status'] == 'success':
            if 'files_modified' in script_result:
                print(f"    修改文件: {script_result['files_modified']}")


def demo_script_parameters():
    """演示脚本参数配置"""
    print("\n⚙️ 脚本参数配置演示")
    print("=" * 40)

    # 创建测试脚本并展示参数
    script = TestRunnerScript()
    status = script.get_status()

    print(f"脚本: {status['name']}")
    print(f"描述: {status['description']}")
    print(f"参数数量: {status['parameter_count']}")
    print("参数详情:")
    for param_name, param_info in status['parameters'].items():
        print(f"  - {param_name}: {param_info['description']}")
        print(f"    默认值: {param_info['value']} (类型: {param_info['type']})")

    # 配置参数并执行
    print("\n🔧 配置参数并执行:")
    script.set_parameter("coverage", False)
    script.set_parameter("max_retries", 2)

    result = script.execute()
    print(f"执行结果: {result['status']}")
    print(f"尝试次数: {result['attempts']}")


def demo_workflow_creation():
    """演示自定义工作流创建"""
    print("\n🎨 自定义工作流创建演示")
    print("=" * 40)

    # 创建自定义工作流
    custom_workflow = ["doc_sync", "test_runner", "refactor_module"]
    default_orchestrator.create_workflow("custom_development", custom_workflow)

    print("✅ 创建自定义工作流: custom_development")
    print(f"包含脚本: {', '.join(custom_workflow)}")

    # 显示工作流信息
    status = default_orchestrator.get_workflow_status("custom_development")
    print(f"工作流详情: {status}")

    # 执行自定义工作流
    print("\n🚀 执行自定义工作流:")
    result = default_orchestrator.execute_workflow_parallel("custom_development")

    print(f"执行状态: {result['status']}")
    print(f"执行时间: {result['execution_time']:.2f}秒")
    print("各脚本状态:")
    for script_result in result['script_results']:
        status_icon = "✅" if script_result['status'] == 'success' else "❌"
        print(f"  {status_icon} {script_result['script_name']}: {script_result['status']}")


if __name__ == "__main__":
    print("🚀 Week 5: 本地终端自动化演示")
    print("=" * 50)

    try:
        demo_individual_scripts()
        demo_parallel_workflows()
        demo_script_parameters()
        demo_workflow_creation()

        print("\n🎉 演示完成！")
        print("\n💡 学习要点:")
        print("  - 本地脚本自动化可以提高开发效率")
        print("  - 并行处理允许多个任务同时执行")
        print("  - 参数化配置使脚本更加灵活")
        print("  - 工作流编排可以协调复杂任务")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
