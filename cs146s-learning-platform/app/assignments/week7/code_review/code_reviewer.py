#!/usr/bin/env python3
"""
Week 7: AI辅助代码审查工具
模拟AI驱动的代码审查功能，用于教学演示
"""

import os
import re
import ast
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime


class CodeReviewComment:
    """代码审查评论"""

    def __init__(self, file_path: str, line_number: int, severity: str,
                 category: str, message: str, suggestion: str = "",
                 reviewer: str = "AI"):
        self.file_path = file_path
        self.line_number = line_number
        self.severity = severity  # 'info', 'warning', 'error'
        self.category = category
        self.message = message
        self.suggestion = suggestion
        self.reviewer = reviewer
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'severity': self.severity,
            'category': self.category,
            'message': self.message,
            'suggestion': self.suggestion,
            'reviewer': self.reviewer,
            'timestamp': self.timestamp.isoformat()
        }


class AICodeReviewer:
    """AI代码审查器"""

    def __init__(self):
        self.review_rules = self._load_review_rules()

    def _load_review_rules(self) -> Dict[str, Dict[str, Any]]:
        """加载代码审查规则"""
        return {
            # Python代码质量规则
            'python-long-function': {
                'name': '函数过长',
                'severity': 'warning',
                'category': 'maintainability',
                'description': '函数过长，建议拆分',
                'max_lines': 50
            },
            'python-complex-conditional': {
                'name': '复杂条件语句',
                'severity': 'warning',
                'category': 'readability',
                'description': '条件语句过于复杂，建议简化'
            },
            'python-missing-docstring': {
                'name': '缺少文档字符串',
                'severity': 'info',
                'category': 'documentation',
                'description': '函数缺少文档字符串'
            },
            'python-unused-import': {
                'name': '未使用的导入',
                'severity': 'warning',
                'category': 'maintainability',
                'description': '导入的模块未被使用'
            },
            'python-broad-exception': {
                'name': '过于宽泛的异常捕获',
                'severity': 'warning',
                'category': 'error-handling',
                'description': '捕获Exception过于宽泛，建议捕获具体异常'
            },
            'python-hardcoded-values': {
                'name': '硬编码值',
                'severity': 'info',
                'category': 'maintainability',
                'description': '建议将硬编码值提取为常量或配置'
            },
            'python-naming-convention': {
                'name': '命名规范',
                'severity': 'info',
                'category': 'style',
                'description': '变量/函数命名不符合Python规范'
            },

            # 一般代码质量规则
            'general-todo-comments': {
                'name': 'TODO注释',
                'severity': 'info',
                'category': 'documentation',
                'description': '发现TODO注释，需要处理'
            },
            'general-fixme-comments': {
                'name': 'FIXME注释',
                'severity': 'warning',
                'category': 'maintainability',
                'description': '发现FIXME注释，需要修复'
            },
            'general-long-lines': {
                'name': '过长代码行',
                'severity': 'info',
                'category': 'style',
                'description': '代码行过长，建议换行',
                'max_length': 100
            }
        }

    def review_file(self, file_path: str) -> List[CodeReviewComment]:
        """审查单个文件"""
        comments = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            file_ext = Path(file_path).suffix.lower()

            # 应用通用规则
            comments.extend(self._apply_general_rules(file_path, lines))

            # 应用语言特定规则
            if file_ext == '.py':
                comments.extend(self._apply_python_rules(file_path, content, lines))
            elif file_ext in ['.js', '.ts']:
                comments.extend(self._apply_javascript_rules(file_path, content, lines))

        except Exception as e:
            comments.append(CodeReviewComment(
                file_path=file_path,
                line_number=1,
                severity='error',
                category='file-error',
                message=f'无法审查文件: {str(e)}',
                reviewer='AI'
            ))

        return comments

    def _apply_general_rules(self, file_path: str, lines: List[str]) -> List[CodeReviewComment]:
        """应用通用审查规则"""
        comments = []

        for i, line in enumerate(lines, 1):
            # 检查TODO注释
            if 'todo' in line.lower():
                comments.append(CodeReviewComment(
                    file_path=file_path,
                    line_number=i,
                    severity='info',
                    category='documentation',
                    message='发现TODO注释，建议及时处理',
                    suggestion='考虑将TODO项添加到任务跟踪系统中'
                ))

            # 检查FIXME注释
            if 'fixme' in line.lower():
                comments.append(CodeReviewComment(
                    file_path=file_path,
                    line_number=i,
                    severity='warning',
                    category='maintainability',
                    message='发现FIXME注释，需要修复',
                    suggestion='优先处理FIXME标记的问题'
                ))

            # 检查过长行
            if len(line) > 100:
                comments.append(CodeReviewComment(
                    file_path=file_path,
                    line_number=i,
                    severity='info',
                    category='style',
                    message=f'代码行过长 ({len(line)} 字符)',
                    suggestion='建议将长行拆分为多行以提高可读性'
                ))

        return comments

    def _apply_python_rules(self, file_path: str, content: str, lines: List[str]) -> List[CodeReviewComment]:
        """应用Python特定审查规则"""
        comments = []

        try:
            # 解析AST
            tree = ast.parse(content)

            # 检查函数长度
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = len(content.split('\n')[node.lineno-1:node.end_lineno])
                    if func_lines > 50:
                        comments.append(CodeReviewComment(
                            file_path=file_path,
                            line_number=node.lineno,
                            severity='warning',
                            category='maintainability',
                            message=f'函数 {node.name} 过长 ({func_lines} 行)',
                            suggestion='考虑将函数拆分为更小的函数'
                        ))

                    # 检查文档字符串
                    if not ast.get_docstring(node):
                        comments.append(CodeReviewComment(
                            file_path=file_path,
                            line_number=node.lineno,
                            severity='info',
                            category='documentation',
                            message=f'函数 {node.name} 缺少文档字符串',
                            suggestion='为函数添加docstring以说明其用途和参数'
                        ))

            # 检查异常处理
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None or (hasattr(node.type, 'id') and node.type.id == 'Exception'):
                        comments.append(CodeReviewComment(
                            file_path=file_path,
                            line_number=node.lineno,
                            severity='warning',
                            category='error-handling',
                            message='捕获Exception过于宽泛',
                            suggestion='捕获更具体的异常类型'
                        ))

            # 检查硬编码值
            for i, line in enumerate(lines, 1):
                # 查找可能的硬编码配置
                if re.search(r'(port|host|url|key|secret)\s*=\s*["\'][^"\']+["\']', line, re.IGNORECASE):
                    comments.append(CodeReviewComment(
                        file_path=file_path,
                        line_number=i,
                        severity='info',
                        category='maintainability',
                        message='发现可能的硬编码配置值',
                        suggestion='考虑使用环境变量或配置文件'
                    ))

        except SyntaxError:
            comments.append(CodeReviewComment(
                file_path=file_path,
                line_number=1,
                severity='error',
                category='syntax',
                message='Python语法错误',
                suggestion='修复语法错误后再进行代码审查'
            ))

        return comments

    def _apply_javascript_rules(self, file_path: str, content: str, lines: List[str]) -> List[CodeReviewComment]:
        """应用JavaScript特定审查规则"""
        comments = []

        # 检查console.log语句（可能遗留在生产代码中）
        for i, line in enumerate(lines, 1):
            if 'console.log' in line and not line.strip().startswith('//'):
                comments.append(CodeReviewComment(
                    file_path=file_path,
                    line_number=i,
                    severity='warning',
                    category='logging',
                    message='生产代码中发现console.log',
                    suggestion='移除调试用的console.log语句'
                ))

        # 检查未使用的变量（简化检查）
        var_declarations = re.findall(r'(?:var|let|const)\s+(\w+)', content)
        var_usages = re.findall(r'\b\w+\b', content)

        # 这是一个简化的检查，实际实现需要更复杂的AST分析
        for var_name in var_declarations[:5]:  # 只检查前5个变量
            if var_usages.count(var_name) <= 1:  # 只声明未使用
                for i, line in enumerate(lines, 1):
                    if var_name in line and ('var ' in line or 'let ' in line or 'const ' in line):
                        comments.append(CodeReviewComment(
                            file_path=file_path,
                            line_number=i,
                            severity='warning',
                            category='maintainability',
                            message=f'变量 {var_name} 可能未使用',
                            suggestion='移除未使用的变量或添加适当的使用'
                        ))
                        break

        return comments

    def review_pull_request(self, pr_files: List[str]) -> Dict[str, Any]:
        """审查PR中的所有文件"""
        pr_review = {
            'summary': {
                'total_files': len(pr_files),
                'total_comments': 0,
                'severity_breakdown': {'error': 0, 'warning': 0, 'info': 0}
            },
            'files': {},
            'recommendations': []
        }

        all_comments = []

        for file_path in pr_files:
            if os.path.exists(file_path):
                comments = self.review_file(file_path)
                all_comments.extend(comments)

                pr_review['files'][file_path] = [comment.to_dict() for comment in comments]

        # 生成汇总
        pr_review['summary']['total_comments'] = len(all_comments)
        for comment in all_comments:
            pr_review['summary']['severity_breakdown'][comment.severity] += 1

        # 生成建议
        pr_review['recommendations'] = self._generate_recommendations(all_comments)

        return pr_review

    def _generate_recommendations(self, comments: List[CodeReviewComment]) -> List[str]:
        """基于审查结果生成建议"""
        recommendations = []

        severity_counts = {'error': 0, 'warning': 0, 'info': 0}
        category_counts = {}

        for comment in comments:
            severity_counts[comment.severity] += 1
            category_counts[comment.category] = category_counts.get(comment.category, 0) + 1

        # 基于严重程度提供建议
        if severity_counts['error'] > 0:
            recommendations.append("🔴 优先修复所有错误级别的审查意见")
        if severity_counts['warning'] > 5:
            recommendations.append("🟡 考虑分批处理警告级别的问题")

        # 基于类别提供建议
        if category_counts.get('maintainability', 0) > 3:
            recommendations.append("🔧 考虑重构以提高代码可维护性")
        if category_counts.get('documentation', 0) > 2:
            recommendations.append("📚 增加代码文档和注释")
        if category_counts.get('error-handling', 0) > 1:
            recommendations.append("⚠️ 改进错误处理逻辑")

        if not recommendations:
            recommendations.append("✅ 代码质量良好，建议通过")

        return recommendations

    def generate_review_report(self, review_results: Dict[str, Any], output_file: str = None) -> str:
        """生成审查报告"""
        report = "# AI代码审查报告\n\n"

        summary = review_results['summary']
        report += "## 审查摘要\n\n"
        report += f"- **审查文件数**: {summary['total_files']}\n"
        report += f"- **总审查意见**: {summary['total_comments']}\n"
        report += f"- **错误**: {summary['severity_breakdown']['error']}\n"
        report += f"- **警告**: {summary['severity_breakdown']['warning']}\n"
        report += f"- **信息**: {summary['severity_breakdown']['info']}\n\n"

        if review_results['recommendations']:
            report += "## 建议\n\n"
            for rec in review_results['recommendations']:
                report += f"- {rec}\n"
            report += "\n"

        if review_results['files']:
            report += "## 详细审查意见\n\n"
            for file_path, comments in review_results['files'].items():
                if comments:
                    report += f"### {file_path}\n\n"
                    for comment in comments:
                        severity_icon = {'error': '🔴', 'warning': '🟡', 'info': '🔵'}[comment['severity']]
                        report += f"**{severity_icon} {comment['category']}** (第{comment['line_number']}行)\n\n"
                        report += f"{comment['message']}\n\n"
                        if comment['suggestion']:
                            report += f"**建议**: {comment['suggestion']}\n\n"

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

        return report


