import multiprocessing

import uvloop
from loguru import logger

from telegram.settings import bot_settings
from telegram.bot import create_bot, create_dispatcher
from telegram.handlers import router
from db.settings import db_settings


async def main() -> None:
    """Application entrypoint"""
    
    logger.info("Starting app...")

    bot = create_bot(bot_settings.token)
    dispatcher = create_dispatcher(include_routers=[router,])

    logger.info("App started")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
