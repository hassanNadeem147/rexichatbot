from app.database.base import Base
from app.database.session import engine
from app.database.models.usermodel import UserModel
async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)