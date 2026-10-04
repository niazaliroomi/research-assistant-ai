from crewai import Agent
from tools.search_tools import web_search, wikipedia_search


def create_web_researcher(llm):
    return Agent(
        role="Web Researcher",
        goal="Collect current, relevant information and source links from the web.",
        backstory=(
            "You are an expert online researcher. You find reliable, recent sources, "
            "extract key facts, and always keep the source URL next to each fact."
        ),
        llm=llm,
        tools=[web_search, wikipedia_search],
        allow_delegation=False,
        verbose=False,
        max_iter=4,
    )
