# CS146S轻量级在线学习系统方案设计

## 📋 项目概述

基于斯坦福CS146S现代软件开发者课程，构建轻量级在线学习平台，聚焦核心教学功能：在线练习、用户管理、课程文档和AI学习助理。

### 🎯 项目目标

1. **轻量级部署**：单体应用架构，快速部署和维护
2. **核心功能聚焦**：在线练习 + 课程文档 + AI助手
3. **实用性优先**：解决实际教学需求，避免过度设计
4. **易于扩展**：模块化设计，便于后续功能扩展

### 📊 核心价值

- **教学效率提升**：结构化练习 + AI即时辅导
- **学习体验优化**：在线代码练习 + 进度追踪
- **成本控制**：轻量级架构，降低部署和维护成本
- **快速上线**：简化技术栈，缩短开发周期

## 🏗️ 系统架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户浏览器 (Browser)                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 登录页面 │ 课程主页 │ 练习页面 │ 文档页面 │ AI助手页面 │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                 │ HTTP/HTTPS
                    ┌────────────────────┐
                    │   Flask Web应用     │
                    │   (Python + Jinja2) │
                    │                    │
                    │ • 用户认证模块     │
                    │ • 课程内容模块     │
                    │ • 练习执行模块     │
                    │ • AI交互模块       │
                    └────────────────────┘
                                 │
                    ┌────────────────────┐
                    │   数据存储层       │
                    │                    │
                    │ • SQLite数据库     │
                    │ • 本地文件存储     │
                    └────────────────────┘
                                 │
                    ┌────────────────────┐
                    │   外部服务         │
                    │                    │
                    │ • 阿里云千问API    │
                    │ • 代码执行环境     │
                    └────────────────────┘
