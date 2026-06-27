"""
LLM Autonomous Agent - Main Entry Point

Usage:
    python main.py                      # Interactive chat mode
    python main.py --task "your task"   # Single task mode
    python main.py --demo               # Run demo tasks
"""

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Validate API key early
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not set.")
    print("   Create a .env file with: OPENAI_API_KEY=your-key-here")
    sys.exit(1)

from agent.agent import AutonomousAgent


DEMO_TASKS = [
    "What is 15% of 847 plus the square root of 289?",
    "Search Wikipedia for 'Large Language Models' and summarize in 3 bullet points.",
    "Write a Python function that checks if a number is prime, test it with 17, and save the code to 'prime_check.py'.",
    "Search the web for the latest AI news and write a brief summary to 'ai_news.txt'.",
]

BANNER = """
╔══════════════════════════════════════════════════════╗
║         🤖  LLM Autonomous Agent  v1.0               ║
║     Powered by LangChain + GPT-4o + ReAct            ║
║  Tools: Search · Calculator · Files · Code · Wiki    ║
╚══════════════════════════════════════════════════════╝
"""


def run_interactive(agent: AutonomousAgent):
    """Interactive chat loop."""
    print(BANNER)
    print("Type your task below. Commands: 'history', 'clear', 'quit'\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("👋 Goodbye!")
            break
        elif user_input.lower() == "history":
            records = agent.memory_store.get_recent(5)
            if not records:
                print("📭 No history yet.")
            for r in records:
                print(f"\n[{r['timestamp'][:19]}]\n Task: {r['task']}\n Reply: {r['response'][:120]}...")
        elif user_input.lower() == "clear":
            agent.memory_store.clear()
            agent.memory.clear()
        else:
            result = agent.run(user_input)
            print(f"\n🤖 Agent: {result['output']}")
            print(f"   (completed in {result['steps']} step(s))\n")


def run_demo(agent: AutonomousAgent):
    """Run predefined demo tasks."""
    print(BANNER)
    print("🎬 Running demo tasks...\n")
    for i, task in enumerate(DEMO_TASKS, 1):
        print(f"\n{'─'*60}\n📋 Demo Task {i}: {task}")
        result = agent.run(task)
        print(f"\n✅ Result: {result['output']}")


def main():
    parser = argparse.ArgumentParser(description="LLM Autonomous Agent")
    parser.add_argument("--task", type=str, help="Run a single task and exit")
    parser.add_argument("--demo", action="store_true", help="Run demo tasks")
    parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model name")
    parser.add_argument("--verbose", action="store_true", default=True)
    args = parser.parse_args()

    agent = AutonomousAgent(model=args.model, verbose=args.verbose)

    if args.task:
        result = agent.run(args.task)
        print(f"\n✅ Result:\n{result['output']}")
    elif args.demo:
        run_demo(agent)
    else:
        run_interactive(agent)


if __name__ == "__main__":
    main()
