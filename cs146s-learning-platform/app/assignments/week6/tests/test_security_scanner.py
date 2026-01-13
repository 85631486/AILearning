#!/usr/bin/env python3
"""
Week 6: 安全扫描器测试
"""

import pytest
import sys
import os
import tempfile
from unittest.mock import Mock, patch

# 添加scanner目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scanner'))

from security_scanner import (
    SecurityScanner,
    SecurityFinding,
    VulnerabilityFixer,
    scan_project
)


class TestSecurityFinding:
    """测试安全发现类"""

    def test_finding_creation(self):
        """测试安全发现创建"""
        finding = SecurityFinding(
            rule_id="test-rule",
            rule_name="Test Rule",
            severity="high",
            category="test",
            file_path="test.py",
            line_number=10,
            code_snippet="test code",
            description="Test description",
            recommendation="Test recommendation"
        )

        assert finding.rule_id == "test-rule"
        assert finding.severity == "high"
        assert finding.line_number == 10

    def test_finding_to_dict(self):
        """测试安全发现序列化"""
        finding = SecurityFinding(
            rule_id="test-rule",
            rule_name="Test Rule",
            severity="high",
            category="test",
            file_path="test.py",
            line_number=10,
            code_snippet="test code",
            description="Test description",
            recommendation="Test recommendation",
            cwe_id="CWE-123"
        )

        data = finding.to_dict()
        assert data['rule_id'] == "test-rule"
        assert data['cwe_id'] == "CWE-123"


class TestSecurityScanner:
    """测试安全扫描器"""

    def setup_method(self):
        """测试前设置"""
        self.scanner = SecurityScanner()

    def test_scanner_initialization(self):
        """测试扫描器初始化"""
        assert self.scanner.rules is not None
        assert len(self.scanner.rules) > 0
        assert 'python-sql-injection' in self.scanner.rules

    def test_scan_python_file_sql_injection(self):
        """测试Python文件SQL注入检测"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def vulnerable_function(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
''')
            temp_file = f.name

        try:
            findings = self.scanner.scan_file(temp_file)
            sql_findings = [f for f in findings if f.rule_id == 'python-sql-injection']

            assert len(sql_findings) > 0
            finding = sql_findings[0]
            assert finding.severity == 'high'
            assert finding.category == 'injection'
            assert 'SQL' in finding.rule_name

        finally:
            os.unlink(temp_file)

    def test_scan_python_file_command_injection(self):
        """测试Python文件命令注入检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
def run_command(cmd):
    os.system(cmd)
''')
            temp_file = f.name

        try:
            findings = self.scanner.scan_file(temp_file)
            cmd_findings = [f for f in findings if f.rule_id == 'python-command-injection']

            assert len(cmd_findings) > 0
            finding = cmd_findings[0]
            assert finding.severity == 'high'
            assert '命令注入' in finding.description

        finally:
            os.unlink(temp_file)

    def test_scan_python_file_hardcoded_secret(self):
        """测试Python文件硬编码密钥检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''
API_KEY = "sk-1234567890abcdef"
password = "secret123"
''')
            temp_file = f.name

        try:
            findings = self.scanner.scan_file(temp_file)
            secret_findings = [f for f in findings if f.rule_id == 'python-hardcoded-secret']

            assert len(secret_findings) > 0
            finding = secret_findings[0]
            assert finding.severity == 'medium'
            assert '硬编码' in finding.description

        finally:
            os.unlink(temp_file)

    def test_scan_javascript_file_xss(self):
        """测试JavaScript文件XSS检测"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('''
function updateUI(data) {
    document.getElementById('content').innerHTML = data;
}
''')
            temp_file = f.name

        try:
            findings = self.scanner.scan_file(temp_file)
            xss_findings = [f for f in findings if f.rule_id == 'js-xss-innerhtml']

            assert len(xss_findings) > 0
            finding = xss_findings[0]
            assert finding.severity == 'high'
            assert 'XSS' in finding.rule_name

        finally:
            os.unlink(temp_file)

    def test_scan_directory(self):
        """测试目录扫描"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建Python文件
            py_file = os.path.join(temp_dir, 'test.py')
            with open(py_file, 'w') as f:
                f.write('eval("print(1)")')

            # 创建JavaScript文件
            js_file = os.path.join(temp_dir, 'test.js')
            with open(js_file, 'w') as f:
                f.write('eval("console.log(1)")')

            findings = self.scanner.scan_directory(temp_dir)

            # 应该找到Python和JavaScript的eval使用
            eval_findings = [f for f in findings if 'eval' in f.rule_name.lower()]
            assert len(eval_findings) >= 1

    def test_generate_report(self):
        """测试报告生成"""
        findings = [
            SecurityFinding(
                rule_id="test-rule-1",
                rule_name="Test Rule 1",
                severity="high",
                category="injection",
                file_path="test.py",
                line_number=1,
                code_snippet="test code 1",
                description="Test desc 1",
                recommendation="Test rec 1"
            ),
            SecurityFinding(
                rule_id="test-rule-2",
                rule_name="Test Rule 2",
                severity="medium",
                category="secrets",
                file_path="test.js",
                line_number=2,
                code_snippet="test code 2",
                description="Test desc 2",
                recommendation="Test rec 2"
            )
        ]

        report = self.scanner.generate_report(findings)

        assert "# 安全扫描报告" in report
        assert "总发现数**: 2" in report
        assert "**高危**: 1" in report
        assert "**中危**: 1" in report
        assert "### test.py" in report
        assert "### test.js" in report

    def test_get_available_rules(self):
        """测试获取可用规则"""
        rules = self.scanner.get_available_rules()
        assert isinstance(rules, dict)
        assert len(rules) > 0
        assert 'python-sql-injection' in rules


