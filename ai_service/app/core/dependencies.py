
from app.service.openai_service import OpenAIService
from app.client.openai_client import client

def get_openai_service():
    return OpenAIService(client=client)