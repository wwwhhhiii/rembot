from loguru import logger
import uvloop
from sqlalchemy.ext.asyncio import create_async_engine

from settings import db_settings
from models import Base


async def run_migrations() -> None:
    engine = create_async_engine(db_settings.connection_string)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvloop.run(run_migrations())
