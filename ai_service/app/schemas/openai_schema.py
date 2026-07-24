from pydantic import BaseModel
from datetime import datetime

class OpenAIRequest(BaseModel):
    message:str

class OpenAIResponse(BaseModel):
    message:str
    time: datetime