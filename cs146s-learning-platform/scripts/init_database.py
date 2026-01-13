#!/usr/bin/env python3
"""
数据库初始化脚本 - 斯坦福CS146S课程
基于 modern-software-dev-assignments-chinese-v2 的课程内容
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Week, Exercise
import json

def init_week1(app):
    """初始化Week 1: 提示工程技术"""
    with app.app_context():
        # 检查Week 1是否已存在
        week1 = Week.query.filter_by(week_number=1).first()
        if week1:
            print("⚠️  Week 1 已存在，跳过创建")
            return week1
        
        # 创建Week 1
        week1 = Week(
            week_number=1,
            title="提示工程技术",
            description="学习使用阿里千问进行有效的AI交互，包括K-shot提示、思维链推理、工具调用、自一致性提示、RAG检索增强和反思技术。",
            content_path="/modern-software-dev-assignments-chinese-v2/week1/assignment.md",
            is_active=True
        )
        db.session.add(week1)
        db.session.flush()
        
        print(f"✅ 创建 Week 1: {week1.title}")
        
        # 练习1: K-shot提示
        exercise1 = Exercise(
            week_id=week1.id,
            title="练习1: K-shot提示技术",
            description="通过提供示例来引导AI模型完成特定任务。学习如何设计有效的few-shot提示。",
            exercise_type="prompt",
            difficulty="beginner",
            initial_code="""# K-shot提示练习
# 文件路径: week1/k_shot_prompting.py
# 
# 任务: 设计一个提示，让AI将非正式文本转换为正式文本
# 
# TODO: 在代码中找到标记为TODO的位置，设计你的提示

from llm_client import get_llm_client

def k_shot_prompting_example():
    client = get_llm_client()
    
    # TODO: 设计你的提示
    prompt = '''
    请将以下非正式文本转换为正式文本：
    
    示例1:
    输入: "嘿，咱们明天见面吧"
    输出: "您好，我们明天见面可以吗？"
    
    示例2:
    输入: "这个东西真不错"
    输出: "这个产品质量很好"
    
    现在请转换:
    输入: "老板，这事儿我搞定了"
    输出:
    '''
    
    response = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(response['content'])
    return response

if __name__ == "__main__":
    k_shot_prompting_example()
""",
            instructions="""## 学习目标
- 理解K-shot提示的概念
- 学习如何通过示例引导AI
- 掌握提示设计的基本原则

## 任务要求
1. 阅读 `week1/k_shot_prompting.py` 文件
2. 找到所有标记为 `TODO` 的位置
3. 设计有效的K-shot提示
4. 运行代码并验证结果
5. 迭代改进直到测试通过

## 评分标准
- 提示设计合理性: 40%
- 输出质量: 40%
- 代码完整性: 20%

## 参考资源
- 阿里千问文档: https://dashscope.aliyuncs.com/
- 提示工程指南: 参考课程材料
""",
            hints=json.dumps([
                "K-shot提示需要提供2-3个清晰的示例",
                "示例应该展示输入和期望输出的模式",
                "确保示例的格式一致",
                "可以添加简短的任务说明"
            ], ensure_ascii=False),
            points=10,
            time_limit=30,
            order_index=1,
            is_active=True
        )
        db.session.add(exercise1)
        
        # 练习2: 思维链提示
        exercise2 = Exercise(
            week_id=week1.id,
            title="练习2: 思维链推理",
            description="引导AI模型展示推理过程，通过逐步思考来解决复杂问题。",
            exercise_type="prompt",
            difficulty="beginner",
            initial_code="""# 思维链提示练习
# 文件路径: week1/chain_of_thought.py
#
# 任务: 设计一个提示，让AI逐步推理解决数学问题
#
# TODO: 在代码中找到标记为TODO的位置，设计你的提示

from llm_client import get_llm_client

def chain_of_thought_example():
    client = get_llm_client()
    
    # TODO: 设计你的思维链提示
    prompt = '''
    请逐步思考并解决以下问题：
    
    问题: 一个班级有30名学生，其中60%是女生。
    如果又来了5名男生，现在男生占全班的百分比是多少？
    
    请按照以下步骤思考：
    1. 计算原来的女生和男生人数
    2. 计算新加入后的总人数
    3. 计算新的男生人数
    4. 计算男生占比
    '''
    
    response = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(response['content'])
    return response

if __name__ == "__main__":
    chain_of_thought_example()
