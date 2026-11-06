
from tools.search_tool import tavily_search
from tools.scraper_tool import scrape_article

# Check Tavily tool
print("Tavily Tool:", tavily_search.name)
print("Tavily Description:", tavily_search.description)

# Check Scraper function
print("Scraper Function:", scrape_article.__name__)
print("Scraper Description:", scrape_article.__doc__)

# Test Tavily independently
results = tavily_search.invoke({
    "query": "Latest cancer treatment news"
})

print("\n===== TAVILY RESULTS =====")
print(results)
