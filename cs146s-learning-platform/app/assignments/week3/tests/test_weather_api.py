#!/usr/bin/env python3
"""
Week 3 MCP服务器测试
测试天气API工具功能
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# 添加服务器目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

from main import WeatherAPI, handle_call_tool


class TestWeatherAPI:
    """测试天气API类"""

    def test_get_weather_known_city(self):
        """测试获取已知城市的天气"""
        api = WeatherAPI()
        weather = api.get_weather("北京")

        assert "temperature" in weather
        assert "condition" in weather
        assert "humidity" in weather
        assert "wind_speed" in weather
        assert weather["condition"] == "晴"

    def test_get_weather_unknown_city(self):
        """测试获取未知城市的天气（应该返回默认值）"""
        api = WeatherAPI()
        weather = api.get_weather("未知城市")

        assert "temperature" in weather
        assert weather["condition"] == "未知"

    def test_get_supported_cities(self):
        """测试获取支持的城市列表"""
        api = WeatherAPI()
        cities = api.get_supported_cities()

        assert isinstance(cities, list)
        assert len(cities) >= 4  # 北京、上海、广州、深圳
        assert "北京" in cities
        assert "上海" in cities


@pytest.mark.asyncio
class TestMCPTools:
    """测试MCP工具功能"""

    async def test_get_weather_tool_valid_city(self):
        """测试天气工具 - 有效城市"""
        result = await handle_call_tool("get_weather", {"city": "北京"})

        assert len(result) == 1
        assert result[0].type == "text"
        content = result[0].text
        assert "北京" in content
        assert "温度" in content
        assert "天气" in content

    async def test_get_weather_tool_empty_city(self):
        """测试天气工具 - 空城市参数"""
        result = await handle_call_tool("get_weather", {})

        assert len(result) == 1
        assert "错误：请提供城市名称" in result[0].text

    async def test_get_supported_cities_tool(self):
        """测试支持城市列表工具"""
        result = await handle_call_tool("get_supported_cities", {})

        assert len(result) == 1
        assert "支持查询天气的城市" in result[0].text
        assert "北京" in result[0].text
        assert "上海" in result[0].text

    async def test_unknown_tool(self):
        """测试未知工具"""
        result = await handle_call_tool("unknown_tool", {})

        assert len(result) == 1
        assert "错误：未知工具" in result[0].text


def test_weather_api_initialization():
    """测试天气API初始化"""
    api = WeatherAPI()
    assert hasattr(api, 'get_weather')
    assert hasattr(api, 'get_supported_cities')


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
