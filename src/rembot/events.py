from loguru import logger
import tortoise


async def connect_to_db(conn_str: str) -> None:
    """Sets up database ORM API"""

    await tortoise.Tortoise.init(
        db_url=conn_str,
        modules={'models': ['db.models']})
