from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.cache.blacklist_repository import TokenBlacklistRepository
from app.cache.cache_repository import CacheRepository
from app.services.auth_service import AuthService
from app.core.redis import redis_client
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security import bearer_scheme
from app.models.user import User
from app.event.publisher import RedisPublisher

def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:

    return UserRepository(db)

def get_cache_repository():
    return CacheRepository(redis_client)

def get_token_blacklist_cache(
    cache : CacheRepository = Depends(get_cache_repository)    
):
    return TokenBlacklistRepository(cache)

def get_publisher():
    return RedisPublisher(redis_client)

def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
    token_blacklist_repository = Depends(get_token_blacklist_cache),
    publisher = Depends(get_publisher)

) -> AuthService:

    return AuthService(repository,token_blacklist_repository,publisher)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    return await service.get_current_user(
        credentials.credentials,
    )

