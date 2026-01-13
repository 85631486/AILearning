#!/usr/bin/env python3
"""
测试千问模型配置和连接
"""

import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.utils.llm_client import LLMClientFactory

def test_qwen_config():
    """测试千问配置"""
    print("\n" + "="*60)
    print("🧪 测试千问模型配置")
    print("="*60 + "\n")
    
    app = create_app()
    
    with app.app_context():
        # 读取配置
        api_key = app.config.get('QWEN_API_KEY')
        base_url = app.config.get('QWEN_BASE_URL')
        model = app.config.get('QWEN_MODEL')
        mock_mode = app.config.get('QWEN_MOCK_MODE')
        
        print("📋 配置信息:")
        print(f"  - API密钥: {'已配置' if api_key else '未配置（将使用Mock模式）'}")
        print(f"  - 基础URL: {base_url}")
        print(f"  - 模型名称: {model}")
        print(f"  - Mock模式: {'启用' if mock_mode else '禁用'}")
        print()
        
        # 创建客户端
        print("🔧 创建LLM客户端...")
        try:
            if api_key and not mock_mode:
                client = LLMClientFactory.create_client(
                    "qwen",
                    api_key=api_key,
                    base_url=base_url
                )
                print("✅ 千问客户端创建成功")
                client_type = "qwen"
            else:
                client = LLMClientFactory.create_client("mock")
                print("✅ Mock客户端创建成功（用于开发测试）")
                client_type = "mock"
        except Exception as e:
            print(f"❌ 客户端创建失败: {e}")
            return False
        
        # 测试对话
        print("\n💬 测试AI对话...")
        try:
            response = client.chat(
                model=model,
                messages=[
                    {"role": "user", "content": "你好，请简单介绍一下你自己。"}
                ],
                options={
                    'max_tokens': 200,
                    'temperature': 0.7
                }
            )
            
            print(f"✅ 对话测试成功")
            print(f"\n📝 AI响应:")
            print(f"  {response['content']}")
            print(f"\n📊 响应信息:")
            print(f"  - 使用token: {response.get('tokens_used', 'N/A')}")
            print(f"  - 响应时间: {response.get('response_time', 'N/A')}秒")
            print(f"  - 客户端类型: {client_type}")
            
        except Exception as e:
            print(f"❌ 对话测试失败: {e}")
            return False
        
        print("\n" + "="*60)
        print("✅ 千问模型配置测试通过！")
        print("="*60 + "\n")
        
        if client_type == "mock":
            print("💡 提示: 当前使用Mock模式")
            print("   要使用真实的千问API，请配置以下环境变量:")
            print("   - QWEN_API_KEY=你的千问API密钥")
            print("   - QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1")
            print("   - QWEN_MODEL=qwen-turbo (或其他模型)")
            print("\n   获取API密钥: https://dashscope.aliyuncs.com/")
            print()
        
        return True


def test_model_configuration():
    """测试模型可配置性"""
    print("\n" + "="*60)
    print("🔧 测试模型可配置性")
    print("="*60 + "\n")
    
    # 测试不同的模型配置
    models = [
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "qwen-long"
    ]
    
    print("📋 支持的千问模型:")
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model}")
    
    print("\n💡 配置方法:")
    print("  在 .env 文件中设置: QWEN_MODEL=qwen-turbo")
    print("  或通过环境变量: export QWEN_MODEL=qwen-plus")
    print()
    
    print("="*60 + "\n")


if __name__ == "__main__":
    success = test_qwen_config()
    test_model_configuration()
    
    sys.exit(0 if success else 1)
