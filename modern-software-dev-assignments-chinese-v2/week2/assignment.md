# 第2周 — 行动项提取器

本周，我们将扩展一个最小的FastAPI + SQLite应用程序，将自由格式的笔记转换为枚举的行动项。

***我们建议在开始之前阅读完整文档。***

提示：预览此markdown文件的方法
- 在Mac上，按 `Command (⌘) + Shift + V`
- 在Windows/Linux上，按 `Ctrl + Shift + V`

## 入门指南

### Cursor设置
按照以下说明设置Cursor并打开项目：
1. 兑换免费一年的Cursor Pro：https://cursor.com/students
2. 下载Cursor：https://cursor.com/download
3. 要启用Cursor命令行工具，打开Cursor并按 `Command (⌘) + Shift+ P`（Mac用户）或 `Ctrl + Shift + P`（非Mac用户）打开命令面板。输入："Shell Command: Install 'cursor' command"。选择它并按Enter。
4. 打开新的终端窗口，导航到项目根目录，运行：`cursor .`

### 当前应用程序
以下是如何启动当前启动应用程序：
1. 激活你的conda环境。
```
conda activate cs146s
```
2. 从项目根目录运行服务器：
```
poetry run uvicorn week2.app.main:app --reload
```
3. 打开网页浏览器并导航到 http://127.0.0.1:8000/。
4. 熟悉应用程序的当前状态。确保你能够成功输入笔记并生成提取的行动项清单。

## 练习
对于每个练习，使用Cursor帮助你实现对当前行动项提取器应用程序的指定改进。

在完成作业的过程中，使用 `writeup.md` 记录你的进度。确保包含你使用的提示，以及你或Cursor所做的任何更改。我们将基于报告内容进行评分。请在代码中添加注释来记录你的更改。

### TODO 1: 搭建新功能

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数，该函数当前使用预定义的启发式方法提取行动项。

你的任务是实现一个**LLM驱动的**替代方案 `extract_action_items_llm()`，使用千问大模型通过大语言模型执行行动项提取。

一些提示：
- 要生成结构化输出（即字符串的JSON数组），请参考此文档：https://help.aliyun.com/zh/model-studio/getting-started/models
- 要浏览可用的千问模型，请参考DashScope文档。注意较大的模型将更耗费资源，所以从小模型开始。要使用模型，请在环境配置中指定模型名称。

### TODO 2: 添加单元测试

为 `extract_action_items_llm()` 编写单元测试，涵盖多种输入（例如，项目符号列表、关键字前缀行、空输入）在 `week2/tests/test_extract.py` 中。

### TODO 3: 重构现有代码以提高清晰度

对后端代码进行重构，特别关注定义明确的API契约/模式、数据库层清理、应用程序生命周期/配置、错误处理。

### TODO 4: 使用代理模式自动化小任务

1. 将LLM驱动的提取作为新端点集成。更新前端以包含"提取LLM"按钮，点击时通过新端点触发提取过程。

2. 公开一个最终端点来检索所有笔记。更新前端以包含"列出笔记"按钮，点击时获取并显示它们。

### TODO 5: 从代码库生成README

***学习目标：***
*学生学习AI如何内省代码库并自动生成文档，展示Cursor解析代码上下文并将其转换为人类可读形式的能力。*

使用Cursor分析当前代码库并生成结构良好的 `README.md` 文件。README至少应包括：
- 项目简要概述
- 如何设置和运行项目
- API端点和功能
- 运行测试套件的说明

## 交付物
根据提供的说明填写 `week2/writeup.md`。确保你的所有更改都在代码库中记录。

## 评分标准（总分100分）
- 第1-5部分每部分20分（生成的代码10分，每个提示10分）。