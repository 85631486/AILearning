#!/usr/bin/env python3
"""
数据种子文件 - 初始化数据库数据
"""

from app import create_app, db
from app.models import Week, Exercise, User, SystemConfig
import json

def seed_data():
    """填充初始数据"""
    app = create_app('development')
    with app.app_context():
        # 创建所有表
        db.create_all()

        # 填充周数据
        seed_weeks()

        # 填充练习数据
        seed_exercises()

        # 填充系统配置
        seed_system_config()

        print("✅ 数据初始化完成！")

def seed_weeks():
    """填充周学习内容"""
    weeks_data = [
        {
            'week_number': 1,
            'title': '提示工程技术',
            'description': '学习如何有效地设计和优化提示词，提升AI模型的输出质量',
            'content_path': 'week1/README.md'
        },
        {
            'week_number': 2,
            'title': '行动项提取器',
            'description': '构建能够从文本中提取行动项的AI应用',
            'content_path': 'week2/README.md'
        },
        {
            'week_number': 3,
            'title': '自定义MCP服务器',
            'description': '设计和实现自定义的MCP服务器架构',
            'content_path': 'week3/README.md'
        },
        {
            'week_number': 4,
            'title': '自主编码代理',
            'description': '开发具有自主编码能力的AI代理',
            'content_path': 'week4/README.md'
        },
        {
            'week_number': 5,
            'title': '多代理工作流',
            'description': '构建多代理协作的工作流系统',
            'content_path': 'week5/README.md'
        },
        {
            'week_number': 6,
            'title': '安全扫描与修复',
            'description': '实现代码安全扫描和自动修复功能',
            'content_path': 'week6/README.md'
        },
        {
            'week_number': 7,
            'title': 'AI代码审查',
            'description': '使用AI进行代码审查和质量评估',
            'content_path': 'week7/README.md'
        },
        {
            'week_number': 8,
            'title': '多栈应用构建',
            'description': '构建支持多种技术栈的完整应用',
            'content_path': 'week8/README.md'
        }
    ]

    for week_data in weeks_data:
        week = Week.query.filter_by(week_number=week_data['week_number']).first()
        if not week:
            week = Week(**week_data)
            db.session.add(week)

    db.session.commit()
    print("✅ 周数据填充完成")

