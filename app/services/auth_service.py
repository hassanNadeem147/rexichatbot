from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.database.models.usermodel import UserModel
from app.schemas.userschema import UserCreateRequest
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
async def register_user(
    session: AsyncSession,
    user_data: UserCreateRequest
) -> UserModel:
    existing_username = await get_user_by_username(
        session,
        user_data.username
    )
    if existing_username:
        raise ValueError("Username already exists")
    existing_email = await get_user_by_email(
        session,
        user_data.email
    )
    if existing_email:
        raise ValueError("Email already exists")
    hashed_password = hash_password(
        user_data.password
    )
    new_user = UserModel(
        fullname=user_data.fullname,
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    return await create_user(
        session,
        new_user
    )
async def login_user(
    session: AsyncSession,
    username: str,
    password: str
) -> tuple[UserModel, str]:
    user = await get_user_by_username(
        session,
        username
    )
    if not user:
        raise ValueError(
            "Invalid username or password"
        )
    if not verify_password(
        password,
        user.password
    ):
        raise ValueError(
            "Invalid username or password"
        )
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
        }
    )
    return user, access_token