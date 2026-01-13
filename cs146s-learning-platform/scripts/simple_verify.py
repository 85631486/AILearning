#!/usr/bin/env python3
"""
简单的作业集成验证脚本
不依赖Flask应用，直接检查文件结构
"""

import os
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (不存在)")
        return False

def check_directory_structure():
    """检查目录结构"""
    print("🔍 检查目录结构...")

    base_dir = Path(__file__).resolve().parents[1]

    # 检查主要目录
    dirs_to_check = [
        ("app/assignments", "作业根目录"),
        ("app/assignments/week1", "Week 1作业目录"),
        ("app/assignments/week2", "Week 2作业目录"),
        ("app/assignments/week3", "Week 3作业目录"),
        ("app/assignments/week4", "Week 4作业目录"),
        ("app/assignments/week5", "Week 5作业目录"),
        ("app/assignments/week6", "Week 6作业目录"),
        ("app/assignments/week7", "Week 7作业目录"),
        ("app/assignments/week8", "Week 8作业目录"),
        ("app/assignments/week1/data", "Week 1数据目录"),
        ("app/assignments/week2/app", "Week 2应用目录"),
        ("app/assignments/week2/tests", "Week 2测试目录"),
        ("app/assignments/week3/server", "Week 3服务器目录"),
        ("app/assignments/week3/tests", "Week 3测试目录"),
        ("app/assignments/week4/agents", "Week 4代理目录"),
        ("app/assignments/week4/tests", "Week 4测试目录"),
        ("app/assignments/week5/scripts", "Week 5脚本目录"),
        ("app/assignments/week5/tests", "Week 5测试目录"),
        ("app/assignments/week6/scanner", "Week 6扫描器目录"),
        ("app/assignments/week6/tests", "Week 6测试目录"),
        ("app/assignments/week7/code_review", "Week 7审查目录"),
        ("app/assignments/week7/tests", "Week 7测试目录"),
        ("app/assignments/week8/generator", "Week 8生成器目录"),
        ("app/assignments/week8/apps", "Week 8应用目录"),
        ("app/assignments/week8/tests", "Week 8测试目录"),
    ]

    all_good = True
    for dir_path, description in dirs_to_check:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✅ {description}: {dir_path}/")
        else:
            print(f"❌ {description}: {dir_path}/ (不存在)")
            all_good = False

    return all_good