class ManualCodeReviewer:
    """手动代码审查指导"""

    def __init__(self):
        self.checklist = self._load_checklist()

    def _load_checklist(self) -> Dict[str, List[str]]:
        """加载手动审查清单"""
        return {
            'correctness': [
                '代码逻辑是否正确？',
                '边界条件是否处理？',
                '错误情况是否适当处理？',
                '并发访问是否安全？'
            ],
            'performance': [
                '是否存在性能瓶颈？',
                '算法复杂度是否合适？',
                '数据库查询是否优化？',
                '内存使用是否合理？'
            ],
            'security': [
                '是否存在安全漏洞？',
                '输入验证是否充分？',
                '敏感数据是否保护？',
                '权限控制是否正确？'
            ],
            'maintainability': [
                '代码是否易于理解？',
                '函数是否职责单一？',
                '命名是否清晰？',
                '注释是否充分？'
            ],
            'testing': [
                '单元测试是否覆盖主要逻辑？',
                '集成测试是否完整？',
                '边缘情况是否测试？',
                '测试是否自动化？'
            ],
            'documentation': [
                'API文档是否完整？',
                '代码注释是否充分？',
                'README是否更新？',
                '变更日志是否记录？'
            ]
        }

    def get_checklist(self, category: str = None) -> Dict[str, List[str]]:
        """获取审查清单"""
        if category:
            return {category: self.checklist.get(category, [])}
        return self.checklist

    def generate_pr_template(self) -> str:
        """生成PR模板"""
        template = """# Pull Request 描述

## 更改概述
简要描述这次更改的目的和范围。

## 技术细节
详细说明实现的技术方案和关键决策。

## 测试结果
运行测试的命令和结果：
```
# 测试命令
test_results_here
```

## 审查清单
- [ ] 代码逻辑正确性
- [ ] 性能优化
- [ ] 安全检查
- [ ] 可维护性
- [ ] 测试覆盖
- [ ] 文档更新

## 风险评估
描述可能的风险和缓解措施。

## 后续工作
如果有未完成的工作，请在此列出。
"""
        return template


