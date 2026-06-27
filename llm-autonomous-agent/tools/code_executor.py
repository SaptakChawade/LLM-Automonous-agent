"""
Safe Python Code Executor Tool
Executes sandboxed Python snippets and returns stdout output.
"""

import sys
import io
import traceback
from langchain.tools import Tool


BLOCKED = ["import os", "import subprocess", "import sys", "__import__", "open(", "exec(", "eval("]


def execute_python(code: str) -> str:
    """Execute a Python code snippet safely and return output."""
    code_lower = code.lower()
    for blocked in BLOCKED:
        if blocked.lower() in code_lower:
            return f"❌ Blocked: '{blocked}' is not allowed for security reasons."

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        local_vars = {}
        exec(code, {"__builtins__": {"print": print, "range": range, "len": len,  # noqa: S102
                                      "str": str, "int": int, "float": float,
                                      "list": list, "dict": dict, "tuple": tuple,
                                      "set": set, "sorted": sorted, "enumerate": enumerate,
                                      "zip": zip, "map": map, "filter": filter,
                                      "sum": sum, "min": min, "max": max, "abs": abs,
                                      "round": round, "isinstance": isinstance}},
             local_vars)
        output = sys.stdout.getvalue()
        return output if output else "✅ Code executed successfully (no output)."
    except Exception:
        return f"❌ Error:\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout


code_executor_tool = Tool(
    name="python_executor",
    func=execute_python,
    description=(
        "Execute a Python code snippet and return the printed output. "
        "Useful for data processing, string manipulation, or logic tasks. "
        "Input: valid Python code. No file I/O or OS access allowed."
    ),
)
