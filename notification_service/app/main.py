from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.subscribers.redis_subscriber import RedisSubscriber


subscriber = RedisSubscriber()

import logging

logging.basicConfig(
    level=logging.INFO,
    force=True,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    await subscriber.start()

    yield

    await subscriber.stop()


app = FastAPI(
    title="Notification Service",
    lifespan=lifespan,
)