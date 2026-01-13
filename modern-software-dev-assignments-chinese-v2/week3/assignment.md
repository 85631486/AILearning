# 第3周 — 构建自定义MCP服务器

设计并实现一个模型上下文协议（MCP）服务器，用于封装真实的外部API。你可以：
- **本地运行**（STDIO传输）并与MCP客户端（如Claude Desktop）集成。
- 或者**远程运行**（HTTP传输）并从模型代理或客户端调用。这更难但可以获得额外学分。

添加认证（API密钥或OAuth2）并与MCP授权规范对齐可以获得奖励积分。

## 学习目标
- 理解核心MCP功能：工具、资源、提示。
- 使用类型化参数和强大的错误处理实现工具定义。
- 遵循日志记录和传输最佳实践（STDIO服务器不能使用stdout）。
- 可选：为HTTP传输实现授权流程。

## 要求
1. 选择一个外部API并记录你将使用的端点。示例：天气、GitHub问题、Notion页面、电影/电视数据库、日历、任务管理器、金融/加密货币、旅行、体育统计。
2. 公开至少两个MCP工具
3. 实现基本弹性：
   - HTTP失败、超时和空结果的优雅错误处理。
   - 遵守API速率限制（例如，简单的退避或用户面对的警告）。
4. 打包和文档：
   - 提供清晰的设置说明、环境变量和运行命令。
   - 包含调用流程示例（在客户端中输入/点击什么来触发工具）。
5. 选择一种部署模式：
   - 本地：STDIO服务器，可以从你的机器运行，并可被Claude Desktop或AI IDE（如Cursor）发现。
   - 远程：HTTP服务器，可通过网络访问，可被MCP感知的客户端或代理运行时调用。如果部署并可访问则获得额外学分。
6. （可选）奖励：认证
   - 通过环境变量和客户端配置支持API密钥；或者
   - HTTP传输的OAuth2风格承载令牌，验证令牌受众，永远不要将令牌传递给上游API。

## 交付物
- `week3/` 下的源代码（建议：`week3/server/`，带有清晰的入口点，如 `main.py` 或 `app.py`）。
- `week3/README.md` 包含：
  - 先决条件、环境设置以及运行说明（本地和/或远程）。
  - 如何配置MCP客户端（本地使用Claude Desktop示例）或远程使用代理运行时。
  - 工具参考：名称、参数、输入/输出示例以及预期行为。

## 评分标准（总分90分）
- 功能性（35分）：实现2个以上工具，正确的API集成，有意义输出。
- 可靠性（20分）：输入验证、错误处理、日志记录、速率限制意识。
- 开发者体验（20分）：清晰设置/文档，易于本地运行；合理的文件夹结构。
- 代码质量（15分）：可读代码、描述性名称、最小复杂度、适用时使用类型提示。
- 额外学分（10分）：
  - +5 远程HTTP MCP服务器，可被代理/客户端调用，如OpenAI/Claude SDK。
  - +5 正确实现认证（API密钥或带受众验证的OAuth2）。

## 有用的参考资料
- MCP服务器快速入门：[modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)。
*注意：你不能提交这个确切的示例。*
- MCP授权（HTTP）：[modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- Cloudflare上的远程MCP（代理）：[developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)。在部署前使用modelcontextprotocol检查器工具在本地调试服务器。
- https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel 如果你选择进行远程MCP部署，Vercel是一个有免费层的良好选择。 