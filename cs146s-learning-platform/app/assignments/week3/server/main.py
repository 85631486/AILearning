#!/usr/bin/env python3
"""
Week 3: Custom MCP Server - Weather API Example
MCP服务器示例：封装天气API，提供天气查询工具
"""

import os
import json
import asyncio
from typing import Any, Dict, List, Optional
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, ImageContent, EmbeddedResource


# 创建MCP服务器实例
app = Server("weather-mcp-server")


class WeatherAPI:
    """模拟天气API客户端"""

    def __init__(self):
        # 在实际实现中，这里会调用真实的天气API
        # 为了演示，我们使用模拟数据
        self.mock_weather_data = {
            "北京": {
                "temperature": 22,
                "condition": "晴",
                "humidity": 45,
                "wind_speed": 12
            },
            "上海": {
                "temperature": 25,
                "condition": "多云",
                "humidity": 60,
                "wind_speed": 8
            },
            "广州": {
                "temperature": 28,
                "condition": "阴",
                "humidity": 75,
                "wind_speed": 5
            },
            "深圳": {
                "temperature": 27,
                "condition": "小雨",
                "humidity": 80,
                "wind_speed": 15
            }
        }

    def get_weather(self, city: str) -> Dict[str, Any]:
        """获取城市天气信息"""
        if city in self.mock_weather_data:
            return self.mock_weather_data[city]
        else:
            # 默认返回一个通用天气
            return {
                "temperature": 20,
                "condition": "未知",
                "humidity": 50,
                "wind_speed": 10
            }

    def get_supported_cities(self) -> List[str]:
        """获取支持的城市列表"""
        return list(self.mock_weather_data.keys())


# 初始化天气API客户端
weather_api = WeatherAPI()


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """列出可用的MCP工具"""
    return [
        Tool(
            name="get_weather",
            description="获取指定城市的天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称（如：北京、上海）"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_supported_cities",
            description="获取支持天气查询的城市列表",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
    """处理工具调用"""

    if name == "get_weather":
        city = arguments.get("city", "")
        if not city:
            return [TextContent(
                type="text",
                text="错误：请提供城市名称"
            )]

        weather_data = weather_api.get_weather(city)

        response = f"""
城市：{city}
温度：{weather_data['temperature']}°C
天气：{weather_data['condition']}
湿度：{weather_data['humidity']}%
风速：{weather_data['wind_speed']} km/h
        """.strip()

        return [TextContent(
            type="text",
            text=response
        )]

    elif name == "get_supported_cities":
        cities = weather_api.get_supported_cities()
        response = f"支持查询天气的城市：{', '.join(cities)}"

        return [TextContent(
            type="text",
            text=response
        )]

    else:
        return [TextContent(
            type="text",
            text=f"错误：未知工具 '{name}'"
        )]


@app.list_resources()
async def handle_list_resources() -> List[Any]:
    """列出可用的资源（此示例中为空）"""
    return []


@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """读取资源内容（此示例中为空）"""
    return ""


@app.list_prompts()
async def handle_list_prompts() -> List[Any]:
    """列出可用的提示模板（此示例中为空）"""
    return []


@app.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, Any]) -> Any:
    """获取提示模板（此示例中为空）"""
    return None


async def main():
    """主函数：启动MCP服务器"""
    # 可以使用stdio或http传输
    # 此处使用stdio传输（适合本地MCP客户端）

    import mcp.server.stdio
    import logging

    # 设置日志
    logging.basicConfig(level=logging.INFO)

    print("🌤️  天气MCP服务器启动中...", flush=True)
    print("📋 可用工具：", flush=True)
    print("  - get_weather: 获取城市天气", flush=True)
    print("  - get_supported_cities: 获取支持城市列表", flush=True)
    print("🚀 服务器已就绪，等待MCP客户端连接...", flush=True)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
