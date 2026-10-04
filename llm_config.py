import os
from crewai import LLM


MODEL_NAME = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def get_groq_llm() -> LLM:
    """Return the shared Groq LLM configuration used by every agent."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Add it to Streamlit Cloud Secrets."
        )

    return LLM(
        model=MODEL_NAME,
        base_url=GROQ_BASE_URL,
        api_key=api_key,
        temperature=0.2,
        timeout=120,
        max_tokens=8000,
    )
