from crewai import Task


def create_fact_check_task(agent, topic: str, web_task, academic_task) -> Task:
    return Task(
        description=f"""
Fact-check the research collected for:

{topic}

Use the outputs from the web and academic researchers as evidence to review,
but independently verify important claims with your own tools.

You MUST use at least one of your research tools.

For important claims, classify them as:
- Supported
- Partially supported
- Conflicting evidence
- Unsupported / needs verification

Also identify:
- Contradictions between sources.
- Claims that appear stronger than the evidence.
- Missing citations.
- Source-quality concerns.
- Important limitations.

Do not invent evidence.
""",
        expected_output=(
            "A fact-check report that evaluates important claims, identifies "
            "supporting evidence, contradictions, missing citations, and "
            "uncertainties."
        ),
        agent=agent,
        context=[web_task, academic_task],
    )
