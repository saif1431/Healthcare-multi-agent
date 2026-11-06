
from langchain.agents import create_agent
from prompts.prompts import FACT_CHECKER_AGENT_PROMPT
from services.llm import create_gemini_model


# 1. Initialize Groq LLM
llm = create_gemini_model()


# 2. Create Fact Checker Agent
fact_checker_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=FACT_CHECKER_AGENT_PROMPT,
    name="healthcare_fact_checker"
)
