from langchain_tavily import TavilySearch
from config import TAVILY_API_KEY



# Initialize Tavily search tool
tavily_search = TavilySearch(
    tavily_api_key=TAVILY_API_KEY,
    max_results=5,
    topic="news"
)

def search_healthcare_news(query: str):
      result = tavily_search.invoke({
            "query": query
      })

      return result