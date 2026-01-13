#!/usr/bin/env python3
"""
千问模型配置测试脚本
运行此脚本验证千问API配置是否正确
"""

import os
from dotenv import load_dotenv
from llm_client import get_llm_client, LLMClientFactory

def test_qwen_connection():
    """测试千问API连接"""
    print("🔍 测试千问模型配置...")

    # 加载环境变量
    load_dotenv()

    try:
        # 检测配置的提供商
        provider = os.getenv("LLM_PROVIDER", "auto")
        print(f"📋 检测到提供商: {provider}")

        # 创建客户端
        print("🔧 创建LLM客户端...")
        client = LLMClientFactory.create_client(provider)
        print(f"✅ 客户端创建成功: {type(client).__name__}")

        # 测试简单对话
        print("💬 测试API调用...")
        messages = [
            {"role": "user", "content": "请用一句话介绍一下你自己。"}
        ]

        # 根据客户端类型选择合适的模型
        if isinstance(client, client.__class__.__bases__[0].__subclasshook__(type(client))):
            # QwenClient
            model = "qwen-turbo"
        else:
            # OllamaClient
            model = "qwen-turbo"  # fallback

        response = client.chat(model, messages, {"temperature": 0.3})
        print("✅ API调用成功!"        print(f"🤖 模型回复: {response['content'][:100]}...")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n🔧 故障排除建议:")
        print("1. 检查 .env 文件中的 QWEN_API_KEY 是否正确")
        print("2. 确认网络连接正常")
        print("3. 验证API密钥是否有效且有余额")
        print("4. 检查防火墙设置")
        return False

def main():
    """主函数"""
    print("🚀 千问模型配置测试工具")
    print("=" * 50)

    success = test_qwen_connection()

    print("\n" + "=" * 50)
    if success:
        print("🎉 配置测试通过！现在可以运行week1的练习了。")
        print("\n📚 运行示例:")
        print("python k_shot_prompting.py")
        print("python chain_of_thought.py")
        print("...")
    else:
        print("⚠️  配置测试失败，请检查上述错误信息。")
        print("📖 详细说明请参考 README_QWEN.md")

if __name__ == "__main__":
    main()
