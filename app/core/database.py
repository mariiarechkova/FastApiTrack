from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Creating an asynchronous PostgreSQL engine
engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

# Creating a session factory (to make queries to the database)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


# The base class for all models
class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
