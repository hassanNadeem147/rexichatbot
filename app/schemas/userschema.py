from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class UserCreateRequest(BaseModel):
    fullname: str = Field(..., max_length=100)
    username: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=8
    )
class UserLoginRequest(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(
        ...,
        min_length=8,
        max_length=8
    )
class UserResponse(BaseModel):
    id: int
    fullname: str
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class UserLoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    user: UserResponse