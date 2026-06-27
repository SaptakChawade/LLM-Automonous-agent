"""
Configuration settings for LLM Autonomous Agent
"""

import os
from dataclasses import dataclass


@dataclass
class AgentConfig:
    # LLM settings
    model: str = "gpt-4o"
    temperature: float = 0.1
    max_tokens: int = 4096

    # Agent behavior
    max_iterations: int = 10
    verbose: bool = True

    # Memory
    memory_window: int = 10  # number of past exchanges to keep

    # Paths
    workspace_dir: str = "./workspace"
    memory_file: str = "./memory/history.json"

    @classmethod
    def from_env(cls) -> "AgentConfig":
        return cls(
            model=os.getenv("AGENT_MODEL", "gpt-4o"),
            temperature=float(os.getenv("AGENT_TEMPERATURE", "0.1")),
            max_iterations=int(os.getenv("AGENT_MAX_ITERATIONS", "10")),
            verbose=os.getenv("AGENT_VERBOSE", "true").lower() == "true",
        )


DEFAULT_CONFIG = AgentConfig()