""",
            instructions="""## 学习目标
- 理解思维链推理的概念
- 学习如何引导AI展示推理过程
- 掌握分步骤解决问题的方法

## 任务要求
1. 阅读 `week1/chain_of_thought.py` 文件
2. 设计思维链提示
3. 确保AI展示完整的推理过程
4. 验证最终答案的正确性

## 评分标准
- 推理步骤完整性: 40%
- 逻辑清晰度: 40%
- 答案准确性: 20%
""",
            hints=json.dumps([
                "明确要求AI展示每一步的思考过程",
                "可以提供推理步骤的框架",
                "使用'让我们一步步思考'等引导语",
                "验证每个步骤的计算是否正确"
            ], ensure_ascii=False),
            points=10,
            time_limit=30,
            order_index=2,
            is_active=True
        )
        db.session.add(exercise2)
        
        # 练习3: 工具调用
        exercise3 = Exercise(
            week_id=week1.id,
            title="练习3: 工具调用",
            description="学习如何让AI模型调用外部工具和函数来完成任务。",
            exercise_type="code",
            difficulty="intermediate",
            initial_code="""# 工具调用练习
# 文件路径: week1/tool_calling.py
#
# 任务: 实现工具调用功能，让AI使用计算器工具
#
# TODO: 完成工具定义和调用逻辑

from llm_client import get_llm_client
import json

# 定义计算器工具
def calculator(operation, num1, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2 if num2 != 0 else "Error: Division by zero"
    else:
        return "Error: Unknown operation"

# TODO: 定义工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行基本的数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "要执行的运算"
                    },
                    "num1": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "num2": {
                        "type": "number",
                        "description": "第二个数字"
                    }
                },
                "required": ["operation", "num1", "num2"]
            }
        }
    }
]

def tool_calling_example():
    client = get_llm_client()
    
    # TODO: 设计提示并调用工具
    prompt = "请计算 (15 + 27) * 3 的结果"
    
    response = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        tools=tools
    )
    
    print(response['content'])
    return response

if __name__ == "__main__":
    tool_calling_example()
""",
            instructions="""## 学习目标
- 理解工具调用的概念
- 学习如何定义工具接口
- 掌握工具调用的实现方法

## 任务要求
1. 阅读 `week1/tool_calling.py` 文件
2. 完成工具定义
3. 实现工具调用逻辑
4. 测试工具功能

## 评分标准
- 工具定义正确性: 30%
- 调用逻辑完整性: 40%
- 功能正确性: 30%
""",
            hints=json.dumps([
                "工具定义需要包含名称、描述和参数",
                "参数需要指定类型和约束",
                "处理工具调用的响应",
                "考虑错误处理"
            ], ensure_ascii=False),
            points=10,
            time_limit=45,
            order_index=3,
            is_active=True
        )
        db.session.add(exercise3)
        
        # 练习4: 自一致性提示
        exercise4 = Exercise(
            week_id=week1.id,
            title="练习4: 自一致性提示",
            description="通过多次采样和投票来提高AI输出的可靠性。",
            exercise_type="prompt",
            difficulty="intermediate",
            initial_code="""# 自一致性提示练习
# 文件路径: week1/self_consistency_prompting.py
#
# 任务: 实现自一致性提示，通过多次采样提高答案可靠性
#
# TODO: 实现多次采样和投票机制

from llm_client import get_llm_client
from collections import Counter

def self_consistency_example():
    client = get_llm_client()
    
    prompt = '''
    问题: 如果一个数字序列是 2, 4, 8, 16, ...
    那么第10个数字是多少？
    
    请给出你的答案和简短推理。
    '''
    
    # TODO: 实现多次采样
    answers = []
    num_samples = 5
    
    for i in range(num_samples):
        response = client.chat(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8  # 增加随机性
        )
        # 提取答案（简化版本）
        answer = response['content']
        answers.append(answer)
        print(f"样本 {i+1}: {answer}\\n")
    
    # TODO: 实现投票机制
    # 这里简化为打印所有答案
    print("\\n=== 所有答案 ===")
    for i, ans in enumerate(answers, 1):
        print(f"{i}. {ans}")
    
    return answers

if __name__ == "__main__":
    self_consistency_example()
""",
            instructions="""## 学习目标
- 理解自一致性的概念
- 学习如何通过多次采样提高可靠性
- 掌握投票机制的实现

