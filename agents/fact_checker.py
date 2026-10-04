from crewai import Agent
from tools.search_tools import web_search, wikipedia_search


def create_fact_checker(llm):
    return Agent(
        role="Fact Checker",
        goal="Verify the key claims from the research and flag anything weak or unsupported.",
        backstory=(
            "You are a careful fact checker. You cross-check claims against independent sources "
            "and label each one as Verified, Partly verified, or Unverified."
        ),
        llm=llm,
        tools=[web_search, wikipedia_search],
        allow_delegation=False,
        verbose=False,
        max_iter=4,
    )
