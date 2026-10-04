import os
import streamlit as st

from crew import run_research


st.set_page_config(
    page_title="AI Research Team",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Multi-Agent Research Assistant")
st.caption(
    "CrewAI + Groq GPT-OSS 120B + research tools + Streamlit"
)

with st.sidebar:
    st.header("About")
    st.write(
        "This application uses five specialized AI agents to plan, "
        "research, verify, and synthesize a research report."
    )
    st.markdown(
        """
**Agents**
1. Research Director
2. Web Researcher
3. Academic Researcher
4. Fact Checker
5. Research Synthesizer
        """
    )

    st.divider()
    st.caption("LLM: openai/gpt-oss-120b via Groq")

topic = st.text_area(
    "Research question",
    placeholder=(
        "Example: What are the major applications, benefits, "
        "limitations, and security risks of generative AI in cybersecurity?"
    ),
    height=150,
)

if st.button("🚀 Start Research", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a research question.")
        st.stop()

    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "GROQ_API_KEY is missing. Add it in Streamlit Cloud → "
            "App settings → Secrets."
        )
        st.stop()

    progress = st.status(
        "Research team is working...",
        expanded=True,
    )

    try:
        progress.write("🧠 Research Director: planning the investigation...")
        result = run_research(topic.strip())

        progress.update(
            label="✅ Research completed",
            state="complete",
            expanded=False,
        )

        st.divider()
        st.subheader("📄 Final Research Report")
        st.markdown(result)

        st.download_button(
            "⬇️ Download report as Markdown",
            data=result,
            file_name="research_report.md",
            mime="text/markdown",
        )

    except Exception as exc:
        progress.update(
            label="❌ Research failed",
            state="error",
            expanded=True,
        )
        st.error("The research workflow failed.")
        st.exception(exc)
