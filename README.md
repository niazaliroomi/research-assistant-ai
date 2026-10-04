# 🔬 Multi-Agent Research Assistant

A modular research assistant built with:

- Streamlit
- CrewAI
- Groq `openai/gpt-oss-120b`
- Custom CrewAI tools
- Wikipedia
- DuckDuckGo HTML search
- arXiv
- Crossref

## Agents

1. Research Director
2. Web Research Specialist
3. Academic Research Specialist
4. Research Fact Checker
5. Senior Research Synthesizer

## Project structure

```text
research-multi-agent/
├── app.py
├── crew.py
├── llm_config.py
├── requirements.txt
├── runtime.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── agents/
├── tasks/
└── tools/
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all files while preserving the folder structure.
3. Go to Streamlit Community Cloud.
4. Create a new app.
5. Select your GitHub repository and branch.
6. Set the main file to `app.py`.
7. Use Python 3.12 if asked.
8. In Advanced settings → Secrets, add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

9. Deploy.

Never commit your real Groq API key to GitHub.

## Important

The research tools use public web APIs/pages. Search engines and public websites can change their HTML or availability, so the tool layer is deliberately isolated in `tools/` for easy maintenance.
