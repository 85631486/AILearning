# 数据库初始化脚本

## 概述

本目录包含数据库初始化脚本，用于创建课程和练习数据。

## 脚本说明

### init_database.py

数据库初始化脚本，用于创建Week 1-8的课程数据和练习题目。

**功能**:
- 创建课程周数据
- 创建练习题目
- 支持数据库重置

**使用方法**:

```bash
# 初始化数据（保留现有数据）
python3.11 scripts/init_database.py

# 重置数据库并初始化（删除所有现有数据）
python3.11 scripts/init_database.py --reset
```

## Week 1 课程内容

### 课程信息
- **标题**: Python基础与Qwen API入门
- **描述**: 学习Python基础语法，了解AI大模型概念，掌握Qwen API的基本使用方法
- **练习数量**: 8个

### 练习列表

#### 练习1: Hello World
- **难度**: 初级 (beginner)
- **分数**: 10分
- **时间限制**: 5分钟
- **描述**: 编写你的第一个Python程序，输出'Hello, World!'

#### 练习2: 变量和数据类型
- **难度**: 初级 (beginner)
- **分数**: 15分
- **时间限制**: 10分钟
- **描述**: 创建不同类型的变量并输出它们的值和类型

#### 练习3: 获取用户输入
- **难度**: 初级 (beginner)
- **分数**: 15分
- **时间限制**: 10分钟
- **描述**: 使用input()函数获取用户输入，并进行简单的处理

#### 练习4: 条件判断
- **难度**: 初级 (beginner)
- **分数**: 20分
- **时间限制**: 15分钟
- **描述**: 使用if-elif-else语句根据分数判断等级

#### 练习5: for循环
- **难度**: 初级 (beginner)
- **分数**: 20分
- **时间限制**: 15分钟
- **描述**: 使用for循环计算1到100的和

#### 练习6: 列表基础
- **难度**: 中级 (intermediate)
- **分数**: 25分
- **时间限制**: 20分钟
- **描述**: 创建列表并进行基本操作

#### 练习7: 定义函数
- **难度**: 中级 (intermediate)
- **分数**: 25分
- **时间限制**: 20分钟
- **描述**: 定义一个计算圆面积的函数

#### 练习8: 理解Qwen API
- **难度**: 中级 (intermediate)
- **分数**: 30分
- **时间限制**: 25分钟
- **描述**: 编写代码展示对Qwen API基本概念的理解

## 数据库结构

### Week表
- `id`: 主键
- `week_number`: 周数 (1-8)
- `title`: 标题
- `description`: 描述
- `content_path`: 内容路径
- `is_active`: 是否激活
- `created_at`: 创建时间
- `updated_at`: 更新时间

### Exercise表
- `id`: 主键
- `week_id`: 所属周ID（外键）
- `title`: 标题
- `description`: 描述
- `exercise_type`: 练习类型 (code, prompt, project)
- `difficulty`: 难度 (beginner, intermediate, advanced)
- `initial_code`: 初始代码模板
- `test_code`: 测试代码
- `solution_code`: 参考答案
- `hints`: 提示信息 (JSON)
- `points`: 分数
- `time_limit`: 时间限制（分钟）
- `order_index`: 排序索引
- `is_active`: 是否激活
- `created_at`: 创建时间
- `updated_at`: 更新时间

## 注意事项

1. **数据库重置**: 使用 `--reset` 参数会删除所有现有数据，请谨慎使用
2. **数据完整性**: 脚本会检查数据是否已存在，避免重复创建
3. **JSON格式**: hints字段使用JSON格式存储，确保使用`ensure_ascii=False`保持中文
4. **外键关系**: Exercise表通过week_id关联到Week表

## 扩展

要添加更多周的数据，可以参考`init_week1()`函数的实现，创建类似的函数：

```python
def init_week2(app):
    """初始化Week 2: 高级Python特性"""
    with app.app_context():
        # 检查Week 2是否已存在
        week2 = Week.query.filter_by(week_number=2).first()
        if week2:
            print("⚠️  Week 2 已存在，跳过创建")
            return week2
        
        # 创建Week 2
        week2 = Week(
            week_number=2,
            title="高级Python特性",
            description="学习Python高级特性...",
            is_active=True
        )
        db.session.add(week2)
        db.session.flush()
        
        # 添加练习...
        
        db.session.commit()
        return week2
```

然后在`init_all_weeks()`函数中调用：

```python
def init_all_weeks(app):
    with app.app_context():
        week1 = init_week1(app)
        week2 = init_week2(app)  # 添加这一行
        # ...
```

## 测试

初始化完成后，可以通过以下方式测试：

```bash
# 测试获取课程周列表
curl http://localhost:5000/api/v1/learning/weeks

# 测试获取练习列表
curl http://localhost:5000/api/v1/exercises?week_id=1

# 测试获取特定练习
curl http://localhost:5000/api/v1/exercises/1
```

## 故障排除

### 问题1: 数据库模型不匹配
**错误**: `no such column: exercises.xxx`

**解决方案**:
```bash
# 重置数据库
python3.11 scripts/init_database.py --reset
```

### 问题2: 数据已存在
**现象**: 脚本提示"Week 1 已存在，跳过创建"

**解决方案**:
- 如果需要重新创建，使用 `--reset` 参数
- 如果只需要添加新数据，修改脚本添加新的周

### 问题3: JSON编码错误
**错误**: 中文显示为Unicode编码

**解决方案**: 确保使用 `json.dumps(..., ensure_ascii=False)`

## 维护

- **定期备份**: 在重置数据库前备份重要数据
- **版本控制**: 使用Flask-Migrate管理数据库迁移
- **数据验证**: 添加数据验证逻辑确保数据完整性

## 相关文档

- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate文档](https://flask-migrate.readthedocs.io/)
- [项目README](../README.md)
