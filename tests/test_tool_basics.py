import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tool_basics import calculator, tool  # noqa: E402


def test_to_string():
    assert calculator.to_string() == (
        "Tool Name: calculator, Description: Multiply two integers., "
        "Arguments: a: int, b: int, Outputs: int"
    )


def test_callable():
    assert calculator(3, 4) == 12


def test_missing_return_annotation():
    @tool
    def f(x: str):
        """Echo."""
        return x

    assert f.outputs == "No return annotation"