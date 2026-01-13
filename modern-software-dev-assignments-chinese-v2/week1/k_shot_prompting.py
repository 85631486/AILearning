import os
from dotenv import load_dotenv
from llm_client import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = ""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """运行提示最多NUM_RUNS_TIMES次，如果任何输出匹配EXPECTED_OUTPUT则返回True。

    找到匹配时打印"SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"运行测试 {idx + 1} / {NUM_RUNS_TIMES}")
        response = chat(
            model="qwen-turbo",  # 使用千问模型代替mistral-nemo:12b
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"期望输出: {EXPECTED_OUTPUT}")
            print(f"实际输出: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)