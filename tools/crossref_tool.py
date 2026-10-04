from typing import Type
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class CrossrefInput(BaseModel):
    query: str = Field(
        ...,
        description="Academic research topic to search in Crossref."
    )


class CrossrefTool(BaseTool):
    name: str = "Crossref Academic Search Tool"
    description: str = (
        "Search Crossref for scholarly publications and metadata such "
        "as titles, authors, dates, and DOI identifiers."
    )
    args_schema: Type[BaseModel] = CrossrefInput

    def _run(self, query: str) -> str:
        url = "https://api.crossref.org/works"

        params = {
            "query.bibliographic": query,
            "rows": 8,
            "select": (
                "DOI,title,author,published,created,URL,"
                "container-title,type"
            ),
        }

        try:
            response = requests.get(
                url,
                params=params,
                headers={"User-Agent": "ResearchMultiAgent/1.0"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            return f"Crossref search failed: {exc}"

        items = data.get("message", {}).get("items", [])

        if not items:
            return "No Crossref results found."

        results = []

        for item in items:
            titles = item.get("title") or ["Unknown title"]
            title = titles[0]

            authors = []
            for author in item.get("author", []):
                given = author.get("given", "")
                family = author.get("family", "")
                full_name = " ".join(
                    part for part in [given, family] if part
                ).strip()
                if full_name:
                    authors.append(full_name)

            doi = item.get("DOI", "N/A")
            item_url = item.get("URL", "N/A")
            container = (item.get("container-title") or [""])[0]
            published = item.get("published", {})
            date_parts = published.get("date-parts", [[]])

            results.append(
                f"Title: {title}\n"
                f"Authors: {', '.join(authors) if authors else 'N/A'}\n"
                f"Publication: {container or 'N/A'}\n"
                f"Date: {date_parts[0] if date_parts else 'N/A'}\n"
                f"DOI: {doi}\n"
                f"URL: {item_url}"
            )

        return "\n\n---\n\n".join(results)