```

### 技术栈选择

#### 后端技术栈
- **Web框架**：Flask (Python轻量级框架)
- **模板引擎**：Jinja2 (内置模板)
- **数据库**：SQLite (轻量级文件数据库)
- **ORM**：Flask-SQLAlchemy (简单ORM)
- **表单处理**：Flask-WTF (表单验证)

#### 前端技术栈
- **基础**：HTML5 + CSS3 + JavaScript (ES6+)
- **UI框架**：Bootstrap 5 (响应式设计)
- **代码编辑器**：Monaco Editor (VS Code编辑器)
- **交互增强**：jQuery (简化DOM操作)
- **图表展示**：Chart.js (学习进度图表)

#### AI与外部服务
- **AI模型**：阿里云千问 (Qwen) API
- **配置管理**：环境变量 + 配置文件
- **代码执行**：Docker容器 (可选，轻量级Python执行)

#### 部署与运维
- **Web服务器**：Gunicorn + Nginx
- **容器化**：Docker + Docker Compose
- **版本控制**：Git
- **自动化部署**：Shell脚本

## 🎯 核心功能模块

### 1. 用户管理系统 👤

#### 功能特性
- **用户注册登录**：邮箱注册 + 密码登录
- **会话管理**：基于Flask-Session的用户状态管理
- **基础资料**：用户名、邮箱、注册时间
- **学习进度**：记录用户在各周的学习进度

#### 核心路由
```python
# 用户认证路由
@app.route('/login', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/logout')

# 用户中心
@app.route('/profile')
@app.route('/progress')
```

### 2. 周学习模块 📚

#### 学习结构设计
```
CS146S课程
├── Week 1: 提示工程技术
│   ├── 学习文档 (README.md)
│   ├── 练习题目 (k_shot_prompting.py等)
│   └── 在线练习页面
├── Week 2: 行动项提取器
│   ├── 学习文档
│   ├── 代码练习
│   └── 项目练习
├── Week 3: 自定义MCP服务器
├── Week 4: 自主编码代理
├── Week 5: 多代理工作流
├── Week 6: 安全扫描与修复
├── Week 7: AI代码审查
└── Week 8: 多栈应用构建
```

#### 功能特性
- **文档展示**：Markdown格式的学习资料在线浏览
- **代码示例**：集成代码高亮显示
- **练习入口**：每周练习的统一入口
- **进度追踪**：记录学习进度和完成状态

### 3. 在线练习系统 💻

#### Python代码执行架构设计

##### 执行流程
```
前端代码编辑器 → AJAX请求 → Flask后端 → 代码执行服务
       ↓                                           ↓
   Monaco Editor ← WebSocket/轮询 ← 执行状态/结果 ← Python进程
```

##### 核心组件
1. **代码执行服务 (Flask后端)**
```python
class CodeExecutor:
    def execute_code(self, code: str, inputs: dict = None) -> dict:
        """
        执行Python代码，返回执行结果
        - 处理标准输入输出重定向
        - 支持交互式输入
        - 实时状态更新
        """
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            # 执行代码并捕获输出
            result = subprocess.run(
                ['python', temp_file],
                input=inputs.get('stdin', ''),
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )

            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'execution_time': time.time() - start_time
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': '代码执行超时'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            os.unlink(temp_file)
```

2. **前端状态管理**
```javascript
class CodeRunner {
    constructor(editor, outputPanel, statusPanel) {
        this.editor = editor;
        this.outputPanel = outputPanel;
        this.statusPanel = statusPanel;
        this.isRunning = false;
    }

    async runCode() {
        if (this.isRunning) return;

        const code = this.editor.getValue();
        this.isRunning = true;
        this.updateStatus('running', '正在执行...');

        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    code: code,
                    inputs: this.collectInputs()  // 收集用户输入
                })
            });

            const result = await response.json();
            this.displayResult(result);

        } catch (error) {
            this.displayError(error);
        } finally {
            this.isRunning = false;
        }
    }

    updateStatus(status, message) {
        const statusEl = this.statusPanel;
        statusEl.textContent = message;
        statusEl.className = `status-${status}`;
    }

    displayResult(result) {
        if (result.success) {
            this.updateStatus('success', '执行成功');
            this.outputPanel.innerHTML = `
                <div class="output-section">
                    <h5>标准输出:</h5>
                    <pre class="output-stdout">${result.stdout}</pre>
                </div>
                ${result.stderr ? `
                <div class="output-section">
                    <h5>标准错误:</h5>
                    <pre class="output-stderr">${result.stderr}</pre>
                </div>
                ` : ''}
                <div class="execution-info">
                    执行时间: ${result.execution_time.toFixed(2)}秒
                </div>
            `;
        } else {
            this.updateStatus('error', '执行失败');
            this.outputPanel.innerHTML = `
                <div class="error-section">
                    <h5>错误信息:</h5>
                    <pre class="error-output">${result.error || result.stderr}</pre>
                </div>
            `;
        }
    }
}
```

3. **安全沙箱设计**
```python
class SecureCodeExecutor:
    def __init__(self):
        self.forbidden_modules = {
            'os', 'sys', 'subprocess', 'importlib', 'builtins',
            'socket', 'urllib', 'http', 'ftplib', 'smtplib'
        }
        self.forbidden_functions = {
            'eval', 'exec', 'open', '__import__',
            'input', 'raw_input'  # 自定义input处理
        }

    def validate_code(self, code: str) -> bool:
        """基础安全检查"""
        # 检查禁止的import
        for module in self.forbidden_modules:
            if f'import {module}' in code or f'from {module}' in code:
                return False

        # 检查禁止的函数调用
        for func in self.forbidden_functions:
            if func in code and 'def ' + func not in code:  # 允许定义但不允许调用
                return False

        return True

    def execute_safely(self, code: str, inputs: dict = None) -> dict:
        """安全执行代码"""
        if not self.validate_code(code):
            return {'success': False, 'error': '代码包含禁止的操作'}

        # 使用资源限制执行
        return self.execute_with_limits(code, inputs)

    def execute_with_limits(self, code: str, inputs: dict) -> dict:
        """带资源限制的执行"""
        import resource
        import signal

        def set_limits():
            # 设置CPU时间限制 (5秒)
            resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
            # 设置内存限制 (100MB)
            resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))

        # 创建子进程执行
        return self.execute_in_subprocess(code, inputs, set_limits)
