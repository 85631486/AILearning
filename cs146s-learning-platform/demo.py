#!/usr/bin/env python3
"""
CS146S 在线学习平台演示脚本
展示主要功能的使用方法
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# 创建会话以保持状态
session = requests.Session()
# 设置JSON请求头
session.headers.update({
    'Content-Type': 'application/json',
    'Accept': 'application/json'
})

def demo_health_check():
    """演示健康检查"""
    print("🏥 健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print("✅ 应用运行正常")
                return True
            else:
                print(f"❌ 应用状态异常: {data}")
                return False
        else:
            print(f"❌ HTTP状态码异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：无法连接到应用服务器")
        print("请确保应用已启动 (运行 python start.py)")
        return False
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def demo_user_registration():
    """演示用户注册"""
    print("\n👤 用户注册...")
    user_data = {
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "demo123456"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            print("✅ 用户注册成功")
            return True
        elif response.status_code == 400:
            data = response.json()
            print(f"⚠️ 注册失败: {data.get('message', '参数错误')}")
            return False
        else:
            print(f"❌ 注册失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.JSONDecodeError:
        print(f"❌ 响应格式错误: {response.text[:100]}")
        return False
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return False

def demo_user_login():
    """演示用户登录"""
    print("\n🔐 用户登录...")
    login_data = {
        "email": "demo@example.com",
        "password": "demo123456"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 登录成功")
                return True
            else:
                print(f"❌ 登录失败: {result.get('message')}")
                return False
        elif response.status_code == 401:
            result = response.json()
            print(f"❌ 登录失败: {result.get('message')}")
            return False
        else:
            print(f"❌ 登录失败: HTTP {response.status_code}")
            return False
    except requests.exceptions.JSONDecodeError:
        print(f"❌ 响应格式错误: {response.text[:100]}")
        return False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False

def demo_get_weeks():
    """演示获取周列表"""
    print("\n📚 获取课程周列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/learning/weeks")
        if response.status_code == 200:
            weeks = response.json().get('weeks', [])
            print(f"✅ 获取到 {len(weeks)} 个课程周")
            if weeks:
                print(f"   第一个周: {weeks[0]['title']}")
            return True
        else:
            print(f"❌ 获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def demo_code_execution():
    """演示代码执行"""
    print("\n💻 代码执行测试...")
    code_data = {
        "code": "print('Hello CS146S!')\nprint(f'2 + 3 = {2 + 3}')"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/exercises/1/execute", json=code_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('result', {}).get('success'):
                print("✅ 代码执行成功")
                print(f"   输出: {result['result'].get('stdout', '').strip()}")
                return True
            else:
                print("❌ 代码执行失败")
                return False
        else:
            print(f"❌ 执行请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主演示函数"""
    print("🚀 CS146S 在线学习平台功能演示")
    print("=" * 50)

    # 健康检查
    if not demo_health_check():
        print("❌ 应用未运行，请先启动应用")
        return

    # 用户注册
    if not demo_user_registration():
        print("⚠️  用户注册失败，可能用户已存在")

    # 用户登录
    if not demo_user_login():
        print("❌ 用户登录失败")
        return

    # 获取周列表
    demo_get_weeks()

    # 代码执行
    demo_code_execution()

    print("\n" + "=" * 50)
    print("🎉 演示完成！")
    print("🌐 访问 http://127.0.0.1:5000 查看完整功能")
    print("📖 查看 README.md 了解更多功能")

if __name__ == "__main__":
    main()
