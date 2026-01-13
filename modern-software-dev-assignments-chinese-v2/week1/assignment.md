# 第1周 — 提示工程技术

你将通过设计提示来完成特定任务，从而练习多种提示工程技术。每项任务的说明都在对应源文件的顶部。

## 安装
确保你已经完成了根目录 `README.md` 中描述的安装步骤。

## 千问模型配置
我们将使用阿里云的千问大模型来进行练习。请按照以下步骤配置：

### 1. 安装依赖
```bash
pip install openai python-dotenv
```

### 2. 获取API密钥
访问 [阿里云DashScope](https://dashscope.aliyuncs.com/) 注册账户并获取API密钥。

### 3. 配置环境变量
创建 `.env` 文件并添加以下配置：
```bash
# 千问API配置
QWEN_API_KEY=你的千问API密钥
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
```

### 4. 验证配置
```bash
python test_qwen_setup.py
```

## 技术与源文件
- K-shot提示 — `week1/k_shot_prompting.py`
- 思维链提示 — `week1/chain_of_thought.py`
- 工具调用 — `week1/tool_calling.py`
- 自一致性提示 — `week1/self_consistency_prompting.py`
- RAG（检索增强生成） — `week1/rag.py`
- 反思技术 — `week1/reflexion.py`

## 交付物
- 阅读每个文件中的任务描述。
- 设计并运行提示（查找代码中标记为 `TODO` 的所有位置）。这应该是你唯一需要修改的地方（即不要修改模型配置）。
- 迭代改进结果直到测试脚本通过。
- 保存每种技术的最终提示和输出。
- 确保提交中包含每个提示工程技术文件的完整代码。***仔细检查所有 `TODO` 都已解决。***

## 评分标准（总分60分）
- 6种不同提示工程技术中每种完成的技术得10分