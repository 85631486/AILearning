#!/usr/bin/env python3
"""
Week 4: 自主编码代理演示
展示代理协作完成编码任务的流程
"""

import sys
import os
from agents.base_agent import AgentOrchestrator, Task
from agents.test_agent import TestAgent
from agents.code_agent import CodeAgent


def demo_agent_collaboration():
    """演示代理协作流程"""
    print("🚀 Week 4: 自主编码代理演示")
    print("=" * 50)

    # 创建编排器
    orchestrator = AgentOrchestrator()

    # 注册代理
    test_agent = TestAgent()
    code_agent = CodeAgent()

    orchestrator.register_agent(test_agent)
    orchestrator.register_agent(code_agent)

    print("✅ 已注册代理:")
    for agent in [test_agent, code_agent]:
        status = agent.get_status()
        print(f"  - {status['name']} ({status['role']})")
        print(f"    能力: {', '.join(status['capabilities'])}")

    print("\n📋 创建任务...")

    # 创建任务
    task1 = orchestrator.create_task(
        task_id="implement_calculator",
        description="实现一个简单的计算器函数，支持加减乘除操作",
        requirements=[
            "函数名为calculator",
            "支持+、-、*、/操作",
            "处理除零错误",
            "返回计算结果"
        ],
        priority="high"
    )

    task2 = orchestrator.create_task(
        task_id="write_calculator_tests",
        description="为计算器函数编写完整的测试用例",
        requirements=[
            "测试所有操作",
            "测试边界情况",
            "测试错误处理"
        ],
        priority="medium"
    )

    print(f"✅ 创建任务: {task1.task_id}")
    print(f"✅ 创建任务: {task2.task_id}")

    print("\n🎯 分配任务...")

    # 分配任务
    orchestrator.assign_task("implement_calculator", "code_agent")
    orchestrator.assign_task("write_calculator_tests", "test_agent")

    print("✅ 任务已分配")

    print("\n⚙️  处理消息队列...")
    orchestrator.process_message_queue()

    print("✅ 消息处理完成")

    # 显示系统状态
    status = orchestrator.get_system_status()
    print("\n📊 系统状态:")
    print(f"  代理数量: {len(status['agents'])}")
    print(f"  任务数量: {status['total_tasks']}")
    print(f"  已完成任务: {status['completed_tasks']}")

    print("\n📝 任务详情:")
    for task_id, task_info in status['tasks'].items():
        print(f"  {task_id}: {task_info['status']} ({task_info['assigned_agent']})")
        if task_info['result']:
            print(f"    结果: {task_info['result']}")

    print("\n🎉 演示完成！")


def demo_individual_agents():
    """演示单个代理的功能"""
    print("\n🔧 个体代理演示")
    print("-" * 30)

    # 测试代理演示
    test_agent = TestAgent()
    print("🧪 测试代理演示:")

    # 分析示例代码
    sample_code = '''
def add_numbers(a, b):
    return a + b

def multiply(x, y):
    return x * y
'''

    analysis = test_agent.use_tool("analyze_code", code=sample_code)
    print(f"  代码分析: {analysis}")

    # 生成测试用例
    test_cases = test_agent.use_tool("generate_test_cases", code_path="sample.py")
    print(f"  生成的测试用例数量: {len(test_cases)}")

    # 代码代理演示
    code_agent = CodeAgent()
    print("\n💻 代码代理演示:")

    # 生成函数
    function_code = code_agent.use_tool("generate_function",
                                       name="process_data",
                                       params=["data", "operation"],
                                       description="处理数据并应用操作")
    print("  生成的函数代码:")
    print(function_code)

    # 分析代码结构
    analysis = code_agent.use_tool("analyze_code", code=function_code)
    print(f"  代码结构分析: {analysis}")


if __name__ == "__main__":
    demo_agent_collaboration()
    demo_individual_agents()
