from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any

# 导入LLM客户端（需要根据实际路径调整）
try:
    from week1.llm_client import chat
except ImportError:
    # 如果在不同环境中运行，提供备选方案
    def chat(model, messages, options=None):
        # Mock implementation for testing
        return type('MockResponse', (), {'message': type('MockMessage', (), {'content': 'Mock response'})()})()

from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    """使用LLM进行行动项提取"""
    # TODO: 实现LLM驱动的行动项提取
    # 提示：使用结构化输出（JSON数组）来获取行动项列表

    system_prompt = """
    你是一个专业的行动项提取助手。从用户提供的笔记和会议记录中提取具体的、可执行的行动项。

    请分析文本内容，识别出需要采取的具体行动、任务或待办事项。

    输出格式要求：
    - 返回一个JSON数组，包含所有提取的行动项
    - 每个行动项应该是具体的、可执行的任务描述
    - 不要包含重复的项目
    - 只提取真正需要执行的行动，不要包含事实陈述

    示例输入："明天开会讨论项目进展，需要准备演示材料。"
    示例输出：["准备项目演示材料", "组织项目进展会议"]
    """

    try:
        response = chat(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请从以下文本中提取行动项：\n\n{text}"}
            ],
            options={"temperature": 0.3}
        )

        # 解析JSON响应
        content = response.message.content.strip()
        if content.startswith('[') and content.endswith(']'):
            try:
                items = json.loads(content)
                if isinstance(items, list):
                    return [str(item).strip() for item in items if item]
            except json.JSONDecodeError:
                pass

        # 如果JSON解析失败，回退到启发式方法
        return extract_action_items(text)

    except Exception as e:
        print(f"LLM提取失败: {e}")
        # 回退到启发式方法
        return extract_action_items(text)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
