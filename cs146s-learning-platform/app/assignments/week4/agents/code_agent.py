"""
Week 4: 代码代理 - 专门负责编写和修改代码的代理
"""

import os
import ast
import inspect
from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent, AgentMessage, Task


class CodeAgent(BaseAgent):
    """代码代理 - 负责编写和重构代码"""

    def __init__(self):
        super().__init__(
            name="code_agent",
            role="软件工程师",
            capabilities=["write_code", "refactor_code", "fix_bugs", "add_features"]
        )

        # 添加代码工具
        self.add_tool("analyze_code", self._analyze_code_structure)
        self.add_tool("generate_function", self._generate_function)
        self.add_tool("refactor_code", self._refactor_code)
        self.add_tool("add_docstring", self._add_docstring)

    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """处理消息"""
        if message.message_type == "task_assignment":
            task_data = message.content.get("task", {})
            task_description = task_data.get("description", "")

            if any(keyword in task_description.lower() for keyword in ["write", "code", "implement", "create"]):
                # 处理代码编写任务
                result = self._handle_code_task(task_data)
                return AgentMessage(
                    sender=self.name,
                    receiver="orchestrator",
                    message_type="task_completed",
                    content={"task_id": task_data.get("task_id"), "result": result},
                    metadata={"original_task": task_data.get("task_id")}
                )

        return None

    def generate_response(self, task: str, context: Dict) -> str:
        """生成任务响应"""
        if "write function" in task.lower():
            return self._generate_function_code(
                context.get("function_name", "example_function"),
                context.get("parameters", []),
                context.get("description", "")
            )
        elif "refactor" in task.lower():
            return self._refactor_code(context.get("code", ""), context.get("improvements", []))
        else:
            return f"代码代理：我可以帮助编写和重构代码。任务：{task}"

    def _handle_code_task(self, task_data: Dict) -> Dict[str, Any]:
        """处理代码任务"""
        task_id = task_data.get("task_id", "")
        description = task_data.get("description", "")

        result = {
            "task_id": task_id,
            "status": "processing",
            "code_generated": "",
            "analysis": {}
        }

        try:
            if "function" in description.lower():
                # 生成函数代码
                func_name = self._extract_function_name(description)
                params = self._extract_parameters(description)
                code = self.use_tool("generate_function",
                                   name=func_name,
                                   params=params,
                                   description=description)
                result["code_generated"] = code

            elif "refactor" in description.lower():
                # 重构代码
                code_path = description.split("file:")[-1].strip() if "file:" in description else ""
                refactored = self.use_tool("refactor_code", code_path=code_path)
                result["code_generated"] = refactored

            # 分析生成的代码
            analysis = self.use_tool("analyze_code", code=result["code_generated"])
            result["analysis"] = analysis

            result["status"] = "completed"

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        return result

    def _analyze_code_structure(self, code: str) -> Dict[str, Any]:
        """分析代码结构"""
        try:
            tree = ast.parse(code)

            analysis = {
                'functions': [],
                'classes': [],
                'imports': [],
                'complexity': 0,
                'lines': len(code.split('\n'))
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append({
                        'name': node.name,
                        'args_count': len(node.args.args),
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append({
                        'name': node.name,
                        'line': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    analysis['imports'].extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    analysis['imports'].append(f"{node.module}.{node.names[0].name}" if node.names else node.module)

            # 简单的复杂度计算
            analysis['complexity'] = len(analysis['functions']) + len(analysis['classes']) * 2

            return analysis

        except SyntaxError as e:
            return {'error': f'代码语法错误: {e}'}

    def _generate_function(self, name: str, params: List[str], description: str) -> str:
        """生成函数代码"""
        # 参数处理
        param_str = ", ".join(params) if params else ""

        # 函数模板
        function_template = f'''def {name}({param_str}):
    """
    {description or f"{name} 函数实现"}
    """
    # TODO: 实现函数逻辑
    pass

'''

        return function_template

    def _refactor_code(self, code: str) -> str:
        """重构代码"""
        try:
            # 简单的重构示例：改进变量命名、添加类型提示等
            lines = code.split('\n')
            refactored_lines = []

            for line in lines:
                # 示例重构：将简单的变量名改进
                line = line.replace('x =', 'result =')
                line = line.replace('y =', 'value =')
                refactored_lines.append(line)

            return '\n'.join(refactored_lines)

        except Exception as e:
            return f"# 重构失败: {e}\n{code}"

    def _add_docstring(self, code: str) -> str:
        """为函数添加文档字符串"""
        try:
            tree = ast.parse(code)
            lines = code.split('\n')

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 在函数定义后添加docstring
                    func_line = node.lineno - 1  # 转换为0索引
                    if func_line + 1 < len(lines):
                        # 检查是否已有docstring
                        if not (func_line + 1 < len(lines) and '"""' in lines[func_line + 1]):
                            # 插入docstring
                            docstring = f'    """{node.name} 函数的文档字符串"""'
                            lines.insert(func_line + 1, docstring)
                            lines.insert(func_line + 2, '    ')

            return '\n'.join(lines)

        except Exception as e:
            return code

    def _extract_function_name(self, description: str) -> str:
        """从描述中提取函数名"""
        # 简单的提取逻辑
        words = description.lower().split()
        if "function" in words:
            idx = words.index("function")
            if idx + 1 < len(words):
                return words[idx + 1].replace(',', '').replace('.', '')

        return "example_function"

    def _extract_parameters(self, description: str) -> List[str]:
        """从描述中提取参数"""
        # 简单的参数提取
        if "takes" in description.lower():
            # 查找参数描述
            return ["param1", "param2"]  # 默认参数

        return ["value"]
