import os
import re
from dotenv import load_dotenv
from llm_client import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = ""


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """从详细的推理跟踪中提取最后的'Answer: ...'行。

    - 查找以'Answer:'开头的最后一行（不区分大小写）
    - 当存在数字时，标准化为'Answer: <number>'
    - 如果未检测到数字，则回退到返回匹配的内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """运行最多NUM_RUNS_TIMES次，如果任何输出匹配EXPECTED_OUTPUT则返回True。

    找到匹配时打印"SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"运行测试 {idx + 1} / {NUM_RUNS_TIMES}")
        response = chat(
            model="qwen-plus",  # 使用千问模型代替llama3.1:8b
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"期望输出: {EXPECTED_OUTPUT}")
            print(f"实际输出: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


