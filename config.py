
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate API keys
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in .env file")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing in .env file")
