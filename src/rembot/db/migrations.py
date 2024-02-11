import tortoise
from loguru import logger


async def init_db() -> None:
    """"""

    await tortoise.Tortoise.init()  # TODO
    await tortoise.Tortoise.generate_schemas()


if __name__ == "__main__":
    tortoise.run_async(init_db())
