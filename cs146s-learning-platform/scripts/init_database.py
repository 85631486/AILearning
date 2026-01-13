#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建Week 1-8的课程数据和练习题目
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Week, Exercise
import json

def init_week1(app):
    """初始化Week 1: Python基础与Qwen API入门"""
    with app.app_context():
        # 检查Week 1是否已存在
        week1 = Week.query.filter_by(week_number=1).first()
        if week1:
            print("⚠️  Week 1 已存在，跳过创建")
            return week1
        
        # 创建Week 1
        week1 = Week(
            week_number=1,
            title="Python基础与Qwen API入门",
            description="学习Python基础语法，了解AI大模型概念，掌握Qwen API的基本使用方法。",
            content_path="/assignments/week1/README.md",
            is_active=True
        )
        db.session.add(week1)
        db.session.flush()  # 获取week1.id
        
        print(f"✅ 创建 Week 1: {week1.title}")
        
        # 练习1: Hello World
        exercise1 = Exercise(
            week_id=week1.id,
            title="练习1: Hello World",
            description="编写你的第一个Python程序，输出'Hello, World!'",
            exercise_type="code",
            difficulty="beginner",
            initial_code="""# 在这里编写你的代码
# 提示: 使用print()函数输出文本

""",
            test_code="""
def test_hello_world():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        exec(code)
    output = f.getvalue().strip()
    
    assert output == "Hello, World!", f"期望输出 'Hello, World!'，实际输出 '{output}'"
    return True
""",
            solution_code="""print('Hello, World!')""",
            hints=json.dumps([
                "使用print()函数可以输出文本",
                "字符串需要用引号包围",
                "注意大小写和标点符号"
            ], ensure_ascii=False),
            points=10,
            time_limit=5,
            order_index=1,
            is_active=True
        )
        db.session.add(exercise1)
        
        # 练习2: 变量和数据类型
        exercise2 = Exercise(
            week_id=week1.id,
            title="练习2: 变量和数据类型",
            description="创建不同类型的变量并输出它们的值和类型",
            exercise_type="code",
            difficulty="beginner",
            initial_code="""# 创建以下变量:
# 1. 一个整数变量 age，值为 20
# 2. 一个浮点数变量 height，值为 1.75
# 3. 一个字符串变量 name，值为 'Alice'
# 4. 一个布尔变量 is_student，值为 True

# 在这里编写你的代码

# 输出所有变量的值
print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"身高: {height}米")
print(f"是否为学生: {is_student}")
""",
            test_code="""
def test_variables():
    # 执行代码
    exec(code, globals())
    
    # 检查变量是否存在
    assert 'age' in globals(), "变量 age 未定义"
    assert 'height' in globals(), "变量 height 未定义"
    assert 'name' in globals(), "变量 name 未定义"
    assert 'is_student' in globals(), "变量 is_student 未定义"
    
    # 检查变量类型
    assert isinstance(age, int), "age 应该是整数类型"
    assert isinstance(height, float), "height 应该是浮点数类型"
    assert isinstance(name, str), "name 应该是字符串类型"
    assert isinstance(is_student, bool), "is_student 应该是布尔类型"
    
    # 检查变量值
    assert age == 20, f"age 应该是 20，实际是 {age}"
    assert height == 1.75, f"height 应该是 1.75，实际是 {height}"
    assert name == 'Alice', f"name 应该是 'Alice'，实际是 '{name}'"
    assert is_student == True, f"is_student 应该是 True，实际是 {is_student}"
    
    return True
""",
            solution_code="""age = 20
height = 1.75
name = 'Alice'
is_student = True

print(f"姓名: {name}")
print(f"年龄: {age}")
print(f"身高: {height}米")
print(f"是否为学生: {is_student}")
""",
            hints=json.dumps([
                "变量赋值使用等号 =",
                "整数不需要小数点，浮点数需要小数点",
                "字符串需要用引号包围",
                "布尔值只有 True 和 False 两个值"
            ], ensure_ascii=False),
            points=15,
            time_limit=10,
            order_index=2,
            is_active=True
        )
        db.session.add(exercise2)
        
        # 练习3: 用户输入
        exercise3 = Exercise(
            week_id=week1.id,
            title="练习3: 获取用户输入",
            description="使用input()函数获取用户输入，并进行简单的处理",
            exercise_type="code",
            difficulty="beginner",
            initial_code="""# 获取用户的姓名和年龄
# 提示: 使用input()函数
# 注意: input()返回的是字符串，需要转换年龄为整数

# 在这里编写你的代码

""",
            test_code="""
def test_user_input():
    import io
    import sys
    from contextlib import redirect_stdout
    
    # 模拟用户输入
    sys.stdin = io.StringIO("Bob\\n25\\n")
    
    f = io.StringIO()
    with redirect_stdout(f):
        exec(code)
    output = f.getvalue()
    
    assert "Bob" in output, "输出中应该包含用户输入的姓名"
    assert "25" in output or "二十五" in output, "输出中应该包含用户输入的年龄"
    
    return True
""",
            solution_code="""name = input("请输入你的姓名: ")
age = int(input("请输入你的年龄: "))

print(f"你好，{name}！")
print(f"你今年{age}岁了。")
print(f"明年你将{age + 1}岁。")
""",
            hints=json.dumps([
                "使用input()函数获取用户输入",
                "input()返回的是字符串类型",
                "使用int()函数将字符串转换为整数",
                "使用f-string格式化输出"
            ], ensure_ascii=False),
            points=15,
            time_limit=10,
            order_index=3,
            is_active=True
        )
        db.session.add(exercise3)
        
        # 练习4: 条件语句
        exercise4 = Exercise(
            week_id=week1.id,
            title="练习4: 条件判断",
            description="使用if-elif-else语句根据分数判断等级",
            exercise_type="code",
            difficulty="beginner",
            initial_code="""# 根据分数判断等级
# 90-100: 优秀
# 80-89: 良好
# 70-79: 中等
# 60-69: 及格
# 0-59: 不及格

score = int(input("请输入分数: "))

# 在这里编写你的代码

""",
            test_code="""
def test_grade():
    import io
    import sys
    from contextlib import redirect_stdout
    
    test_cases = [
        (95, "优秀"),
        (85, "良好"),
        (75, "中等"),
        (65, "及格"),
        (55, "不及格")
    ]
    
    for score, expected_grade in test_cases:
        sys.stdin = io.StringIO(f"{score}\\n")
        f = io.StringIO()
        with redirect_stdout(f):
            exec(code)
        output = f.getvalue()
        
        assert expected_grade in output, f"分数{score}应该输出'{expected_grade}'，实际输出: {output}"
    
    return True
""",
            solution_code="""score = int(input("请输入分数: "))

if score >= 90 and score <= 100:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 70:
    grade = "中等"
elif score >= 60:
    grade = "及格"
else:
    grade = "不及格"

print(f"你的分数是{score}，等级是: {grade}")
""",
            hints=json.dumps([
                "使用if-elif-else结构",
                "注意条件的顺序，从高到低判断",
                "使用比较运算符 >=, <=",
                "可以使用 and 连接多个条件"
            ], ensure_ascii=False),
            points=20,
            time_limit=15,
            order_index=4,
            is_active=True
        )
        db.session.add(exercise4)
        
        # 练习5: 循环
        exercise5 = Exercise(
            week_id=week1.id,
            title="练习5: for循环",
            description="使用for循环计算1到100的和",
            exercise_type="code",
            difficulty="beginner",
            initial_code="""# 计算1到100的和
# 提示: 使用for循环和range()函数

total = 0

# 在这里编写你的代码

print(f"1到100的和是: {total}")
""",
            test_code="""
def test_sum():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        exec(code)
    output = f.getvalue()
    
    expected_sum = sum(range(1, 101))
    assert str(expected_sum) in output, f"应该输出 {expected_sum}"
    
    return True
""",
            solution_code="""total = 0

for i in range(1, 101):
    total += i

print(f"1到100的和是: {total}")
""",
            hints=json.dumps([
                "使用range(1, 101)生成1到100的数字",
                "使用for循环遍历这些数字",
                "使用 += 运算符累加",
                "1到100的和应该是5050"
            ], ensure_ascii=False),
            points=20,
            time_limit=15,
            order_index=5,
            is_active=True
        )
        db.session.add(exercise5)
        
        # 练习6: 列表操作
        exercise6 = Exercise(
            week_id=week1.id,
            title="练习6: 列表基础",
            description="创建列表并进行基本操作",
            exercise_type="code",
            difficulty="intermediate",
            initial_code="""# 创建一个包含5个学生姓名的列表
students = ["Alice", "Bob", "Charlie", "David", "Eve"]

# 1. 输出列表的长度
# 2. 输出第一个和最后一个学生的姓名
# 3. 添加一个新学生 "Frank"
# 4. 删除 "Charlie"
# 5. 输出最终的列表

# 在这里编写你的代码

""",
            test_code="""
def test_list_operations():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        exec(code)
    output = f.getvalue()
    
    # 检查输出
    assert "5" in output, "应该输出列表长度5"
    assert "Alice" in output, "应该输出第一个学生Alice"
    assert "Eve" in output, "应该输出最后一个学生Eve"
    assert "Frank" in output, "应该包含新添加的Frank"
    
    return True
""",
            solution_code="""students = ["Alice", "Bob", "Charlie", "David", "Eve"]

# 1. 输出列表的长度
print(f"学生人数: {len(students)}")

# 2. 输出第一个和最后一个学生
print(f"第一个学生: {students[0]}")
print(f"最后一个学生: {students[-1]}")

# 3. 添加新学生
students.append("Frank")
print(f"添加Frank后: {students}")

# 4. 删除Charlie
students.remove("Charlie")
print(f"删除Charlie后: {students}")

# 5. 输出最终列表
print(f"最终学生列表: {students}")
""",
            hints=json.dumps([
                "使用len()函数获取列表长度",
                "使用索引访问元素，第一个是[0]，最后一个是[-1]",
                "使用append()方法添加元素",
                "使用remove()方法删除元素"
            ], ensure_ascii=False),
            points=25,
            time_limit=20,
            order_index=6,
            is_active=True
        )
        db.session.add(exercise6)
        
        # 练习7: 函数定义
        exercise7 = Exercise(
            week_id=week1.id,
            title="练习7: 定义函数",
            description="定义一个计算圆面积的函数",
            exercise_type="code",
            difficulty="intermediate",
            initial_code="""# 定义一个函数calculate_circle_area，接收半径作为参数
# 返回圆的面积（面积 = π * r²）
# 使用 3.14159 作为 π 的值

# 在这里编写你的代码

# 测试函数
radius = 5
area = calculate_circle_area(radius)
print(f"半径为{radius}的圆，面积为{area:.2f}")
""",
            test_code="""
def test_circle_area():
    exec(code, globals())
    
    # 测试不同半径
    assert abs(calculate_circle_area(1) - 3.14159) < 0.01, "半径1的面积应该约为3.14"
    assert abs(calculate_circle_area(5) - 78.53975) < 0.01, "半径5的面积应该约为78.54"
    assert abs(calculate_circle_area(10) - 314.159) < 0.01, "半径10的面积应该约为314.16"
    
    return True
""",
            solution_code="""def calculate_circle_area(radius):
    # 计算圆的面积
    pi = 3.14159
    area = pi * radius ** 2
    return area

# 测试函数
radius = 5
area = calculate_circle_area(radius)
print(f"半径为{radius}的圆，面积为{area:.2f}")
""",
            hints=json.dumps([
                "使用def关键字定义函数",
                "函数需要接收一个参数radius",
                "使用 ** 运算符计算平方",
                "使用return返回计算结果"
            ], ensure_ascii=False),
            points=25,
            time_limit=20,
            order_index=7,
            is_active=True
        )
        db.session.add(exercise7)
        
        # 练习8: Qwen API基础（概念题）
        exercise8 = Exercise(
            week_id=week1.id,
            title="练习8: 理解Qwen API",
            description="编写代码展示对Qwen API基本概念的理解",
            exercise_type="code",
            difficulty="intermediate",
            initial_code="""# 这是一个概念性练习，展示如何使用Qwen API
# 注意: 这里不会真正调用API，只是展示代码结构

# 模拟一个简单的API调用函数
def call_qwen_api(prompt, api_key="demo_key"):
    # 模拟调用Qwen API
    # 参数: prompt(提示词), api_key(API密钥)
    # 在实际应用中，这里会发送HTTP请求到Qwen API
    response = f"[模拟响应] 收到提示: '{prompt}'"
    return response

# 使用函数
user_prompt = "你好，请介绍一下Python"
response = call_qwen_api(user_prompt)
print(response)

# 任务: 修改上面的代码，添加以下功能:
# 1. 添加一个参数 temperature，默认值为0.7
# 2. 在返回的响应中包含 temperature 的值
# 3. 调用函数时传入 temperature=0.9

# 在这里编写你的代码

""",
            test_code="""
def test_api_understanding():
    import io
    import sys
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        exec(code)
    output = f.getvalue()
    
    # 检查是否包含关键信息
    assert "temperature" in output.lower() or "0.9" in output, "应该在输出中包含temperature参数"
    assert "模拟响应" in output or "收到提示" in output, "应该输出API响应"
    
    return True
""",
            solution_code="""def call_qwen_api(prompt, api_key="demo_key", temperature=0.7):
    # 模拟调用Qwen API
    # 参数: prompt(提示词), api_key(API密钥), temperature(随机性)
    response = f"[模拟响应] 收到提示: '{prompt}' (temperature={temperature})"
    return response

# 使用函数
user_prompt = "你好，请介绍一下Python"
response = call_qwen_api(user_prompt, temperature=0.9)
print(response)
print(f"\\n说明: temperature参数控制AI响应的随机性")
print(f"- temperature=0: 响应更确定、更保守")
print(f"- temperature=1: 响应更随机、更有创造性")
""",
            hints=json.dumps([
                "在函数定义中添加temperature参数",
                "设置默认值使用 temperature=0.7",
                "在返回的字符串中包含temperature的值",
                "调用函数时使用关键字参数传递temperature"
            ], ensure_ascii=False),
            points=30,
            time_limit=25,
            order_index=8,
            is_active=True
        )
        db.session.add(exercise8)
        
        db.session.commit()
        print(f"✅ Week 1 创建完成，包含 8 个练习")
        
        return week1


def init_all_weeks(app):
    """初始化所有周的数据（目前只有Week 1）"""
    with app.app_context():
        print("\n" + "="*60)
        print("🚀 开始初始化数据库")
        print("="*60 + "\n")
        
        # 初始化Week 1
        week1 = init_week1(app)
        
        # 统计信息
        total_weeks = Week.query.count()
        total_exercises = Exercise.query.count()
        
        print("\n" + "="*60)
        print("✅ 数据库初始化完成！")
        print("="*60)
        print(f"📚 总课程周数: {total_weeks}")
        print(f"💻 总练习数量: {total_exercises}")
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
    
    parser = argparse.ArgumentParser(description='数据库初始化脚本')
    parser.add_argument('--reset', action='store_true', help='重置数据库（删除所有数据）')
    args = parser.parse_args()
    
    app = create_app()
    
    if args.reset:
        reset_database(app)
    
    init_all_weeks(app)


if __name__ == "__main__":
    main()
