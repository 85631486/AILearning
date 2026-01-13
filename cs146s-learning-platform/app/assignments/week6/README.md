# Week 6: 安全漏洞扫描与修复

本项目实现了一个Semgrep风格的安全扫描器，用于检测和修复代码中的安全漏洞。

## 核心概念

### 安全扫描器
- **静态分析**: 通过模式匹配和AST分析检测安全问题
- **多语言支持**: 支持Python和JavaScript代码扫描
- **分类报告**: 按严重程度和类别生成详细的安全报告

### 支持的漏洞类型
- **注入漏洞**: SQL注入、命令注入、代码注入
- **XSS攻击**: DOM-based XSS漏洞
- **信息泄露**: 硬编码密钥和敏感信息
- **弱加密**: 使用不安全的加密算法

## 项目结构

```
week6/
├── scanner/
│   └── security_scanner.py    # 安全扫描器核心
├── fixes/                     # 修复示例（可扩展）
├── tests/                     # 测试文件
├── demo.py                   # 演示脚本
├── requirements.txt          # 依赖列表
└── README.md                # 说明文档
```

## 支持的安全规则

### Python安全规则
| 规则ID | 名称 | 严重程度 | CWE |
|--------|------|----------|-----|
| python-sql-injection | SQL注入 | 高 | CWE-89 |
| python-command-injection | 命令注入 | 高 | CWE-78 |
| python-eval | 代码注入(eval) | 高 | CWE-95 |
| python-hardcoded-secret | 硬编码密钥 | 中 | CWE-798 |
| python-weak-crypto | 弱加密算法 | 中 | CWE-327 |

### JavaScript安全规则
| 规则ID | 名称 | 严重程度 | CWE |
|--------|------|----------|-----|
| js-xss-innerhtml | DOM XSS | 高 | CWE-79 |
| js-eval | 代码注入(eval) | 高 | CWE-95 |
| js-hardcoded-api-key | 硬编码API密钥 | 中 | CWE-798 |

## 运行演示

### 运行完整演示
```bash
python demo.py
```

这将展示：
- Python代码安全扫描
- JavaScript代码安全扫描
- 漏洞修复示例
- 项目级安全评估
- 安全最佳实践

### 单独运行扫描器
```python
from scanner.security_scanner import scan_project

# 扫描当前目录
findings = scan_project(".")
print(f"发现 {len(findings)} 个安全问题")
```

### 扫描特定文件
```python
from scanner.security_scanner import scanner

# 扫描单个文件
findings = scanner.scan_file("example.py")
for finding in findings:
    print(f"{finding.rule_name}: {finding.description}")
```

## 扫描结果示例

```
🔍 开始扫描目录: .
📊 发现 5 个安全问题

高危: 2
中危: 3
低危: 0

详细发现:
vulnerable.py:15 - SQL注入 (高危)
  代码: query = f"SELECT * FROM users WHERE id = {user_id}"
  建议: 使用参数化查询或预处理语句

vulnerable.py:20 - 命令注入 (高危)
  代码: os.system(f"ls {user_input}")
  建议: 避免shell=True，使用shlex.quote转义参数，或使用subprocess列表参数
```

## 修复建议

### SQL注入修复
```python
# ❌ 有漏洞
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 修复后
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### 命令注入修复
```python
# ❌ 有漏洞
os.system(f"ls {user_command}")

# ✅ 修复后
subprocess.run(["ls", user_command], check=True)
```

### 硬编码密钥修复
```python
# ❌ 有漏洞
password = "secret123"

# ✅ 修复后
password = os.getenv("DB_PASSWORD")
```

## 安全最佳实践

### 1. 输入验证
- 始终验证和清理用户输入
- 使用类型检查、长度限制和正则表达式

### 2. 安全的数据库操作
- 使用参数化查询防止SQL注入
- 避免字符串拼接构建SQL语句

### 3. 安全的系统调用
- 避免`shell=True`参数
- 使用`subprocess`的列表参数形式

### 4. 密钥管理
- 不要在代码中硬编码敏感信息
- 使用环境变量或安全凭据存储

### 5. 前端安全
- 避免使用`innerHTML`，使用`textContent`
- 实施内容安全策略(CSP)

## 扩展扫描器

### 添加新规则
```python
# 在security_scanner.py的rules字典中添加新规则
new_rule = {
    'rule_id': 'python-new-vulnerability',
    'name': '新漏洞类型',
    'severity': 'medium',
    'category': 'misc',
    'pattern': r'pattern_to_match',
    'cwe': 'CWE-XXX',
    'description': '漏洞描述',
    'recommendation': '修复建议'
}
```

### 自定义修复器
```python
class CustomFixer:
    def apply_fix(self, finding):
        # 实现自定义修复逻辑
        pass
```

## 学习要点

1. **静态分析**: 如何通过代码模式识别安全漏洞
2. **风险评估**: 如何根据严重程度和影响评估漏洞
3. **修复策略**: 如何选择合适的修复方法
4. **预防措施**: 如何在编码过程中避免常见安全问题
5. **安全文化**: 为什么安全应该是开发过程中的一部分

## 测试

```bash
python -m pytest tests/ -v
```

## 实际应用场景

安全扫描器适用于：
- **代码审查**: 在提交前自动检查安全问题
- **持续集成**: 在CI/CD流水线中集成安全扫描
- **合规检查**: 确保代码符合安全标准和法规要求
- **教育培训**: 帮助开发者学习安全编码实践

## 下一步扩展

- 集成真实的Semgrep工具
- 添加更多编程语言支持
- 实现自动修复功能
- 添加机器学习辅助检测
- 支持自定义规则配置
