from typing import Type
from urllib.parse import quote_plus
import re
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class WebSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The web research query to search for."
    )


class WebSearchTool(BaseTool):
    name: str = "Web Search Tool"
    description: str = (
        "Search the public web for information relevant to a research "
        "question. Returns result titles, snippets, and URLs. Use it for "
        "current or general web research."
    )
    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        url = "https://html.duckduckgo.com/html/?q=" + quote_plus(query)

        try:
            response = requests.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (ResearchMultiAgent/1.0; "
                        "+https://streamlit.io)"
                    )
                },
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            return f"Web search failed: {exc}"

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for item in soup.select(".result")[:8]:
            title_el = item.select_one(".result__title")
            link_el = item.select_one(".result__a")
            snippet_el = item.select_one(".result__snippet")

            if not link_el:
                continue

            title = (
                title_el.get_text(" ", strip=True)
                if title_el
                else link_el.get_text(" ", strip=True)
            )
            link = link_el.get("href", "")
            snippet = (
                snippet_el.get_text(" ", strip=True)
                if snippet_el
                else ""
            )

            results.append(
                f"Title: {title}\n"
                f"URL: {link}\n"
                f"Snippet: {snippet}"
            )

        if not results:
            return "No web search results were returned."

        return "\n\n---\n\n".join(results)
