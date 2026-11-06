
from langchain.agents import create_agent
from prompts.prompts import REPORT_AGENT_PROMPT
from services.llm import create_gemini_model


# 1. Initialize Groq LLM
llm = create_gemini_model()


# 2. Create Report Agent
report_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=REPORT_AGENT_PROMPT,
    name="healthcare_report_agent"
)
