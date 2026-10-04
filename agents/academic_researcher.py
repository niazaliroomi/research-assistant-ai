from crewai import Agent
from tools.search_tools import arxiv_search, wikipedia_search


def create_academic_researcher(llm):
    return Agent(
        role="Academic Researcher",
        goal="Find and summarize scholarly papers and research findings on the topic.",
        backstory=(
            "You are a research scientist who reads academic literature. "
            "You report paper titles, years, authors, links, and what each paper found. "
            "You never invent papers."
        ),
        llm=llm,
        tools=[arxiv_search, wikipedia_search],
        allow_delegation=False,
        verbose=False,
        max_iter=4,
    )
