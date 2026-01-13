#!/usr/bin/env python3
"""
Week 6: 安全扫描演示
展示Semgrep风格的安全漏洞扫描和修复过程
"""

import sys
import os
from scanner.security_scanner import scanner, fixer, scan_project, SecurityFinding


def demo_security_scanning():
    """演示安全扫描功能"""
    print("🔍 Week 6: 安全扫描演示")
    print("=" * 40)

    # 创建示例有漏洞的代码
    vulnerable_code = '''
# 示例：有安全漏洞的Python代码
import os
import subprocess

def authenticate_user(username, password):
    """用户认证函数 - 存在SQL注入漏洞"""
    # SQL注入漏洞：直接字符串拼接
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return query

def run_system_command(user_command):
    """执行系统命令 - 存在命令注入漏洞"""
    # 命令注入漏洞：直接执行用户输入
    os.system(f"echo {user_command}")

def process_user_input(user_input):
    """处理用户输入 - 存在代码注入风险"""
    # 代码注入：使用eval
    result = eval(user_input)
    return result

def hash_password(password):
    """密码哈希 - 使用弱加密算法"""
    import hashlib
    # 弱加密：使用MD5
    return hashlib.md5(password.encode()).hexdigest()

# 硬编码密钥 - 严重安全问题
API_SECRET = "super_secret_key_12345"
DB_PASSWORD = "admin123"
'''

    # 保存到示例文件
    example_file = "vulnerable_example.py"
    with open(example_file, 'w', encoding='utf-8') as f:
        f.write(vulnerable_code)

    print("📁 已创建示例漏洞文件")

    # 扫描文件
    print("\n🔎 开始扫描...")
    findings = scanner.scan_file(example_file)

    print(f"发现 {len(findings)} 个安全问题：")

    # 显示发现的问题
    for i, finding in enumerate(findings, 1):
        print(f"\n{i}. 🚨 {finding.rule_name}")
        print(f"   严重程度: {finding.severity.upper()}")
        print(f"   类别: {finding.category}")
        print(f"   文件: {finding.file_path}:{finding.line_number}")
        if finding.cwe_id:
            print(f"   CWE: {finding.cwe_id}")
        print(f"   描述: {finding.description}")
        print(f"   代码片段: {finding.code_snippet}")
        print(f"   修复建议: {finding.recommendation}")

    # 生成报告
    print("\n📄 生成扫描报告...")
    report = scanner.generate_report(findings, "security_scan_report.md")
    print("报告已保存到: security_scan_report.md"

    # 清理示例文件
    os.remove(example_file)


def demo_vulnerability_fixes():
    """演示漏洞修复功能"""
    print("\n🔧 漏洞修复演示")
    print("=" * 40)

    # 显示可用的修复类型
    print("📋 可修复的漏洞类型:")
    fixes = fixer.fixes
    for rule_id, fix_info in fixes.items():
        print(f"  - {rule_id}: {fix_info['description']}")

    print("\n🔍 修复示例:")

    # 创建修复示例
    examples = [
        {
            'title': 'SQL注入修复',
            'before': "cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")",
            'after': "cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))"
        },
        {
            'title': '命令注入修复',
            'before': "os.system(f\"ls {directory}\")",
            'after': "subprocess.run(['ls', directory], check=True)"
        },
        {
            'title': '硬编码密钥修复',
            'before': "password = 'secret123'",
            'after': "password = os.getenv('DB_PASSWORD')"
        },
        {
            'title': 'XSS漏洞修复',
            'before': "element.innerHTML = user_input",
            'after': "element.textContent = user_input"
        }
    ]

    for example in examples:
        print(f"\n{example['title']}:")
        print(f"  ❌ 修复前: {example['before']}")
        print(f"  ✅ 修复后: {example['after']}")


