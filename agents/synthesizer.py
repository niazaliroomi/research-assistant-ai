from crewai import Agent
from llm_config import get_groq_llm


def create_synthesizer() -> Agent:
    return Agent(
        role="Senior Research Synthesizer",
        goal=(
            "Combine the research team's evidence into a clear, balanced, "
            "well-structured research report with transparent sourcing."
        ),
        backstory=(
            "You are a senior research writer. You synthesize evidence "
            "without inventing facts or citations, distinguish established "
            "findings from uncertainty, and produce reports that are easy "
            "for readers to audit."
        ),
        llm=get_groq_llm(),
        verbose=False,
        allow_delegation=False,
    )
