"""
Calculator Tool - safe math expression evaluator
"""

import math
from langchain.tools import Tool


def safe_calculate(expression: str) -> str:
    """Safely evaluate a math expression."""
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)  # noqa: S307
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Calculation error: {str(e)}"


calculator_tool = Tool(
    name="calculator",
    func=safe_calculate,
    description=(
        "Evaluate mathematical expressions. "
        "Supports basic arithmetic, trigonometry, logarithms, etc. "
        "Input: a valid Python math expression like '2 ** 10' or 'math.sqrt(144)'."
    ),
)
