#!/usr/bin/env python3
"""
Week 6: 安全扫描器 - Semgrep风格的安全漏洞检测
模拟Semgrep的安全扫描功能，用于教学演示
"""

import os
import re
import ast
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SecurityFinding:
    """安全发现"""
    rule_id: str
    rule_name: str
    severity: str
    category: str
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    recommendation: str
    cwe_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'severity': self.severity,
            'category': self.category,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'code_snippet': self.code_snippet.strip(),
            'description': self.description,
            'recommendation': self.recommendation,
            'cwe_id': self.cwe_id
        }


class SecurityScanner:
    """安全扫描器 - 模拟Semgrep功能"""

    def __init__(self):
        self.rules = self._load_security_rules()

    def _load_security_rules(self) -> Dict[str, Dict[str, Any]]:
        """加载安全规则"""
        return {
            # Python安全规则
            'python-sql-injection': {
                'name': 'SQL Injection',
                'severity': 'high',
                'category': 'injection',
                'pattern': r'(execute|executemany)\s*\(\s*["\'](.*?)["\']',
                'cwe': 'CWE-89',
                'description': 'Potential SQL injection vulnerability',
                'recommendation': 'Use parameterized queries or prepared statements'
            },
            'python-command-injection': {
                'name': 'Command Injection',
                'severity': 'high',
                'category': 'injection',
                'pattern': r'(os\.system|subprocess\.call|subprocess\.run)\s*\(\s*(.*?)\)',
                'cwe': 'CWE-78',
                'description': 'Potential command injection vulnerability',
                'recommendation': 'Avoid shell=True, use shlex.quote for arguments, or use subprocess with list arguments'
            },
            'python-xss': {
                'name': 'Cross-Site Scripting (XSS)',
                'severity': 'medium',
                'category': 'xss',
                'pattern': r'innerHTML\s*=\s*(.*?)(?=\n|;)',
                'cwe': 'CWE-79',
                'description': 'Potential XSS vulnerability through innerHTML',
                'recommendation': 'Use textContent or createElement, or sanitize HTML content'
            },
            'python-hardcoded-secret': {
                'name': 'Hardcoded Secret',
                'severity': 'medium',
                'category': 'secrets',
                'pattern': r'(password|secret|key|token)\s*=\s*["\']([^"\']+)["\']',
                'cwe': 'CWE-798',
                'description': 'Hardcoded secret or credential',
                'recommendation': 'Use environment variables or secure credential storage'
            },
            'python-eval': {
                'name': 'Code Injection via eval()',
                'severity': 'high',
                'category': 'injection',
                'pattern': r'eval\s*\(',
                'cwe': 'CWE-95',
                'description': 'Use of eval() can lead to code injection',
                'recommendation': 'Avoid eval(), use ast.literal_eval() for safe evaluation, or find alternative approaches'
            },
            'python-weak-crypto': {
                'name': 'Weak Cryptographic Algorithm',
                'severity': 'medium',
                'category': 'crypto',
                'pattern': r'(md5|sha1)\s*\(',
                'cwe': 'CWE-327',
                'description': 'Use of weak cryptographic hash function',
                'recommendation': 'Use SHA-256 or stronger hashing algorithms'
            },

            # JavaScript安全规则
            'js-xss-innerhtml': {
                'name': 'DOM XSS via innerHTML',
                'severity': 'high',
                'category': 'xss',
                'pattern': r'\.innerHTML\s*=\s*(.*?)(?=\n|;)',
                'cwe': 'CWE-79',
                'description': 'Potential DOM-based XSS through innerHTML assignment',
                'recommendation': 'Use textContent, innerText, or sanitize HTML input'
            },
            'js-eval': {
                'name': 'Code Injection via eval',
                'severity': 'high',
                'category': 'injection',
                'pattern': r'eval\s*\(',
                'cwe': 'CWE-95',
                'description': 'Use of eval() can lead to code injection',
                'recommendation': 'Avoid eval(), use JSON.parse() or find alternative approaches'
            },
            'js-hardcoded-api-key': {
                'name': 'Hardcoded API Key',
                'severity': 'medium',
                'category': 'secrets',
                'pattern': r'(api[_-]?key|apikey)\s*[:=]\s*["\']([^"\']+)["\']',
                'cwe': 'CWE-798',
                'description': 'Hardcoded API key in client-side code',
                'recommendation': 'Use server-side API key storage, never expose keys in client code'
            }
        }

    def scan_file(self, file_path: str) -> List[SecurityFinding]:
        """扫描单个文件"""
        findings = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # 根据文件类型选择规则
            file_ext = Path(file_path).suffix.lower()
            if file_ext == '.py':
                relevant_rules = {k: v for k, v in self.rules.items() if k.startswith('python-')}
            elif file_ext == '.js':
                relevant_rules = {k: v for k, v in self.rules.items() if k.startswith('js-')}
            else:
                relevant_rules = {}

            # 应用每条规则
            for rule_id, rule_config in relevant_rules.items():
                pattern = rule_config['pattern']

                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        finding = SecurityFinding(
                            rule_id=rule_id,
                            rule_name=rule_config['name'],
                            severity=rule_config['severity'],
                            category=rule_config['category'],
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            description=rule_config['description'],
                            recommendation=rule_config['recommendation'],
                            cwe_id=rule_config.get('cwe')
                        )
                        findings.append(finding)

        except Exception as e:
            print(f"扫描文件 {file_path} 时出错: {e}")

        return findings

    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[SecurityFinding]:
        """扫描目录"""
        if extensions is None:
            extensions = ['.py', '.js', '.html']

        findings = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file_path).suffix.lower()

                if file_ext in extensions:
                    file_findings = self.scan_file(file_path)
                    findings.extend(file_findings)

        return findings

    def generate_report(self, findings: List[SecurityFinding], output_file: str = None) -> str:
        """生成扫描报告"""
        # 按严重程度分组
        severity_counts = {'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        category_counts = {}

        for finding in findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
            category_counts[finding.category] = category_counts.get(finding.category, 0) + 1

        # 生成报告
        report = "# 安全扫描报告\n\n"
        report += f"## 扫描摘要\n\n"
        report += f"- **总发现数**: {len(findings)}\n"
        report += f"- **高危**: {severity_counts['high']}\n"
        report += f"- **中危**: {severity_counts['medium']}\n"
        report += f"- **低危**: {severity_counts['low']}\n\n"

        report += "## 类别分布\n\n"
        for category, count in category_counts.items():
            report += f"- **{category}**: {count}\n"
        report += "\n"

        if findings:
            report += "## 详细发现\n\n"
            # 按文件分组
            findings_by_file = {}
            for finding in findings:
                if finding.file_path not in findings_by_file:
                    findings_by_file[finding.file_path] = []
                findings_by_file[finding.file_path].append(finding)

            for file_path, file_findings in findings_by_file.items():
                report += f"### {file_path}\n\n"
                for finding in file_findings:
                    report += f"#### {finding.rule_name} ({finding.severity})\n\n"
                    report += f"- **规则ID**: {finding.rule_id}\n"
                    report += f"- **行号**: {finding.line_number}\n"
                    report += f"- **类别**: {finding.category}\n"
                    if finding.cwe_id:
                        report += f"- **CWE**: {finding.cwe_id}\n"
                    report += f"- **描述**: {finding.description}\n"
                    report += f"- **代码片段**: `{finding.code_snippet}`\n"
                    report += f"- **建议修复**: {finding.recommendation}\n\n"

        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)

        return report

    def get_available_rules(self) -> Dict[str, Dict[str, Any]]:
        """获取可用规则"""
        return self.rules