def seed_exercises():
    """填充练习数据"""
    exercises_data = [
        # Week 1 练习 - 提示工程技术
        {
            'week_id': 1,
            'title': 'K-shot提示技术',
            'description': '学习使用少量示例提升AI模型输出的准确性和质量',
            'exercise_type': 'code',
            'difficulty': 'beginner',
            'initial_code': 'import os\nfrom dotenv import load_dotenv\nfrom llm_client import chat\n\nload_dotenv()\n\nNUM_RUNS_TIMES = 5\n\n# TODO: Fill this in!\nYOUR_SYSTEM_PROMPT = ""\n\nUSER_PROMPT = """\nReverse the order of letters in the following word. Only output the reversed word, no other text:\n\nhttpstatus\n"""\n\nEXPECTED_OUTPUT = "sutatsptth"',
            'test_code': 'def test_k_shot_prompt():\n    # 测试k-shot提示效果\n    assert YOUR_SYSTEM_PROMPT != ""  # 必须填写系统提示\n    # 这里可以添加更复杂的验证逻辑',
            'assignment_files': '["k_shot_prompting.py", "llm_client.py", "test_qwen_setup.py"]',
            'test_files': '["test_qwen_setup.py"]',
            'instructions': '修改k_shot_prompting.py中的YOUR_SYSTEM_PROMPT变量，设计有效的k-shot提示来解决单词反转任务。运行测试脚本验证效果。',
            'hints_sequence': '[{"step": 1, "hint": "考虑提供几个单词反转的示例"}, {"step": 2, "hint": "明确指示AI只输出反转后的单词"}, {"step": 3, "hint": "测试不同的提示策略"}]',
            'validation_rules': '{"require_system_prompt": true, "test_runs": 5, "expected_output": "sutatsptth"}',
            'points': 15
        },
        {
            'week_id': 1,
            'title': '思维链推理',
            'description': '掌握让AI逐步思考和推理的提示技术',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 思维链推理练习\n# 要求AI逐步分析问题并给出推理过程',
            'test_code': 'def test_chain_of_thought():\n    # 验证思维链推理的效果\n    pass',
            'assignment_files': '["chain_of_thought.py", "llm_client.py"]',
            'test_files': '[]',
            'instructions': '实现chain_of_thought.py中的提示，让AI通过逐步推理解决逻辑问题。',
            'hints_sequence': '[{"step": 1, "hint": "要求AI逐步解释推理过程"}, {"step": 2, "hint": "提供思维链的示例"}, {"step": 3, "hint": "测试不同复杂度的推理任务"}]',
            'points': 20
        },
        {
            'week_id': 1,
            'title': '工具调用',
            'description': '学习让AI使用工具和API进行复杂任务的提示技术',
            'exercise_type': 'code',
            'difficulty': 'advanced',
            'initial_code': '# 工具调用练习\n# 让AI学会使用外部工具解决问题',
            'test_code': 'def test_tool_calling():\n    # 验证工具调用功能\n    pass',
            'assignment_files': '["tool_calling.py", "llm_client.py"]',
            'test_files': '[]',
            'instructions': '实现tool_calling.py，让AI能够调用外部工具或API来解决问题。',
            'hints_sequence': '[{"step": 1, "hint": "定义可用的工具函数"}, {"step": 2, "hint": "设计工具调用的提示格式"}, {"step": 3, "hint": "实现工具结果的处理"}]',
            'points': 25
        },
        {
            'week_id': 1,
            'title': '自一致性提示',
            'description': '使用多种推理路径提高AI回答的一致性和准确性',
            'exercise_type': 'code',
            'difficulty': 'advanced',
            'initial_code': '# 自一致性提示练习\n# 通过多次推理提高答案质量',
            'test_code': 'def test_self_consistency():\n    # 验证自一致性效果\n    pass',
            'assignment_files': '["self_consistency_prompting.py", "llm_client.py"]',
            'test_files': '[]',
            'instructions': '实现self_consistency_prompting.py，使用多种推理路径来提高答案质量。',
            'hints_sequence': '[{"step": 1, "hint": "多次调用AI进行推理"}, {"step": 2, "hint": "比较不同推理路径的结果"}, {"step": 3, "hint": "选择最一致或最优的答案"}]',
            'points': 25
        },

        # Week 2 练习 - 行动项提取器
        {
            'week_id': 2,
            'title': 'FastAPI应用搭建',
            'description': '构建FastAPI + SQLite应用，实现笔记到行动项的自动转换',
            'exercise_type': 'project',
            'difficulty': 'intermediate',
            'initial_code': '# FastAPI应用框架\nfrom fastapi import FastAPI\nfrom app.db import init_db\nfrom app.routers import notes, action_items\n\ninit_db()\napp = FastAPI(title="Action Item Extractor")\n\napp.include_router(notes.router)\napp.include_router(action_items.router)',
            'test_code': '# FastAPI应用测试\nimport pytest\nfrom fastapi.testclient import TestClient\n\n# 测试代码会验证应用是否正确启动和响应',
            'assignment_files': '["app/main.py", "app/db.py", "app/services/extract.py", "tests/test_extract.py"]',
            'test_files': '["tests/test_extract.py"]',
            'instructions': '实现一个完整的FastAPI应用，包含笔记管理和行动项提取功能。使用SQLite作为数据库，创建一个REST API来管理笔记和行动项。',
            'hints_sequence': '[{"step": 1, "hint": "创建FastAPI应用实例和路由"}, {"step": 2, "hint": "实现SQLite数据库操作"}, {"step": 3, "hint": "创建笔记和行动项的CRUD API"}, {"step": 4, "hint": "添加行动项提取逻辑"}]',
            'validation_rules': '{"require_api_endpoints": true, "require_database": true, "require_tests": true}',
            'points': 25
        },
        {
            'week_id': 2,
            'title': 'LLM驱动提取',
            'description': '实现基于千问大模型的智能行动项提取功能',
            'exercise_type': 'code',
            'difficulty': 'advanced',
            'initial_code': 'import os\nfrom dotenv import load_dotenv\nfrom week1.llm_client import chat\n\nload_dotenv()\n\ndef extract_action_items_llm(text: str):\n    """使用LLM进行行动项提取"""\n    # TODO: 实现LLM驱动的提取逻辑\n    pass',
            'test_code': 'def test_extract_action_items_llm():\n    text = "明天开会讨论项目进展，需要准备演示材料。"\n    items = extract_action_items_llm(text)\n    assert isinstance(items, list)\n    assert len(items) > 0',
            'assignment_files': '["app/services/extract.py"]',
            'test_files': '["tests/test_extract.py"]',
            'instructions': '修改extract.py中的extract_action_items函数，实现基于千问大模型的行动项提取。使用结构化提示让AI返回JSON格式的行动项列表。',
            'hints_sequence': '[{"step": 1, "hint": "设计有效的系统提示词"}, {"step": 2, "hint": "实现JSON格式的结构化输出"}, {"step": 3, "hint": "添加错误处理和回退机制"}, {"step": 4, "hint": "测试不同类型的输入文本"}]',
            'validation_rules': '{"require_llm_integration": true, "require_json_output": true, "test_various_inputs": true}',
            'points': 30
        },
        {
            'week_id': 2,
            'title': '单元测试编写',
            'description': '为行动项提取功能编写完整的单元测试套件',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': 'import pytest\nfrom app.services.extract import extract_action_items, extract_action_items_llm\n\n# 编写测试用例覆盖各种输入场景',
            'test_code': '# 测试验证测试本身\nimport pytest\n\ndef test_test_structure():\n    # 这个测试验证测试文件结构正确\n    assert True',
            'assignment_files': '["tests/test_extract.py"]',
            'test_files': '["tests/test_extract.py"]',
            'instructions': '为extract_action_items和extract_action_items_llm函数编写全面的单元测试。测试应覆盖项目符号列表、关键字前缀、空输入等多种场景。',
            'hints_sequence': '[{"step": 1, "hint": "分析现有代码的边界情况"}, {"step": 2, "hint": "编写测试用例覆盖不同输入格式"}, {"step": 3, "hint": "测试错误处理和边界条件"}, {"step": 4, "hint": "验证测试覆盖率"}]',
            'validation_rules': '{"require_multiple_test_cases": true, "test_edge_cases": true, "test_error_handling": true}',
            'points': 20
        },

        # Week 3 练习 - 自定义MCP服务器
        {
            'week_id': 3,
            'title': '天气查询MCP服务器',
            'description': '构建一个天气查询的MCP服务器，实现工具封装和API集成',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# MCP服务器入口点\nfrom server.main import app\n\nif __name__ == "__main__":\n    # 启动MCP服务器\n    import asyncio\n    asyncio.run(app.run())',
            'test_code': '# MCP服务器测试\nfrom server.main import WeatherAPI\n\napi = WeatherAPI()\nweather = api.get_weather("北京")\nassert "temperature" in weather\nprint("✅ 天气API测试通过")',
            'assignment_files': '["server/main.py", "server/requirements.txt", "server/README.md", "tests/test_weather_api.py"]',
            'test_files': '["tests/test_weather_api.py"]',
            'instructions': '实现一个完整的MCP服务器，提供天气查询功能。服务器应包含至少两个工具：get_weather和get_supported_cities。使用模拟数据实现天气API，避免外部依赖。',
            'hints_sequence': '[{"step": 1, "hint": "创建WeatherAPI类封装天气数据"}, {"step": 2, "hint": "实现MCP工具定义和处理函数"}, {"step": 3, "hint": "添加错误处理和输入验证"}, {"step": 4, "hint": "编写完整的README文档"}]',
            'validation_rules': '{"require_mcp_tools": true, "require_weather_api": true, "require_documentation": true, "test_weather_tools": true}',
            'points': 30
        },
        {
            'week_id': 3,
            'title': 'MCP工具扩展',
            'description': '为MCP服务器添加更多工具和功能',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 扩展MCP服务器工具\ndef get_weather_forecast(city, days=3):\n    """获取天气预报"""\n    # 实现预报功能\n    pass\n\ndef search_nearby_places(city, place_type="restaurant"):\n    """搜索附近地点"""\n    # 实现地点搜索\n    pass',
            'test_code': 'def test_extended_tools():\n    # 测试扩展工具\n    assert True  # 占位符测试',
            'assignment_files': '["server/main.py"]',
            'test_files': '["tests/test_weather_api.py"]',
            'instructions': '扩展MCP服务器，添加天气预报和地点搜索工具。实现参数验证和错误处理。',
            'hints_sequence': '[{"step": 1, "hint": "添加新的工具定义到handle_list_tools"}, {"step": 2, "hint": "实现预报和搜索的数据结构"}, {"step": 3, "hint": "添加参数验证和类型检查"}]',
            'validation_rules': '{"require_additional_tools": true, "validate_parameters": true}',
            'points': 20
        },
        # Week 4 练习 - 自主编码代理
        {
            'week_id': 4,
            'title': '基础代理系统实现',
            'description': '实现一个基础的自主编码代理系统，包含代理基类和编排器',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# 代理系统入口\nfrom agents.base_agent import AgentOrchestrator\nfrom agents.test_agent import TestAgent\nfrom agents.code_agent import CodeAgent\n\n# 创建编排器和代理\norchestrator = AgentOrchestrator()\ntest_agent = TestAgent()\ncode_agent = CodeAgent()\n\n# 注册代理\norchestrator.register_agent(test_agent)\norchestrator.register_agent(code_agent)',
            'test_code': '# 代理系统测试\nfrom agents.base_agent import AgentOrchestrator\nfrom agents.test_agent import TestAgent\n\norchestrator = AgentOrchestrator()\nagent = TestAgent()\norchestrator.register_agent(agent)\n\n# 测试基本功能\nstatus = orchestrator.get_system_status()\nassert len(status["agents"]) == 1\nassert status["agents"]["test_agent"]["name"] == "test_agent"\nprint("✅ 代理系统测试通过")',
            'assignment_files': '["agents/base_agent.py", "agents/test_agent.py", "agents/code_agent.py", "demo.py", "tests/test_agents.py"]',
            'test_files': '["tests/test_agents.py"]',
            'instructions': '实现一个完整的代理系统，包含BaseAgent基类、TestAgent测试代理、CodeAgent代码代理和AgentOrchestrator编排器。系统应支持任务创建、分配和代理协作。',
            'hints_sequence': '[{"step": 1, "hint": "实现BaseAgent基类和AgentMessage类"}, {"step": 2, "hint": "创建TestAgent类，实现测试相关工具"}, {"step": 3, "hint": "创建CodeAgent类，实现代码编写工具"}, {"step": 4, "hint": "实现AgentOrchestrator编排器"}, {"step": 5, "hint": "添加消息传递和任务处理机制"}]',
            'validation_rules': '{"require_base_agent": true, "require_test_agent": true, "require_code_agent": true, "require_orchestrator": true, "test_agent_collaboration": true}',
            'points': 35
        },
        {
            'week_id': 4,
            'title': '代理协作任务',
            'description': '使用代理系统完成实际的编码任务，展示代理协作流程',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 代理协作示例\nfrom agents.base_agent import AgentOrchestrator, Task\nfrom agents.test_agent import TestAgent\nfrom agents.code_agent import CodeAgent\n\n# 创建系统\norchestrator = AgentOrchestrator()\norchestrator.register_agent(TestAgent())\norchestrator.register_agent(CodeAgent())\n\n# 创建任务\ntask = orchestrator.create_task(\n    "implement_sorting",\n    "实现一个排序函数，支持多种排序算法",\n    ["冒泡排序", "快速排序", "处理边界情况"],\n    "medium"\n)\n\n# 分配任务\norchestrator.assign_task("implement_sorting", "code_agent")',
            'test_code': '# 测试代理协作\ndef test_agent_task_completion():\n    from agents.base_agent import AgentOrchestrator\n    from agents.code_agent import CodeAgent\n    \n    orchestrator = AgentOrchestrator()\n    agent = CodeAgent()\n    orchestrator.register_agent(agent)\n    \n    # 创建并分配任务\n    task = orchestrator.create_task("test_task", "编写测试函数", ["基本功能"])\n    orchestrator.assign_task("test_task", "code_agent")\n    \n    # 处理消息\n    orchestrator.process_message_queue()\n    \n    # 检查结果\n    status = orchestrator.get_system_status()\n    assert status["completed_tasks"] >= 0\n    print("✅ 代理协作测试通过")',
            'assignment_files': '["agents/base_agent.py", "agents/code_agent.py", "demo.py"]',
            'test_files': '["tests/test_agents.py"]',
            'instructions': '使用已实现的代理系统完成一个实际的编码任务。创建一个排序函数的任务，分配给CodeAgent，然后验证任务完成情况。',
            'hints_sequence': '[{"step": 1, "hint": "创建排序函数的任务描述"}, {"step": 2, "hint": "使用CodeAgent生成排序函数代码"}, {"step": 3, "hint": "验证生成的代码是否正确"}, {"step": 4, "hint": "测试代理协作流程"}]',
            'validation_rules': '{"require_task_creation": true, "require_agent_assignment": true, "validate_code_generation": true, "test_collaboration": true}',
            'points': 25
        },
        # Week 5 练习 - 本地终端自动化
        {
            'week_id': 5,
            'title': '本地脚本自动化框架',
            'description': '构建一个本地终端自动化框架，支持脚本执行和并行工作流',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# 自动化框架入口\nfrom scripts.automation_framework import default_orchestrator, TestRunnerScript\n\n# 使用默认编排器\norchestrator = default_orchestrator\n\n# 执行测试脚本\nresult = orchestrator.execute_script("test_runner")\nprint(f"测试结果: {result}")',
            'test_code': '# 自动化框架测试\nfrom scripts.automation_framework import WorkflowOrchestrator, TestRunnerScript\n\norchestrator = WorkflowOrchestrator()\nscript = TestRunnerScript()\norchestrator.register_script(script)\n\n# 执行脚本\nresult = orchestrator.execute_script("test_runner")\nassert result["status"] in ["success", "failed"]\nprint("✅ 自动化框架测试通过")',
            'assignment_files': '["scripts/automation_framework.py", "demo.py", "tests/test_automation.py"]',
            'test_files': '["tests/test_automation.py"]',
            'instructions': '实现一个完整的本地终端自动化框架，包含AutomationScript基类、TestRunnerScript、DocSyncScript、RefactorScript等具体脚本，以及WorkflowOrchestrator编排器。',
            'hints_sequence': '[{"step": 1, "hint": "实现AutomationScript基类和参数管理系统"}, {"step": 2, "hint": "创建TestRunnerScript，支持测试执行和覆盖率"}, {"step": 3, "hint": "创建DocSyncScript，实现文档同步功能"}, {"step": 4, "hint": "创建RefactorScript，支持模块重构"}, {"step": 5, "hint": "实现WorkflowOrchestrator，支持并行工作流"}]',
            'validation_rules': '{"require_automation_script": true, "require_test_runner": true, "require_doc_sync": true, "require_refactor_script": true, "require_orchestrator": true, "test_parallel_execution": true}',
            'points': 35
        },
        {
            'week_id': 5,
            'title': '并行工作流实践',
            'description': '创建和执行包含多个脚本的并行工作流，展示自动化效率提升',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 并行工作流示例\nfrom scripts.automation_framework import default_orchestrator\n\n# 创建自定义工作流\norchestrator = default_orchestrator\norchestrator.create_workflow("dev_pipeline", ["test_runner", "doc_sync"])\n\n# 执行并行工作流\nresult = orchestrator.execute_workflow_parallel("dev_pipeline")\nprint(f"工作流状态: {result[\"status\"]}")\nprint(f"执行时间: {result[\"execution_time\"]:.2f}秒")',
            'test_code': '# 工作流测试\ndef test_parallel_workflow():\n    from scripts.automation_framework import WorkflowOrchestrator, TestRunnerScript, DocSyncScript\n    \n    orchestrator = WorkflowOrchestrator()\n    orchestrator.register_script(TestRunnerScript())\n    orchestrator.register_script(DocSyncScript())\n    \n    # 创建工作流\n    orchestrator.create_workflow("test_flow", ["test_runner", "doc_sync"])\n    \n    # 执行工作流\n    result = orchestrator.execute_workflow_parallel("test_flow")\n    \n    assert result["total_scripts"] == 2\n    assert "execution_time" in result\n    print("✅ 并行工作流测试通过")',
            'assignment_files': '["scripts/automation_framework.py", "demo.py"]',
            'test_files': '["tests/test_automation.py"]',
            'instructions': '创建包含多个自动化脚本的并行工作流，执行并分析性能提升。比较串行执行和并行执行的时间差异。',
            'hints_sequence': '[{"step": 1, "hint": "创建包含多个脚本的工作流"}, {"step": 2, "hint": "实现并行执行逻辑"}, {"step": 3, "hint": "测量执行时间"}, {"step": 4, "hint": "分析性能提升和资源利用"}]',
            'validation_rules': '{"require_workflow_creation": true, "require_parallel_execution": true, "measure_performance": true, "analyze_efficiency": true}',
            'points': 25
        },
        # Week 6 练习 - 安全漏洞扫描与修复
        {
            'week_id': 6,
            'title': '安全扫描器实现',
            'description': '实现一个Semgrep风格的安全漏洞扫描器，检测Python和JavaScript代码中的安全问题',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# 安全扫描器入口\nfrom scanner.security_scanner import scanner\n\n# 扫描示例文件\nfindings = scanner.scan_file("example.py")\nprint(f"发现 {len(findings)} 个安全问题")\n\nfor finding in findings:\n    print(f"- {finding.rule_name}: {finding.description}")',
            'test_code': '# 安全扫描器测试\nfrom scanner.security_scanner import SecurityScanner\n\nscanner = SecurityScanner()\n\n# 创建测试文件\nimport tempfile\nwith tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:\n    f.write("os.system(\'ls\')")\n    temp_file = f.name\n\nfindings = scanner.scan_file(temp_file)\nassert len(findings) > 0\nassert any("命令注入" in f.description for f in findings)\nprint("✅ 安全扫描器测试通过")',
            'assignment_files': '["scanner/security_scanner.py", "demo.py", "tests/test_security_scanner.py"]',
            'test_files': '["tests/test_security_scanner.py"]',
            'instructions': '实现一个完整的Semgrep风格安全扫描器，支持检测SQL注入、命令注入、XSS、硬编码密钥等常见安全漏洞。扫描器应能生成详细的安全报告。',
            'hints_sequence': '[{"step": 1, "hint": "实现SecurityScanner类和规则引擎"}, {"step": 2, "hint": "添加Python安全规则（SQL注入、命令注入、eval等）"}, {"step": 3, "hint": "添加JavaScript安全规则（XSS、eval等）"}, {"step": 4, "hint": "实现扫描报告生成功能"}, {"step": 5, "hint": "创建VulnerabilityFixer类提供修复建议"}]',
            'validation_rules': '{"require_security_scanner": true, "support_python_scanning": true, "support_js_scanning": true, "generate_reports": true, "provide_fixes": true, "test_vulnerability_detection": true}',
            'points': 35
        },
        {
            'week_id': 6,
            'title': '安全修复实践',
            'description': '使用安全扫描器识别漏洞并实施修复，学习安全编码实践',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 安全修复示例\nfrom scanner.security_scanner import scanner, fixer\n\n# 扫描项目\nfindings = scanner.scan_directory(".")\nprint(f"发现 {len(findings)} 个安全问题")\n\n# 显示前3个高危问题\nhigh_severity = [f for f in findings if f.severity == "high"][:3]\nfor finding in high_severity:\n    print(f"\\n🔴 {finding.rule_name}")\n    print(f"   文件: {finding.file_path}:{finding.line_number}")\n    print(f"   问题: {finding.description}")\n    \n    # 获取修复建议\n    fix = fixer.get_fix_suggestion(finding.rule_id)\n    if fix:\n        print(f"   修复建议: {fix[\'description\']}")',
            'test_code': '# 安全修复测试\ndef test_security_fixes():\n    from scanner.security_scanner import scanner, fixer\n    \n    # 扫描示例代码\n    import tempfile\n    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:\n        f.write(\'\'\'\nquery = f"SELECT * FROM users WHERE id = {user_id}"\nos.system(f"ls {path}")\npassword = "secret123"\n\'\'\')\n        temp_file = f.name\n    \n    findings = scanner.scan_file(temp_file)\n    \n    # 应该发现多个安全问题\n    assert len(findings) >= 3\n    \n    # 检查修复建议\n    for finding in findings[:2]:  # 测试前两个\n        fix = fixer.get_fix_suggestion(finding.rule_id)\n        assert fix is not None\n        assert "description" in fix\n    \n    print("✅ 安全修复测试通过")',
            'assignment_files': '["scanner/security_scanner.py", "demo.py"]',
            'test_files': '["tests/test_security_scanner.py"]',
            'instructions': '使用安全扫描器扫描代码库，识别至少3个安全漏洞，并为每个漏洞提供修复方案。记录修复前后的代码差异和安全改进。',
            'hints_sequence': '[{"step": 1, "hint": "运行安全扫描器识别漏洞"}, {"step": 2, "hint": "分析发现的问题和严重程度"}, {"step": 3, "hint": "为每个漏洞选择合适的修复策略"}, {"step": 4, "hint": "实施修复并验证效果"}, {"step": 5, "hint": "记录修复过程和安全改进"}]',
            'validation_rules': '{"require_vulnerability_scan": true, "identify_three_vulnerabilities": true, "provide_fix_solutions": true, "implement_fixes": true, "validate_fix_effectiveness": true}',
            'points': 25
        },
        # Week 7 练习 - AI辅助代码审查
        {
            'week_id': 7,
            'title': 'AI代码审查器实现',
            'description': '实现一个AI辅助代码审查系统，结合自动化检查和手动审查指导',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# AI代码审查器入口\nfrom code_review.code_reviewer import ai_reviewer\n\n# 审查示例文件\ncomments = ai_reviewer.review_file("example.py")\nprint(f"发现 {len(comments)} 个审查意见")\n\nfor comment in comments:\n    print(f"- {comment.severity}: {comment.message}")',
            'test_code': '# 代码审查器测试\nfrom code_review.code_reviewer import AICodeReviewer\n\nreviewer = AICodeReviewer()\n\n# 创建测试文件\nimport tempfile\nwith tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:\n    f.write(\'\'\'\n# TODO: 实现这个功能\neval("print(1)")  # 危险代码\ndef long_function():\n    pass  # 故意很长的函数\n\'\'\' * 20)\n    temp_file = f.name\n\ncomments = reviewer.review_file(temp_file)\nassert len(comments) > 0\nassert any("TODO" in c.message for c in comments)\nprint("✅ 代码审查器测试通过")',
            'assignment_files': '["code_review/code_reviewer.py", "demo.py", "tests/test_code_reviewer.py"]',
            'test_files': '["tests/test_code_reviewer.py"]',
            'instructions': '实现一个完整的AI辅助代码审查系统，支持Python和JavaScript代码的自动化检查，包括安全漏洞、代码质量、文档完整性等方面的审查。',
            'hints_sequence': '[{"step": 1, "hint": "实现AICodeReviewer类和规则系统"}, {"step": 2, "hint": "添加Python代码审查规则（函数长度、文档字符串、安全问题等）"}, {"step": 3, "hint": "添加JavaScript代码审查规则（XSS、调试代码等）"}, {"step": 4, "hint": "实现审查报告生成功能"}, {"step": 5, "hint": "添加手动审查指导和PR模板"}]',
            'validation_rules': '{"require_ai_reviewer": true, "support_python_review": true, "support_js_review": true, "generate_reports": true, "provide_manual_guidance": true, "test_review_functionality": true}',
            'points': 35
        },
        {
            'week_id': 7,
            'title': '代码审查实践',
            'description': '使用AI审查工具分析代码质量，并与手动审查进行对比',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 代码审查实践\nfrom code_review.code_reviewer import ai_reviewer, manual_reviewer\n\n# AI审查代码\ncomments = ai_reviewer.review_file("target_code.py")\nprint(f"AI发现 {len(comments)} 个问题")\n\n# 显示按严重程度分组的问题\nseverity_count = {"error": 0, "warning": 0, "info": 0}\nfor comment in comments:\n    severity_count[comment.severity] += 1\n\nprint(f"错误: {severity_count[\'error\']}, 警告: {severity_count[\'warning\']}, 信息: {severity_count[\'info\']}")\n\n# 获取手动审查清单\nchecklist = manual_reviewer.get_checklist()\nprint("\\n手动审查清单:")\nfor category, questions in checklist.items():\n    print(f"\\n{category.upper()}:")\n    for question in questions[:2]:  # 只显示前2个问题\n        print(f"  • {question}")',
            'test_code': '# 审查实践测试\ndef test_code_review_practice():\n    from code_review.code_reviewer import ai_reviewer, manual_reviewer\n    \n    # 创建测试代码\n    import tempfile\n    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:\n        f.write(\'\'\'\ndef bad_function():\n    # 缺少文档字符串\n    eval("code")  # 危险操作\n    return "done"\n\'\'\')\n        temp_file = f.name\n    \n    # AI审查\n    comments = ai_reviewer.review_file(temp_file)\n    assert len(comments) >= 2  # 至少发现文档和安全问题\n    \n    # 手动审查指导\n    checklist = manual_reviewer.get_checklist()\n    assert "correctness" in checklist\n    assert len(checklist["correctness"]) > 0\n    \n    print("✅ 代码审查实践测试通过")',
            'assignment_files': '["code_review/code_reviewer.py", "demo.py"]',
            'test_files': '["tests/test_code_reviewer.py"]',
            'instructions': '使用AI代码审查器分析提供的代码示例，对发现的问题进行分类和优先级排序。同时学习手动代码审查的方法和最佳实践。',
            'hints_sequence': '[{"step": 1, "hint": "运行AI审查器分析代码质量"}, {"step": 2, "hint": "按严重程度对问题进行分类"}, {"step": 3, "hint": "学习手动审查清单的使用"}, {"step": 4, "hint": "对比AI和手动审查的差异"}, {"step": 5, "hint": "制定代码审查改进计划"}]',
            'validation_rules': '{"run_ai_review": true, "categorize_issues": true, "use_manual_checklist": true, "compare_methods": true, "create_improvement_plan": true}',
            'points': 25
        },

        # Week 4 练习 - 自主编码代理
        {
            'week_id': 4,
            'title': 'AI编码代理基础',
            'description': '实现基本的AI编码代理功能',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': 'class AICodingAgent:\n    """AI编码代理"""\n    def __init__(self):\n        self.llm_client = None\n\n    def generate_code(self, requirements):\n        """根据需求生成代码"""\n        # 实现AI编码逻辑\n        pass',
            'test_code': 'def test_ai_agent():\n    agent = AICodingAgent()\n    code = agent.generate_code("print hello world")\n    assert "print" in code',
            'points': 20
        },

        # Week 5 练习 - 多代理工作流
        {
            'week_id': 5,
            'title': '多代理协作',
            'description': '实现多个AI代理之间的协作工作流',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': 'class MultiAgentWorkflow:\n    """多代理工作流"""\n    def __init__(self):\n        self.agents = []\n\n    def add_agent(self, agent):\n        """添加代理"""\n        self.agents.append(agent)\n\n    def execute_workflow(self, task):\n        """执行工作流"""\n        # 实现多代理协作逻辑\n        pass',
            'test_code': '# 多代理工作流测试\nworkflow = MultiAgentWorkflow()\n# 添加测试代理\nresult = workflow.execute_workflow("开发一个待办事项应用")\nassert result is not None',
            'points': 30
        },

        # Week 6 练习 - 安全扫描
        {
            'week_id': 6,
            'title': '代码安全扫描',
            'description': '实现代码安全漏洞扫描功能',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': 'class SecurityScanner:\n    """代码安全扫描器"""\n    def __init__(self):\n        self.vulnerabilities = []\n\n    def scan_code(self, code):\n        """扫描代码安全问题"""\n        # 实现安全扫描逻辑\n        pass\n\n    def generate_report(self):\n        """生成安全报告"""\n        return self.vulnerabilities',
            'test_code': 'def test_security_scan():\n    scanner = SecurityScanner()\n    issues = scanner.scan_code("eval(user_input)")\n    assert len(issues) > 0',
            'points': 25
        },

        # Week 7 练习 - AI代码审查
        {
            'week_id': 7,
            'title': 'AI代码审查',
            'description': '使用AI进行代码质量评估和改进建议',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': 'class AICodeReviewer:\n    """AI代码审查器"""\n    def __init__(self):\n        self.llm_client = None\n\n    def review_code(self, code):\n        """审查代码质量"""\n        # 实现AI代码审查逻辑\n        pass\n\n    def suggest_improvements(self, code):\n        """提供改进建议"""\n        # 实现改进建议逻辑\n        pass',
            'test_code': 'def test_code_review():\n    reviewer = AICodeReviewer()\n    feedback = reviewer.review_code("def bad_function(): pass")\n    assert "docstring" in feedback.lower()',
            'points': 20
        },

        # Week 8 练习 - 多技术栈AI加速Web应用构建
        {
            'week_id': 8,
            'title': 'AI应用生成器实现',
            'description': '实现一个AI驱动的应用生成器，支持多技术栈Web应用自动生成',
            'exercise_type': 'project',
            'difficulty': 'advanced',
            'initial_code': '# AI应用生成器入口\nfrom generator.app_generator import generator\n\n# 定义应用规格\nspec = {\n    "name": "TaskManager",\n    "description": "任务管理系统",\n    "tech_stack": "react-flask",\n    "features": ["任务管理", "用户管理"],\n    "entities": [\n        {"name": "task", "fields": ["title", "description", "status"]},\n        {"name": "user", "fields": ["name", "email"]}\n    ],\n    "frontend_framework": "react",\n    "backend_framework": "flask",\n    "database": "sqlite"\n}\n\n# 生成应用\nresult = generator.generate_app(spec, "generated_app")\nprint(f"生成成功: {result[\'success\']}")',
            'test_code': '# 应用生成器测试\nfrom generator.app_generator import AppGenerator, AppSpecification\n\ngenerator = AppGenerator()\nspec = AppSpecification(\n    name="TestApp",\n    description="Test application",\n    tech_stack="react-flask",\n    features=["CRUD operations"],\n    entities=[{"name": "item", "fields": ["name"]}], \n    frontend_framework="react",\n    backend_framework="flask",\n    database="sqlite"\n)\n\nresult = generator.generate_app(spec, "test_output")\nassert result["success"] is True\nassert len(result["files_generated"]) > 0\nprint("✅ 应用生成器测试通过")',
            'assignment_files': '["generator/app_generator.py", "demo.py", "tests/test_app_generator.py"]',
            'test_files': '["tests/test_app_generator.py"]',
            'instructions': '实现一个完整的AI应用生成器，支持React+Flask、Vue+FastAPI、Angular+Django等多种技术栈组合，能够根据应用规格自动生成完整的前后端代码、数据库模型、API接口和前端组件。',
            'hints_sequence': '[{"step": 1, "hint": "实现AppGenerator类和模板系统"}, {"step": 2, "hint": "添加Flask后端生成器（模型、路由、配置）"}, {"step": 3, "hint": "添加React前端生成器（组件、API调用、路由）"}, {"step": 4, "hint": "实现配置文件生成（Docker、环境变量等）"}, {"step": 5, "hint": "添加文档和部署配置自动生成"}]',
            'validation_rules': '{"require_app_generator": true, "support_multiple_stacks": true, "generate_complete_apps": true, "include_deployment_config": true, "test_generation_functionality": true}',
            'points': 40
        },
        {
            'week_id': 8,
            'title': '多技术栈应用构建实践',
            'description': '使用AI生成器在3个不同技术栈中构建相同的Web应用',
            'exercise_type': 'code',
            'difficulty': 'intermediate',
            'initial_code': '# 多技术栈应用构建\nfrom generator.app_generator import generator, AppSpecification\n\n# 技术栈列表\ntech_stacks = ["react-flask", "vue-fastapi", "angular-django"]\n\n# 应用规格\nspec = {\n    "name": "TaskManager",\n    "description": "跨技术栈任务管理系统",\n    "features": ["任务CRUD", "用户管理", "状态跟踪"],\n    "entities": [\n        {"name": "task", "fields": ["title", "description", "status", "priority"]},\n        {"name": "user", "fields": ["name", "email"]}\n    ]\n}\n\n# 为每个技术栈生成应用\nfor tech_stack in tech_stacks:\n    print(f"\\n🔧 生成 {tech_stack} 应用...")\n    \n    app_spec = AppSpecification(\n        name=f"TaskManager_{tech_stack.replace(\'-\', \'_\')}",\n        description=spec["description"],\n        tech_stack=tech_stack,\n        features=spec["features"],\n        entities=spec["entities"],\n        frontend_framework=tech_stack.split("-")[0],\n        backend_framework=tech_stack.split("-")[1],\n        database="sqlite"\n    )\n    \n    result = generator.generate_app(app_spec, f"generated_apps/{app_spec.name}")\n    print(f"✅ {tech_stack} 应用生成完成")',
            'test_code': '# 多技术栈构建测试\ndef test_multi_stack_generation():\n    from generator.app_generator import generator, AppSpecification\n    \n    # 测试两个主要技术栈\n    tech_stacks = ["react-flask", "vue-fastapi"]\n    \n    for tech_stack in tech_stacks:\n        spec = AppSpecification(\n            name=f"TestApp_{tech_stack}",\n            description="Test multi-stack app",\n            tech_stack=tech_stack,\n            features=["Basic CRUD"],\n            entities=[{"name": "item", "fields": ["name"]}], \n            frontend_framework=tech_stack.split("-")[0],\n            backend_framework=tech_stack.split("-")[1],\n            database="sqlite"\n        )\n        \n        result = generator.generate_app(spec, f"test_output_{tech_stack.replace(\'-\', \'_\')}")\n        assert result["success"] is True\n        assert len(result["files_generated"]) > 5  # 至少生成5个文件\n    \n    print("✅ 多技术栈构建测试通过")',
            'assignment_files': '["generator/app_generator.py", "apps/taskmanager_react_flask/backend/app/__init__.py", "apps/taskmanager_react_flask/frontend/src/App.js", "demo.py"]',
            'test_files': '["tests/test_app_generator.py"]',
            'instructions': '使用AI应用生成器在至少3个不同技术栈中构建相同的任务管理系统，对比不同技术栈的优缺点和适用场景。',
            'hints_sequence': '[{"step": 1, "hint": "选择3个不同的技术栈组合"}, {"step": 2, "hint": "定义统一的应用规格和功能需求"}, {"step": 3, "hint": "为每个技术栈生成完整应用"}, {"step": 4, "hint": "测试各应用的基本功能"}, {"step": 5, "hint": "对比技术栈的差异和适用场景"}]',
            'validation_rules': '{"generate_three_stacks": true, "test_basic_functionality": true, "compare_tech_stacks": true, "document_findings": true, "include_deployment_guide": true}',
            'points': 30
        }
    ]

    for exercise_data in exercises_data:
        exercise = Exercise.query.filter_by(
            week_id=exercise_data['week_id'],
            title=exercise_data['title']
        ).first()

        if not exercise:
            exercise = Exercise(**exercise_data)
            db.session.add(exercise)

    db.session.commit()
    print("✅ 练习数据填充完成")

def seed_system_config():
    """填充系统配置"""
    configs_data = [
        {
            'config_key': 'max_execution_time',
            'config_value': '30',
            'config_type': 'int',
            'description': '代码执行最大时间限制（秒）'
        },
        {
            'config_key': 'max_memory_mb',
            'config_value': '100',
            'config_type': 'int',
            'description': '代码执行最大内存限制（MB）'
        },
        {
            'config_key': 'max_cpu_time',
            'config_value': '10',
            'config_type': 'int',
            'description': '代码执行最大CPU时间限制（秒）'
        },
        {
            'config_key': 'ai_model',
            'config_value': 'qwen-turbo',
            'config_type': 'string',
            'description': '默认AI模型'
        },
        {
            'config_key': 'max_conversation_history',
            'config_value': '50',
            'config_type': 'int',
            'description': '最大对话历史记录数'
        }
    ]

    for config_data in configs_data:
        config = SystemConfig.query.filter_by(
            config_key=config_data['config_key']
        ).first()

        if not config:
            config = SystemConfig(**config_data)
            db.session.add(config)

    db.session.commit()
    print("✅ 系统配置填充完成")

if __name__ == '__main__':
    seed_data()
