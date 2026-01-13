#!/usr/bin/env python3
"""
简单的千问连接测试
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 加载环境变量
load_dotenv()

def test_qwen_connection():
    """测试千问连接"""
    print("🔗 测试千问连接...")

    try:
        # 检查环境变量
        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")

        print(f"API Key: {api_key[:10] if api_key else 'None'}...")
        print(f"Base URL: {base_url}")

        if not api_key:
            print("❌ 未找到 QWEN_API_KEY")
            return False

        # 测试OpenAI客户端
        import openai

        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        print("✅ OpenAI客户端创建成功")

        # 测试简单调用
        print("📡 发送测试请求...")
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            max_tokens=10
        )

        content = response.choices[0].message.content
        print(f"✅ 收到回复: {content}")
        return True

    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_qwen_connection()
    print("\n" + "="*50)
    if success:
        print("🎉 千问连接测试成功！")
    else:
        print("⚠️  千问连接测试失败")
        print("请检查：")
        print("1. API密钥是否正确")
        print("2. 网络连接是否正常")
        print("3. API余额是否充足")
