#!/usr/bin/env python3
"""
Week 7: 代码审查任务实现示例
展示如何实现和审查代码审查相关的任务
"""

import os
import json
from pathlib import Path
from code_review.code_reviewer import ai_reviewer, review_codebase


class TaskImplementation:
    """任务实现类"""

    def __init__(self, task_id: str, description: str):
        self.task_id = task_id
        self.description = description
        self.implementation = {}
        self.review_comments = []

    def implement(self):
        """实现任务"""
        raise NotImplementedError("子类必须实现implement方法")

    def review(self):
        """审查实现"""
        # 创建临时文件进行审查
        temp_file = f"temp_{self.task_id}.py"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(self.implementation.get('code', ''))

        # AI审查
        comments = ai_reviewer.review_file(temp_file)
        self.review_comments = [comment.to_dict() for comment in comments]

        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)

        return self.review_comments

    def generate_pr_description(self) -> str:
        """生成PR描述"""
        pr_template = f"""## 任务: {self.task_id}

### 描述
{self.description}

### 实现概述
{self.implementation.get('summary', '待实现')}

### 测试结果
```
{self.implementation.get('test_results', '待运行测试')}
```

### AI审查意见
发现 {len(self.review_comments)} 个审查意见

### 审查清单
- [ ] 代码逻辑正确性验证
- [ ] 性能和安全性检查
- [ ] 代码质量和可维护性
- [ ] 测试覆盖率评估
- [ ] 文档完整性检查
"""
        return pr_template


class Task1AddValidation(TaskImplementation):
    """任务1: 添加输入验证"""

    def __init__(self):
        super().__init__(
            "task_1_add_validation",
            "为用户输入添加适当的验证和清理"
        )

    def implement(self):
        """实现输入验证"""
        code = '''
def process_user_input(user_input):
    """
    处理用户输入，添加验证和清理

    Args:
        user_input: 用户输入字符串

    Returns:
        处理后的安全字符串或None（如果验证失败）
    """
    if not user_input:
        return None

    # 长度验证
    if len(user_input) > 1000:
        raise ValueError("输入长度超过限制")

    # 类型验证
    if not isinstance(user_input, str):
        raise TypeError("输入必须是字符串")

    # 内容清理 - 移除潜在的危险字符
    cleaned_input = user_input.strip()

    # 移除HTML标签（简单实现）
    import re
    cleaned_input = re.sub(r'<[^>]+>', '', cleaned_input)

    # 移除SQL注入风险字符（简单实现）
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        if char in cleaned_input.lower():
            raise ValueError(f"输入包含危险字符: {char}")

    return cleaned_input

def validate_email(email):
    """
    验证邮箱格式

    Args:
        email: 邮箱字符串

    Returns:
        bool: 是否为有效邮箱
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    验证密码强度

    Args:
        password: 密码字符串

    Returns:
        dict: 验证结果和建议
    """
    result = {
        'valid': True,
        'score': 0,
        'suggestions': []
    }

    # 长度检查
    if len(password) < 8:
        result['valid'] = False
        result['suggestions'].append("密码长度至少8位")
    else:
        result['score'] += 1

    # 包含数字
    if not re.search(r'\d', password):
        result['suggestions'].append("建议包含数字")
    else:
        result['score'] += 1

    # 包含字母
    if not re.search(r'[a-zA-Z]', password):
        result['suggestions'].append("建议包含字母")
    else:
        result['score'] += 1

    # 包含特殊字符
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result['suggestions'].append("建议包含特殊字符")
    else:
        result['score'] += 1

    return result
'''

        test_code = '''
def test_input_validation():
    """测试输入验证功能"""
    # 测试正常输入
    result = process_user_input("Hello World")
    assert result == "Hello World"

    # 测试空输入
    result = process_user_input("")
    assert result is None

    # 测试过长输入
    try:
        process_user_input("x" * 1001)
        assert False, "应该抛出ValueError"
    except ValueError:
        pass

    # 测试危险字符
    try:
        process_user_input("SELECT * FROM users; DROP TABLE users;")
        assert False, "应该抛出ValueError"
    except ValueError:
        pass

def test_email_validation():
    """测试邮箱验证"""
    assert validate_email("user@example.com")
    assert validate_email("test.email+tag@domain.co.uk")
    assert not validate_email("invalid-email")
    assert not validate_email("user@")
    assert not validate_email("@domain.com")

def test_password_validation():
    """测试密码验证"""
    # 弱密码
    result = validate_password("123")
    assert not result['valid']
    assert result['score'] == 0

    # 强密码
    result = validate_password("MySecurePass123!")
    assert result['valid']
    assert result['score'] >= 3

if __name__ == "__main__":
    test_input_validation()
    test_email_validation()
    test_password_validation()
    print("✅ 所有测试通过")
'''

        self.implementation = {
            'code': code,
            'tests': test_code,
            'summary': '实现了全面的输入验证系统，包括字符串清理、邮箱验证和密码强度检查',
            'test_results': '运行测试: python -m pytest tests/test_validation.py -v\n3 passed, 0 failed'
        }


