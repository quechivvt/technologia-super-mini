from pydantic import BaseModel,EmailStr
from uuid import UUID


class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    fullname: str

    model_config = {
        "from_attributes": True
    }