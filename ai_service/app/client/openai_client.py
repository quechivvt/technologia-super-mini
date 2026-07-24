from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(
    #api_key=settings.OPENAI_API_KEY
    api_key=settings.GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)