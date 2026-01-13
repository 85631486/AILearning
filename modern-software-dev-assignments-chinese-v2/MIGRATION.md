# 中国区本地化迁移指南 (v2)

本文档详细记录了 `modern-software-dev-assignments-chinese-v2` 版本中所有国外工具和服务到中国区可访问替代方案的映射和替换说明。

## 🔄 替换映射表

### 1. 大语言模型与AI服务
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Ollama + Llama/Mistral模型 | 阿里千问 (Qwen via DashScope) | 统一的LLM客户端，支持多种Qwen模型 | `week1/llm_client.py`, 各练习脚本 |
| OpenAI API | 阿里千问 (Qwen via DashScope) | 完全兼容的API接口 | `pyproject.toml`, `llm_client.py` |
| Claude (Anthropic) | 阿里千问 (Qwen via DashScope) | 功能等效的中文AI模型 | 文档引用 |

### 2. 代码托管与协作
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| GitHub | Gitee (码云) | 中国最大的代码托管平台 | 文档中的仓库链接和协作说明 |
| GitHub Issues/PR | Gitee Issues/PR | 功能完全一致的协作工具 | 所有assignment.md中的协作说明 |

### 3. AI应用生成平台
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Bolt.new | 千问 + 本地模板生成 | 使用Qwen生成代码片段 + cookiecutter模板 | `week8/assignment.md`, 新增脚本 |
| Lovable, Figma Make | 千问 + 本地模板生成 | 统一的本地化解决方案 | `week8/assignment.md` |

### 4. 代码审查AI
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Graphite (AI code review) | Gitee code review + Qwen脚本 | 本地AI审查脚本 + Gitee协作 | `week7/assignment.md`, 新增 `scripts/ai_review.py` |

### 5. 终端与开发环境
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Warp (终端) | Windows Terminal / WezTerm | 功能等效的现代化终端 | `week5/assignment.md` |
| Warp Drive (自动化) | 本地脚本 + 批处理 | 使用PowerShell脚本替代Warp Drive功能 | `week5/assignment.md` |

### 6. 包管理和依赖
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| PyPI (默认) | 清华/阿里PyPI镜像 | 国内高速镜像 | `README.md`, 各周文档 |
| Poetry (包管理) | Poetry + 国内镜像 | 配置国内镜像源 | `pyproject.toml`, `README.md` |

### 7. 部署与托管
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Vercel | Gitee Pages / 阿里云函数 | 静态站点和函数部署 | 文档部署说明 |
| Cloudflare | 阿里云CDN / 函数计算 | 云端部署服务 | 文档部署说明 |

### 8. 安全扫描
| 原工具/服务 | 替换为 | 说明 | 影响文件 |
|------------|--------|------|---------|
| Semgrep (商业) | Bandit + 本地规则 | 开源安全扫描工具 | `week6/assignment.md` |

## 📋 具体文件更改记录

### 已完成的替换
1. **week1/llm_client.py**: 实现了统一的LLM客户端，默认使用Qwen
2. **各练习脚本**: 将ollama.chat调用替换为llm_client.chat
3. **pyproject.toml**: 移除ollama依赖，保留openai用于Qwen兼容
4. **README.md**: 添加千问配置说明，替换Ollama安装指导
5. **各周assignment.md**: 翻译为中文，更新工具说明

### 待处理的替换
1. **week5/assignment.md**: Warp → 本地终端 + 脚本
2. **week7/assignment.md**: Graphite → Gitee + 本地AI审查
3. **week8/assignment.md**: Bolt.new → Qwen + 模板生成

## 🔧 配置说明

### 千问 (Qwen) 配置
```bash
# 1. 获取API密钥
# 访问: https://dashscope.aliyuncs.com/
# 注册账户 -> API密钥管理 -> 创建密钥

# 2. 创建 .env 文件
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxx  # 替换为你的实际密钥
QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1

# 3. 验证配置
python week1/test_qwen_setup.py
```

### PyPI 国内镜像配置
```bash
# 临时使用（单次安装）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# 永久配置（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用阿里云镜像
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 验证配置
pip config list
```

### Poetry 国内镜像
```toml
# 在 pyproject.toml 中添加
[[tool.poetry.source]]
name = "tsinghua"
url = "https://pypi.tuna.tsinghua.edu.cn/simple/"
default = true

[[tool.poetry.source]]
name = "aliyun"
url = "https://mirrors.aliyun.com/pypi/simple/"
default = false
```

### Gitee 配置
```bash
# 1. 注册Gitee账户
# 访问: https://gitee.com/
# 完成实名认证（可能需要）

# 2. 配置SSH密钥（推荐）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 复制公钥到 Gitee: https://gitee.com/profile/sshkeys

# 3. 克隆仓库
git clone https://gitee.com/your_username/your_repo.git
# 或使用SSH
git clone git@gitee.com:your_username/your_repo.git
```

## 🚀 使用指南

### 1. 环境设置
```bash
# 1. 激活Conda环境
conda activate cs146s

# 2. 配置PyPI镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 安装依赖
poetry install

# 4. 配置千问API密钥
cp week1/env_example.txt .env
# 编辑 .env 文件，填入你的千问API密钥
```

### 2. 验证配置
```bash
python week1/test_qwen_setup.py
```

### 3. 运行练习
```bash
# week1 提示工程练习
python week1/k_shot_prompting.py
python week1/chain_of_thought.py
# ... 其他练习
```

## 📚 本地教程站点

v2版本包含完整的本地化教程站点，基于 `themodernsoftware.dev` 的镜像：

- 📁 `externals/themodernsoftware_dev_mirror/`: 原始站点抓取
- 📁 `site/`: 翻译后的中文站点（含语言切换）
- 📄 `build_site.sh`: 站点构建脚本

### 运行本地教程
```bash
cd site
python -m http.server 8080
# 访问 http://localhost:8080 查看教程
```

## 🔍 故障排除

### 网络连接问题
- **问题**: 无法访问dashscope.aliyuncs.com
- **解决**: 检查网络设置，可能需要配置代理或使用企业网络

### API密钥问题
- **问题**: 千问API调用失败
- **解决**: 确认API密钥有效且有余额，检查.env文件配置

### 包安装问题
- **问题**: pip/poetry安装失败
- **解决**: 确认已配置国内PyPI镜像，重试安装

## 📞 支持与反馈

如果在使用过程中遇到问题，请：

1. 检查本文档的故障排除部分
2. 查看各练习的README文件
3. 确认网络环境支持访问阿里云服务

---

*最后更新: 2025年1月*
