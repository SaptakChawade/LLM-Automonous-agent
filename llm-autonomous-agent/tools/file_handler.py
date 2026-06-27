"""
File I/O Tools - Read and write files safely within the workspace
"""

import os
from pathlib import Path
from langchain.tools import Tool

WORKSPACE = Path("./workspace")
WORKSPACE.mkdir(exist_ok=True)


def read_file(filename: str) -> str:
    """Read a file from the workspace."""
    filepath = WORKSPACE / Path(filename).name  # prevent path traversal
    try:
        if not filepath.exists():
            return f"File '{filename}' not found in workspace."
        return filepath.read_text(encoding="utf-8")
    except Exception as e:
        return f"Read error: {str(e)}"


def write_file(input_str: str) -> str:
    """Write content to a file in the workspace.
    Format: 'filename.txt|content here'
    """
    if "|" not in input_str:
        return "Error: Use format 'filename|content'"
    filename, content = input_str.split("|", 1)
    filepath = WORKSPACE / Path(filename.strip()).name

    try:
        filepath.write_text(content.strip(), encoding="utf-8")
        return f"✅ Saved to workspace/{filepath.name} ({len(content)} chars)"
    except Exception as e:
        return f"Write error: {str(e)}"


file_read_tool = Tool(
    name="file_read",
    func=read_file,
    description=(
        "Read a file from the workspace directory. "
        "Input: just the filename, e.g. 'notes.txt'."
    ),
)

file_write_tool = Tool(
    name="file_write",
    func=write_file,
    description=(
        "Write content to a file in the workspace. "
        "Input format: 'filename.txt|content to write'. "
        "Use pipe '|' to separate filename and content."
    ),
)
