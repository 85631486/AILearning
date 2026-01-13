"""
Unified LLM Client for CS146S Learning Platform
Supports Qwen API and mock fallback for development/testing
"""
import os
import time
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM clients"""

    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send chat request and return response"""
        pass


class QwenClient(LLMClient):
    """Qwen client implementation using OpenAI-compatible API"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url or "https://dashscope.aliyuncs.com/api/v1"

        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError("OpenAI package not installed. Install with: pip install openai")
        else:
            self.client = None

    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("Qwen client not properly configured")

        # Set default options
        options = options or {}
        options.setdefault('temperature', 0.7)
        options.setdefault('max_tokens', 2000)

        start_time = time.time()
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **options
        )
        response_time = time.time() - start_time

        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0

        return {
            "content": content,
            "tokens_used": tokens_used,
            "response_time": round(response_time, 2),
            "full_response": response
        }


class MockClient(LLMClient):
    """Mock client for development and testing"""

    def __init__(self, mock_responses: Optional[Dict[str, str]] = None):
        self.mock_responses = mock_responses or {
            "default": "这是一个模拟的AI响应，用于开发和测试环境。在生产环境中，请配置真实的QWEN_API_KEY。",
            "explain": "这是对代码的模拟解释。在生产环境中，AI会提供详细的代码分析。",
            "debug": "这是调试帮助的模拟响应。在生产环境中，AI会分析错误并提供修复建议。",
            "guidance": "这是学习指导的模拟响应。在生产环境中，AI会根据你的进度提供个性化建议。",
            "hint": "这是提示的模拟响应。在生产环境中，AI会提供恰当的线索帮助你解决问题。"
        }
        self.call_count = 0

    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.call_count += 1

        # Determine response type based on the last user message
        last_message = messages[-1]['content'] if messages else ""
        response_key = "default"

        if any(keyword in last_message.lower() for keyword in ["解释", "explain", "what"]):
            response_key = "explain"
        elif any(keyword in last_message.lower() for keyword in ["错误", "debug", "error", "bug"]):
            response_key = "debug"
        elif any(keyword in last_message.lower() for keyword in ["学习", "指导", "guidance", "progress"]):
            response_key = "guidance"
        elif any(keyword in last_message.lower() for keyword in ["提示", "hint", "help"]):
            response_key = "hint"

        # Simulate some processing time
        time.sleep(0.1)

        return {
            "content": f"{self.mock_responses.get(response_key, self.mock_responses['default'])}\n\n[模拟响应 #{self.call_count}]",
            "tokens_used": len(last_message.split()) * 2,  # Rough token estimation
            "response_time": 0.1,
            "full_response": {"mock": True, "call_count": self.call_count}
        }


class LLMClientFactory:
    """Factory for creating LLM clients"""

    @staticmethod
    def create_client(provider: str = "auto", **kwargs) -> LLMClient:
        """
        Create LLM client based on provider
        Args:
            provider: "qwen", "mock", or "auto" (auto-detect based on env vars)
            **kwargs: Additional arguments for client initialization
        """
        if provider == "auto":
            # Auto-detect based on environment variables
            if os.getenv("QWEN_API_KEY"):
                provider = "qwen"
            else:
                provider = "mock"

        if provider == "qwen":
            return QwenClient(**kwargs)
        elif provider == "mock":
            return MockClient(**kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")


# Global client instance
_llm_client: Optional[LLMClient] = None


def get_llm_client(provider: str = "auto", **kwargs) -> LLMClient:
    """Get or create global LLM client instance"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClientFactory.create_client(provider, **kwargs)
    return _llm_client


def chat(model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None, provider: str = "auto") -> Any:
    """
    Unified chat function compatible with existing code
    Returns an object with .message.content attribute for backward compatibility
    """
    client = get_llm_client(provider)
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
