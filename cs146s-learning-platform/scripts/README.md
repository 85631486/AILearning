# 数据库初始化脚本使用指南

本目录包含用于初始化和管理CS146S在线学习平台数据库的脚本。

## 📚 课程内容

本平台基于**斯坦福大学CS146S：现代软件开发者课程**（中文本地化版本v2）。

课程源码位置: `/modern-software-dev-assignments-chinese-v2/`

### 课程结构

| 周次 | 标题 | 内容 | 练习数 |
|------|------|------|--------|
| Week 1 | 提示工程技术 | K-shot、思维链、工具调用、自一致性、RAG、反思 | 6个 |
| Week 2 | 行动项提取器 | FastAPI + SQLite应用开发 | 1个项目 |
| Week 3 | 自定义MCP服务器 | 模型上下文协议服务器开发 | 1个项目 |
| Week 4 | 自主编码代理 | Claude Code自动化工作流 | 1个项目 |
| Week 5 | 多代理工作流 | 本地终端环境多任务协作 | 1个项目 |
| Week 6 | 安全扫描与修复 | Semgrep静态代码分析 | 1个项目 |
| Week 7 | AI代码审查 | Gitee + AI脚本代码审查 | 1个项目 |
| Week 8 | 多栈应用构建 | 3种技术栈Web应用开发 | 1个项目 |

**总计**: 8周课程，13个练习/项目

## 🚀 快速开始

### 1. 初始化数据库

首次使用或需要重置数据库时：

```bash
cd cs146s-learning-platform
python3.11 scripts/init_database.py --reset
```

### 2. 配置千问API

在项目根目录创建 `.env` 文件：

```bash
# 千问API配置
QWEN_API_KEY=你的千问API密钥
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
QWEN_MODEL=qwen-turbo
```

获取API密钥: https://dashscope.aliyuncs.com/

### 3. 测试配置

```bash
python3.11 scripts/test_qwen_config.py
```

### 4. 启动系统

```bash
python3.11 run.py
```

访问: http://localhost:5000

## 🔧 脚本说明

### init_database.py

初始化数据库，创建所有课程周和练习数据。

**参数**:
- `--reset`: 重置数据库（删除所有数据）

**使用场景**:
- 首次部署系统
- 数据库损坏需要重建
- 开发环境重置

### test_qwen_config.py

测试千问模型配置和连接。

**功能**:
- 验证API密钥
- 测试模型连接
- 检查配置

## 📖 详细文档

完整的使用指南和故障排除，请参考项目文档。

---

**版本**: v2.0  
**更新日期**: 2026-01-13
