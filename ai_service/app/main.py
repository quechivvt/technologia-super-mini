from fastapi import FastAPI
from app.routers.openai_router import router as openai_router

app = FastAPI()
app.include_router(openai_router)