from fastapi import status
from datetime import datetime, timezone

from app.core.jwt import decode_access_token
from app.core.exceptions import ApiException
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.cache.blacklist_repository import TokenBlacklistRepository
from app.schemas.auth_request import LoginRequest, RegisterRequest
from app.schemas.auth_response import LoginResponse
from app.schemas.user_response import UserResponse
from app.event.channels import Channels
from app.event.events import UserEvent
from app.event.publisher import RedisPublisher



class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
        token_blacklist_repository: TokenBlacklistRepository,
        publisher : RedisPublisher,
    ):
        self.user_repository = user_repository
        self.token_blacklist_repository = token_blacklist_repository
        self.publisher = publisher

    async def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:

        if await self.user_repository.get_by_username(request.username):
            raise ApiException(
                status.HTTP_409_CONFLICT,
                "Username already exists.",
            )

        if await self.user_repository.get_by_email(request.email):
            raise ApiException(
                status.HTTP_409_CONFLICT,
                "Email already exists.",
            )

        user = User(
            username=request.username,
            email=request.email,
            fullname=request.fullname,
            password=hash_password(request.password),
        )

        user = await self.user_repository.create(user)

        await self.publisher.publish(
            Channels.USER,
            {
                "event": UserEvent.REGISTER,
                "user_id": str(user.user_id),
                "username": user.username,
            },
        )

        return UserResponse.model_validate(user)

    async def login(
        self,
        request: LoginRequest,
    ) -> LoginResponse:

        user = await self.user_repository.get_by_username(
            request.username
        )

        if user is None:
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid username or password.",
            )

        if not verify_password(
            request.password,
            user.password,
        ):
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid username or password.",
            )

        access_token = create_access_token(
            str(user.user_id)
        )

        await self.publisher.publish(
            Channels.USER,
            {
                "event": UserEvent.LOGIN,
                "user_id": str(user.user_id),
                "username": user.username,
            },
        )

        return LoginResponse(
            access_token=access_token,
            token_type="Bearer",
        )

    async def logout(
        self,
        token: str,
    ) -> None:

        payload = decode_access_token(token)

        if payload is None:
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid access token.",
            )

        jti = payload["jti"]
        exp = payload["exp"]

        ttl = max(
            0,
            exp - int(datetime.now(timezone.utc).timestamp()),
        )

        await self.token_blacklist_repository.add(
            jti=jti,
            ttl=ttl,
        )

        await self.publisher.publish(
            Channels.USER,
            {
                "event": UserEvent.LOGOUT,
                "user_id": payload["sub"],
            },
        )

    async def get_current_user(
        self,
        token: str,
    ) -> User:

        payload = decode_access_token(token)

        if payload is None:
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid access token.",
            )

        jti = payload["jti"]

        if await self.token_blacklist_repository.exists(jti):
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "Token has been revoked.",
            )

        user_id = payload["sub"]

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise ApiException(
                status.HTTP_401_UNAUTHORIZED,
                "User not found.",
            )

        return user