"""
Persistent Memory Store using JSON
Saves task/response history across sessions.
"""

import json
import os
from datetime import datetime
from pathlib import Path


MEMORY_FILE = Path("./memory/history.json")


class MemoryStore:
    def __init__(self):
        MEMORY_FILE.parent.mkdir(exist_ok=True)
        if not MEMORY_FILE.exists():
            MEMORY_FILE.write_text(json.dumps([]), encoding="utf-8")

    def _load(self) -> list:
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_all(self, records: list):
        MEMORY_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def save(self, task: str, response: str):
        """Save a task-response pair with timestamp."""
        records = self._load()
        records.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "response": response,
        })
        self._save_all(records[-100:])  # keep last 100 entries

    def get_recent(self, n: int = 5) -> list:
        """Return the n most recent entries."""
        return self._load()[-n:]

    def clear(self):
        """Clear all memory."""
        self._save_all([])
        print("🧹 Memory cleared.")
