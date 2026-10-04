from crewai import Agent


def create_synthesizer(llm):
    return Agent(
        role="Research Synthesizer",
        goal="Write a clear, well-structured final research report from the verified findings.",
        backstory=(
            "You are an expert technical writer. You combine findings into a readable report, "
            "keep only verified claims, and cite sources with links."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=False,
        max_iter=3,
    )
