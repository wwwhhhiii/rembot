import asyncio
import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from db.settings import db_settings

engine = create_async_engine(db_settings.connection_string)
session_factory = async_sessionmaker(engine)


@contextlib.asynccontextmanager
async def async_scoped_session_factory() -> AsyncIterator[AsyncSession]:
    """Used in tasks to dispose sessions explicitly."""

    scoped_session = async_scoped_session(
        session_factory,
        scopefunc=asyncio.current_task,
    )

    try:
        async with scoped_session() as session:
            yield session
    finally:
        await scoped_session.remove()