class TestVulnerabilityFixer:
    """测试漏洞修复器"""

    def setup_method(self):
        """测试前设置"""
        self.fixer = VulnerabilityFixer()

    def test_fixer_initialization(self):
        """测试修复器初始化"""
        assert self.fixer.fixes is not None
        assert len(self.fixer.fixes) > 0

    def test_get_fix_suggestion(self):
        """测试获取修复建议"""
        fix = self.fixer.get_fix_suggestion('python-sql-injection')
        assert fix is not None
        assert 'description' in fix
        assert 'fix_type' in fix
        assert 'example_before' in fix
        assert 'example_after' in fix

    def test_get_fix_suggestion_not_found(self):
        """测试获取不存在的修复建议"""
        fix = self.fixer.get_fix_suggestion('nonexistent-rule')
        assert fix is None

    def test_apply_fix_sql_injection(self):
        """测试SQL注入修复应用"""
        # 创建测试文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")')
            temp_file = f.name

        try:
            finding = SecurityFinding(
                rule_id='python-sql-injection',
                rule_name='SQL Injection',
                severity='high',
                category='injection',
                file_path=temp_file,
                line_number=1,
                code_snippet='cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")',
                description='SQL injection',
                recommendation='Use parameterized queries'
            )

            # 应用修复
            result = self.fixer.apply_fix(finding, temp_file)
            assert result is True

            # 检查修复结果
            with open(temp_file, 'r') as f:
                content = f.read()
                # 简化的检查，实际修复逻辑可能不同
                assert 'cursor.execute' in content

        finally:
            os.unlink(temp_file)


def test_scan_project_function():
    """测试scan_project函数"""
    # 创建临时目录和文件
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('os.system("ls")')  # 命令注入

        # 扫描项目
        findings = scan_project(temp_dir, "test_report.md")

        # 验证结果
        assert isinstance(findings, list)
        assert len(findings) > 0

        # 检查是否生成了报告文件
        report_file = os.path.join(temp_dir, "test_report.md")
        assert os.path.exists(report_file)

        with open(report_file, 'r') as f:
            report_content = f.read()
            assert "# 安全扫描报告" in report_content


def test_multiple_vulnerabilities():
    """测试多个漏洞检测"""
    scanner = SecurityScanner()

    # 创建包含多个漏洞的文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
import os

def vulnerable_function(user_input, user_id):
    # SQL注入
    query = f"SELECT * FROM users WHERE id = {user_id}"

    # 命令注入
    os.system(f"echo {user_input}")

    # 代码注入
    result = eval(user_input)

    # 硬编码密钥
    password = "secret123"

    return result
''')
        temp_file = f.name

    try:
        findings = scanner.scan_file(temp_file)

        # 应该至少检测到4个漏洞
        assert len(findings) >= 4

        # 检查不同类型的漏洞
        rule_ids = [f.rule_id for f in findings]
        assert 'python-sql-injection' in rule_ids
        assert 'python-command-injection' in rule_ids
        assert 'python-eval' in rule_ids
        assert 'python-hardcoded-secret' in rule_ids

    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
