"""
Unified LLM Client for different model providers
Supports both Ollama and Qwen models
"""
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send chat request and return response"""
        pass


class OllamaClient(LLMClient):
    """Ollama client implementation"""

    def __init__(self):
        try:
            from ollama import chat as ollama_chat
            self.chat_func = ollama_chat
        except ImportError:
            raise ImportError("Ollama package not installed. Install with: pip install ollama")

    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.chat_func(
            model=model,
            messages=messages,
            options=options or {}
        )
        return {
            "content": response.message.content,
            "full_response": response
        }


class QwenClient(LLMClient):
    """Qwen client implementation using DashScope API directly"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.base_url = base_url or os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")

        if not self.api_key:
            raise ValueError("QWEN_API_KEY environment variable not set")

        # 使用requests库直接调用API，避免httpx版本冲突
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("requests package not installed. Install with: pip install requests")

    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """调用千问API进行对话"""

        # 转换消息格式
        dashscope_messages = []
        for msg in messages:
            dashscope_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # 准备请求参数
        parameters = {}
        if options:
            if "temperature" in options:
                parameters["temperature"] = options["temperature"]
            if "max_tokens" in options:
                parameters["max_tokens"] = options["max_tokens"]
            # 默认参数
            parameters.setdefault("temperature", 0.7)
            parameters.setdefault("max_tokens", 1500)

        # DashScope API请求体
        payload = {
            "model": model,
            "input": {
                "messages": dashscope_messages
            },
            "parameters": parameters
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = self.requests.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            if "output" in result and "text" in result["output"]:
                content = result["output"]["text"]
            else:
                content = str(result)

            return {
                "content": content,
                "full_response": result
            }

        except self.requests.exceptions.RequestException as e:
            raise RuntimeError(f"千问API调用失败: {e}")
        except Exception as e:
            raise RuntimeError(f"千问客户端错误: {e}")


class LLMClientFactory:
    """Factory for creating LLM clients"""

    @staticmethod
    def create_client(provider: str = "auto") -> LLMClient:
        """
        Create LLM client based on provider
        Args:
            provider: "ollama", "qwen", or "auto" (auto-detect based on env vars)
        """
        if provider == "auto":
            # Auto-detect based on environment variables
            if os.getenv("QWEN_API_KEY"):
                provider = "qwen"
            elif os.getenv("OLLAMA_HOST"):
                provider = "ollama"
            else:
                # Default to qwen if no specific configuration
                provider = "qwen"

        if provider == "qwen":
            return QwenClient()
        elif provider == "ollama":
            try:
                return OllamaClient()
            except ImportError:
                # Fallback to qwen if ollama is not available
                print("⚠️  Ollama不可用，自动切换到千问")
                return QwenClient()
        else:
            raise ValueError(f"Unknown provider: {provider}")


# Global client instance
_llm_client: Optional[LLMClient] = None

def get_llm_client(provider: str = "auto") -> LLMClient:
    """Get or create global LLM client instance"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClientFactory.create_client(provider)
    return _llm_client

def chat(model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Any:
    """
    Unified chat function compatible with existing ollama.chat calls
    Returns an object with .message.content attribute for backward compatibility
    """
    client = get_llm_client()
    response = client.chat(model, messages, options)

    # Create a mock response object for backward compatibility
    class MockMessage:
        def __init__(self, content: str):
            self.content = content

    class MockResponse:
        def __init__(self, content: str, full_response: Any = None):
            self.message = MockMessage(content)
            self.full_response = full_response

    return MockResponse(response["content"], response.get("full_response"))
