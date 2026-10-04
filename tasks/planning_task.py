from crewai import Task


def create_planning_task(agent, topic: str) -> Task:
    return Task(
        description=f"""
Research question:

{topic}

Create a rigorous research plan for the team.

Include:
1. The main research question.
2. 4-8 focused subquestions.
3. Key concepts that must be defined.
4. Evidence that should be collected.
5. Which source types should be used.
6. Potential disagreements, limitations, or uncertainty.
7. Search terms that the web and academic researchers should investigate.

Do not write the final report. Produce a practical research blueprint.
""",
        expected_output=(
            "A structured research blueprint containing the main question, "
            "subquestions, evidence requirements, source types, risks, and "
            "recommended search terms."
        ),
        agent=agent,
    )
