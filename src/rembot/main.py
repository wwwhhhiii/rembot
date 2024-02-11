import multiprocessing

import uvloop
from loguru import logger

from settings.bot import bot_settings
from telegram.bot import create_bot, create_dispatcher
from telegram.handlers import router
from celery_app import app


async def main() -> None:
    
    logger.debug("Starting app")

    bot = create_bot(bot_settings.token)
    dispatcher = create_dispatcher(include_routers=[router,])

    logger.info("Starting Celery worker...")
    multiprocessing.Process(target=app.worker_main, args=(["worker", "--loglevel=INFO"],)).start()

    logger.info("Starting polling...")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
