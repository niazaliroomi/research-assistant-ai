from crewai import Task


def create_synthesis_task(
    agent,
    topic: str,
    planning_task,
    web_task,
    academic_task,
    fact_check_task,
) -> Task:
    return Task(
        description=f"""
Write the final research report for:

{topic}

Use all previous task outputs supplied as context.

The report MUST contain:

# Executive Summary
# Introduction
# Research Findings
# Academic Evidence
# Web Evidence
# Conflicting or Uncertain Findings
# Limitations
# Conclusion
# Sources

Requirements:
- Synthesize rather than merely copy the research notes.
- Do not invent facts, statistics, papers, URLs, DOI numbers, or quotations.
- Preserve source URLs and identifiers supplied by the researchers.
- Clearly distinguish evidence from interpretation.
- If sources disagree, explain the disagreement rather than hiding it.
- If evidence is weak or incomplete, say so.
- Do not claim that a source supports a statement unless the research notes
  provide evidence for that connection.
- The Sources section should contain only sources that actually appeared
  in the research outputs.
""",
        expected_output=(
            "A polished research report with an executive summary, findings, "
            "academic and web evidence, uncertainty, limitations, conclusion, "
            "and a source list containing URLs or identifiers."
        ),
        agent=agent,
        context=[
            planning_task,
            web_task,
            academic_task,
            fact_check_task,
        ],
    )
