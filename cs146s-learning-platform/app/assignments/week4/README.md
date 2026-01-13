# Week 4: 自主编码代理

本项目实现了一个简化的自主编码代理系统，展示代理协作完成软件开发任务的概念。

## 核心概念

### 代理类型
- **TestAgent**: 专门负责编写和运行测试的代理
- **CodeAgent**: 专门负责编写和重构代码的代理
- **AgentOrchestrator**: 协调多个代理工作的编排器

### 代理协作流程
1. **任务创建**: Orchestrator接收开发任务
2. **任务分配**: 将任务分配给合适的代理
3. **代理执行**: 每个代理使用其专业技能完成任务
4. **结果整合**: 收集和整合各代理的输出

## 项目结构

```
week4/
├── agents/
│   ├── base_agent.py      # 代理基类和编排器
│   ├── test_agent.py      # 测试代理实现
│   └── code_agent.py      # 代码代理实现
├── tools/                 # 代理工具（可扩展）
├── tests/                 # 代理系统测试
├── demo.py               # 演示脚本
├── requirements.txt      # 依赖列表
└── README.md            # 说明文档
```

## 运行演示

### 运行完整演示
```bash
python demo.py
```

这将展示：
- 代理注册过程
- 任务创建和分配
- 代理间协作
- 结果整合

### 运行单个代理演示
```bash
python -c "from agents.test_agent import TestAgent; agent = TestAgent(); print(agent.get_status())"
```

## 代理能力

### TestAgent 能力
- **write_tests**: 编写测试用例
- **run_tests**: 执行测试套件
- **analyze_coverage**: 分析测试覆盖率
- **identify_edge_cases**: 识别边界情况

### CodeAgent 能力
- **write_code**: 编写新代码
- **refactor_code**: 重构现有代码
- **fix_bugs**: 修复代码缺陷
- **add_features**: 添加新功能

## 扩展代理系统

### 添加新代理
1. 继承 `BaseAgent` 类
2. 实现 `process_message` 和 `generate_response` 方法
3. 定义代理的角色和能力
4. 在 Orchestrator 中注册代理

### 添加新工具
```python
# 在代理的 __init__ 方法中
self.add_tool("tool_name", self.tool_function)

def tool_function(self, **kwargs):
    # 工具实现
    pass
```

## 学习要点

1. **代理协作**: 不同专业代理如何协同工作
2. **任务分解**: 如何将复杂任务分解为可管理的子任务
3. **消息传递**: 代理间通信机制
4. **工具集成**: 如何为代理添加专业工具
5. **结果整合**: 如何收集和整合多个代理的输出

## 实际应用

自主编码代理可以用于：
- 自动化测试生成
- 代码重构辅助
- 文档生成
- 代码审查
- 持续集成优化

## 运行测试

```bash
python -m pytest tests/ -v
```

## 下一步扩展

- 添加更多类型的代理（文档代理、部署代理等）
- 实现持久化存储
- 添加用户界面
- 集成真实的Claude Code工具
- 实现更复杂的任务规划算法
