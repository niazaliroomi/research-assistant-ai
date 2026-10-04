from typing import Type
import urllib.parse
import requests
import xml.etree.ElementTree as ET
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class ArxivInput(BaseModel):
    query: str = Field(
        ...,
        description="Academic topic to search on arXiv."
    )


class ArxivTool(BaseTool):
    name: str = "arXiv Academic Search Tool"
    description: str = (
        "Search arXiv for academic papers. Returns titles, authors, "
        "publication dates, abstracts, and paper URLs."
    )
    args_schema: Type[BaseModel] = ArxivInput

    def _run(self, query: str) -> str:
        base_url = "https://export.arxiv.org/api/query"

        params = {
            "search_query": "all:" + query,
            "start": 0,
            "max_results": 8,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        try:
            response = requests.get(
                base_url,
                params=params,
                headers={"User-Agent": "ResearchMultiAgent/1.0"},
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            return f"arXiv search failed: {exc}"

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as exc:
            return f"Could not parse arXiv response: {exc}"

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []

        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            summary_el = entry.find("atom:summary", ns)
            published_el = entry.find("atom:published", ns)
            id_el = entry.find("atom:id", ns)

            authors = [
                a.findtext("atom:name", default="Unknown", namespaces=ns)
                for a in entry.findall("atom:author", ns)
            ]

            title = (
                title_el.text.strip()
                if title_el is not None and title_el.text
                else "Unknown"
            )
            summary = (
                summary_el.text.strip()
                if summary_el is not None and summary_el.text
                else ""
            )
            published = (
                published_el.text.strip()
                if published_el is not None and published_el.text
                else "Unknown"
            )
            paper_url = (
                id_el.text.strip()
                if id_el is not None and id_el.text
                else "Unknown"
            )

            papers.append(
                f"Title: {title}\n"
                f"Authors: {', '.join(authors)}\n"
                f"Published: {published}\n"
                f"Abstract: {summary}\n"
                f"URL: {paper_url}"
            )

        if not papers:
            return "No arXiv papers found."

        return "\n\n---\n\n".join(papers)

