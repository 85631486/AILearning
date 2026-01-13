"""测试安全代码执行器"""

import pytest
import tempfile
import os
import platform
from unittest.mock import patch, MagicMock
from app.services.code_executor import SecureCodeExecutor
from app.utils.security import CodeSecurityChecker


class TestSecureCodeExecutor:
    """安全代码执行器测试"""

    def setup_method(self):
        """测试前准备"""
        self.executor = SecureCodeExecutor()

    def teardown_method(self):
        """测试后清理"""
        # 清理可能遗留的临时文件
        pass

    def test_safe_code_execution(self):
        """测试安全代码执行"""
        code = "print('Hello World')"
        result = self.executor.execute_code(code)

        assert result['success'] == True
        assert 'Hello World' in result['stdout']
        assert result['returncode'] == 0
        assert 'execution_time' in result

    def test_code_with_input(self):
        """测试带输入的代码执行"""
        code = "name = input('Enter name: ')\nprint(f'Hello {name}')"
        inputs = {"stdin": "Alice"}
        result = self.executor.execute_code(code, inputs)

        assert result['success'] == True
        assert 'Hello Alice' in result['stdout']

    def test_dangerous_import_blocked(self):
        """测试危险导入被阻止"""
        code = "import os\nos.system('echo hello')"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']
        assert 'issues' in result

    def test_dangerous_function_blocked(self):
        """测试危险函数被阻止"""
        code = "import subprocess\nsubprocess.call(['echo', 'hello'])"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']

    def test_eval_blocked(self):
        """测试eval函数被阻止"""
        code = "result = eval('1 + 1')\nprint(result)"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']

    def test_exec_blocked(self):
        """测试exec函数被阻止"""
        code = "exec('print(\"hello\")')"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']

    def test_file_operations_blocked(self):
        """测试文件操作被阻止"""
        code = "with open('test.txt', 'w') as f:\n    f.write('hello')"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '不安全的操作' in result['error']

    def test_private_attribute_access_blocked(self):
        """测试私有属性访问被阻止"""
        code = "class Test:\n    def __init__(self):\n        self.__private = 'secret'\nprint('done')"
        result = self.executor.execute_code(code)

        # 这应该通过，因为只是定义类，不调用私有属性
        assert result['success'] == True

    def test_syntax_error_handling(self):
        """测试语法错误处理"""
        code = "print('hello world'"  # 缺少右括号
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '语法错误' in result['error']

    @pytest.mark.skipif(platform.system() == 'Windows', reason="Timeout test may behave differently on Windows")
    def test_timeout_handling(self):
        """测试超时处理"""
        code = "import time\ntime.sleep(10)"  # 比默认超时时间长的代码
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert result.get('timeout') == True or '超时' in result['error']

    def test_memory_limit_enforcement(self):
        """测试内存限制执行"""
        # 创建一个大列表来消耗内存
        code = "data = [0] * (50 * 1024 * 1024)  # 约200MB数据"
        result = self.executor.execute_code(code)

        # 在有内存限制的系统上应该失败
        if hasattr(self.executor, 'max_memory_mb') and self.executor.max_memory_mb < 200:
            assert result['success'] == False

    def test_complex_allowed_code(self):
        """测试复杂的允许代码"""
        code = """
import math
import random
from collections import defaultdict

# 复杂的数学计算
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 数据结构使用
data = defaultdict(list)
for i in range(10):
    data[random.choice(['a', 'b', 'c'])].append(i)

# 数学函数使用
result = math.sqrt(144) + fibonacci(10)
print(f"Result: {result}")
"""
        result = self.executor.execute_code(code)
        assert result['success'] == True
        assert 'Result:' in result['stdout']

    def test_empty_code_rejection(self):
        """测试空代码被拒绝"""
        result = self.executor.execute_code("")
        assert result['success'] == False
        assert '不能为空' in result['error']

    def test_whitespace_only_code_rejection(self):
        """测试只有空白字符的代码被拒绝"""
        result = self.executor.execute_code("   \n\t   ")
        assert result['success'] == False
        assert '不能为空' in result['error']

    def test_temporary_file_cleanup(self):
        """测试临时文件清理"""
        code = "print('test')"
        result = self.executor.execute_code(code)

        # 检查临时文件是否被清理（这很难直接测试，但至少确保执行成功）
        assert result['success'] == True

    @patch('subprocess.run')
    def test_command_execution_fallback(self, mock_run):
        """测试命令执行回退"""
        mock_run.side_effect = FileNotFoundError("python not found")

        code = "print('test')"
        result = self.executor.execute_code(code)

        assert result['success'] == False
        assert '未找到' in result['error']

    def test_config_values_used(self):
        """测试配置值被正确使用"""
        # 创建一个带有自定义配置的执行器
        with patch('current_app.config') as mock_config:
            mock_config.get.side_effect = lambda key, default: {
                'CODE_EXECUTION_TIMEOUT': 60,
                'MAX_MEMORY_MB': 200,
                'MAX_CPU_TIME': 20
            }.get(key, default)

            executor = SecureCodeExecutor()
            assert executor.max_execution_time == 60
            assert executor.max_memory_mb == 200
            assert executor.max_cpu_time == 20

    def test_input_validation(self):
        """测试输入数据验证"""
        # 测试有效的输入
        code = "print('test')"
        inputs = {"stdin": "valid input"}
        result = self.executor.execute_code(code, inputs)
        assert result['success'] == True

        # 测试None输入（应该正常工作）
        result = self.executor.execute_code(code, None)
        assert result['success'] == True

    def test_exception_handling(self):
        """测试异常处理"""
        # 强制触发异常
        with patch.object(self.executor, '_execute_with_limits', side_effect=Exception("Test error")):
            result = self.executor.execute_code("print('test')")
            assert result['success'] == False
            assert 'Test error' in result['error']

    def test_cross_platform_compatibility(self):
        """测试跨平台兼容性"""
        code = "print('Cross-platform test')"
        result = self.executor.execute_code(code)

        # 应该在所有平台上工作
        assert result['success'] == True
        assert 'Cross-platform test' in result['stdout']
