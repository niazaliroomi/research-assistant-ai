from crewai import Agent
from llm_config import get_groq_llm

from tools.wikipedia_tool import WikipediaTool
from tools.web_search_tool import WebSearchTool


def create_web_researcher() -> Agent:
    return Agent(
        role="Web Research Specialist",
        goal=(
            "Find useful, current, and verifiable web-based information "
            "for the research question and identify the sources supporting "
            "important claims."
        ),
        backstory=(
            "You are an investigative web researcher. You search for "
            "relevant information, inspect source pages, compare sources, "
            "and report evidence rather than unsupported assumptions."
        ),
        tools=[
            WebSearchTool(),
            WikipediaTool(),
        ],
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
