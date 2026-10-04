import re
import xml.etree.ElementTree as ET

import requests
from crewai.tools import tool

HEADERS = {"User-Agent": "research-assistant-ai/1.0 (streamlit app)"}
MAX_CHARS = 3500  # keeps token usage low


def _clip(text: str) -> str:
    return text if len(text) <= MAX_CHARS else text[:MAX_CHARS] + "\n...[truncated]"


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the web and return titles, links and snippets for the query."""
    try:
        from ddgs import DDGS

        results = DDGS().text(query, max_results=6)
        if not results:
            return "No web results found."
        lines = []
        for r in results:
            lines.append(
                f"- {r.get('title', '')}\n  URL: {r.get('href', '')}\n  {r.get('body', '')}"
            )
        return _clip("\n".join(lines))
    except Exception as e:
        return f"Web search failed: {e}"


@tool("Wikipedia Search")
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return article titles, snippets and links."""
    try:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": 4,
                "format": "json",
            },
            headers=HEADERS,
            timeout=20,
        )
        r.raise_for_status()
        items = r.json().get("query", {}).get("search", [])
        if not items:
            return "No Wikipedia results found."
        lines = []
        for it in items:
            title = it["title"]
            snippet = re.sub(r"<[^>]+>", "", it.get("snippet", ""))
            url = "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
            lines.append(f"- {title}\n  URL: {url}\n  {snippet}")
        return _clip("\n".join(lines))
    except Exception as e:
        return f"Wikipedia search failed: {e}"


@tool("arXiv Search")
def arxiv_search(query: str) -> str:
    """Search arXiv for academic papers and return titles, authors, dates, links and abstracts."""
    try:
        r = requests.get(
            "https://export.arxiv.org/api/query",
            params={
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": 5,
                "sortBy": "relevance",
            },
            headers=HEADERS,
            timeout=30,
        )
        r.raise_for_status()
        ns = {"a": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(r.text)
        entries = root.findall("a:entry", ns)
        if not entries:
            return "No arXiv papers found."
        lines = []
        for e in entries:
            title = " ".join((e.findtext("a:title", "", ns) or "").split())
            summary = " ".join((e.findtext("a:summary", "", ns) or "").split())[:500]
            link = e.findtext("a:id", "", ns)
            date = (e.findtext("a:published", "", ns) or "")[:10]
            authors = ", ".join(
                a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)
            )[:150]
            lines.append(
                f"- {title} ({date})\n  Authors: {authors}\n  URL: {link}\n  Abstract: {summary}"
            )
        return _clip("\n".join(lines))
    except Exception as e:
        return f"arXiv search failed: {e}"
