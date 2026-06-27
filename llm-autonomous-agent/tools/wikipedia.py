"""
Wikipedia Tool - fetch summaries from Wikipedia
"""

from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper


wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=2000)


def search_wikipedia(query: str) -> str:
    """Search Wikipedia for a topic summary."""
    try:
        result = wiki.run(query)
        return result if result else "No Wikipedia article found."
    except Exception as e:
        return f"Wikipedia error: {str(e)}"


wikipedia_tool = Tool(
    name="wikipedia",
    func=search_wikipedia,
    description=(
        "Look up factual information, history, science, or definitions on Wikipedia. "
        "Best for encyclopedic knowledge. Input: a topic or concept name."
    ),
)
