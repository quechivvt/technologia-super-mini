from fastapi import FastAPI
import app.models   

from app.routers.product_router import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/health")
async def health():
    return {"status": "ok"}




