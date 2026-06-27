"""
Web Search Tool using DuckDuckGo (free, no API key needed)
"""

from langchain.tools import Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


search = DuckDuckGoSearchAPIWrapper(max_results=5)


def run_web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    try:
        results = search.run(query)
        return results if results else "No results found."
    except Exception as e:
        return f"Search error: {str(e)}"


web_search_tool = Tool(
    name="web_search",
    func=run_web_search,
    description=(
        "Search the internet for current information. "
        "Use this for recent news, facts, or anything you don't know. "
        "Input: a search query string."
    ),
)
