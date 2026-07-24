from uuid import UUID

import jwt
from jwt import InvalidTokenError

from app.core.config import settings
from app.core.exceptions import ApiException


def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload

    except InvalidTokenError:
        raise ApiException(
            status_code=401,
            message="Invalid or expired access token.",
        )


def get_user_id(token: str) -> UUID:
    payload = verify_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise ApiException(
            status_code=401,
            message="Invalid access token.",
        )

    return UUID(user_id)