<div align="center">

# 🤖 LLM Autonomous Agent

**A multi-tool autonomous AI agent built with LangChain + GPT-4o + ReAct reasoning**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green?logo=chainlink)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple?logo=openai)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/llm-autonomous-agent?style=social)](https://github.com/yourusername/llm-autonomous-agent)

*Give it a task. Watch it think, plan, and execute — autonomously.*

</div>

---

## 📸 Screenshots

### Interactive Mode
![Interactive Mode](screenshots/01_interactive_mode.svg)

### Multi-Step Reasoning
![Multi-Step Reasoning](screenshots/02_multi_step_reasoning.svg)

### Available Tools
![Tools Overview](screenshots/03_tools_overview.svg)

---

## ✨ Features

- **🧠 ReAct Reasoning Loop** — Think → Act → Observe → Repeat until solved
- **🌐 Web Search** — Live internet search via DuckDuckGo (no API key needed)
- **🔢 Calculator** — Safe math expression evaluator with trig, sqrt, log support
- **📁 File I/O** — Read and write files in a sandboxed workspace
- **🐍 Code Executor** — Run Python snippets safely with restricted builtins
- **📖 Wikipedia** — Fetch encyclopedic knowledge from Wikipedia API
- **💾 Persistent Memory** — Conversation history saved to JSON across sessions
- **🔄 Multi-turn Chat** — Context-aware conversations with sliding window memory
- **⚙️ Configurable** — Model, temperature, max iterations via `.env`

---

## 🏗️ Architecture

```
llm-autonomous-agent/
├── main.py                    # Entry point (interactive / single task / demo)
├── requirements.txt
├── .env.example
│
├── agent/
│   └── agent.py               # Core AutonomousAgent class (ReAct loop)
│
├── tools/
│   ├── web_search.py          # DuckDuckGo web search
│   ├── calculator.py          # Safe math evaluator
│   ├── file_handler.py        # File read/write (sandboxed)
│   ├── code_executor.py       # Python snippet executor
│   └── wikipedia.py           # Wikipedia API wrapper
│
├── memory/
│   └── memory_store.py        # JSON-based persistent memory
│
├── config/
│   └── settings.py            # AgentConfig dataclass
│
├── tests/
│   └── test_tools.py          # Unit tests (no API key required)
│
├── workspace/                 # Agent's working directory (auto-created)
└── screenshots/               # Demo screenshots
```

### How It Works

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│         ReAct Agent Loop            │
│                                     │
│  Thought → What do I need to do?   │
│  Action  → Pick the right tool     │
│  Input   → Prepare tool input      │
│  Observe → Get tool result         │
│  Repeat  → Until final answer      │
└─────────────────────────────────────┘
    │
    ▼
Final Answer + Saved to Memory
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/llm-autonomous-agent.git
cd llm-autonomous-agent
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 5 — Run the agent

```bash
python main.py
```

---

## 💻 Usage

### Interactive Mode (default)

```bash
python main.py
```

Chat with the agent in a loop. Special commands:

| Command     | Action                          |
|-------------|----------------------------------|
| `history`   | Show last 5 task/response pairs  |
| `clear`     | Clear conversation memory        |
| `quit`      | Exit the agent                   |

### Single Task Mode

```bash
python main.py --task "Search for the latest AI news and summarize it"
```

### Demo Mode

```bash
python main.py --demo
```

Runs 4 predefined demo tasks showcasing all tools.

### Custom Model

```bash
python main.py --model gpt-4-turbo
```

---

## 🧪 Running Tests

Tests run without an API key — they test tool logic only.

```bash
pip install pytest
pytest tests/ -v
```

Expected output:

```
tests/test_tools.py::TestCalculator::test_basic_arithmetic    PASSED
tests/test_tools.py::TestCalculator::test_sqrt                PASSED
tests/test_tools.py::TestCalculator::test_division_by_zero    PASSED
tests/test_tools.py::TestCodeExecutor::test_simple_print      PASSED
tests/test_tools.py::TestCodeExecutor::test_blocked_import_os PASSED
tests/test_tools.py::TestFileHandler::test_write_and_read     PASSED
tests/test_tools.py::TestMemoryStore::test_save_and_retrieve  PASSED
...
```

---

## 🔧 Configuration

All settings can be controlled via `.env`:

```env
OPENAI_API_KEY=sk-...          # Required
AGENT_MODEL=gpt-4o             # Model to use (default: gpt-4o)
AGENT_TEMPERATURE=0.1          # Creativity 0.0–1.0 (default: 0.1)
AGENT_MAX_ITERATIONS=10        # Max reasoning steps (default: 10)
AGENT_VERBOSE=true             # Show reasoning steps (default: true)
```

---

## 📌 Example Tasks

```bash
# Math
"What is 15% of 847 plus the square root of 289?"

# Research + Save
"Search Wikipedia for Transformer neural networks and save a summary to transformers.txt"

# Web + Code
"Search for the Fibonacci sequence formula, then write Python code to compute the first 10 numbers"

# Multi-step
"Find information about GPT-4, calculate how many parameters it has compared to GPT-3, and write a comparison report"
```

---

## 🛠️ Tech Stack

| Component      | Technology                    |
|----------------|-------------------------------|
| LLM            | OpenAI GPT-4o                 |
| Agent Framework| LangChain 0.3                 |
| Reasoning      | ReAct (Reason + Act)          |
| Web Search     | DuckDuckGo (free, no key)     |
| Memory         | ConversationBufferWindowMemory|
| Persistence    | JSON file store               |
| Tests          | pytest                        |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-tool`
3. Commit your changes: `git commit -m 'Add new tool: weather lookup'`
4. Push to the branch: `git push origin feature/my-new-tool`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ using [LangChain](https://langchain.com) and [OpenAI](https://openai.com)

⭐ Star this repo if you found it useful!

</div>

