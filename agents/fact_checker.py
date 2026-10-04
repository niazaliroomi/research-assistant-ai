from crewai import Agent
from llm_config import get_groq_llm

from tools.web_search_tool import WebSearchTool
from tools.wikipedia_tool import WikipediaTool
from tools.arxiv_tool import ArxivTool
from tools.crossref_tool import CrossrefTool


def create_fact_checker() -> Agent:
    return Agent(
        role="Research Fact Checker",
        goal=(
            "Verify important claims, identify contradictions, detect "
            "unsupported statements, and assess whether evidence actually "
            "supports the conclusions being drawn."
        ),
        backstory=(
            "You are a meticulous fact checker. You do not accept claims "
            "just because another agent reported them. You use research "
            "tools to verify important facts and explicitly report uncertainty."
        ),
        tools=[
            WebSearchTool(),
            WikipediaTool(),
            ArxivTool(),
            CrossrefTool(),
        ],
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
