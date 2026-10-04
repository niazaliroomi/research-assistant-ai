import streamlit as st
from crewai import LLM

def get_llm() -> LLM:
    provider = st.secrets.get("LLM_PROVIDER", "groq")

    if provider == "openrouter":
        return LLM(
            model="openai/openai/gpt-oss-120b",
            base_url="https://openrouter.ai/api/v1",
            api_key=st.secrets["OPENROUTER_API_KEY"],
            temperature=0.2,
        )

    return LLM(
        model="openai/openai/gpt-oss-120b",
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets["GROQ_API_KEY"],
        temperature=0.2,
    )
