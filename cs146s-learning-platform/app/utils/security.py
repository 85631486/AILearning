import ast
import re
import html

class CodeSecurityChecker:
    """代码安全检查器"""

    # 扩展的危险模式检测
    DANGEROUS_PATTERNS = [
        # 系统和文件操作
        r'import\s+(os|sys|subprocess|socket|urllib|http|shutil|pathlib)',
        r'from\s+(os|sys|subprocess|socket|urllib|http|shutil|pathlib)',
        r'__\w+__',  # 私有属性访问
        r'eval\s*\(',
        r'exec\s*\(',
        r'open\s*\(',
        r'file\s*\(',
        # input() 允许使用，通过stdin重定向处理
        # 文件系统操作
        r'\.remove\s*\(',
        r'\.unlink\s*\(',
        r'\.rmdir\s*\(',
        r'\.rename\s*\(',
        # 进程操作
        r'\.kill\s*\(',
        r'\.terminate\s*\(',
        # 网络操作
        r'\.connect\s*\(',
        r'\.bind\s*\(',
        r'\.listen\s*\(',
        r'\.accept\s*\(',
        # 动态代码执行
        r'compile\s*\(',
        r'getattr\s*\(',
        r'setattr\s*\(',
        r'delattr\s*\(',
        # 内存操作
        r'ctypes',
        r'mmap',
    ]

    FORBIDDEN_FUNCTIONS = [
        # 系统命令
        'exit', 'quit', 'system', 'popen', 'call', 'run',
        'spawn', 'Popen', 'check_output', 'check_call',
        # 文件操作
        'remove', 'unlink', 'rmdir', 'rename', 'chmod', 'chown',
        # 进程操作
        'kill', 'terminate', 'killpg',
        # 网络操作
        'connect', 'bind', 'listen', 'accept', 'send', 'recv',
        # 危险的内置函数
        'globals', 'locals', 'vars', 'dir', '__import__',
        # 动态执行
        'compile', 'execfile',
    ]

    # 允许的模块白名单
    ALLOWED_MODULES = {
        'math', 'random', 'datetime', 'time', 'collections',
        'itertools', 'functools', 'operator', 'string',
        're', 'json', 'csv', 'heapq', 'bisect', 'array',
        'copy', 'pprint', 'reprlib', 'enum', 'numbers',
        'fractions', 'decimal', 'statistics', 'contextlib'
    }

    def check_code(self, code: str) -> dict:
        """检查代码安全性"""
        issues = []

        # 检查危险模式
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    'type': 'dangerous_pattern',
                    'pattern': pattern,
                    'message': f'检测到危险代码模式: {pattern}'
                })

        # 检查禁止函数
        for func in self.FORBIDDEN_FUNCTIONS:
            if re.search(r'\b' + re.escape(func) + r'\s*\(', code):
                issues.append({
                    'type': 'forbidden_function',
                    'function': func,
                    'message': f'禁止使用函数: {func}'
                })

        # AST分析
        try:
            tree = ast.parse(code)
            ast_issues = self._analyze_ast(tree)
            issues.extend(ast_issues)
        except SyntaxError as e:
            issues.append({
                'type': 'syntax_error',
                'message': f'语法错误: {e.msg}',
                'line': e.lineno
            })

        return {
            'is_safe': len(issues) == 0,
            'issues': issues
        }

    def _analyze_ast(self, tree: ast.AST) -> list:
        """AST深度分析"""
        issues = []

        class SecurityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.imported_modules = set()

            def visit_Import(self, node):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]  # 获取顶级模块名
                    self.imported_modules.add(module_name)

                    # 检查危险导入
                    if module_name in ['os', 'sys', 'subprocess', 'socket', 'urllib', 'http', 'shutil', 'ctypes']:
                        issues.append({
                            'type': 'dangerous_import',
                            'module': module_name,
                            'message': f'禁止导入模块: {module_name}'
                        })
                    # 检查不在白名单中的模块
                    elif module_name not in CodeSecurityChecker.ALLOWED_MODULES and module_name not in ['__future__']:
                        issues.append({
                            'type': 'restricted_import',
                            'module': module_name,
                            'message': f'模块不在允许列表中: {module_name}'
                        })
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                module_name = node.module.split('.')[0] if node.module else None
                if module_name:
                    self.imported_modules.add(module_name)

                    # 检查危险导入
                    if module_name in ['os', 'sys', 'subprocess', 'socket', 'urllib', 'http', 'shutil', 'ctypes']:
                        issues.append({
                            'type': 'dangerous_import',
                            'module': node.module,
                            'message': f'禁止导入模块: {node.module}'
                        })
                    # 检查不在白名单中的模块
                    elif module_name not in CodeSecurityChecker.ALLOWED_MODULES:
                        issues.append({
                            'type': 'restricted_import',
                            'module': module_name,
                            'message': f'模块不在允许列表中: {module_name}'
                        })

                self.generic_visit(node)

            def visit_Call(self, node):
                # 检查函数调用
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in CodeSecurityChecker.FORBIDDEN_FUNCTIONS:
                        issues.append({
                            'type': 'forbidden_function_call',
                            'function': func_name,
                            'message': f'禁止调用函数: {func_name}'
                        })
                elif isinstance(node.func, ast.Attribute):
                    # 检查方法调用
                    if isinstance(node.func.value, ast.Name):
                        obj_name = node.func.value.id
                        method_name = node.func.attr

                        # 检查对象.方法调用
                        dangerous_methods = ['system', 'popen', 'call', 'run', 'exec', 'eval', 'open']
                        if method_name in dangerous_methods:
                            issues.append({
                                'type': 'dangerous_method_call',
                                'method': f'{obj_name}.{method_name}',
                                'message': f'禁止调用方法: {obj_name}.{method_name}'
                            })

                self.generic_visit(node)

            def visit_Attribute(self, node):
                # 检查私有属性访问
                if isinstance(node.attr, str) and node.attr.startswith('__') and node.attr.endswith('__'):
                    issues.append({
                        'type': 'private_attribute_access',
                        'attribute': node.attr,
                        'message': f'禁止访问私有属性: {node.attr}'
                    })

                self.generic_visit(node)

        visitor = SecurityVisitor()
        visitor.visit(tree)

        return issues


