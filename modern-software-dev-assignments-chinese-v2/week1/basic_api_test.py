#!/usr/bin/env python3
"""
使用requests库测试千问API的基本连接
"""

import os
import json
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

def test_qwen_api_direct():
    """直接测试千问API"""
    print("🔗 使用requests直接测试千问API...")

    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        print("❌ 未找到 QWEN_API_KEY")
        return False

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {"role": "user", "content": "Say hello in one word."}
            ]
        },
        "parameters": {
            "temperature": 0.3,
            "max_tokens": 50
        }
    }

    try:
        print("📡 发送API请求...")
        response = requests.post(url, headers=headers, json=data, timeout=30)

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功！")

            # 解析响应
            if "output" in result and "text" in result["output"]:
                content = result["output"]["text"]
                print(f"🤖 回复: {content}")
                return True
            else:
                print(f"📄 完整响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return False
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"📄 错误详情: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 网络连接错误")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    success = test_qwen_api_direct()
    print("\n" + "="*50)
    if success:
        print("🎉 千问API测试成功！")
    else:
        print("⚠️  千问API测试失败")
        print("可能的原因：")
        print("1. API密钥无效或过期")
        print("2. 网络无法访问dashscope.aliyuncs.com")
        print("3. API账户余额不足")
        print("4. 防火墙或代理设置问题")
