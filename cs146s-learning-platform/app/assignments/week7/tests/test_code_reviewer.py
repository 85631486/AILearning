#!/usr/bin/env python3
"""
Week 7: 代码审查器测试
"""

import pytest
import sys
import os
import tempfile

# 添加code_review目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code_review'))

from code_reviewer import (
    AICodeReviewer,
    CodeReviewComment,
    review_codebase
)


class TestCodeReviewComment:
    """测试代码审查评论类"""

    def test_comment_creation(self):
        """测试评论创建"""
        comment = CodeReviewComment(
            file_path="test.py",
            line_number=10,
            severity="warning",
            category="maintainability",
            message="函数过长",
            suggestion="拆分函数",
            reviewer="AI"
        )

        assert comment.file_path == "test.py"
        assert comment.line_number == 10
        assert comment.severity == "warning"
        assert comment.reviewer == "AI"

    def test_comment_to_dict(self):
        """测试评论序列化"""
        comment = CodeReviewComment(
            file_path="test.py",
            line_number=5,
            severity="error",
            category="security",
            message="SQL注入风险",
            suggestion="使用参数化查询",
            cwe_id="CWE-89"
        )

        data = comment.to_dict()
        assert data['file_path'] == "test.py"
        assert data['cwe_id'] == "CWE-89"


class TestAICodeReviewer:
    """测试AI代码审查器"""

    def setup_method(self):
        """测试前设置"""
        self.reviewer = AICodeReviewer()

    def test_reviewer_initialization(self):
        """测试审查器初始化"""
        assert self.reviewer.rules is not None
        assert len(self.reviewer.rules) > 0
        assert 'python-sql-injection' in self.reviewer.rules

    def test_review_python_file_sql_injection(self):
        """测试Python文件SQL注入检测"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def vulnerable_query(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
''')
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            sql_comments = [c for c in comments if 'SQL' in c.message]

            assert len(sql_comments) > 0
            comment = sql_comments[0]
            assert comment.severity == 'high'
            assert comment.category == 'injection'

        finally:
            os.unlink(temp_file)

    def test_review_python_file_long_function(self):
        """测试Python文件长函数检测"""
        # 创建一个故意很长的函数
        long_function = '''
def very_long_function():
    """这个函数故意写得很长"""
''' + '\n'.join([f'    step{i} = {i}' for i in range(60)]) + '''
    return step59
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(long_function)
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            long_func_comments = [c for c in comments if '过长' in c.message]

            assert len(long_func_comments) > 0
            comment = long_func_comments[0]
            assert comment.severity == 'warning'
            assert '函数过长' in comment.message

        finally:
            os.unlink(temp_file)

    def test_review_python_file_missing_docstring(self):
        """测试Python文件文档字符串检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def function_without_docstring(param1, param2):
    return param1 + param2

def function_with_docstring(param1):
    """这个函数有文档字符串"""
    return param1 * 2
''')
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            docstring_comments = [c for c in comments if '文档字符串' in c.message]

            # 应该只检测到缺少文档字符串的函数
            assert len(docstring_comments) == 1
            comment = docstring_comments[0]
            assert 'function_without_docstring' in comment.message

        finally:
            os.unlink(temp_file)

    def test_review_javascript_file_console_log(self):
        """测试JavaScript文件console.log检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('''
function testFunction() {
    console.log("debug message"); // 遗留的调试代码
    const result = compute();
    return result;
}

function anotherFunction() {
    const data = "test";
    // console.log(data); // 已注释的调试代码
    return data.toUpperCase();
}
''')
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            console_comments = [c for c in comments if 'console.log' in c.message]

            assert len(console_comments) > 0
            comment = console_comments[0]
            assert comment.severity == 'warning'
            assert 'console.log' in comment.message

        finally:
            os.unlink(temp_file)

    def test_review_todo_comments(self):
        """测试TODO注释检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def my_function():
    # TODO: 实现这个功能
    # FIXME: 修复这个bug
    pass
''')
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            todo_comments = [c for c in comments if 'TODO' in c.message or 'FIXME' in c.message]

            assert len(todo_comments) >= 2  # 应该检测到TODO和FIXME

        finally:
            os.unlink(temp_file)

    def test_review_long_lines(self):
        """测试长代码行检测"""
        long_line = 'x' * 120  # 120个字符的长行

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(f'variable = "{long_line}"\n')
            temp_file = f.name

        try:
            comments = self.reviewer.review_file(temp_file)
            long_line_comments = [c for c in comments if '过长' in c.message]

            assert len(long_line_comments) > 0
            comment = long_line_comments[0]
            assert comment.severity == 'info'
            assert '代码行过长' in comment.message

        finally:
            os.unlink(temp_file)

    def test_generate_report(self):
        """测试报告生成"""
        comments = [
            CodeReviewComment("file1.py", 1, "high", "security", "SQL注入", "使用参数化查询"),
            CodeReviewComment("file2.py", 5, "warning", "style", "长代码行", "拆分行"),
            CodeReviewComment("file3.py", 10, "info", "documentation", "缺少文档", "添加文档")
        ]

        results = {
            'summary': {
                'total_files': 3,
                'total_comments': 3,
                'severity_breakdown': {'high': 1, 'warning': 1, 'info': 1}
            },
            'files': {},
            'recommendations': ['修复安全问题', '改进代码风格']
        }

        report = self.reviewer.generate_report(results)

        assert "# 安全扫描报告" in report
        assert "总发现数**: 3" in report
        assert "**高危**: 1" in report
        assert "**警告**: 1" in report
        assert "**信息**: 1" in report

    def test_review_pull_request(self):
        """测试PR审查"""
        # 创建测试文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('eval("print(1)")')  # 危险代码
            temp_file = f.name

        try:
            results = self.reviewer.review_pull_request([temp_file])

            assert 'summary' in results
            assert 'files' in results
            assert 'recommendations' in results
            assert results['summary']['total_files'] == 1
            assert results['summary']['total_comments'] >= 1

        finally:
            os.unlink(temp_file)


def test_review_codebase_function():
    """测试review_codebase函数"""
    # 创建临时目录和文件
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('os.system("ls")')  # 命令注入

        # 运行审查（不生成报告文件）
        results = review_codebase(temp_dir, None)

        assert 'summary' in results
        assert 'files' in results
        assert results['summary']['total_comments'] >= 1


def test_multiple_file_types():
    """测试多种文件类型审查"""
    reviewer = AICodeReviewer()

    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # Python文件
        py_file = os.path.join(temp_dir, 'test.py')
        with open(py_file, 'w') as f:
            f.write('eval("code")')

        # JavaScript文件
        js_file = os.path.join(temp_dir, 'test.js')
        with open(js_file, 'w') as f:
            f.write('eval("js_code")')

        results = reviewer.review_pull_request([py_file, js_file])

        assert results['summary']['total_files'] == 2
        assert results['summary']['total_comments'] >= 2  # 每个文件至少一个eval问题


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