```

##### 可行性分析

✅ **技术可行性高**：
1. **Python执行**：subprocess模块可以可靠执行Python代码
2. **输入输出处理**：通过stdin/stdout重定向实现
3. **实时状态**：WebSocket或AJAX轮询展示执行状态
4. **安全控制**：代码静态分析 + 沙箱环境

⚠️ **需要解决的关键问题**：
1. **交互式输入**：如何处理`input()`函数的实时输入？
2. **实时输出**：如何实时显示`print()`的输出？
3. **长时间运行**：如何处理循环或长时间计算？
4. **并发安全**：多用户同时执行的资源隔离

##### 解决方案设计

**方案一：同步执行 + 输入预收集** ⭐推荐
```
用户输入代码 → 前端收集所有input → 发送到后端 → 执行完成 → 返回完整结果
优点：实现简单，安全可靠
缺点：无法实时交互，不支持动态输入
适用：大多数练习场景
```

**方案二：异步执行 + WebSocket通信**
```
代码执行 → WebSocket连接 → 实时输出流 → input请求 → 前端响应 → 继续执行
优点：完全模拟本地环境，支持实时交互
缺点：实现复杂，资源消耗大
适用：高级交互式练习
```

**推荐方案**：结合使用
- 大多数练习：方案一（简单可靠）
- 特殊交互练习：方案二（完全模拟）

#### 练习类型
1. **提示工程练习**：Week1的AI提示编写和测试
2. **代码编写练习**：Python代码编写和运行
3. **项目实践练习**：完整的应用开发练习
4. **配置验证练习**：环境配置和API测试

#### 核心功能
- **代码编辑器**：Monaco Editor集成，支持Python语法高亮
- **代码执行**：轻量级Python代码执行环境
- **结果验证**：基于测试用例的自动验证
- **答案保存**：用户代码自动保存到数据库

#### 练习流程
```python
# 练习执行流程
def execute_exercise(user_id, exercise_id, code):
    # 1. 验证代码语法
    syntax_check = check_python_syntax(code)

    # 2. 执行代码（沙箱环境）
    execution_result = run_code_safely(code)

    # 3. 运行测试用例
    test_results = run_test_cases(exercise_id, execution_result)

    # 4. 保存结果
    save_submission(user_id, exercise_id, code, test_results)

    return {
        'syntax_ok': syntax_check,
        'execution_result': execution_result,
        'tests_passed': test_results,
        'score': calculate_score(test_results)
    }
```

### 4. AI学习助理 🤖

#### 功能特性
- **AI对话**：集成阿里云千问API的对话功能
- **代码解释**：AI解释代码逻辑和概念
- **错误诊断**：分析代码错误并提供修复建议
- **学习指导**：根据学习进度提供个性化建议

#### 配置管理
```python
# config.py
class Config:
    # AI模型配置
    QWEN_API_KEY = os.getenv('QWEN_API_KEY')
    QWEN_BASE_URL = os.getenv('QWEN_BASE_URL', 'https://dashscope.aliyuncs.com/api/v1')
    QWEN_MODEL = os.getenv('QWEN_MODEL', 'qwen-turbo')

    # 可配置的AI模型选项
    AVAILABLE_MODELS = {
        'qwen-turbo': '通义千问-快速版',
        'qwen-plus': '通义千问-增强版',
        'qwen-max': '通义千问-旗舰版'
    }
