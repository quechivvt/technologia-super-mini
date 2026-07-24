import logging

from app.cache.cache_keys import TokenBlacklistKey
from app.cache.cache_repository import CacheRepository

logger = logging.getLogger(__name__)


class TokenBlacklistRepository:

    def __init__(
        self,
        cache_repository: CacheRepository,
    ):
        self.cache_repository = cache_repository

    async def add(
        self,
        jti: str,
        ttl: int,
    ) -> None:
        logger.info("🚫 Add token to blacklist | jti=%s", jti)

        await self.cache_repository.set(
            key=TokenBlacklistKey.blacklist(jti),
            value="1",
            ttl=ttl,
        )

    async def exists(
        self,
        jti: str,
    ) -> bool:
        logger.info("🔍 Check blacklist | jti=%s", jti)

        return await self.cache_repository.exists(
            TokenBlacklistKey.blacklist(jti),
        )