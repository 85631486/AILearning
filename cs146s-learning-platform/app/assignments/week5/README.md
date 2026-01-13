# Week 5: 本地终端自动化

本项目实现了一个本地终端自动化框架，展示如何使用脚本和并行处理来提高开发工作流程的效率。

## 核心概念

### 自动化脚本
- **TestRunnerScript**: 带覆盖率的测试运行器，支持失败重试
- **DocSyncScript**: 从OpenAPI规范自动生成和更新API文档
- **RefactorScript**: 模块重构工具，自动更新导入和依赖

### 工作流编排器
- **WorkflowOrchestrator**: 支持多任务并行处理的工作流管理系统
- 支持并发执行多个自动化脚本
- 提供工作流状态监控和结果收集

## 项目结构

```
week5/
├── scripts/
│   └── automation_framework.py    # 自动化框架核心
├── workflows/                     # 工作流配置（可扩展）
├── tests/                         # 测试文件
├── demo.py                       # 演示脚本
├── requirements.txt              # 依赖列表
└── README.md                    # 说明文档
```

## 内置脚本功能

### 1. TestRunnerScript - 测试运行器
```python
script = TestRunnerScript()
script.set_parameter("coverage", True)
script.set_parameter("max_retries", 3)
result = script.execute()
```

**参数**:
- `test_path`: 测试文件路径（默认 "."）
- `coverage`: 是否生成覆盖率报告（默认 True）
- `max_retries`: 最大重试次数（默认 3）
- `verbose`: 详细输出（默认 False）

### 2. DocSyncScript - 文档同步器
```python
script = DocSyncScript()
script.set_parameter("openapi_file", "openapi.json")
script.set_parameter("output_file", "docs/API.md")
result = script.execute()
```

**参数**:
- `openapi_file`: OpenAPI规范文件路径
- `output_file`: 输出文档文件路径
- `force_update`: 强制更新现有文档

### 3. RefactorScript - 重构工具
```python
script = RefactorScript()
script.set_parameter("old_name", "extract")
script.set_parameter("new_name", "parser")
result = script.execute()
```

**参数**:
- `old_name`: 旧模块名
- `new_name`: 新模块名
- `target_dir`: 目标目录
- `run_tests`: 重构后运行测试
- `run_lint`: 重构后运行代码检查

## 工作流示例

### 完整CI工作流
```python
# 注册脚本到编排器
orchestrator = WorkflowOrchestrator()
orchestrator.register_script(TestRunnerScript())
orchestrator.register_script(DocSyncScript())

# 创建工作流
orchestrator.create_workflow("full_ci", ["test_runner", "doc_sync"])

# 执行工作流
result = orchestrator.execute_workflow_parallel("full_ci")
```

### 自定义工作流
```python
# 创建包含多个脚本的工作流
orchestrator.create_workflow("development_pipeline",
                           ["doc_sync", "test_runner", "refactor_module"])

# 并行执行
result = orchestrator.execute_workflow_parallel("development_pipeline")
```

## 运行演示

### 运行完整演示
```bash
python demo.py
```

这将展示：
- 单个脚本的功能演示
- 并行工作流的执行
- 脚本参数配置
- 自定义工作流创建

### 运行特定演示
```python
# 只演示脚本功能
from demo import demo_individual_scripts
demo_individual_scripts()

# 只演示并行工作流
from demo import demo_parallel_workflows
demo_parallel_workflows()
```

## 扩展自动化框架

### 添加新脚本
1. 继承 `AutomationScript` 类
2. 实现 `execute()` 方法
3. 定义脚本参数
4. 在编排器中注册脚本

```python
class CustomScript(AutomationScript):
    def __init__(self):
        super().__init__("custom_script", "自定义脚本描述")
        self.add_parameter("custom_param", "default_value", "参数描述")

    def execute(self) -> Dict[str, Any]:
        # 实现脚本逻辑
        return {"status": "success", "result": "执行结果"}

# 注册到编排器
orchestrator.register_script(CustomScript())
```

### 创建复杂工作流
```python
# 定义多阶段工作流
complex_workflow = [
    "doc_sync",      # 第一阶段：文档同步
    "test_runner",   # 第二阶段：运行测试
    "refactor_module" # 第三阶段：代码重构
]

orchestrator.create_workflow("complex_pipeline", complex_workflow)
```

## 性能和并发

### 并行执行优势
- **并发处理**: 多个独立任务可以同时执行
- **资源利用**: 充分利用多核CPU
- **时间节省**: 显著减少总执行时间

### 并发限制
- **依赖管理**: 脚本间的依赖关系需要 careful 处理
- **资源竞争**: 避免多个脚本同时访问相同资源
- **错误隔离**: 一个脚本失败不应该影响其他脚本

## 学习要点

1. **脚本自动化**: 如何将重复性任务转换为可重用脚本
2. **参数化配置**: 如何使脚本更加灵活和可配置
3. **并行处理**: 如何使用并发提高执行效率
4. **工作流编排**: 如何协调多个自动化任务
5. **错误处理**: 如何处理脚本执行中的异常情况

## 实际应用场景

本地终端自动化适用于：
- **持续集成**: 自动运行测试和代码检查
- **文档管理**: 自动生成和更新API文档
- **代码重构**: 批量重命名和更新依赖
- **发布流程**: 自动化版本管理和发布准备
- **开发环境**: 设置和维护开发环境

## 测试

```bash
python -m pytest tests/ -v
```

## 下一步扩展

- 添加更多内置脚本类型
- 支持脚本间的消息传递
- 实现工作流依赖图
- 添加监控和日志功能
- 支持分布式执行