class InputValidator:
    """输入验证器"""

    @staticmethod
    def validate_code(code: str, max_length: int = 50000) -> dict:
        """验证代码输入"""
        if not isinstance(code, str):
            return {'valid': False, 'error': '代码必须是字符串类型'}

        if len(code) > max_length:
            return {'valid': False, 'error': f'代码长度超过限制 ({max_length} 字符)'}

        if len(code.strip()) == 0:
            return {'valid': False, 'error': '代码不能为空'}

        # 检查基本语法
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return {'valid': False, 'error': f'语法错误: {e.msg} (行 {e.lineno})'}

        return {'valid': True}

    @staticmethod
    def validate_message(message: str, max_length: int = 10000) -> dict:
        """验证消息输入"""
        if not isinstance(message, str):
            return {'valid': False, 'error': '消息必须是字符串类型'}

        if len(message) > max_length:
            return {'valid': False, 'error': f'消息长度超过限制 ({max_length} 字符)'}

        if len(message.strip()) == 0:
            return {'valid': False, 'error': '消息不能为空'}

        return {'valid': True}

    @staticmethod
    def validate_exercise_id(exercise_id: int) -> dict:
        """验证练习ID"""
        if not isinstance(exercise_id, int) or exercise_id <= 0:
            return {'valid': False, 'error': '练习ID必须是正整数'}

        return {'valid': True}

    @staticmethod
    def sanitize_html(text: str) -> str:
        """清理HTML内容，防止XSS"""
        if not isinstance(text, str):
            return ""

        # 使用html.escape进行基础转义
        return html.escape(text, quote=True)

    @staticmethod
    def validate_json_data(data, max_depth: int = 10, max_size: int = 1000000) -> dict:
        """验证JSON数据结构"""
        if data is None:
            return {'valid': True}

        def check_depth(obj, current_depth=0):
            if current_depth > max_depth:
                return False

            if isinstance(obj, dict):
                return all(check_depth(v, current_depth + 1) for v in obj.values())
            elif isinstance(obj, (list, tuple)):
                return all(check_depth(item, current_depth + 1) for item in obj)
            else:
                return True

        if not check_depth(data):
            return {'valid': False, 'error': f'数据结构深度超过限制 ({max_depth})'}

        # 估算数据大小
        try:
            import json
            size = len(json.dumps(data))
            if size > max_size:
                return {'valid': False, 'error': f'数据大小超过限制 ({max_size} 字节)'}
        except:
            pass

        return {'valid': True}
