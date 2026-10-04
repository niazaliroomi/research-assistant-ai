import os
import streamlit as st
from crewai import LLM

# Real model ID on Groq and OpenRouter is "openai/gpt-oss-120b".
# CrewAI strips the first "openai/" prefix, so we add it twice.
MODEL = "openai/openai/gpt-oss-120b"


def _secret(name: str, default=None):
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name, default)


def get_llm() -> LLM:
    provider = str(_secret("LLM_PROVIDER", "groq")).lower()

    if provider == "openrouter":
        return LLM(
            model=MODEL,
            base_url="https://openrouter.ai/api/v1",
            api_key=_secret("OPENROUTER_API_KEY"),
            temperature=0.2,
            max_tokens=3000,
        )

    return LLM(
        model=MODEL,
        base_url="https://api.groq.com/openai/v1",
        api_key=_secret("GROQ_API_KEY"),
        temperature=0.2,
        max_tokens=3000,
    )
