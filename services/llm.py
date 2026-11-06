from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_MODEL, GOOGLE_API_KEY


def create_gemini_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0,
        max_output_tokens=1000,
        google_api_key=GOOGLE_API_KEY,
        retries=6,
    )
