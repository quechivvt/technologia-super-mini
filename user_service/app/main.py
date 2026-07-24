from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router
from app.grpc.server import serve

logging.basicConfig(
    level=logging.INFO,
    force=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(serve())

    yield

    grpc_task.cancel()


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
async def health():
    return {"status": "ok"}