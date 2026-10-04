from crewai import Task


def build_tasks(director, web, academic, checker, synthesizer):
    plan = Task(
        description=(
            "Research question: {topic}\n\n"
            "Create a research plan: 4-6 key sub-questions, the best search keywords for "
            "web and academic sources, and what evidence is needed."
        ),
        expected_output="A concise research plan with sub-questions and keywords.",
        agent=director,
    )

    web_task = Task(
        description=(
            "Using the plan, search the web for information on: {topic}\n"
            "Collect key facts, recent developments, real-world examples, and source URLs. "
            "Use at most 3 searches."
        ),
        expected_output="A bullet list of findings, each with its source URL.",
        agent=web,
        context=[plan],
    )

    academic_task = Task(
        description=(
            "Using the plan, find academic papers relevant to: {topic}\n"
            "Report title, year, authors, link, and the main finding of each paper. "
            "Use at most 2 searches. Only report papers returned by the tools."
        ),
        expected_output="A list of papers with year, link, and key findings.",
        agent=academic,
        context=[plan],
    )

    check_task = Task(
        description=(
            "Review the web and academic findings about: {topic}\n"
            "Pick the 5-8 most important claims and verify them. "
            "Label each Verified, Partly verified, or Unverified, with a short reason."
        ),
        expected_output="A verification table of claims with status and reasons.",
        agent=checker,
        context=[web_task, academic_task],
    )

    final_task = Task(
        description=(
            "Write the final research report on: {topic}\n"
            "Use the verified findings. Structure: Executive Summary, Key Applications/Findings, "
            "Benefits, Limitations and Risks, Future Outlook, Conclusion, Sources (with links). "
            "Do not include claims marked Unverified."
        ),
        expected_output="A complete, well-formatted markdown research report with sources.",
        agent=synthesizer,
        context=[plan, web_task, academic_task, check_task],
    )

    return [plan, web_task, academic_task, check_task, final_task]
