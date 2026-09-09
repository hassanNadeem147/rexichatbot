from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from app.config.settings import config_database
# Create engine
engine = create_async_engine(
    config_database.DATABASE_URL,
    echo = False
)
# Create Session
AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

async def get_session():
    """Get a database session."""
    async with AsyncSessionLocal() as session:
        yield session