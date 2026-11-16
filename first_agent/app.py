"""Primer agente con smolagents."""
import datetime
import os

import pytz
from dotenv import load_dotenv
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    FinalAnswerTool,
    GradioUI,
    InferenceClientModel,
    tool,
)

load_dotenv()


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Fetch the current local time in a specified timezone.

    Args:
        timezone: A valid timezone name (e.g., 'America/Bogota').
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {now}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {e}"


@tool
def my_custom_tool(arg1: str, arg2: int) -> str:
    """A placeholder tool: replace it with something useful.

    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return f"What magic will you build? ({arg1}, {arg2})"


model = InferenceClientModel(
    model_id=os.getenv("MODEL_ID", "Qwen/Qwen2.5-Coder-32B-Instruct"),
    max_tokens=2096,
    temperature=0.5,
    token=os.getenv("HF_TOKEN"),
)

agent = CodeAgent(
    model=model,
    tools=[
        FinalAnswerTool(),
        DuckDuckGoSearchTool(),
        get_current_time_in_timezone,
        my_custom_tool,
    ],
    max_steps=6,
    verbosity_level=1,
)

if __name__ == "__main__":
    GradioUI(agent).launch()