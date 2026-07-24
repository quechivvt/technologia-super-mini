from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_auth_service
from app.schemas.auth_request import LoginRequest, RegisterRequest
from app.schemas.auth_response import LoginResponse
from app.schemas.user_response import UserResponse
from app.services.auth_service import AuthService
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security import bearer_scheme

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register(request)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(request)

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: AuthService = Depends(get_auth_service),
):
    token = credentials.credentials
    await service.logout(token)

    return {
        "message": "Logout successfully."
    }