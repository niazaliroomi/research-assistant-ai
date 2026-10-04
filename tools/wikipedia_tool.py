from typing import Type
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class WikipediaInput(BaseModel):
    query: str = Field(
        ...,
        description="Topic to search on Wikipedia."
    )


class WikipediaTool(BaseTool):
    name: str = "Wikipedia Research Tool"
    description: str = (
        "Search Wikipedia for background information, definitions, "
        "historical context, and general factual information."
    )
    args_schema: Type[BaseModel] = WikipediaInput

    def _run(self, query: str) -> str:
        api_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 5,
        }

        try:
            response = requests.get(
                api_url,
                params=params,
                headers={"User-Agent": "ResearchMultiAgent/1.0"},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            return f"Wikipedia search failed: {exc}"

        results = data.get("query", {}).get("search", [])

        if not results:
            return "No Wikipedia results found."

        output = []

        for item in results:
            title = item.get("title", "Unknown")
            snippet = item.get("snippet", "")
            page_url = (
                "https://en.wikipedia.org/wiki/"
                + title.replace(" ", "_")
            )

            output.append(
                f"Title: {title}\n"
                f"Snippet: {snippet}\n"
                f"URL: {page_url}"
            )

        return "\n\n---\n\n".join(output)
