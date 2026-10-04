from crewai import Crew, Process

from agents.research_director import create_research_director
from agents.web_researcher import create_web_researcher
from agents.academic_researcher import create_academic_researcher
from agents.fact_checker import create_fact_checker
from agents.synthesizer import create_synthesizer

from tasks.planning_task import create_planning_task
from tasks.web_research_task import create_web_research_task
from tasks.academic_research_task import create_academic_research_task
from tasks.fact_check_task import create_fact_check_task
from tasks.synthesis_task import create_synthesis_task


def run_research(topic: str) -> str:
    """Run the complete five-agent research workflow."""

    # Agents
    director = create_research_director()
    web_researcher = create_web_researcher()
    academic_researcher = create_academic_researcher()
    fact_checker = create_fact_checker()
    synthesizer = create_synthesizer()

    # Tasks
    planning_task = create_planning_task(
        director,
        topic,
    )

    web_task = create_web_research_task(
        web_researcher,
        topic,
        planning_task,
    )

    academic_task = create_academic_research_task(
        academic_researcher,
        topic,
        planning_task,
    )

    fact_check_task = create_fact_check_task(
        fact_checker,
        topic,
        web_task,
        academic_task,
    )

    synthesis_task = create_synthesis_task(
        synthesizer,
        topic,
        planning_task,
        web_task,
        academic_task,
        fact_check_task,
    )

    crew = Crew(
        agents=[
            director,
            web_researcher,
            academic_researcher,
            fact_checker,
            synthesizer,
        ],
        tasks=[
            planning_task,
            web_task,
            academic_task,
            fact_check_task,
            synthesis_task,
        ],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()

    # CrewOutput normally exposes .raw. The fallback keeps the app
    # compatible with minor output-object changes.
    final_text = getattr(result, "raw", None)

    if not final_text:
        final_text = str(result)

    return final_text