def demo_javascript_scanning():
    """演示JavaScript代码扫描"""
    print("\n🌐 JavaScript安全扫描演示")
    print("=" * 40)

    # 创建示例有漏洞的JavaScript代码
    js_vulnerable_code = '''
// 示例：有安全漏洞的JavaScript代码

function updateUI(userInput) {
    // XSS漏洞：使用innerHTML
    document.getElementById('content').innerHTML = userInput;
}

function executeCode(codeString) {
    // 代码注入：使用eval
    return eval(codeString);
}

function makeAPICall(endpoint) {
    // 硬编码API密钥
    const apiKey = "sk-1234567890abcdef";
    fetch(endpoint, {
        headers: {
            'Authorization': `Bearer ${apiKey}`
        }
    });
}

function hashData(data) {
    // 弱加密：使用过时的算法
    return md5(data);
}
'''

    # 保存到示例文件
    js_example_file = "vulnerable_example.js"
    with open(js_example_file, 'w', encoding='utf-8') as f:
        f.write(js_vulnerable_code)

    print("📁 已创建JavaScript示例文件")

    # 扫描JavaScript文件
    print("\n🔎 扫描JavaScript代码...")
    findings = scanner.scan_file(js_example_file)

    print(f"发现 {len(findings)} 个安全问题：")

    for i, finding in enumerate(findings, 1):
        print(f"\n{i}. 🚨 {finding.rule_name}")
        print(f"   严重程度: {finding.severity.upper()}")
        print(f"   类别: {finding.category}")
        print(f"   文件: {finding.file_path}:{finding.line_number}")
        print(f"   描述: {finding.description}")
        print(f"   代码片段: {finding.code_snippet}")

    # 清理文件
    os.remove(js_example_file)


def demo_project_scan():
    """演示项目级扫描"""
    print("\n🏗️ 项目级安全扫描演示")
    print("=" * 40)

    # 创建示例项目结构
    os.makedirs("example_project/src", exist_ok=True)
    os.makedirs("example_project/tests", exist_ok=True)

    # 创建Python源文件
    python_code = '''
import os
def insecure_function(user_input):
    os.system(user_input)  # 命令注入
    eval(user_input)       # 代码注入
'''

    with open("example_project/src/main.py", 'w', encoding='utf-8') as f:
        f.write(python_code)

    # 创建JavaScript文件
    js_code = '''
function vulnerableFunction(data) {
    document.getElementById('output').innerHTML = data;  // XSS
}
const apiKey = "hardcoded_key_123";  // 硬编码密钥
'''

    with open("example_project/src/app.js", 'w', encoding='utf-8') as f:
        f.write(js_code)

    print("📁 已创建示例项目结构")

    # 扫描整个项目
    print("\n🔎 扫描整个项目...")
    findings = scanner.scan_directory("example_project")

    print(f"项目总共发现 {len(findings)} 个安全问题")

    # 按文件分组显示
    findings_by_file = {}
    for finding in findings:
        file_path = finding.file_path
        if file_path not in findings_by_file:
            findings_by_file[file_path] = []
        findings_by_file[file_path].append(finding)

    for file_path, file_findings in findings_by_file.items():
        print(f"\n📄 {file_path}: {len(file_findings)} 个问题")
        for finding in file_findings:
            print(f"   - {finding.rule_name} ({finding.severity})")

    # 生成完整报告
    print("\n📄 生成完整项目报告...")
    report = scanner.generate_report(findings, "project_security_report.md")
    print("项目安全报告已保存到: project_security_report.md"

    # 清理示例项目
    import shutil
    shutil.rmtree("example_project")


def demo_security_best_practices():
    """演示安全最佳实践"""
    print("\n🛡️ 安全最佳实践演示")
    print("=" * 40)

    print("🔒 安全编码最佳实践:")
    print()

    practices = [
        {
            'category': '输入验证',
            'practice': '始终验证和清理用户输入',
            'example': '使用类型检查、长度限制、正则表达式验证'
        },
        {
            'category': '参数化查询',
            'practice': '使用参数化SQL查询防止注入',
            'example': "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
        },
        {
            'category': '安全命令执行',
            'practice': '避免shell=True，使用列表参数',
            'example': "subprocess.run(['ls', safe_path], check=True)"
        },
        {
            'category': '密钥管理',
            'practice': '使用环境变量存储敏感信息',
            'example': "password = os.getenv('DB_PASSWORD')"
        },
        {
            'category': '内容安全策略',
            'practice': '设置CSP头和XSS防护',
            'example': "Content-Security-Policy: default-src 'self'"
        },
        {
            'category': '依赖管理',
            'practice': '定期更新依赖，监控安全漏洞',
            'example': "使用npm audit、pip-audit等工具"
        }
    ]

    for practice in practices:
        print(f"📋 {practice['category']}:")
        print(f"   实践: {practice['practice']}")
        print(f"   示例: {practice['example']}")
        print()


if __name__ == "__main__":
    try:
        demo_security_scanning()
        demo_vulnerability_fixes()
        demo_javascript_scanning()
        demo_project_scan()
        demo_security_best_practices()

        print("\n🎉 安全扫描演示完成！")
        print("\n💡 学习要点:")
        print("  - 安全扫描可以及早发现潜在漏洞")
        print("  - 不同类型的漏洞需要不同的修复策略")
        print("  - 安全是一个持续的过程，需要定期扫描")
        print("  - 遵循安全最佳实践可以显著降低风险")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
