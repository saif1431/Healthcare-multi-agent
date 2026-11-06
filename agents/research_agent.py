
from langchain.agents import create_agent
from tools.search_tool import search_healthcare_news
from tools.scraper_tool import scrape_article
from prompts.prompts import RESEARCH_AGENT_PROMPT
from services.llm import create_gemini_model


# 1. Initialize Groq LLM
llm = create_gemini_model()


# 2. Register tools
research_tools = [
    search_healthcare_news,
    scrape_article
]


# 3. Create Research Agent
research_agent = create_agent(
    model=llm,
    tools=research_tools,
    system_prompt=RESEARCH_AGENT_PROMPT,
    name="healthcare_research_agent"
)