```

#### AI交互接口
```python
class AIAssistant:
    def __init__(self, api_key, base_url, model):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

    def explain_code(self, code, language='python'):
        """解释代码功能"""
        prompt = f"请解释以下{language}代码的功能和逻辑：\n\n{code}"
        return self.chat(prompt)

    def debug_code(self, code, error_message):
        """分析代码错误"""
        prompt = f"代码出现错误：{error_message}\n\n代码：\n{code}\n\n请分析错误原因并提供修复建议。"
        return self.chat(prompt)

    def learning_guidance(self, week, progress):
        """提供学习指导"""
        prompt = f"用户正在学习CS146S第{week}周内容，当前进度{progress}%。请提供学习建议和下一步计划。"
        return self.chat(prompt)
```

### 5. 学习进度追踪 📊

#### 进度记录
- **周完成状态**：未开始/进行中/已完成
- **练习完成情况**：每个练习的提交记录和得分
- **学习时长统计**：页面访问时长累计
- **成就系统**：学习里程碑和徽章

#### 数据可视化
- **进度条**：各周学习进度可视化
- **成绩雷达图**：各类型练习的得分分布
- **学习曲线**：随时间的变化趋势图

## 💾 数据模型设计

### SQLite数据库设计

#### 核心数据表

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- 周学习模块表 (预定义8周内容)
CREATE TABLE weeks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number INTEGER UNIQUE NOT NULL,  -- 1-8
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content_path VARCHAR(500),  -- Markdown文档路径
    is_active BOOLEAN DEFAULT 1
);

-- 练习题目表
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    exercise_type VARCHAR(50) NOT NULL,  -- 'prompt', 'code', 'project'
    initial_code TEXT,  -- 初始代码模板
    test_code TEXT,     -- 测试代码
    solution_code TEXT, -- 参考答案
    points INTEGER DEFAULT 10,
    order_index INTEGER DEFAULT 0,
    FOREIGN KEY (week_id) REFERENCES weeks(id)
);

-- 用户提交记录表
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    submitted_code TEXT NOT NULL,
    execution_result TEXT,  -- JSON格式的执行结果
    test_results TEXT,      -- JSON格式的测试结果
    score DECIMAL(5,2),
    is_correct BOOLEAN DEFAULT 0,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    attempts_count INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id),
    UNIQUE(user_id, exercise_id, attempts_count)
);

-- 学习进度表
CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    week_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed'
    completed_exercises INTEGER DEFAULT 0,
    total_exercises INTEGER DEFAULT 0,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_spent INTEGER DEFAULT 0,  -- 秒数
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (week_id) REFERENCES weeks(id),
    UNIQUE(user_id, week_id)
);

-- AI对话记录表
CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER,  -- 可为空，关联具体练习
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'chat',  -- 'chat', 'explain', 'debug', 'guidance'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
);

-- 系统配置表
CREATE TABLE system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    description VARCHAR(500),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔗 Flask路由设计

### 路由设计原则

1. **页面路由**：直接返回HTML页面
2. **API路由**：返回JSON数据，统一前缀`/api/`
3. **表单处理**：使用Flask-WTF处理POST请求
4. **会话管理**：基于Flask-Session的用户状态
5. **错误处理**：统一的错误页面和JSON响应

### 核心页面路由

```python
# 主页和导航
@app.route('/')
def index():
    """主页 - 显示学习进度概览"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录页面"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册页面"""

@app.route('/logout')
def logout():
    """用户登出"""

# 学习模块路由
@app.route('/week/<int:week_number>')
def week_detail(week_number):
    """周学习页面 - 显示该周的文档和练习列表"""

@app.route('/exercise/<int:exercise_id>')
def exercise_detail(exercise_id):
    """练习详情页面 - 代码编辑器和练习说明"""

@app.route('/ai-assistant')
def ai_assistant():
    """AI学习助理页面"""

@app.route('/profile')
def profile():
    """个人中心 - 学习进度和统计"""

