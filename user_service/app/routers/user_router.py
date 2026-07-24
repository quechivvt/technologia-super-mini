from fastapi import APIRouter, Depends
from app.schemas.user_response import UserResponse
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Authentication"],
)

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_profile_me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)