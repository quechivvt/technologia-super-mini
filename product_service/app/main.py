from fastapi import FastAPI

from app.routers.product_router import router as product_router

import logging

logging.basicConfig(
    level=logging.INFO,
    force=True,
)

app = FastAPI()

app.include_router(product_router)

@app.get("/health")
async def health():
    return {"status": "ok"}