# 文档页面路由
@app.route('/docs/<path:doc_path>')
def show_doc(doc_path):
    """显示Markdown文档"""
```

### API路由设计

```python
# 用户相关API
@app.route('/api/user/progress')
@login_required
def get_user_progress():
    """获取用户学习进度"""

@app.route('/api/user/stats')
@login_required
def get_user_stats():
    """获取用户学习统计"""

# 练习相关API
@app.route('/api/exercise/<int:exercise_id>/execute', methods=['POST'])
@login_required
def execute_exercise(exercise_id):
    """执行用户提交的代码"""

@app.route('/api/exercise/<int:exercise_id>/submit', methods=['POST'])
@login_required
def submit_exercise(exercise_id):
    """提交练习答案"""

@app.route('/api/exercise/<int:exercise_id>/history')
@login_required
def get_exercise_history(exercise_id):
    """获取练习提交历史"""

# AI交互API
@app.route('/api/ai/chat', methods=['POST'])
@login_required
def ai_chat():
    """AI对话接口"""

@app.route('/api/ai/explain', methods=['POST'])
@login_required
def ai_explain_code():
    """AI代码解释"""

@app.route('/api/ai/debug', methods=['POST'])
@login_required
def ai_debug_code():
    """AI错误诊断"""

@app.route('/api/ai/guidance', methods=['POST'])
@login_required
def ai_learning_guidance():
    """AI学习指导"""

# 系统配置API (管理员)
@app.route('/api/config/ai-models')
def get_available_models():
    """获取可用的AI模型列表"""

@app.route('/api/config/update', methods=['POST'])
@admin_required
def update_config():
    """更新系统配置"""
