import sys

import uvloop
from loguru import logger
import loguru

from telegram.settings import bot_settings
from telegram.bot import create_bot, create_dispatcher
from telegram.handlers import router
from db.settings import db_settings


def configure_logging(logger: "loguru.Logger") -> None:
    """Configures application logging"""

    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG" if bot_settings.debug else "INFO",
    )


async def main() -> None:
    """Application entrypoint"""

    configure_logging(logger)
    logger.debug("Running in DEBUG mode...")

    logger.info("Starting app...")

    bot = create_bot(bot_settings.token)
    dispatcher = create_dispatcher(
        include_routers=[
            router,
        ]
    )

    logger.info("App started")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
