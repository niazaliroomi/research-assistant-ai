from crewai import Agent


def create_research_director(llm):
    return Agent(
        role="Research Director",
        goal="Break the research question into a clear, focused investigation plan.",
        backstory=(
            "You are a senior research lead who designs investigations. "
            "You define key sub-questions, search keywords, and what evidence is needed."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=3,
    )
