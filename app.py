import traceback
import streamlit as st

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔬", layout="wide")

from crew import run_research

STEPS = [
    "🧠 Research Director: plan created",
    "🌐 Web Researcher: web findings collected",
    "📚 Academic Researcher: papers collected",
    "✅ Fact Checker: claims verified",
    "📝 Synthesizer: final report written",
]

with st.sidebar:
    st.header("About")
    st.write(
        "This application uses five specialized AI agents to plan, research, "
        "verify, and synthesize a research report."
    )
    st.markdown(
        "**Agents**\n"
        "- Research Director\n- Web Researcher\n- Academic Researcher\n"
        "- Fact Checker\n- Research Synthesizer"
    )
    st.caption("LLM: openai/gpt-oss-120b via Groq")

st.title("🔬 Multi-Agent Research Assistant")
st.caption("CrewAI + Groq GPT-OSS 120B + research tools + Streamlit")

topic = st.text_area(
    "Research question",
    placeholder="e.g. What are the major applications, benefits and limitations of generative AI in cybersecurity?",
    height=100,
)

if st.button("Run research", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research question.")
    else:
        progress = st.empty()
        done = []

        def on_task_done(_output):
            if len(done) < len(STEPS):
                done.append(STEPS[len(done)])
            progress.markdown("\n\n".join(done))

        try:
            with st.spinner("Agents are working. This can take a few minutes..."):
                report = run_research(topic.strip(), task_callback=on_task_done)
            st.session_state["report"] = report
            st.session_state["topic"] = topic.strip()
            progress.empty()
            st.success("Research complete")
        except Exception as e:
            st.error("❌ Research failed")
            st.code(f"{type(e).__name__}: {e}")
            with st.expander("Traceback"):
                st.code(traceback.format_exc())

if "report" in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state["report"])
    st.download_button(
        "Download report (.md)",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.9em;'>"
    "Developed by <b>Niaz Ali Roomi</b> · Multi-Agent Research Assistant"
    "</div>",
    unsafe_allow_html=True,
)
