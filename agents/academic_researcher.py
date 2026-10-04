from crewai import Agent
from llm_config import get_groq_llm

from tools.arxiv_tool import ArxivTool
from tools.crossref_tool import CrossrefTool


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal=(
            "Find high-quality academic papers, scholarly sources, "
            "and research evidence relevant to the research question."
        ),
        backstory=(
            "You are an experienced academic researcher specializing "
            "in finding and evaluating scholarly literature. You search "
            "academic sources, identify relevant papers, compare findings, "
            "and provide evidence-based research insights."
        ),
        tools=[
            ArxivTool(),
            CrossrefTool(),
        ],
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
