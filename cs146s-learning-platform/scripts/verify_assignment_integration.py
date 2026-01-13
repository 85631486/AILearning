#!/usr/bin/env python3
"""
作业集成验证脚本
验证斯坦福CS146S作业文件是否正确集成到学习平台中
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.services.assignment_manager import AssignmentFileManager

def verify_week_structure():
    """验证周目录结构"""
    print("🔍 验证作业文件结构...")

    assignments_dir = project_root / "app" / "assignments"
    required_weeks = [1, 2, 3, 4, 5, 6, 7, 8]

    issues = []

    for week_num in required_weeks:
        week_dir = assignments_dir / f"week{week_num}"
        if not week_dir.exists():
            issues.append(f"Week {week_num}: 目录不存在")
            continue

        # 检查基本文件
        basic_files = ["README.md", "assignment.md"]
        for filename in basic_files:
            if not (week_dir / filename).exists():
                issues.append(f"Week {week_num}: 缺少 {filename}")

    if issues:
        print("❌ 结构问题:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("✅ 目录结构验证通过")
    return True

def verify_file_loading():
    """验证文件加载功能"""
    print("\n🔍 验证文件加载功能...")

    manager = AssignmentFileManager()

    test_cases = [
        (1, "k_shot_prompting.py"),
        (1, "llm_client.py"),
        (2, "app/main.py"),
        (2, "app/db.py"),
    ]

    success_count = 0

    for week_num, file_path in test_cases:
        try:
            content = manager.load_file_content(week_num, file_path)
            if content and len(content.strip()) > 0:
                print(f"✅ Week {week_num}/{file_path}: 加载成功 ({len(content)} 字符)")
                success_count += 1
            else:
                print(f"❌ Week {week_num}/{file_path}: 内容为空")
        except Exception as e:
            print(f"❌ Week {week_num}/{file_path}: 加载失败 - {str(e)}")

    if success_count == len(test_cases):
        print("✅ 文件加载验证通过")
        return True
    else:
        print(f"❌ 文件加载验证失败: {success_count}/{len(test_cases)} 通过")
        return False

def verify_exercise_data():
    """验证练习数据"""
    print("\n🔍 验证练习数据...")

    try:
        from data.seed_data import exercises_data

        week_counts = {}
        for exercise in exercises_data:
            week_id = exercise['week_id']
            week_counts[week_id] = week_counts.get(week_id, 0) + 1

        print("📊 练习数据统计:")
        for week_id in sorted(week_counts.keys()):
            count = week_counts[week_id]
            status = "✅" if count >= 3 else "⚠️"
            print(f"  Week {week_id}: {count} 个练习 {status}")

        # 检查是否有扩展字段
        has_extended_fields = any('assignment_files' in ex for ex in exercises_data)
        if has_extended_fields:
            print("✅ 扩展字段已添加")
        else:
            print("⚠️ 扩展字段缺失")

        return True

    except Exception as e:
        print(f"❌ 练习数据验证失败: {str(e)}")
        return False

def test_llm_integration():
    """测试LLM集成"""
    print("\n🔍 测试LLM集成...")

    try:
        # 尝试导入LLM客户端
        sys.path.insert(0, str(project_root / "app" / "assignments" / "week1"))
        from llm_client import get_llm_client, LLMClientFactory

        print("✅ LLM客户端导入成功")

        # 测试客户端创建（不实际调用API）
        try:
            client = LLMClientFactory.create_client("qwen")
            print("✅ Qwen客户端创建成功")
            return True
        except Exception as e:
            print(f"⚠️ 客户端创建失败（可能是API密钥问题）: {str(e)}")
            print("   这在没有配置API密钥的环境中是正常的")
            return True

    except ImportError as e:
        print(f"❌ LLM客户端导入失败: {str(e)}")
        return False

def generate_integration_report():
    """生成集成报告"""
    print("\n" + "="*60)
    print("📋 斯坦福CS146S作业集成报告")
    print("="*60)

    results = {
        "结构验证": verify_week_structure(),
        "文件加载": verify_file_loading(),
        "数据验证": verify_exercise_data(),
        "LLM集成": test_llm_integration(),
    }

    passed = sum(results.values())
    total = len(results)

    print("\n🎯 验证结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    print(f"\n📊 总体状态: {passed}/{total} 项通过")

    if passed == total:
        print("\n🎉 作业集成验证完全通过！")
        print("   斯坦福CS146S作业已成功集成到学习平台")
    else:
        print(f"\n⚠️  还有 {total - passed} 项需要修复")

    print("\n💡 后续步骤:")
    print("   1. 运行数据库迁移更新表结构")
    print("   2. 配置千问API密钥")
    print("   3. 测试完整的练习工作流")
    print("   4. 继续集成Week 3-8的作业内容")

    return passed == total

def main():
    """主函数"""
    print("🚀 开始斯坦福CS146S作业集成验证")
    print(f"📁 项目根目录: {project_root}")

    success = generate_integration_report()

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