## 任务要求
1. 阅读 `week1/self_consistency_prompting.py` 文件
2. 实现多次采样逻辑
3. 实现答案提取和投票
4. 分析结果的一致性

## 评分标准
- 采样实现: 30%
- 投票机制: 40%
- 结果分析: 30%
""",
            hints=json.dumps([
                "使用较高的temperature增加多样性",
                "需要从响应中提取关键答案",
                "可以使用多数投票选择最终答案",
                "考虑如何处理不一致的情况"
            ], ensure_ascii=False),
            points=10,
            time_limit=45,
            order_index=4,
            is_active=True
        )
        db.session.add(exercise4)
        
        # 练习5: RAG检索增强生成
        exercise5 = Exercise(
            week_id=week1.id,
            title="练习5: RAG检索增强生成",
            description="学习如何结合外部知识库来增强AI的回答能力。",
            exercise_type="code",
            difficulty="advanced",
            initial_code="""# RAG检索增强生成练习
# 文件路径: week1/rag.py
#
# 任务: 实现简单的RAG系统
#
# TODO: 实现文档检索和增强生成

from llm_client import get_llm_client

# 模拟知识库
knowledge_base = [
    {"id": 1, "content": "Python是一种高级编程语言，由Guido van Rossum于1991年创建。"},
    {"id": 2, "content": "Python支持多种编程范式，包括面向对象、命令式和函数式编程。"},
    {"id": 3, "content": "Python的设计哲学强调代码的可读性和简洁的语法。"},
    {"id": 4, "content": "Python拥有丰富的标准库和第三方库生态系统。"},
]

def simple_retrieval(query, knowledge_base, top_k=2):
    # TODO: 实现简单的关键词匹配检索
    # 这里使用简化的检索逻辑
    results = []
    for doc in knowledge_base:
        # 简单的关键词匹配
        if any(word in doc['content'] for word in query.split()):
            results.append(doc)
    
    return results[:top_k]

def rag_example():
    client = get_llm_client()
    
    query = "Python的特点是什么？"
    
    # TODO: 检索相关文档
    retrieved_docs = simple_retrieval(query, knowledge_base)
    
    # TODO: 构建增强提示
    context = "\\n".join([doc['content'] for doc in retrieved_docs])
    
    prompt = f'''
    基于以下背景信息回答问题：
    
    背景信息:
    {context}
    
    问题: {query}
    
    请基于背景信息给出准确的回答。
    '''
    
    response = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print("检索到的文档:")
    for doc in retrieved_docs:
        print(f"- {doc['content']}")
    print(f"\\nAI回答:\\n{response['content']}")
    
    return response

if __name__ == "__main__":
    rag_example()
""",
            instructions="""## 学习目标
- 理解RAG的概念和应用
- 学习如何检索相关文档
- 掌握如何将检索结果融入提示

## 任务要求
1. 阅读 `week1/rag.py` 文件
2. 实现文档检索功能
3. 构建增强提示
4. 验证回答质量

## 评分标准
- 检索功能: 30%
- 提示构建: 40%
- 回答质量: 30%
""",
            hints=json.dumps([
                "可以使用简单的关键词匹配",
                "将检索到的文档作为上下文",
                "明确指示AI基于提供的信息回答",
                "考虑如何处理检索不到相关文档的情况"
            ], ensure_ascii=False),
            points=10,
            time_limit=60,
            order_index=5,
            is_active=True
        )
        db.session.add(exercise5)
        
        # 练习6: 反思技术
        exercise6 = Exercise(
            week_id=week1.id,
            title="练习6: 反思技术",
            description="让AI模型评估和改进自己的输出，通过迭代提高质量。",
            exercise_type="prompt",
            difficulty="advanced",
            initial_code="""# 反思技术练习
# 文件路径: week1/reflexion.py
#
# 任务: 实现反思机制，让AI评估和改进自己的输出
#
# TODO: 实现反思和改进循环

from llm_client import get_llm_client

