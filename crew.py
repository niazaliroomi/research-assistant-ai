import os

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai import Crew, Process

from llm import get_llm
from agents.research_director import create_research_director
from agents.web_researcher import create_web_researcher
from agents.academic_researcher import create_academic_researcher
from agents.fact_checker import create_fact_checker
from agents.synthesizer import create_synthesizer
from tasks.research_tasks import build_tasks


def run_research(topic: str, task_callback=None) -> str:
    llm = get_llm()

    director = create_research_director(llm)
    web = create_web_researcher(llm)
    academic = create_academic_researcher(llm)
    checker = create_fact_checker(llm)
    synthesizer = create_synthesizer(llm)

    tasks = build_tasks(director, web, academic, checker, synthesizer)

    crew = Crew(
        agents=[director, web, academic, checker, synthesizer],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        max_rpm=20,
        task_callback=task_callback,
    )

    result = crew.kickoff(inputs={"topic": topic})
    return getattr(result, "raw", None) or str(result)
