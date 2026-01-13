#!/usr/bin/env python3
"""
Week 7: 代码审查演示
展示AI辅助代码审查和手动审查的对比
"""

import sys
import os
from code_review.code_reviewer import ai_reviewer, manual_reviewer, review_codebase
from tasks.task_implementation import demonstrate_tasks


def demo_ai_code_review():
    """演示AI代码审查功能"""
    print("🤖 AI代码审查演示")
    print("=" * 40)

    # 创建示例代码进行审查
    sample_code = '''
import os
import sys

def process_data(input_data):
    """处理输入数据 - 这个函数有一些问题"""
    # TODO: 添加输入验证
    # FIXME: 这个函数太长了，需要重构

    # 硬编码的数据库URL
    db_url = "postgresql://localhost:5432/mydb"

    # 复杂的条件语句
    if input_data and len(input_data) > 0 and isinstance(input_data, str) and len(input_data) < 1000:
        result = input_data.upper()
        print(result)  # 调试信息遗留在生产代码中

        # 危险的eval使用
        try:
            processed = eval(input_data)
            return processed
        except:
            return None
    else:
        return "INVALID"

# 过长的函数（故意写的很长）
def very_long_function(param1, param2, param3, param4, param5):
    """这个函数故意写得很长来演示审查"""
    step1 = param1 + param2
    step2 = step1 * param3
    step3 = step2 - param4
    step4 = step3 / param5 if param5 != 0 else 0
    step5 = step4 ** 2
    step6 = step5 + 1
    step7 = step6 * 2
    step8 = step7 - 3
    step9 = step8 / 4
    step10 = step9 + 5
    step11 = step10 * 6
    step12 = step11 - 7
    step13 = step12 / 8
    step14 = step13 + 9
    step15 = step14 * 10
    step16 = step15 - 11
    step17 = step16 / 12
    step18 = step17 + 13
    step19 = step18 * 14
    step20 = step19 - 15

    return step20

class DataProcessor:
    def __init__(self):
        self.data = []

    def add_item(self, item):
        self.data.append(item)

    def process_all(self):
        return [item.upper() for item in self.data]
'''

    # 保存到示例文件
    sample_file = "sample_code_review.py"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_code)

    print("📁 已创建示例代码文件")

    # 执行AI审查
    print("\n🔍 执行AI代码审查...")
    comments = ai_reviewer.review_file(sample_file)

    print(f"\n📊 发现 {len(comments)} 个审查意见:")

    # 按严重程度分组显示
    severity_groups = {'error': [], 'warning': [], 'info': []}
    for comment in comments:
        severity_groups[comment.severity].append(comment)

    for severity, comment_list in severity_groups.items():
        if comment_list:
            print(f"\n{severity.upper()} ({len(comment_list)} 个):")
            for comment in comment_list:
                print(f"  • 第{comment.line_number}行: {comment.message}")
                if comment.suggestion:
                    print(f"    💡 {comment.suggestion}")

    # 生成审查报告
    print("\n📄 生成审查报告...")
    review_results = ai_reviewer.review_pull_request([sample_file])
    report = ai_reviewer.generate_review_report(review_results, "ai_review_report.md")
    print("报告已保存到: ai_review_report.md"

    # 清理示例文件
    os.remove(sample_file)


def demo_manual_review_guidance():
    """演示手动审查指导"""
    print("\n👥 手动代码审查指导")
    print("=" * 40)

    print("📋 手动审查清单:")

    checklist = manual_reviewer.get_checklist()
    for category, questions in checklist.items():
        print(f"\n🔍 {category.upper()}:")
        for question in questions:
            print(f"  • {question}")

    print("
📝 PR模板示例:"    pr_template = manual_reviewer.generate_pr_template()
    print(pr_template)

    # 保存PR模板
    with open("pr_template.md", 'w', encoding='utf-8') as f:
        f.write(pr_template)
    print("PR模板已保存到: pr_template.md"


def demo_review_comparison():
    """演示AI审查与手动审查的对比"""
    print("\n⚖️ AI审查 vs 手动审查对比")
    print("=" * 40)

    comparison_data = {
        'ai_review_advantages': [
            '⚡ 快速自动化检查',
            '🎯 覆盖常见模式和最佳实践',
            '📊 一致的审查标准',
            '🔍 检测代码异味和潜在问题',
            '📈 可扩展到大型代码库'
        ],
        'manual_review_advantages': [
            '🧠 理解业务逻辑和上下文',
            '🎨 发现设计和架构问题',
            '💡 提供建设性改进建议',
            '👥 知识分享和团队协作',
            '🎯 关注用户体验和功能正确性'
        ],
        'best_practices': [
            '🤝 将AI审查作为第一道防线',
            '🔍 手动审查重点关注复杂逻辑',
            '📋 使用标准化清单确保覆盖',
            '💬 审查时进行建设性对话',
            '📈 持续改进审查流程和标准'
        ]
    }

    for category, items in comparison_data.items():
        category_names = {
            'ai_review_advantages': '🤖 AI审查优点',
            'manual_review_advantages': '👥 手动审查优点',
            'best_practices': '💡 最佳实践'
        }

        print(f"\n{category_names[category]}:")
        for item in items:
            print(f"  {item}")

    print("
📊 实际应用建议:"    print("小型PR (< 50行): AI审查 + 快速手动检查")
    print("中型PR (50-200行): AI审查 + 详细手动审查")
    print("大型PR (> 200行): AI审查 + 多人审查 + 结对编程")
    print("复杂功能: AI审查 + 架构审查 + 用户验收测试")


def demo_full_workflow():
    """演示完整的工作流程"""
    print("\n🔄 完整代码审查工作流程演示")
    print("=" * 50)

    workflow_steps = [
        {
            'step': 1,
            'title': '代码提交',
            'description': '开发者提交代码到功能分支',
            'actions': [
                '创建功能分支',
                '实现功能代码',
                '编写单元测试',
                '提交代码变更'
            ]
        },
        {
            'step': 2,
            'title': '创建Pull Request',
            'description': '创建PR并添加基本描述',
            'actions': [
                '填写PR标题和描述',
                '添加相关标签',
                '关联相关问题',
                '请求审查者'
            ]
        },
        {
            'step': 3,
            'title': 'AI自动审查',
            'description': '运行AI审查工具进行初步检查',
            'actions': [
                '运行代码质量检查',
                '检测安全漏洞',
                '检查代码规范',
                '生成审查报告'
            ]
        },
        {
            'step': 4,
            'title': '手动代码审查',
            'description': '人工审查代码逻辑和设计',
            'actions': [
                '检查业务逻辑正确性',
                '评估代码设计和架构',
                '验证测试覆盖率',
                '检查文档完整性'
            ]
        },
        {
            'step': 5,
            'title': '修复和迭代',
            'description': '根据审查意见进行修复',
            'actions': [
                '修复发现的问题',
                '改进代码质量',
                '更新测试和文档',
                '重新提交代码'
            ]
        },
        {
            'step': 6,
            'title': '最终批准',
            'description': '审查通过后合并代码',
            'actions': [
                '获得审查者批准',
                '运行CI/CD流水线',
                '合并到主分支',
                '部署到生产环境'
            ]
        }
    ]

    for step_info in workflow_steps:
        print(f"\n{step_info['step']}. {step_info['title']}")
        print(f"   {step_info['description']}")
        print("   执行操作:"
        for action in step_info['actions']:
            print(f"   • {action}")

    print("
🎯 工作流程关键点:"    print("  • 🔄 持续集成：自动化测试和构建")
    print("  • 👥 协作审查：多人参与提高质量")
    print("  • 📈 持续改进：从每次审查中学习")
    print("  • 🛡️ 质量保障：多层次的检查机制")


def main():
    """主演示函数"""
    print("🚀 Week 7: 代码审查演示")
    print("=" * 60)

    try:
        demo_ai_code_review()
        demo_manual_review_guidance()
        demo_review_comparison()
        demo_full_workflow()

        print("
📚 运行任务演示..."        demonstrate_tasks()

        print("
🎉 代码审查演示完成！"        print("\n📁 生成的文件:")
        print("  - ai_review_report.md (AI审查报告)")
        print("  - pr_template.md (PR模板)")
        print("  - pr_task_1_add_validation.md (任务1 PR)")
        print("  - pr_task_2_add_error_handling.md (任务2 PR)")

        print("
💡 学习要点:"        print("  • AI审查提供快速、一致的初步检查")
        print("  • 手动审查关注业务逻辑和设计质量")
        print("  • 结合两者可以获得最佳审查效果")
        print("  • 良好的审查流程是高质量代码的保障")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
