from app.core.config import settings
from datetime import datetime
from zoneinfo import ZoneInfo
from app.schemas.openai_schema import OpenAIResponse
from openai_service import AsyncOpenAI

class OpenAIService:

    def __init__(
        self,
        client: AsyncOpenAI, 
    ):
        self.client = client

    async def chat(self, message:str):
        response = await self.client.chat.completions.create(
            model=settings.GEMINI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        
        message = response.choices[0].message.content or ""
        
        return OpenAIResponse(
            message=message,
            time=datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")),
        )