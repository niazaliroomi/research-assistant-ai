from crewai import Task


def create_web_research_task(agent, topic: str, planning_task) -> Task:
    return Task(
        description=f"""
Investigate this research question:

{topic}

First use the research plan supplied in the previous task.

You MUST use your assigned research tools. Search multiple relevant "
web queries rather than relying on the model's memory.

Collect:
- Important factual background.
- Recent or relevant developments when applicable.
- Information from authoritative or primary web sources when available.
- Source titles and URLs.
- Evidence supporting important claims.

Do not invent URLs, publications, statistics, or quotations.
Clearly mark information that could not be independently verified.
""",
        expected_output=(
            "A structured web research dossier containing findings, "
            "source titles, URLs, and evidence for important claims."
        ),
        agent=agent,
        context=[planning_task],
    )
