from loguru import logger
import tortoise

from settings import db_settings


async def run_migrations() -> None:
    """"""

    await tortoise.Tortoise.init(
        db_url=db_settings.connection_string,
        modules={'models': ['models']})

    logger.info("Generating schemas...")
    await tortoise.Tortoise.generate_schemas()
    logger.info("Schemas has been generated")


if __name__ == "__main__":
    tortoise.run_async(run_migrations())
