
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate API keys
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env file")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing in .env file")