# 创建全局审查器实例
ai_reviewer = AICodeReviewer()
manual_reviewer = ManualCodeReviewer()


def review_codebase(directory: str = ".", output_file: str = "code_review_report.md") -> Dict[str, Any]:
    """审查整个代码库"""
    print(f"🔍 开始审查目录: {directory}")

    pr_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.java')):
                pr_files.append(os.path.join(root, file))

    print(f"📋 发现 {len(pr_files)} 个代码文件")

    # 执行AI审查
    review_results = ai_reviewer.review_pull_request(pr_files)

    # 生成报告
    report = ai_reviewer.generate_review_report(review_results, output_file)

    print(f"📄 审查报告已保存到: {output_file}")
    print(f"📊 发现 {review_results['summary']['total_comments']} 个审查意见")

    return review_results


def demonstrate_review_comparison():
    """演示AI审查与手动审查的比较"""
    print("🔍 代码审查对比演示")
    print("=" * 50)

    # 示例代码片段
    sample_code = '''
def process_user_data(user_input):
    # 这是一个有问题的函数
    result = eval(user_input)  # 安全问题：任意代码执行
    print(result)  # 调试代码遗留

    # 硬编码值
    database_url = "postgresql://localhost:5432/mydb"

    # 复杂的条件语句
    if user_input and len(user_input) > 0 and user_input.isdigit() and int(user_input) > 100:
        return "valid"
    else:
        return "invalid"

# TODO: 添加错误处理
# FIXME: 这个函数需要重构
'''

    # 保存到临时文件
    temp_file = "sample_review.py"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(sample_code)

    print("📝 示例代码已创建")

    # AI审查
    print("\n🤖 AI审查结果:")
    ai_comments = ai_reviewer.review_file(temp_file)

    for i, comment in enumerate(ai_comments, 1):
        print(f"{i}. {comment.category.upper()}: {comment.message}")
        if comment.suggestion:
            print(f"   建议: {comment.suggestion}")

    # 手动审查指导
    print("
👥 手动审查清单:"    checklist = manual_reviewer.get_checklist()
    for category, questions in checklist.items():
        print(f"\n{category.upper()}:")
        for question in questions:
            print(f"  • {question}")

    # 清理临时文件
    os.remove(temp_file)

    print("
📊 对比分析:"    print("🤖 AI审查优点:")
    print("  - 快速自动化检查")
    print("  - 覆盖常见模式和最佳实践")
    print("  - 一致的审查标准")

    print("\n👥 手动审查优点:")
    print("  - 理解业务逻辑和上下文")
    print("  - 发现逻辑错误和设计问题")
    print("  - 提供建设性建议和改进方向")

    print("\n💡 最佳实践:")
    print("  - 将AI审查作为第一道防线")
    print("  - 手动审查重点关注复杂逻辑")
    print("  - 结合两者获得最佳审查效果")


if __name__ == "__main__":
    demonstrate_review_comparison()
