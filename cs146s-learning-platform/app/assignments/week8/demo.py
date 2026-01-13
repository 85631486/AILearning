#!/usr/bin/env python3
"""
Week 8: 多技术栈AI加速Web应用构建演示
展示AI应用生成器和多技术栈Web应用示例
"""

import sys
import os
from generator.app_generator import generator, generate_app_from_prompt


def demo_app_generation() -> None:
    """演示AI应用生成功能"""
    print("🤖 Week 8: AI应用生成演示")
    print("=" * 50)

    # 显示可用模板
    print("📋 可用技术栈模板:")
    templates = generator.list_available_templates()
    for name, info in templates.items():
        print(f"  - {name}: {info['description']}")

    print("
🔧 生成示例应用..."    # 生成一个React + Flask应用
    spec = {
        'name': 'TaskManager',
        'description': '任务管理系统',
        'tech_stack': 'react-flask',
        'features': ['任务管理', '用户管理', '状态跟踪'],
        'entities': [
            {'name': 'task', 'fields': ['title', 'description', 'status', 'due_date']},
            {'name': 'user', 'fields': ['name', 'email']}
        ],
        'frontend_framework': 'react',
        'backend_framework': 'flask',
        'database': 'sqlite'
    }

    try:
        result = generator.generate_app(spec, "generated_taskmanager")

        if result['success']:
            print("✅ 应用生成成功!"            print(f"📁 输出目录: {result['app_path']}")
            print(f"📄 生成文件数: {len(result['files_generated'])}")

            print("
📋 生成的文件:"            for file_path in result['files_generated'][:10]:  # 只显示前10个
                print(f"  - {file_path}")
            if len(result['files_generated']) > 10:
                print(f"  ... 还有 {len(result['files_generated']) - 10} 个文件")

            print("
🚀 后续设置步骤:"            for step in result['next_steps']:
                print(f"  • {step}")
        else:
            print(f"❌ 生成失败: {result.get('error', '未知错误')}")

    except Exception as e:
        print(f"❌ 生成过程中出现错误: {e}")


def demo_multiple_tech_stacks() -> None:
    """演示多技术栈应用生成"""
    print("\n🌐 多技术栈应用生成演示")
    print("=" * 50)

    tech_stacks = [
        ('react-flask', 'React前端 + Flask后端'),
        ('vue-fastapi', 'Vue前端 + FastAPI后端'),
        ('angular-django', 'Angular前端 + Django后端')
    ]

    for tech_stack, description in tech_stacks:
        print(f"\n🔧 生成 {description} 应用...")

        try:
            result = generate_app_from_prompt(
                f"创建一个使用{tech_stack}技术栈的任务管理应用",
                tech_stack
            )

            if result['success']:
                print(f"✅ {tech_stack} 应用生成成功")
                print(f"   📁 位置: generated_apps/TaskManager_{tech_stack}")
                print(f"   📄 文件数: {len(result['files_generated'])}")
            else:
                print(f"❌ {tech_stack} 生成失败: {result.get('error', '未知错误')}")

        except Exception as e:
            print(f"❌ {tech_stack} 生成错误: {e}")


def demo_app_structure_analysis() -> None:
    """分析生成的应用结构"""
    print("\n📊 应用结构分析")
    print("=" * 50)

    # 分析已生成的TaskManager应用结构
    generated_dir = "generated_taskmanager"

    if not os.path.exists(generated_dir):
        print("⚠️  未找到生成的TaskManager应用，请先运行应用生成")
        return

    print("📁 生成的应用结构:")

    def print_directory_structure(path, prefix="", max_depth=3):
        """递归打印目录结构"""
        if max_depth <= 0:
            return

        try:
            items = os.listdir(path)
            items.sort()

            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1

                # 选择连接符
                connector = "└── " if is_last else "├── "

                print(f"{prefix}{connector}{item}")

                if os.path.isdir(item_path):
                    extension = "    " if is_last else "│   "
                    print_directory_structure(item_path, prefix + extension, max_depth - 1)

        except PermissionError:
            print(f"{prefix}└── [权限不足]")

    print_directory_structure(generated_dir)

    # 统计文件类型
    file_types = {}
    total_files = 0

    for root, dirs, files in os.walk(generated_dir):
        for file in files:
            total_files += 1
            ext = os.path.splitext(file)[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1

    print("
📈 文件统计:"    print(f"  总文件数: {total_files}")
    print("  文件类型分布:")
    for ext, count in sorted(file_types.items()):
        print(f"    {ext or '无扩展名'}: {count} 个文件")


def demo_tech_stack_comparison() -> None:
    """技术栈对比分析"""
    print("\n⚖️ 技术栈对比分析")
    print("=" * 50)

    tech_comparison = {
        'React + Flask': {
            '优点': [
                'React生态丰富，组件化开发',
                'Flask轻量，学习曲线平缓',
                '热重载开发体验良好',
                'Python后端处理逻辑强大'
            ],
            '适用场景': '中小型Web应用，快速原型开发',
            '复杂度': '中低',
            '学习成本': '中低'
        },
        'Vue + FastAPI': {
            '优点': [
                'Vue学习曲线平缓，模板语法直观',
                'FastAPI自动生成API文档',
                'TypeScript支持，类型安全',
                '异步处理性能优秀'
            ],
            '适用场景': '现代化Web应用，API驱动开发',
            '复杂度': '中低',
            '学习成本': '中低'
        },
        'Angular + Django': {
            '优点': [
                'Angular企业级框架，功能完备',
                'Django内置管理后台',
                '强类型支持，代码质量高',
                '安全性配置完善'
            ],
            '适用场景': '大型企业应用，复杂业务逻辑',
            '复杂度': '高',
            '学习成本': '高'
        }
    }

    for tech, details in tech_comparison.items():
        print(f"\n🔧 {tech}")
        print(f"  📈 复杂度: {details['复杂度']}")
        print(f"  🎓 学习成本: {details['学习成本']}")
        print(f"  🎯 适用场景: {details['适用场景']}")

        print("  ✅ 优点:")
        for advantage in details['优点']:
            print(f"    • {advantage}")


def demo_deployment_options() -> None:
    """演示部署选项"""
    print("\n🚀 部署选项演示")
    print("=" * 50)

    deployment_options = {
        'Docker + Docker Compose': {
            '描述': '容器化部署，环境一致性好',
            '优点': ['环境隔离', '易于扩展', '版本控制'],
            '配置文件': ['Dockerfile', 'docker-compose.yml'],
            '适用场景': '云原生应用，微服务架构'
        },
        'Heroku/Vercel': {
            '描述': 'PaaS平台，一键部署',
            '优点': ['无需服务器管理', '自动扩展', 'CDN支持'],
            '配置文件': ['requirements.txt', 'package.json', 'Procfile'],
            '适用场景': '快速原型，中小型应用'
        },
        'AWS/GCP/Azure': {
            '描述': '云服务，灵活配置',
            '优点': ['高可用性', '全球分发', '集成服务丰富'],
            '配置文件': ['Terraform配置', 'CI/CD流水线'],
            '适用场景': '企业级应用，大规模部署'
        },
        '传统服务器': {
            '描述': '自托管服务器',
            '优点': ['完全控制', '成本可控', '定制化'],
            '配置文件': ['Nginx配置', 'systemd服务'],
            '适用场景': '特定环境要求，私有部署'
        }
    }

    for option, details in deployment_options.items():
        print(f"\n🏗️  {option}")
        print(f"  📝 {details['描述']}")

        print("  ✅ 优点:")
        for advantage in details['优点']:
            print(f"    • {advantage}")

        print(f"  📄 配置文件: {', '.join(details['配置文件'])}")
        print(f"  🎯 适用场景: {details['适用场景']}")


def demo_ai_acceleration_benefits() -> None:
    """演示AI加速的优势"""
    print("\n⚡ AI加速开发优势")
    print("=" * 50)

    benefits = {
        '代码生成': {
            '描述': 'AI根据需求自动生成代码框架和组件',
            '时间节省': '60-80%',
            '质量保证': '遵循最佳实践，减少错误'
        },
        '技术栈选择': {
            '描述': 'AI帮助选择合适的技术栈和架构',
            '决策效率': '提升50%',
            '匹配度': '基于项目需求智能推荐'
        },
        '文档生成': {
            '描述': '自动生成README、API文档和部署指南',
            '完整性': '覆盖所有必要信息',
            '一致性': '格式统一，信息准确'
        },
        '配置管理': {
            '描述': '自动生成Docker、CI/CD等配置文件',
            '标准化': '遵循行业标准',
            '可维护性': '配置清晰，易于修改'
        },
        '学习加速': {
            '描述': '通过示例代码加速学习新技术栈',
            '上手速度': '提升70%',
            '实践机会': '立即获得可运行的代码'
        }
    }

    for benefit, details in benefits.items():
        print(f"\n🚀 {benefit}")
        print(f"  📝 {details['描述']}")

        if '时间节省' in details:
            print(f"  ⏱️  时间节省: {details['时间节省']}")
        if '质量保证' in details:
            print(f"  ✨ 质量保证: {details['质量保证']}")
        if '决策效率' in details:
            print(f"  🎯 决策效率: {details['决策效率']}")
        if '匹配度' in details:
            print(f"  🔍 匹配度: {details['匹配度']}")
        if '完整性' in details:
            print(f"  📚 完整性: {details['完整性']}")
        if '一致性' in details:
            print(f"  🔄 一致性: {details['一致性']}")
        if '标准化' in details:
            print(f"  📏 标准化: {details['标准化']}")
        if '可维护性' in details:
            print(f"  🔧 可维护性: {details['可维护性']}")
        if '上手速度' in details:
            print(f"  📈 上手速度: {details['上手速度']}")
        if '实践机会' in details:
            print(f"  🛠️  实践机会: {details['实践机会']}")


def main() -> None:
    """主演示函数"""
    print("🚀 Week 8: 多技术栈AI加速Web应用构建演示")
    print("=" * 70)

    try:
        demo_app_generation()
        demo_multiple_tech_stacks()
        demo_app_structure_analysis()
        demo_tech_stack_comparison()
        demo_deployment_options()
        demo_ai_acceleration_benefits()

        print("
🎉 多技术栈应用构建演示完成！"        print("\n📁 生成的文件和目录:")
        print("  - generated_taskmanager/ (完整应用)")
        print("  - generated_apps/ (多技术栈应用)")
        print("  - app/assignments/week8/apps/taskmanager_react_flask/ (示例完整应用)")

        print("
💡 学习要点:"        print("  • AI可以显著加速Web应用开发过程")
        print("  • 不同技术栈各有优势，选择要基于项目需求")
        print("  • 生成的应用包含完整的前后端和部署配置")
        print("  • AI生成的应用可以作为学习和快速原型的起点")
        print("  • 理解多技术栈可以帮助做出更好的架构决策")

        print("
🚀 实际应用建议:"        print("  • 从AI生成的基础应用开始，逐步添加业务逻辑")
        print("  • 对比不同技术栈的优缺点，选择最适合的方案")
        print("  • 使用生成的应用作为团队培训和学习材料")
        print("  • 在实际项目中结合手动优化和AI生成的代码")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