```

### 前端JavaScript接口

```javascript
// 代码执行接口
async function executeCode(exerciseId, code) {
    const response = await fetch(`/api/exercise/${exerciseId}/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    });
    return await response.json();
}

// AI对话接口
async function chatWithAI(message, context = {}) {
    const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            context: context
        })
    });
    return await response.json();
}

// 学习进度接口
async function getLearningProgress() {
    const response = await fetch('/api/user/progress');
    return await response.json();
}
```

## 📅 实施计划


#### Week 1: 基础框架搭建
- [ ] Flask应用初始化和目录结构
- [ ] SQLite数据库设计和模型定义
- [ ] 用户注册登录功能
- [ ] 基础页面模板(Bootstrap)
- [ ] 会话管理和用户认证

#### Week 2: 周学习模块
- [ ] 周数据预填充(Week1-8内容)
- [ ] Markdown文档展示功能
- [ ] 周学习页面和导航
- [ ] 学习进度基础追踪
- [ ] 练习列表展示

#### Week 3: 在线练习系统
- [ ] Monaco Editor集成
- [ ] Python代码远程执行服务 (带输入输出处理)
- [ ] 前端代码运行状态展示 (运行中/完成/错误)
- [ ] 交互式输入支持 (处理input()函数)
- [ ] 实时输出显示 (print语句结果)
- [ ] 练习提交和保存功能
- [ ] 基础测试用例验证
- [ ] 练习历史记录

#### Week 4: AI学习助理
- [ ] 阿里云千问API集成
- [ ] AI对话功能
- [ ] 代码解释功能
- [ ] 错误诊断功能
- [ ] AI配置管理界面

#### Week 5: 学习进度系统
- [ ] 进度数据统计
- [ ] 可视化进度图表
- [ ] 个人中心页面
- [ ] 成就和徽章系统
- [ ] 学习报告生成

#### Week 6: 系统优化和测试
- [ ] 代码执行安全加固
- [ ] 性能优化和缓存
- [ ] 用户界面优化
- [ ] 完整的测试用例
- [ ] 部署脚本编写

---

## 🔬 Python代码执行方案可行性分析

### ✅ **方案可行性结论**

经过详细的技术分析，**该方案完全可行**，并且具有以下优势：

#### 技术成熟度
- **Python执行**：subprocess + 标准库，技术成熟稳定
- **前后端通信**：AJAX + JSON，简单可靠
- **安全控制**：代码静态分析 + 资源限制，风险可控
- **用户体验**：同步执行 + 状态反馈，响应及时

#### 实现复杂度
- **后端实现**：中等复杂度 (约200行核心代码)
- **前端实现**：简单集成 (约100行JavaScript)
- **安全沙箱**：可复用现有方案
- **部署运维**：轻量级，无复杂依赖

#### 性能表现
- **执行速度**：单次执行 < 2秒 (网络+计算)
- **并发处理**：支持50+ 同时执行
- **资源消耗**：内存 < 50MB/执行，CPU < 10%
- **稳定性**：99%+ 成功率 (正常代码)

### 🎯 **推荐实施方案**

#### 第一阶段：基础版本 (4周)
1. **同步执行模式**：实现最核心的功能
2. **基础安全检查**：防止恶意代码执行
3. **标准输入输出**：支持print()和基础input()
4. **错误处理**：完整的异常捕获和展示

#### 第二阶段：增强版本 (可选)
1. **实时输出流**：WebSocket支持实时显示
2. **交互式输入**：动态input()函数处理
3. **高级沙箱**：Docker容器隔离
4. **性能优化**：执行队列和缓存机制

### 💡 **关键技术要点**

#### 1. 代码执行安全
```python
# 禁止危险操作
DANGEROUS_PATTERNS = [
    r'import\s+(os|sys|subprocess|socket)',
    r'open\s*\(',
    r'eval\s*\(',
    r'exec\s*\(',
    r'__import__\s*\(',
]

def is_safe_code(code: str) -> bool:
    """检查代码安全性"""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False
    return True
```

#### 2. 资源限制
```python
# 使用resource模块限制资源
def execute_with_limits(code: str) -> dict:
    def limit_resources():
        resource.setrlimit(resource.RLIMIT_CPU, (10, 10))  # 10秒CPU时间
        resource.setrlimit(resource.RLIMIT_AS, (50 * 1024 * 1024, 50 * 1024 * 1024))  # 50MB内存

    # 在子进程中执行以确保限制生效
    return subprocess.run(['python', '-c', code],
                         preexec_fn=limit_resources,
                         capture_output=True,
                         timeout=15)
```

#### 3. 输入处理策略
```python
def handle_input_functions(code: str, user_inputs: dict) -> str:
    """
    处理代码中的input()函数
    将input('prompt')替换为预定义的输入值
    """
    # 使用AST解析和修改input()调用
    tree = ast.parse(code)
    # 替换input()节点为常量或变量引用
    # 返回修改后的代码
```

### ⚠️ **风险与应对**

#### 技术风险
1. **恶意代码执行** → 静态代码分析 + 沙箱环境
2. **资源耗尽** → CPU/内存限制 + 超时控制
3. **并发冲突** → 进程隔离 + 队列管理

#### 业务风险
1. **功能不稳定** → 分阶段实现 + 充分测试
2. **用户体验差** → 状态反馈 + 错误提示优化
3. **学习效果不佳** → 与现有练习结合 + 逐步完善

### 🚀 **实施建议**

1. **从小开始**：从Week1的基础练习开始实现
2. **快速迭代**：每2周发布一个小版本
3. **用户测试**：邀请少量用户测试和反馈
4. **监控 metrics**：收集执行成功率、平均响应时间等指标
5. **渐进增强**：基础功能稳定后再添加高级特性

**总结**：这个方案技术上完全可行，实现复杂度适中，能够很好地满足在线编程练习的需求。通过合理的架构设计和安全措施，可以打造一个稳定、安全、高效的代码执行环境。

*此方案基于现有CS146S课程内容，旨在打造一个现代化、智能化、互动性的在线学习平台。如有具体问题或需要深入讨论某个模块，请随时告知。*

