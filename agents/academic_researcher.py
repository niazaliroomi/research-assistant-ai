from crewai import Agent
from llm_config import get_groq_llm

from tools.arxiv_tool import ArxivTool
from tools.crossref_tool import CrossrefTool


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal=(
            "Find relevant scholarly literature and extract useful "
            "publication metadata and research findings."
        ),
        backstory=(
            "You are an academic research specialist. You search scholarly "
            "literature, prioritize relevant publications, and distinguish "
            "research evidence from speculation."
        ),
        tools=[
            ArxivTool(),
            CrossrefTool(),
        ],
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
