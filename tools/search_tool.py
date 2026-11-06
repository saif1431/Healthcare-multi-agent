from langchain_tavily import TavilySearch
from config import TAVILY_API_KEY


tavily_search = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=1,
    topic="news"
)


def search_healthcare_news(query: str) -> list[dict[str, str]]:
    """Return one compact healthcare news result for the research agent."""
    response = tavily_search.invoke({"query": query})
    results = response.get("results", []) if isinstance(response, dict) else []

    return [
        {
            "title": str(result.get("title", "")),
            "url": str(result.get("url", "")),
            "content": str(result.get("content", ""))[:1200],
        }
        for result in results[:1]
    ]