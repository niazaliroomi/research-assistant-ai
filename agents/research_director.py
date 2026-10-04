from crewai import Agent
from llm_config import get_groq_llm


def create_research_director() -> Agent:
    return Agent(
        role="Research Director",
        goal=(
            "Turn the user's research question into a rigorous research "
            "plan with subquestions, evidence requirements, and source types."
        ),
        backstory=(
            "You are a senior research director. You break difficult "
            "questions into focused research problems and make sure the "
            "research team investigates the topic systematically."
        ),
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