def reflexion_example():
    client = get_llm_client()
    
    task = "写一篇关于人工智能的简短介绍（100字以内）"
    
    # 第一次生成
    initial_prompt = f"请完成以下任务: {task}"
    
    response1 = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": initial_prompt}]
    )
    
    initial_output = response1['content']
    print(f"初始输出:\\n{initial_output}\\n")
    
    # TODO: 实现反思
    reflection_prompt = f'''
    请评估以下文本的质量：
    
    任务要求: {task}
    
    生成的文本:
    {initial_output}
    
    请从以下方面评估：
    1. 是否符合字数要求
    2. 内容是否准确和完整
    3. 表达是否清晰
    4. 有哪些可以改进的地方
    '''
    
    response2 = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": reflection_prompt}]
    )
    
    reflection = response2['content']
    print(f"反思评估:\\n{reflection}\\n")
    
    # TODO: 基于反思改进
    improvement_prompt = f'''
    原始任务: {task}
    
    初始输出:
    {initial_output}
    
    评估反馈:
    {reflection}
    
    请基于评估反馈，重新生成一个改进的版本。
    '''
    
    response3 = client.chat(
        model="qwen-turbo",
        messages=[{"role": "user", "content": improvement_prompt}]
    )
    
    improved_output = response3['content']
    print(f"改进输出:\\n{improved_output}\\n")
    
    return {
        'initial': initial_output,
        'reflection': reflection,
        'improved': improved_output
    }

if __name__ == "__main__":
    reflexion_example()
""",
            instructions="""## 学习目标
- 理解反思技术的概念
- 学习如何让AI评估自己的输出
- 掌握迭代改进的方法

## 任务要求
1. 阅读 `week1/reflexion.py` 文件
2. 实现初始生成
3. 实现反思评估
4. 实现基于反思的改进
5. 比较改进前后的质量

## 评分标准
- 反思评估质量: 40%
- 改进效果: 40%
- 整体流程: 20%
""",
            hints=json.dumps([
                "反思提示应该包含明确的评估标准",
                "可以让AI指出具体的问题",
                "改进提示应该包含原始输出和反思结果",
                "可以进行多轮反思和改进"
            ], ensure_ascii=False),
            points=10,
            time_limit=60,
            order_index=6,
            is_active=True
        )
        db.session.add(exercise6)
        
        db.session.commit()
        print(f"✅ Week 1 创建完成，包含 6 个练习")
        
        return week1


def init_week2(app):
    """初始化Week 2: 行动项提取器"""
    with app.app_context():
        week2 = Week.query.filter_by(week_number=2).first()
        if week2:
            print("⚠️  Week 2 已存在，跳过创建")
            return week2
        
        week2 = Week(
            week_number=2,
            title="行动项提取器",
            description="构建FastAPI + SQLite应用，实现笔记到行动项的自动转换。学习全栈开发和AI集成。",
            content_path="/modern-software-dev-assignments-chinese-v2/week2/assignment.md",
            is_active=True
        )
        db.session.add(week2)
        db.session.flush()
        
        print(f"✅ 创建 Week 2: {week2.title}")
        
        # Week 2的练习是项目型，创建一个综合练习
        exercise = Exercise(
            week_id=week2.id,
            title="项目: 行动项提取器应用",
            description="扩展FastAPI + SQLite应用，将自由格式的笔记转换为枚举的行动项。",
            exercise_type="project",
            difficulty="intermediate",
            instructions="""## 项目概述
构建一个全栈应用，使用AI将自由格式的笔记转换为结构化的行动项。

## 技术栈
- 后端: FastAPI + SQLAlchemy + SQLite
- 前端: 静态HTML/CSS/JavaScript
- AI: 阿里千问API

## 功能要求
1. 笔记管理（CRUD）
2. AI行动项提取
3. 行动项管理
4. 用户界面

## 评分标准
- 后端API实现: 30%
- AI集成: 30%
- 前端功能: 20%
- 代码质量: 20%

