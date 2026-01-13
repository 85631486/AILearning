# CS146S：现代软件开发者作业 - 中文本地化版本 (v2)

这是斯坦福大学2025年秋季开设的[CS146S：现代软件开发者](https://themodernsoftware.dev)课程的作业仓库。

## 🎯 本地化特色 (v2版本)

本版本专门针对**无法访问国际互联网的中国区学员**进行了全面本地化：

### ✅ 主要改进
- 🔒 **网络环境适配**：所有工具和服务均可在国内网络环境下正常使用
- 🤖 **AI模型本地化**：使用阿里千问替代Ollama/OpenAI/Claude等国外AI服务
- 📚 **教程离线化**：提供完整的本地静态教程站点，支持离线浏览
- 🛠️ **工具链国产化**：GitHub→Gitee，PyPI→国内镜像，各类SaaS→本地替代方案

### 📋 本地化工具映射
| 原工具/服务 | 本地化替代 | 状态 |
|------------|-----------|------|
| GitHub | Gitee | ✅ 已替换 |
| OpenAI/Claude | 阿里千问 | ✅ 已集成 |
| Ollama | 阿里千问 | ✅ 已集成 |
| Bolt.new | 本地AI生成器 | ✅ 脚本实现 |
| Graphite | 本地AI审查脚本 | ✅ 脚本实现 |
| Warp | Windows Terminal | ✅ 文档更新 |
| Vercel | Gitee Pages | ✅ 文档更新 |
| PyPI | 清华/阿里镜像 | ✅ 配置文档 |

## 🚀 快速开始

### 环境要求
- Python 3.10+
- 现代操作系统 (Windows/Linux/macOS)
- **无需国际互联网连接**

### 1. 环境设置
```bash
# 创建Conda环境
conda create -n cs146s python=3.12 -y
conda activate cs146s

# 配置PyPI国内镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 获取千问API密钥
1. 访问 [阿里云DashScope](https://dashscope.aliyuncs.com/)
2. 注册账户并完成实名认证
3. 在"API密钥管理"中创建密钥
4. 账户充值确保有足够余额（建议至少50元）

### 3. 配置环境变量
```bash
# 创建 .env 文件
QWEN_API_KEY=你的千问API密钥
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
```

### 4. 安装项目依赖
```bash
# 安装Poetry
curl -sSL https://install.python-poetry.org | python -

# 安装项目依赖
poetry install --no-interaction
```

### 5. 验证安装
```bash
# 测试千问连接
python week1/test_qwen_setup.py

# 测试AI代码审查脚本
python scripts/ai_review.py --file week1/k_shot_prompting.py

# 测试应用生成脚本
python scripts/generate_app_template.py "待办事项管理应用"
```

## 📚 本地教程站点

v2版本包含完整的本地化教程站点：

```bash
# 构建教程站点
./scripts/build_site.sh

# 本地预览
cd site && python -m http.server 8080
# 访问: http://localhost:8080
```

### 教程内容
- 📖 完整的中文课程指南
- 🛠️ 本地化工具使用说明
- 💻 实践代码示例
- ❓ 常见问题解答

## 📖 课程结构

### 第1周: 提示工程技术
学习使用阿里千问进行有效的AI交互，包括：
- K-shot提示技术
- 思维链推理
- 工具调用
- 自一致性提示
- RAG检索增强
- 反思技术

### 第2周: 行动项提取器
构建FastAPI + SQLite应用，实现笔记到行动项的自动转换。

### 第3周: 自定义MCP服务器
设计并实现模型上下文协议服务器。

### 第4周: 自主编码代理
使用AI工具进行自主开发。

### 第5周: 多代理工作流
学习本地脚本实现多任务协作。

### 第6周: 安全扫描与修复
使用安全工具进行代码分析。

### 第7周: AI代码审查
使用本地AI脚本进行代码质量检查。

### 第8周: 多栈应用构建
使用本地AI生成器构建跨技术栈应用。

## 🔧 开发工具

### 本地AI工具
- **AI代码审查**: `python scripts/ai_review.py --file your_file.py`
- **应用生成**: `python scripts/generate_app_template.py "应用描述"`
- **千问测试**: `python week1/test_qwen_setup.py`

### 代码质量工具
```bash
# 格式化代码
poetry run black .

# 检查代码质量
poetry run ruff check .

# 运行测试
poetry run pytest
```

## 🐛 故障排除

### 网络连接问题
```bash
# 测试千问API连接
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen-turbo", "input": {"messages": [{"role": "user", "content": "Hello"}]}}'
```

### 包安装问题
```bash
# 清除缓存重试
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

### API密钥问题
- 确认密钥格式正确（以`sk-`开头）
- 检查账户余额充足
- 验证网络能访问`dashscope.aliyuncs.com`

## 📞 获取帮助

1. 查看 `MIGRATION.md` 获取详细的本地化说明
2. 访问本地教程站点了解详细用法
3. 使用AI工具进行问题诊断：
   ```bash
   python scripts/ai_review.py --file problem_file.py
   ```

## 📋 版本说明

- **v1版本**: 基础中文翻译 + 千问集成
- **v2版本**: 完全本地化 + 离线教程 + 本地AI工具

---

*本项目已针对中国大陆网络环境进行全面优化，确保学员无需国际互联网即可完成所有学习任务。*

3. 验证配置
   ```bash
   python week1/test_qwen_setup.py
   ```