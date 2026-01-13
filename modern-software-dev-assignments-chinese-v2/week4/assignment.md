# 第4周 — 自主编码代理实战

> ***我们建议在开始之前阅读完整文档。***

本周，你的任务是在此仓库的上下文中构建至少**2个自动化**，使用以下**Claude Code**功能的任意组合：

- 自定义斜杠命令（检入到`.claude/commands/*.md`）

- `CLAUDE.md`文件用于仓库或上下文指导

- Claude子代理（角色专业化代理协同工作）

- 集成到Claude Code中的MCP服务器

你的自动化应该有意义地改进开发者工作流程——例如，通过简化测试、文档、重构或数据相关任务。然后你将使用创建的自动化来扩展`week4/`中的启动应用程序。

## 了解Claude Code
为了更深入地理解Claude Code并探索你的自动化选项，请阅读以下两个资源：

1. **Claude Code最佳实践：**[anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **子代理概述：**[docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 探索启动应用程序
设计为**"开发者指挥中心"**的最小全栈启动应用程序。
- 带有SQLite的FastAPI后端（SQLAlchemy）
- 静态前端（无需Node工具链）
- 最小测试（pytest）
- 预提交（black + ruff）
- 练习代理驱动工作流程的任务

使用此应用程序作为你的游乐场来实验你构建的Claude自动化。

### 结构

```
backend/                # FastAPI应用
frontend/               # 由FastAPI服务的静态UI
data/                   # SQLite数据库 + 种子数据
docs/                   # 代理驱动工作流程的任务
```

### 快速开始

1) 激活你的conda环境。

```bash
conda activate cs146s
```

2) （可选）安装预提交钩子

```bash
pre-commit install
```

3) 运行应用（从`week4/`目录）

```bash
make run
```

4) 打开`http://localhost:8000`查看前端，`http://localhost:8000/docs`查看API文档。

5) 试用启动应用程序以熟悉其当前特性和功能。

### 测试
运行测试（从`week4/`目录）
```bash
make test
```

### 格式化/代码检查
```bash
make format
make lint
```

## 第一部分：构建你的自动化（选择2个或更多）
现在你已经熟悉了启动应用程序，你的下一步是构建自动化来增强或扩展它。下面是几个你可以选择的自动化选项。你可以在类别之间混合搭配。

在构建自动化时，在`writeup.md`文件中记录你的更改。现在先将*"如何使用自动化来增强启动应用程序"*部分留空——你将在作业的第二部分返回到此。

### A) Claude自定义斜杠命令
斜杠命令是重复工作流程的功能，让你可以在`.claude/commands/`内的Markdown文件中创建可重用的工作流程。Claude通过`/`公开这些。

- 示例1：带覆盖率的测试运行器
  - 名称：`tests.md`
  - 意图：运行`pytest -q backend/tests --maxfail=1 -x`，如果通过则运行覆盖率。
  - 输入：可选标记或路径。
  - 输出：总结失败并建议后续步骤。
- 示例2：文档同步
  - 名称：`docs-sync.md`
  - 意图：读取`/openapi.json`，更新`docs/API.md`，并列出路由差异。
  - 输出：类似diff的总结和TODO。
- 示例3：重构工具
  - 名称：`refactor-module.md`
  - 意图：重命名模块（例如，`services/extract.py` → `services/parser.py`），更新导入，运行代码检查/测试。
  - 输出：修改文件清单和验证步骤。

>*提示：保持命令专注，使用`$ARGUMENTS`，偏好幂等步骤。考虑允许列出安全工具并使用无头模式以提高可重复性。*

### B) `CLAUDE.md`指导文件
`CLAUDE.md`文件在开始对话时自动读取，允许你提供影响Claude行为的仓库特定说明、上下文或指导。在仓库根目录（以及可选的`week4/`子文件夹）创建`CLAUDE.md`来指导Claude的行为。

- 示例1：代码导航和入口点
  - 包括：如何运行应用、路由位置（`backend/app/routers`）、测试位置、数据库如何种子化。
- 示例2：风格和安全护栏
  - 包括：工具期望（black/ruff）、可以运行的安全命令、要避免的命令，以及代码检查/测试门。
- 示例3：工作流程片段
  - 包括："当被要求添加端点时，首先编写失败测试，然后实现，然后运行预提交。"

> *提示：像提示一样迭代`CLAUDE.md`，保持简洁可操作，并记录你期望Claude使用的自定义工具/脚本。*

### C) 子代理（角色专业化）

子代理是配置为使用自己的系统提示、工具和上下文处理特定任务的专业化AI助手。设计两个或更多协作代理，每个负责单个工作流程中的不同步骤。

- 示例1：TestAgent + CodeAgent
  - 流程：TestAgent为更改编写/更新测试 → CodeAgent实现代码以通过测试 → TestAgent验证。
- 示例2：DocsAgent + CodeAgent
  - 流程：CodeAgent添加新API路由 → DocsAgent更新`API.md`和`TASKS.md`，并根据`/openapi.json`检查偏差。
- 示例3：DBAgent + RefactorAgent
  - 流程：DBAgent提出架构更改（调整`data/seed.sql`）→ RefactorAgent更新模型/架构/路由并修复代码检查。

>*提示：使用清单/草稿板，在角色之间重置上下文（`/clear`），并为独立任务并行运行代理。*

## 第二部分：让你的自动化发挥作用
现在你已经构建了2个以上的自动化，让我们使用它们！在`writeup.md`中的*"如何使用自动化来增强启动应用程序"*部分，描述你如何利用每个自动化来改进或扩展应用的功能。

例如，如果你实现了自定义斜杠命令`/generate-test-cases`，解释你如何使用它与启动应用程序交互和测试。

## 交付物
1) 两个或更多自动化，可能包括：
   - `.claude/commands/*.md`中的斜杠命令
   - `CLAUDE.md`文件
   - 子代理提示/配置（清楚记录，任何文件/脚本）

2) `week4/`下的报告`writeup.md`，包括：
  - 设计灵感（例如，引用最佳实践和/或子代理文档）
  - 每个自动化的设计，包括目标、输入/输出、步骤
  - 如何运行它（确切命令）、预期输出以及回滚/安全说明
  - 前后对比（即手动工作流程vs自动化工作流程）
  - 如何使用自动化来增强启动应用程序

## 提交说明
1. 确保所有更改已推送到远程仓库以供评分。
2. **确保你已将brentju和febielin添加为作业仓库的协作者。**
3. 通过Gradescope提交。 



