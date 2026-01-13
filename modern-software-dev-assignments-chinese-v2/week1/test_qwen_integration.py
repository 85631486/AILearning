#!/usr/bin/env python3
"""
千问集成测试脚本
测试阿里云DashScope API集成是否正常工作
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from llm_client import chat, get_llm_client

def test_qwen_basic_chat():
    """测试千问基本对话功能"""
    print("🧪 测试千问基本对话功能...")

    try:
        # 测试基本对话
        messages = [
            {"role": "user", "content": "你好，请介绍一下你自己。"}
        ]

        response = chat(
            model="qwen-turbo",
            messages=messages,
            options={"temperature": 0.3}
        )

        content = response.message.content
        print("✅ 千问API调用成功！"        print(f"🤖 回复内容: {content[:100]}...")

        # 验证回复不为空
        assert content.strip(), "回复内容为空"
        assert len(content) > 10, "回复内容太短"

        return True

    except Exception as e:
        print(f"❌ 千问集成测试失败: {e}")
        return False

def test_qwen_code_generation():
    """测试千问代码生成功能"""
    print("🧪 测试千问代码生成功能...")

    try:
        messages = [
            {"role": "user", "content": "请写一个Python函数，计算斐波那契数列的第n项。要求使用递归实现。"}
        ]

        response = chat(
            model="qwen-plus",
            messages=messages,
            options={"temperature": 0.7}
        )

        content = response.message.content
        print("✅ 代码生成测试成功！"        print(f"📝 生成内容预览: {content[:150]}...")

        # 检查是否包含Python代码
        assert "def" in content or "```python" in content, "未检测到Python代码"

        return True

    except Exception as e:
        print(f"❌ 代码生成测试失败: {e}")
        return False

def test_qwen_error_handling():
    """测试错误处理"""
    print("🧪 测试错误处理...")

    try:
        # 测试无效模型
        response = chat(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "test"}]
        )
        print("⚠️  错误处理测试 - 未按预期失败")
        return False

    except Exception as e:
        print(f"✅ 错误处理正常: {type(e).__name__}")
        return True

def main():
    """主测试函数"""
    print("🚀 千问集成全面测试")
    print("=" * 50)

    # 加载环境变量
    load_dotenv()

    # 检查API密钥
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        print("❌ 未找到 QWEN_API_KEY 环境变量")
        print("请确保 .env 文件存在且包含有效的API密钥")
        return False

    print(f"🔑 检测到API密钥: {api_key[:8]}...")

    # 运行测试
    tests = [
        test_qwen_basic_chat,
        test_qwen_code_generation,
        test_qwen_error_handling
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        if test_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有千问集成测试通过！")
        print("✅ 可以开始使用千问进行开发任务了")
        return True
    else:
        print("⚠️  部分测试失败，请检查配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