def check_week1_files():
    """检查Week 1文件"""
    print("\n🔍 检查Week 1文件...")

    base_dir = Path(__file__).resolve().parents[1]
    week1_dir = base_dir / "app" / "assignments" / "week1"

    files_to_check = [
        ("k_shot_prompting.py", "K-shot提示脚本"),
        ("llm_client.py", "LLM客户端"),
        ("test_qwen_setup.py", "千问配置测试"),
    ]

    all_good = True
    for filename, description in files_to_check:
        filepath = week1_dir / filename
        if not check_file_exists(filepath, description):
            all_good = False

    # 检查文件内容
    llm_client = week1_dir / "llm_client.py"
    if llm_client.exists():
        try:
            with open(llm_client, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'class QwenClient' in content and 'dashscope.aliyuncs.com' in content:
                    print("✅ LLM客户端包含千问集成")
                else:
                    print("⚠️ LLM客户端可能缺少千问集成")
                    all_good = False
        except Exception as e:
            print(f"❌ 读取LLM客户端失败: {e}")
            all_good = False

    return all_good

def check_week2_files():
    """检查Week 2文件"""
    print("\n🔍 检查Week 2文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week2/app/main.py", "FastAPI主应用"),
        ("app/assignments/week2/app/db.py", "数据库模块"),
        ("app/assignments/week2/app/services/extract.py", "提取服务"),
        ("app/assignments/week2/tests/test_extract.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week3_files():
    """检查Week 3文件"""
    print("\n🔍 检查Week 3文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week3/server/main.py", "MCP服务器主程序"),
        ("app/assignments/week3/server/requirements.txt", "依赖文件"),
        ("app/assignments/week3/server/README.md", "说明文档"),
        ("app/assignments/week3/tests/test_weather_api.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week4_files():
    """检查Week 4文件"""
    print("\n🔍 检查Week 4文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week4/agents/base_agent.py", "代理基类"),
        ("app/assignments/week4/agents/test_agent.py", "测试代理"),
        ("app/assignments/week4/agents/code_agent.py", "代码代理"),
        ("app/assignments/week4/demo.py", "演示脚本"),
        ("app/assignments/week4/requirements.txt", "依赖文件"),
        ("app/assignments/week4/README.md", "说明文档"),
        ("app/assignments/week4/tests/test_agents.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week5_files():
    """检查Week 5文件"""
    print("\n🔍 检查Week 5文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week5/scripts/automation_framework.py", "自动化框架"),
        ("app/assignments/week5/demo.py", "演示脚本"),
        ("app/assignments/week5/requirements.txt", "依赖文件"),
        ("app/assignments/week5/README.md", "说明文档"),
        ("app/assignments/week5/tests/test_automation.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week6_files():
    """检查Week 6文件"""
    print("\n🔍 检查Week 6文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week6/scanner/security_scanner.py", "安全扫描器"),
        ("app/assignments/week6/demo.py", "演示脚本"),
        ("app/assignments/week6/requirements.txt", "依赖文件"),
        ("app/assignments/week6/README.md", "说明文档"),
        ("app/assignments/week6/tests/test_security_scanner.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week7_files():
    """检查Week 7文件"""
    print("\n🔍 检查Week 7文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week7/code_review/code_reviewer.py", "代码审查器"),
        ("app/assignments/week7/tasks/task_implementation.py", "任务实现"),
        ("app/assignments/week7/demo.py", "演示脚本"),
        ("app/assignments/week7/requirements.txt", "依赖文件"),
        ("app/assignments/week7/README.md", "说明文档"),
        ("app/assignments/week7/tests/test_code_reviewer.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_week8_files():
    """检查Week 8文件"""
    print("\n🔍 检查Week 8文件...")

    base_dir = Path(__file__).resolve().parents[1]

    files_to_check = [
        ("app/assignments/week8/generator/app_generator.py", "应用生成器"),
        ("app/assignments/week8/apps/taskmanager_react_flask/backend/app/__init__.py", "Flask后端"),
        ("app/assignments/week8/apps/taskmanager_react_flask/frontend/src/App.js", "React前端"),
        ("app/assignments/week8/demo.py", "演示脚本"),
        ("app/assignments/week8/requirements.txt", "依赖文件"),
        ("app/assignments/week8/README.md", "说明文档"),
        ("app/assignments/week8/tests/test_app_generator.py", "测试文件"),
    ]

    all_good = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_good = False

    return all_good

def check_seed_data():
    """检查种子数据"""
    print("\n🔍 检查种子数据...")

    base_dir = Path(__file__).resolve().parents[1]
    seed_file = base_dir / "data" / "seed_data.py"

    if not seed_file.exists():
        print("❌ 种子数据文件不存在")
        return False

    try:
        # 简单检查文件内容
        with open(seed_file, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = [
            ("'week_id': 1" in content, "包含Week 1数据"),
            ("'week_id': 2" in content, "包含Week 2数据"),
            ("'week_id': 3" in content, "包含Week 3数据"),
            ("'week_id': 4" in content, "包含Week 4数据"),
            ("'week_id': 5" in content, "包含Week 5数据"),
            ("'week_id': 6" in content, "包含Week 6数据"),
            ("'week_id': 7" in content, "包含Week 7数据"),
            ("'week_id': 8" in content, "包含Week 8数据"),
            ('k_shot_prompting.py' in content, "包含Week 1文件引用"),
            ('server/main.py' in content, "包含Week 3文件引用"),
            ('base_agent.py' in content, "包含Week 4文件引用"),
            ('automation_framework.py' in content, "包含Week 5文件引用"),
            ('security_scanner.py' in content, "包含Week 6文件引用"),
            ('code_reviewer.py' in content, "包含Week 7文件引用"),
            ('app_generator.py' in content, "包含Week 8文件引用"),
            ('assignment_files' in content, "包含扩展字段"),
            ('hints_sequence' in content, "包含分步提示"),
        ]

        all_good = True
        for condition, description in checks:
            if condition:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                all_good = False

        return all_good

    except Exception as e:
        print(f"❌ 读取种子数据失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 斯坦福CS146S作业集成验证")
    print("="*60)

    checks = [
        ("目录结构", check_directory_structure),
        ("Week 1文件", check_week1_files),
        ("Week 2文件", check_week2_files),
        ("Week 3文件", check_week3_files),
        ("Week 4文件", check_week4_files),
        ("Week 5文件", check_week5_files),
        ("Week 6文件", check_week6_files),
        ("Week 7文件", check_week7_files),
        ("Week 8文件", check_week8_files),
        ("种子数据", check_seed_data),
    ]

    results = {}
    for check_name, check_func in checks:
        print(f"\n📋 检查: {check_name}")
        results[check_name] = check_func()

    print("\n" + "="*60)
    print("📊 验证结果:")

    passed = 0
    total = len(results)

    for check_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {check_name}: {status}")
        if result:
            passed += 1

    print(f"\n📈 总体状态: {passed}/{total} 项通过")

    if passed == total:
        print("\n🎉 作业集成验证完全通过！")
        print("   斯坦福CS146S作业已成功集成到学习平台")
        print("\n💡 下一步:")
        print("   1. 运行数据库迁移")
        print("   2. 配置千问API密钥")
        print("   3. 测试练习功能")
        print("   4. 继续集成Week 3-8")
    else:
        print(f"\n⚠️  还有 {total - passed} 项需要修复")

    return passed == total

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
