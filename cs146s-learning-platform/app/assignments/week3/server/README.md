# Week 3: 自定义MCP服务器 - 天气查询示例

本项目实现了一个简单的MCP (Model Context Protocol) 服务器，提供天气查询功能。

## 功能特性

- **get_weather**: 查询指定城市的天气信息
- **get_supported_cities**: 获取支持查询的城市列表

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务器

### 本地STDIO模式（推荐用于学习）

```bash
python main.py
```

服务器将在本地启动，等待MCP客户端连接。

### 配置MCP客户端（以Claude Desktop为例）

1. 打开Claude Desktop
2. 进入设置 > MCP服务器
3. 添加新的本地服务器：
   ```json
   {
     "mcpServers": {
       "weather-server": {
         "command": "python",
         "args": ["/path/to/week3/server/main.py"],
         "env": {}
       }
     }
   }
   ```

4. 重启Claude Desktop

## 测试工具

### 工具1: get_weather
**描述**: 获取指定城市的天气信息

**参数**:
- `city` (string): 城市名称，如"北京"、"上海"

**示例调用**:
```
用户: 北京今天的天气怎么样？
助手: 让我查询一下北京的天气信息。
[调用工具: get_weather, 参数: {"city": "北京"}]
```

**示例输出**:
```
城市：北京
温度：22°C
天气：晴
湿度：45%
风速：12 km/h
```

### 工具2: get_supported_cities
**描述**: 获取所有支持天气查询的城市列表

**参数**: 无

**示例调用**:
```
用户: 你们支持查询哪些城市的天气？
助手: 让我查看支持的城市列表。
[调用工具: get_supported_cities, 参数: {}]
```

**示例输出**:
```
支持查询天气的城市：北京, 上海, 广州, 深圳
```

## 开发说明

### 项目结构
```
server/
├── main.py          # MCP服务器主程序
├── requirements.txt # 依赖列表
└── README.md       # 说明文档
```

### 扩展功能

1. **添加更多工具**: 在`handle_list_tools()`中添加新工具定义
2. **集成真实API**: 修改`WeatherAPI`类调用真实的天气API
3. **添加认证**: 实现API密钥验证
4. **HTTP传输**: 修改为HTTP服务器模式以支持远程访问

### 错误处理

服务器实现了基本的错误处理：
- 输入验证
- API调用异常处理
- 网络超时处理
- 无效城市名的降级处理

## 学习要点

- MCP协议的基本概念和实现
- 工具定义和参数验证
- 错误处理和日志记录
- 客户端集成配置
- 异步编程模式
