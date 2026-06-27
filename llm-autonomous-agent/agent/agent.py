"""
LLM Autonomous Agent - Core Agent Module
Uses LangChain + OpenAI GPT-4 with ReAct reasoning loop
"""

import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain import hub
from langchain_core.prompts import PromptTemplate

from tools.web_search import web_search_tool
from tools.calculator import calculator_tool
from tools.file_handler import file_read_tool, file_write_tool
from tools.code_executor import code_executor_tool
from tools.wikipedia import wikipedia_tool
from memory.memory_store import MemoryStore


SYSTEM_PROMPT = """You are an autonomous AI agent capable of planning and executing multi-step tasks.
You have access to tools for web search, calculation, file I/O, code execution, and Wikipedia.
Always think step-by-step before acting. Be concise and precise.

Available tools: {tools}
Tool names: {tool_names}

Use this format:
Thought: What do I need to do?
Action: tool_name
Action Input: input to the tool
Observation: result
... (repeat as needed)
Thought: I now have the final answer
Final Answer: your complete answer

Begin!

{chat_history}
Human: {input}
{agent_scratchpad}"""


class AutonomousAgent:
    def __init__(self, model: str = "gpt-4o", temperature: float = 0.1, verbose: bool = True):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.tools = [
            web_search_tool,
            calculator_tool,
            file_read_tool,
            file_write_tool,
            code_executor_tool,
            wikipedia_tool,
        ]

        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=10,
            return_messages=False,
        )

        self.memory_store = MemoryStore()

        prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=verbose,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

    def run(self, task: str) -> dict:
        """Run the agent on a given task and return result + steps."""
        print(f"\n🤖 Agent Task: {task}\n{'='*60}")
        result = self.executor.invoke({"input": task})

        # Save to persistent memory
        self.memory_store.save(task, result["output"])

        return {
            "task": task,
            "output": result["output"],
            "steps": len(result.get("intermediate_steps", [])),
        }

    def chat(self, message: str) -> str:
        """Simple single-turn chat."""
        result = self.run(message)
        return result["output"]
