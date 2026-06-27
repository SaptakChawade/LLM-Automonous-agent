"""
Tests for LLM Autonomous Agent tools (no API key needed)
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.calculator import safe_calculate
from tools.code_executor import execute_python
from tools.file_handler import read_file, write_file
from memory.memory_store import MemoryStore


# ─── Calculator Tests ────────────────────────────────────────────
class TestCalculator:
    def test_basic_arithmetic(self):
        assert safe_calculate("2 + 2") == "4"

    def test_multiplication(self):
        assert safe_calculate("6 * 7") == "42"

    def test_power(self):
        assert safe_calculate("2 ** 10") == "1024"

    def test_sqrt(self):
        assert safe_calculate("sqrt(144)") == "12.0"

    def test_division_by_zero(self):
        result = safe_calculate("1 / 0")
        assert "zero" in result.lower()

    def test_float(self):
        result = safe_calculate("1 / 3")
        assert "0.333" in result


# ─── Code Executor Tests ─────────────────────────────────────────
class TestCodeExecutor:
    def test_simple_print(self):
        result = execute_python("print('hello world')")
        assert "hello world" in result

    def test_loop(self):
        result = execute_python("for i in range(3): print(i)")
        assert "0" in result and "2" in result

    def test_blocked_import_os(self):
        result = execute_python("import os; os.listdir('.')")
        assert "Blocked" in result or "❌" in result

    def test_no_output(self):
        result = execute_python("x = 1 + 1")
        assert "successfully" in result.lower()

    def test_syntax_error(self):
        result = execute_python("def broken(:")
        assert "Error" in result


# ─── File Handler Tests ──────────────────────────────────────────
class TestFileHandler:
    def test_write_and_read(self):
        write_result = write_file("test_output.txt|Hello from test!")
        assert "Saved" in write_result or "✅" in write_result

        read_result = read_file("test_output.txt")
        assert "Hello from test!" in read_result

    def test_read_missing_file(self):
        result = read_file("nonexistent_file_xyz.txt")
        assert "not found" in result.lower()

    def test_write_invalid_format(self):
        result = write_file("no_pipe_here")
        assert "Error" in result or "format" in result.lower()


# ─── Memory Store Tests ──────────────────────────────────────────
class TestMemoryStore:
    def test_save_and_retrieve(self):
        store = MemoryStore()
        store.save("test task", "test response")
        recent = store.get_recent(1)
        assert len(recent) >= 1
        assert recent[-1]["task"] == "test task"

    def test_clear(self):
        store = MemoryStore()
        store.save("another task", "another response")
        store.clear()
        assert store.get_recent() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
