import json

from redis.asyncio import Redis


class RedisPublisher:

    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def publish(
        self,
        channel: str,
        message: dict,
    ):
        await self.redis.publish(
            channel,
            json.dumps(message),
        )