## 参考
查看 week2/ 目录下的启动代码和文档。
""",
            hints=json.dumps([
                "先理解启动代码的结构",
                "使用Cursor或其他AI工具辅助开发",
                "测试API端点",
                "逐步添加功能"
            ], ensure_ascii=False),
            points=100,
            time_limit=300,
            order_index=1,
            is_active=True
        )
        db.session.add(exercise)
        
        db.session.commit()
        print(f"✅ Week 2 创建完成，包含 1 个项目")
        
        return week2


def init_week3_to_8(app):
    """初始化Week 3-8"""
    with app.app_context():
        weeks_data = [
            {
                "number": 3,
                "title": "自定义MCP服务器",
                "description": "设计并实现模型上下文协议（MCP）服务器，封装真实的外部API。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week3/assignment.md"
            },
            {
                "number": 4,
                "title": "自主编码代理",
                "description": "使用Claude Code功能构建自动化工作流，包括自定义命令、子代理和MCP集成。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week4/assignment.md"
            },
            {
                "number": 5,
                "title": "多代理工作流",
                "description": "使用本地终端环境和脚本实现多任务协作的代理工作流。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week5/assignment.md"
            },
            {
                "number": 6,
                "title": "安全扫描与修复",
                "description": "使用Semgrep进行静态代码分析，发现并修复安全漏洞。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week6/assignment.md"
            },
            {
                "number": 7,
                "title": "AI代码审查",
                "description": "使用Gitee和AI脚本进行代码审查，提高代码质量。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week7/assignment.md"
            },
            {
                "number": 8,
                "title": "多栈应用构建",
                "description": "在3个不同技术栈中构建相同的功能性Web应用程序。",
                "content_path": "/modern-software-dev-assignments-chinese-v2/week8/assignment.md"
            }
        ]
        
        for week_data in weeks_data:
            week = Week.query.filter_by(week_number=week_data["number"]).first()
            if week:
                print(f"⚠️  Week {week_data['number']} 已存在，跳过创建")
                continue
            
            week = Week(
                week_number=week_data["number"],
                title=week_data["title"],
                description=week_data["description"],
                content_path=week_data["content_path"],
                is_active=True
            )
            db.session.add(week)
            db.session.flush()
            
            # 为每周创建一个项目型练习
            exercise = Exercise(
                week_id=week.id,
                title=f"项目: {week_data['title']}",
                description=week_data["description"],
                exercise_type="project",
                difficulty="advanced" if week_data["number"] >= 6 else "intermediate",
                instructions=f"""## 项目概述
{week_data['description']}

## 详细要求
请查看 {week_data['content_path']} 获取完整的项目要求和评分标准。

## 提示
- 仔细阅读作业文档
- 使用AI工具辅助开发
- 注意代码质量和文档
- 按时提交完整的项目
""",
                hints=json.dumps([
                    "查看课程目录下的详细文档",
                    "参考提供的启动代码",
                    "使用AI工具提高效率",
                    "注意测试和文档"
                ], ensure_ascii=False),
                points=100,
                time_limit=300,
                order_index=1,
                is_active=True
            )
            db.session.add(exercise)
            
            print(f"✅ 创建 Week {week_data['number']}: {week_data['title']}")
        
        db.session.commit()
        print(f"✅ Week 3-8 创建完成")


def init_all_weeks(app):
    """初始化所有周的数据"""
    with app.app_context():
        print("\n" + "="*60)
        print("🚀 开始初始化数据库 - 斯坦福CS146S课程")
        print("="*60 + "\n")
        
        # 初始化所有周
        init_week1(app)
        init_week2(app)
        init_week3_to_8(app)
        
        # 统计信息
        total_weeks = Week.query.count()
        total_exercises = Exercise.query.count()
        
        print("\n" + "="*60)
        print("✅ 数据库初始化完成！")
        print("="*60)
        print(f"📚 总课程周数: {total_weeks}")
        print(f"💻 总练习数量: {total_exercises}")
        print("\n课程概览:")
        
        weeks = Week.query.order_by(Week.week_number).all()
        for week in weeks:
            exercise_count = Exercise.query.filter_by(week_id=week.id).count()
            print(f"  Week {week.week_number}: {week.title} ({exercise_count}个练习)")
        
        print("\n提示: 可以通过以下方式查看数据:")
        print("  - 访问 http://localhost:5000/api/v1/learning/weeks")
        print("  - 访问 http://localhost:5000/api/v1/exercises")
        print("="*60 + "\n")


def reset_database(app):
    """重置数据库（删除所有数据并重新创建表）"""
    with app.app_context():
        print("\n⚠️  警告: 即将删除所有数据并重新创建数据库")
        response = input("确认继续? (yes/no): ")
        
        if response.lower() != 'yes':
            print("❌ 操作已取消")
            return
        
        print("\n🗑️  删除所有表...")
        db.drop_all()
        
        print("📋 创建所有表...")
        db.create_all()
        
        print("✅ 数据库重置完成\n")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库初始化脚本 - 斯坦福CS146S课程')
    parser.add_argument('--reset', action='store_true', help='重置数据库（删除所有数据）')
    args = parser.parse_args()
    
    app = create_app()
    
    if args.reset:
        reset_database(app)
    
    init_all_weeks(app)


if __name__ == "__main__":
    main()
