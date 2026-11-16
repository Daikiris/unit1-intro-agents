"""Que es una Tool: descripcion textual + callable + argumentos tipados."""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]
    arguments: list[tuple[str, str]]
    outputs: str

    def to_string(self) -> str:
        args = ", ".join(f"{n}: {t}" for n, t in self.arguments)
        return (
            f"Tool Name: {self.name}, Description: {self.description}, "
            f"Arguments: {args}, Outputs: {self.outputs}"
        )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)


def _type_name(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty:
        return "Any"
    return getattr(annotation, "__name__", str(annotation))


def tool(func: Callable[..., Any]) -> Tool:
    """Convierte una funcion con type hints y docstring en un Tool."""
    sig = inspect.signature(func)
    arguments = [(p.name, _type_name(p.annotation)) for p in sig.parameters.values()]
    outputs = (
        "No return annotation"
        if sig.return_annotation is inspect.Signature.empty
        else _type_name(sig.return_annotation)
    )
    description = inspect.getdoc(func) or "No description provided."
    return Tool(func.__name__, description, func, arguments, outputs)


@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def tools_to_prompt(tools: list[Tool]) -> str:
    """Bloque de texto que se pega en el system prompt."""
    return "\n".join(f"- {t.to_string()}" for t in tools)


if __name__ == "__main__":
    print(calculator.to_string())
    print(calculator(6, 7))