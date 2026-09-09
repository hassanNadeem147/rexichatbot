from sqlalchemy import  select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.usermodel import UserModel
async def get_user_by_username(session:AsyncSession,username:str) -> UserModel | None:
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    return result.scalar_one_or_none()
async def get_user_by_email(session: AsyncSession,email: str) -> UserModel | None:
    result = await session.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one_or_none() 
async def create_user(session: AsyncSession, user: UserModel) -> UserModel:
    result = await session.execute(select(UserModel).where(UserModel.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise ValueError("Username already exists")
    result = await session.execute(select(UserModel).where(UserModel.email == user.email))
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise ValueError("Email already exists")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