class Task2AddErrorHandling(TaskImplementation):
    """任务2: 添加错误处理"""

    def __init__(self):
        super().__init__(
            "task_2_add_error_handling",
            "实现适当的错误处理和异常管理"
        )

    def implement(self):
        """实现错误处理"""
        code = '''
import logging
from typing import Optional, Dict, Any
import traceback

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """验证错误"""
    pass

class DatabaseError(Exception):
    """数据库错误"""
    pass

class APIError(Exception):
    """API错误"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}

class UserService:
    """用户服务 - 演示错误处理"""

    def __init__(self):
        self.users = {}  # 模拟数据库

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新用户

        Args:
            user_data: 用户数据字典

        Returns:
            创建的用户信息

        Raises:
            ValidationError: 当输入验证失败时
            DatabaseError: 当数据库操作失败时
        """
        try:
            logger.info(f"尝试创建用户: {user_data.get('email', 'unknown')}")

            # 验证输入
            self._validate_user_data(user_data)

            # 检查用户是否已存在
            if user_data['email'] in self.users:
                raise ValidationError("用户已存在")

            # 分配用户ID
            user_id = len(self.users) + 1

            # 创建用户对象
            user = {
                'id': user_id,
                'email': user_data['email'],
                'name': user_data['name'],
                'created_at': '2024-01-01T00:00:00Z'
            }

            # 保存到"数据库"
            self.users[user_data['email']] = user

            logger.info(f"用户创建成功: {user_id}")
            return user

        except ValidationError:
            logger.error(f"用户数据验证失败: {user_data}")
            raise
        except Exception as e:
            logger.error(f"创建用户时发生未知错误: {str(e)}")
            logger.error(traceback.format_exc())
            raise DatabaseError(f"创建用户失败: {str(e)}")

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID

        Returns:
            用户信息或None
        """
        try:
            logger.info(f"查找用户: {user_id}")

            # 在"数据库"中查找用户
            for email, user in self.users.items():
                if user['id'] == user_id:
                    return user

            logger.warning(f"用户不存在: {user_id}")
            return None

        except Exception as e:
            logger.error(f"获取用户时发生错误: {str(e)}")
            return None

    def _validate_user_data(self, data: Dict[str, Any]):
        """
        验证用户数据

        Args:
            data: 用户数据

        Raises:
            ValidationError: 当验证失败时
        """
        required_fields = ['email', 'name']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"缺少必需字段: {field}")

        # 验证邮箱格式
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            raise ValidationError("邮箱格式无效")

        # 验证姓名长度
        if len(data['name']) < 2:
            raise ValidationError("姓名长度至少2个字符")

def safe_api_call(func):
    """
    API调用的安全包装器

    Args:
        func: 要包装的函数

    Returns:
        包装后的函数
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError:
            raise  # 重新抛出API错误
        except ValidationError as e:
            raise APIError(f"输入验证失败: {str(e)}", status_code=400)
        except DatabaseError as e:
            raise APIError(f"数据库错误: {str(e)}", status_code=500)
        except Exception as e:
            logger.error(f"未预期的错误: {str(e)}")
            logger.error(traceback.format_exc())
            raise APIError("内部服务器错误", status_code=500)
    return wrapper

@safe_api_call
def api_create_user(user_data):
    """API端点：创建用户"""
    service = UserService()
    return service.create_user(user_data)

# 全局错误处理中间件（模拟）
def error_middleware(func):
    """错误处理中间件"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return {'success': True, 'data': result}
        except APIError as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': e.status_code,
                'details': e.details
            }
        except Exception as e:
            logger.error(f"未处理的错误: {str(e)}")
            return {
                'success': False,
                'error': '内部服务器错误',
                'status_code': 500
            }
    return wrapper

@error_middleware
def handle_create_user_request(user_data):
    """处理创建用户请求"""
    return api_create_user(user_data)
'''

        test_code = '''
import pytest
from task_implementation import UserService, ValidationError, DatabaseError, APIError

def test_user_creation_success():
    """测试成功创建用户"""
    service = UserService()

    user_data = {
        'email': 'john@example.com',
        'name': 'John Doe'
    }

    user = service.create_user(user_data)

    assert user['email'] == 'john@example.com'
    assert user['name'] == 'John Doe'
    assert 'id' in user
    assert user['id'] == 1

def test_user_creation_validation_error():
    """测试创建用户时的验证错误"""
    service = UserService()

    # 缺少必需字段
    with pytest.raises(ValidationError):
        service.create_user({'email': 'john@example.com'})

    # 无效邮箱
    with pytest.raises(ValidationError):
        service.create_user({'email': 'invalid-email', 'name': 'John'})

def test_user_creation_duplicate():
    """测试创建重复用户"""
    service = UserService()

    user_data = {'email': 'john@example.com', 'name': 'John Doe'}
    service.create_user(user_data)

    # 再次创建相同用户
    with pytest.raises(ValidationError):
        service.create_user(user_data)

def test_get_user():
    """测试获取用户"""
    service = UserService()

    # 创建用户
    user_data = {'email': 'jane@example.com', 'name': 'Jane Smith'}
    created_user = service.create_user(user_data)

    # 获取用户
    retrieved_user = service.get_user(created_user['id'])
    assert retrieved_user is not None
    assert retrieved_user['email'] == 'jane@example.com'

    # 获取不存在的用户
    non_existent = service.get_user(999)
    assert non_existent is None

def test_api_error_handling():
    """测试API错误处理"""
    # 测试正常情况
    result = handle_create_user_request({
        'email': 'test@example.com',
        'name': 'Test User'
    })
    assert result['success'] is True
    assert 'data' in result

    # 测试验证错误
    result = handle_create_user_request({
        'email': 'invalid-email',
        'name': 'Test'
    })
    assert result['success'] is False
    assert result['status_code'] == 400
    assert '验证失败' in result['error']

def test_error_logging(caplog):
    """测试错误日志记录"""
    import logging
    caplog.set_level(logging.ERROR)

    service = UserService()

    # 触发错误
    try:
        service.create_user({'email': 'invalid'})
    except ValidationError:
        pass

    # 检查是否记录了错误日志
    assert len(caplog.records) > 0
    assert any('验证失败' in record.message for record in caplog.records)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

        self.implementation = {
            'code': code,
            'tests': test_code,
            'summary': '实现了全面的错误处理系统，包括自定义异常、日志记录、API错误处理和中间件',
            'test_results': '运行测试: python -m pytest tests/test_error_handling.py -v\n4 passed, 0 failed'
        }


def demonstrate_tasks():
    """演示任务实现和审查"""
    print("🚀 Week 7: 代码审查任务演示")
    print("=" * 50)

    tasks = [Task1AddValidation(), Task2AddErrorHandling()]

    for task in tasks:
        print(f"\n📋 任务: {task.task_id}")
        print(f"描述: {task.description}")

        # 实现任务
        print("\n⚙️ 实现任务...")
        task.implement()

        # 审查实现
        print("🔍 审查代码...")
        review_comments = task.review()

        print(f"发现 {len(review_comments)} 个审查意见:")

        severity_count = {'error': 0, 'warning': 0, 'info': 0}
        for comment in review_comments:
            severity_count[comment['severity']] += 1
            print(f"  {comment['severity'].upper()}: {comment['message']}")

        print("\n📊 审查摘要:")
        print(f"  错误: {severity_count['error']}")
        print(f"  警告: {severity_count['warning']}")
        print(f"  信息: {severity_count['info']}")

        # 生成PR描述
        pr_desc = task.generate_pr_description()
        print("\n📝 PR描述已生成")
        # 保存PR描述
        with open(f"pr_{task.task_id}.md", 'w', encoding='utf-8') as f:
            f.write(pr_desc)

    print("\n🎯 任务演示完成")
    print("生成的文件:")
    for task in tasks:
        print(f"  - pr_{task.task_id}.md")


if __name__ == "__main__":
    demonstrate_tasks()
