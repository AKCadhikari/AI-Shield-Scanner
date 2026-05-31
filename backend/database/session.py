""" DB session factory and async connection pool """

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker, 
    create_async_engine,
)

from backend.config import settings

# engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=1800,
)

# session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a DB session and guarantees
    rollback on error, close on exit.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
        
async def get_db_dep() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends-compatible wrapper."""
    async with get_db() as session:
        yield session

async def init_db() -> None:
    """Creates all tables — used in dev/test."""
    from backend.database.base import Base
    import backend.models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db() -> None:
    """Dispose engine on application shutdown."""
    await engine.dispose()