class VulnerabilityFixer:
    """漏洞修复器"""

    def __init__(self):
        self.fixes = self._load_fixes()

    def _load_fixes(self) -> Dict[str, Dict[str, Any]]:
        """加载修复模板"""
        return {
            'python-sql-injection': {
                'description': '修复SQL注入漏洞',
                'fix_type': 'parameterize_query',
                'example_before': "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
                'example_after': "cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))"
            },
            'python-command-injection': {
                'description': '修复命令注入漏洞',
                'fix_type': 'use_subprocess_list',
                'example_before': "os.system(f\"ls {user_input}\")",
                'example_after': "subprocess.run(['ls', user_input], check=True)"
            },
            'python-xss': {
                'description': '修复XSS漏洞',
                'fix_type': 'use_text_content',
                'example_before': "element.innerHTML = user_input",
                'example_after': "element.textContent = user_input"
            },
            'python-hardcoded-secret': {
                'description': '修复硬编码密钥',
                'fix_type': 'use_env_var',
                'example_before': "password = 'secret123'",
                'example_after': "password = os.getenv('DB_PASSWORD')"
            },
            'python-eval': {
                'description': '修复eval代码注入',
                'fix_type': 'use_ast_literal_eval',
                'example_before': "result = eval(user_input)",
                'example_after': "result = ast.literal_eval(user_input)"
            }
        }

    def get_fix_suggestion(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """获取修复建议"""
        return self.fixes.get(rule_id)

    def apply_fix(self, finding: SecurityFinding, target_file: str) -> bool:
        """应用修复（简化版本，实际实现需要更复杂的AST操作）"""
        try:
            # 这里是简化的修复逻辑
            # 实际实现需要解析AST并进行精确的代码修改

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')

            # 简单的字符串替换（仅用于演示）
            if finding.rule_id == 'python-hardcoded-secret':
                # 将硬编码密码替换为环境变量
                old_line = lines[finding.line_number - 1]
                new_line = old_line.replace("'secret123'", "os.getenv('DB_PASSWORD')")
                lines[finding.line_number - 1] = new_line

            elif finding.rule_id == 'python-sql-injection':
                # 将字符串格式化替换为参数化查询
                old_line = lines[finding.line_number - 1]
                new_line = old_line.replace('f"', '"').replace('user_id', '%s", (user_id,)')
                lines[finding.line_number - 1] = new_line

            # 写回文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            return True

        except Exception as e:
            print(f"应用修复失败: {e}")
            return False


# 创建全局扫描器实例
scanner = SecurityScanner()
fixer = VulnerabilityFixer()


def scan_project(directory: str = ".", output_file: str = "security_report.md") -> List[SecurityFinding]:
    """扫描整个项目"""
    print(f"🔍 开始扫描目录: {directory}")
    findings = scanner.scan_directory(directory)
    report = scanner.generate_report(findings, output_file)

    print(f"📊 发现 {len(findings)} 个安全问题")
    print(f"📄 报告已保存到: {output_file}")

    return findings


def demonstrate_fixes():
    """演示修复功能"""
    print("🔧 演示安全修复功能")

    # 创建示例有漏洞的代码
    vulnerable_code = '''
# 有漏洞的代码示例
import os

def get_user_data(user_id):
    # SQL注入漏洞
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

def run_command(cmd):
    # 命令注入漏洞
    os.system(cmd)

# 硬编码密钥
password = "secret123"
'''

    # 保存到临时文件
    temp_file = "temp_vulnerable.py"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(vulnerable_code)

    # 扫描文件
    findings = scanner.scan_file(temp_file)

    print(f"发现 {len(findings)} 个安全问题:")

    for finding in findings:
        print(f"\n🚨 {finding.rule_name} (行 {finding.line_number})")
        print(f"   代码: {finding.code_snippet}")
        print(f"   建议: {finding.recommendation}")

        # 获取修复建议
        fix = fixer.get_fix_suggestion(finding.rule_id)
        if fix:
            print(f"   修复示例:")
            print(f"   前: {fix['example_before']}")
            print(f"   后: {fix['example_after']}")

    # 清理临时文件
    os.remove(temp_file)


if __name__ == "__main__":
    demonstrate_fixes()
