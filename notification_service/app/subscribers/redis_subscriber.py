import asyncio
import json
import logging

from app.core.redis import redis
from app.handlers.product_handler import ProductHandler
from app.handlers.user_handler import UserHandler

logger = logging.getLogger(__name__)


class RedisSubscriber:

    def __init__(self):
        self.pubsub = redis.pubsub()
        self.task: asyncio.Task | None = None

        self.user_handler = UserHandler()
        self.product_handler = ProductHandler()

    async def start(self):

        await self.pubsub.subscribe(
            "user.events",
            "product.events",
        )

        logger.info("✅ Subscribe channels")

        self.task = asyncio.create_task(
            self.listen()
        )

    async def stop(self):

        if self.task:
            self.task.cancel()

        await self.pubsub.close()

    async def listen(self):

        async for message in self.pubsub.listen():

            if message["type"] != "message":
                continue

            channel = message["channel"]
            data = json.loads(message["data"])

            logger.info(
                "📩 Receive [%s] %s",
                channel,
                data,
            )

            if channel == "user.events":
                await self.user_handler.handle(data)

            elif channel == "product.events":
                await self.product_handler.handle(data)