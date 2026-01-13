#!/usr/bin/env python3
"""
基于modern-software-dev-assignments-chinese-v2的真实练习内容初始化数据库
"""
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Week, Exercise

def load_parsed_assignments():
    """加载解析后的练习数据"""
    json_file = "/home/ubuntu/parsed_assignments.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def init_weeks_and_exercises():
    """初始化Week和Exercise数据"""
    print("📚 开始初始化Week和Exercise数据...")
    
    # 加载解析后的数据
    exercises_data = load_parsed_assignments()
    
    # Week信息
    weeks_info = [
        {"week_number": 1, "title": "提示工程技术", "description": "学习使用提示工程技术与AI模型交互，包括K-shot提示、思维链、工具调用、自一致性、RAG检索增强和反思技术。"},
        {"week_number": 2, "title": "行动项提取器", "description": "构建FastAPI + SQLite应用，实现笔记记录到行动项的自动转换。学习全栈开发和AI集成。"},
        {"week_number": 3, "title": "自定义MCP服务器", "description": "设计并实现规模上下文协议（MCP）服务器，封装真实的外部API。"},
        {"week_number": 4, "title": "自主编码代理", "description": "使用Claude Code功能构建自动化工作流，包含自定义命令、子代理和MCP集成。"},
        {"week_number": 5, "title": "多代理工作流", "description": "使用本地终端环境和脚本来测试本次现任务的代理工作流。"},
        {"week_number": 6, "title": "安全扫描与修复", "description": "使用Semgrep进行静态代码分析，发现并修复安全漏洞。"},
        {"week_number": 7, "title": "AI代码审查", "description": "使用Gitee实现AI驱动的代码审查流程。"},
        {"week_number": 8, "title": "多栈应用构建", "description": "综合运用所学知识，构建一个完整的多栈应用。"}
    ]
    
    # 创建Week记录
    for week_info in weeks_info:
        week = Week.query.filter_by(week_number=week_info["week_number"]).first()
        if not week:
            week = Week(
                week_number=week_info["week_number"],
                title=week_info["title"],
                description=week_info["description"]
            )
            db.session.add(week)
            print(f"  ✅ 创建Week {week_info['week_number']}: {week_info['title']}")
        else:
            print(f"  ⏭️  Week {week_info['week_number']} 已存在")
    
    db.session.commit()
    
    # 创建Exercise记录
    for ex_data in exercises_data:
        week = Week.query.filter_by(week_number=ex_data["week"]).first()
        if not week:
            print(f"  ❌ Week {ex_data['week']} 不存在，跳过练习")
            continue
        
        # 检查练习是否已存在
        exercise = Exercise.query.filter_by(
            week_id=week.id,
            title=ex_data["title"]
        ).first()
        
        if not exercise:
            exercise = Exercise(
                week_id=week.id,
                title=ex_data["title"],
                description=ex_data["description"],
                exercise_type=ex_data["type"],
                difficulty=ex_data["difficulty"],
                points=ex_data["points"],
                time_limit=30 if ex_data["type"] == "prompt" else 120,  # 提示工程30分钟，项目120分钟
                order_index=ex_data["order"],
                initial_code=ex_data["initial_code"],
                test_code=ex_data["test_code"],
                solution_code=ex_data["solution_code"],
                hints=f"1. 阅读{ex_data['file_path']}中的任务描述\n2. 查找代码中的TODO标记\n3. 完成TODO部分的代码\n4. 运行测试验证结果\n5. 参考文件: {ex_data['file_path']}"
            )
            db.session.add(exercise)
            print(f"  ✅ 创建练习: Week {ex_data['week']} - {ex_data['title']}")
        else:
            print(f"  ⏭️  练习已存在: Week {ex_data['week']} - {ex_data['title']}")
    
    db.session.commit()
    print("✅ Week和Exercise数据初始化完成！")

def main():
    """主函数"""
    app = create_app()
    
    with app.app_context():
        print("🚀 开始初始化数据库...")
        print("=" * 60)
        
        # 初始化Week和Exercise
        init_weeks_and_exercises()
        
        print("=" * 60)
        print("🎉 数据库初始化完成！")
        
        # 统计信息
        total_weeks = Week.query.count()
        total_exercises = Exercise.query.count()
        
        print(f"\n📊 统计信息:")
        print(f"  - 总Week数: {total_weeks}")
        print(f"  - 总练习数: {total_exercises}")
        
        for week_num in range(1, 9):
            week = Week.query.filter_by(week_number=week_num).first()
            if week:
                ex_count = Exercise.query.filter_by(week_id=week.id).count()
                print(f"  - Week {week_num}: {ex_count}个练习")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='初始化数据库')
    parser.add_argument('--reset', action='store_true', help='重置数据库（删除所有数据）')
    args = parser.parse_args()
    
    if args.reset:
        print("⚠️  警告：将删除所有现有数据！")
        confirm = input("确认重置数据库？(yes/no): ")
        if confirm.lower() == 'yes':
            app = create_app()
            with app.app_context():
                print("🗑️  删除所有Exercise...")
                Exercise.query.delete()
                print("🗑️  删除所有Week...")
                Week.query.delete()
                db.session.commit()
                print("✅ 数据库已重置")
            main()
        else:
            print("❌ 取消重置")
    else:
        main()
