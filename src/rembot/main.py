import multiprocessing

import uvloop
from loguru import logger

from telegram.settings import bot_settings
from telegram.bot import create_bot, create_dispatcher
from telegram.handlers import router
from db.settings import db_settings
from events import connect_to_db
from celery_app import app


async def main() -> None:
    """Application entrypoint"""
    
    logger.info("Starting app...")

    bot = create_bot(bot_settings.token)
    dispatcher = create_dispatcher(include_routers=[router,])

    logger.info("Starting Celery worker...")
    multiprocessing.Process(
        target=app.worker_main,
        args=(["worker", "--loglevel=INFO"],)).start()
    logger.info("Celery worker started")

    logger.info("Connecting to database...")
    await connect_to_db(db_settings.connection_string)
    logger.info("Database connection established")

    logger.info("App started")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
