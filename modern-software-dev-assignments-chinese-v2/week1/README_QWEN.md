# 使用千问模型运行Week1提示工程练习

本工程已适配支持阿里的千问模型，可以完全替代Ollama环境。

## 环境配置

### 1. 安装依赖

首先安装必要的Python包：

```bash
pip install openai python-dotenv
```

### 2. 配置千问API

创建 `.env` 文件并添加以下配置：

```bash
# 千问API配置
QWEN_API_KEY=your_qwen_api_key_here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1

# 可选：指定使用的模型提供商（默认会自动检测）
LLM_PROVIDER=qwen
```

### 3. 获取千问API密钥

1. 访问 [阿里云DashScope](https://dashscope.aliyuncs.com/)
2. 注册账户并获取API Key
3. 将API Key填入 `.env` 文件中的 `QWEN_API_KEY`

## 支持的千问模型

工程中使用的模型映射：

| 原Ollama模型 | 千问模型替代 | 说明 |
|-------------|-------------|------|
| `mistral-nemo:12b` | `qwen-turbo` | 用于k-shot提示练习 |
| `llama3.1:8b` | `qwen-plus` | 用于其他练习的高性能模型 |

## 可用模型列表

千问提供以下模型（可根据需要调整）：

- `qwen-turbo`: 快速模型，适合简单任务
- `qwen-plus`: 高性能模型，适合复杂推理
- `qwen-max`: 最大性能模型
- `qwen-max-longcontext`: 长上下文模型

## 使用方法

### 运行单个练习

```bash
# 进入week1目录
cd week1

# 运行k-shot提示练习
python k_shot_prompting.py

# 运行思维链练习
python chain_of_thought.py

# 运行工具调用练习
python tool_calling.py

# 运行自一致性练习
python self_consistency_prompting.py

# 运行RAG练习
python rag.py

# 运行反思练习
python reflexion.py
```

### 切换回Ollama

如果你想切换回Ollama，只需：

1. 注释掉 `.env` 中的千问配置
2. 确保已安装并运行Ollama服务
3. 系统会自动检测并使用Ollama

```bash
# .env文件
# QWEN_API_KEY=your_key
# LLM_PROVIDER=ollama  # 或移除此行
```

## 代码架构

### LLM客户端统一接口

创建了 `llm_client.py` 来统一不同模型提供商的接口：

- `OllamaClient`: Ollama客户端
- `QwenClient`: 千问客户端（基于OpenAI兼容API）
- `LLMClientFactory`: 客户端工厂，支持自动检测

### 向后兼容

所有练习文件保持原有API不变，只需修改导入：

```python
# 原代码
from ollama import chat

# 新代码
from llm_client import chat
```

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ValueError: QWEN_API_KEY environment variable not set
   ```
   解决：检查 `.env` 文件中的API密钥配置

2. **网络连接问题**
   ```
   ConnectionError: Failed to connect
   ```
   解决：检查网络连接和API端点配置

3. **模型不存在**
   ```
   BadRequestError: model not found
   ```
   解决：检查使用的模型名称是否正确

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 性能对比

| 方面 | Ollama本地 | 千问云端 |
|------|-----------|---------|
| 启动速度 | 慢（需下载模型） | 快（云端服务） |
| 硬件要求 | 高（GPU内存） | 低（仅网络） |
| 成本 | 免费 | 按量付费 |
| 稳定性 | 依赖本地硬件 | 云端高可用 |
| 模型更新 | 手动更新 | 自动更新 |

## 扩展到其他模型

框架支持轻松扩展到其他OpenAI兼容的模型提供商，只需：

1. 在 `LLMClientFactory` 中添加新的客户端类
2. 实现 `LLMClient` 接口
3. 配置相应的环境变量

例如，支持Claude、Gemini等其他模型。
