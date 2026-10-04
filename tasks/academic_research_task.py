from crewai import Task


def create_academic_research_task(agent, topic: str, planning_task) -> Task:
    return Task(
        description=f"""
Conduct academic research for:

{topic}

Use the research plan supplied in the previous task.

You MUST use your assigned academic tools, especially arXiv and Crossref.

Find relevant scholarly publications and report:
- Title.
- Authors where available.
- Publication date where available.
- DOI where available.
- Abstract or concise finding.
- URL or identifier.
- Why the publication is relevant.

Do not invent papers, authors, DOI numbers, findings, or citations.
Distinguish established evidence from preliminary research.
""",
        expected_output=(
            "A structured academic literature dossier with relevant papers, "
            "authors, publication metadata, findings, identifiers, and URLs."
        ),
        agent=agent,
        context=[planning_task],
    )

