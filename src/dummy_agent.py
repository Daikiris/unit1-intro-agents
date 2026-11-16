"""Agente minimo desde cero: ciclo Thought -> Action -> Observation.

Stop and parse: el LLM se detiene antes de inventar la "Observation:";
nosotros parseamos la accion, ejecutamos la tool y anadimos el resultado real.
"""
from __future__ import annotations

import json
import os
import re

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from tool_basics import Tool, tool, tools_to_prompt

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-Coder-32B-Instruct")
client = InferenceClient(model=MODEL_ID, token=os.getenv("HF_TOKEN"))


@tool
def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is sunny with low temperatures."


TOOLS: dict[str, Tool] = {"get_weather": get_weather}

SYSTEM_PROMPT = """Answer the user's question as best you can. You have access to these tools:

{tools}

Use the following format, and always respond with ONE step at a time:

Thought: reason about what to do next.
Action:
```json
{{"action": "tool_name", "action_input": {{"arg": "value"}}}}
```
Observation: (this will be provided to you, never write it yourself)

When you know the final answer, respond with:

Thought: I now know the final answer.
Final Answer: <answer for the user>
"""

ACTION_RE = re.compile(r"Action:\s*```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
FINAL_RE = re.compile(r"Final Answer:\s*(.*)", re.DOTALL)


def parse_action(text: str) -> dict | None:
    m = ACTION_RE.search(text)
    return json.loads(m.group(1)) if m else None


def run_agent(question: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(tools=tools_to_prompt(list(TOOLS.values())))},
        {"role": "user", "content": question},
    ]
    for step in range(1, max_steps + 1):
        out = client.chat.completions.create(
            messages=messages,
            max_tokens=400,
            stop=["Observation:"],
        ).choices[0].message.content

        print(f"\n--- paso {step} ---\n{out}")

        final = FINAL_RE.search(out)
        if final:
            return final.group(1).strip()

        action = parse_action(out)
        if action is None:
            return out.strip()

        tool_fn = TOOLS.get(action["action"])
        if tool_fn is None:
            observation = f"Error: unknown tool '{action['action']}'."
        else:
            try:
                observation = str(tool_fn(**action["action_input"]))
            except Exception as e:
                observation = f"Error running tool: {e}"

        messages.append({"role": "assistant", "content": out})
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Max steps reached without a final answer."


if __name__ == "__main__":
    print("\nRESPUESTA:", run_agent("What's the weather in London?"))