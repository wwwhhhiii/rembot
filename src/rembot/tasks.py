import uuid
import asyncio
from typing import Coroutine, Any
import datetime

import gevent
import uvloop
from loguru import logger
from celery import shared_task
import tortoise

from celery_app import app, REMINDERS_CHECK_INTEVAL_SEC
from db import queries as db_queries
from db.settings import db_settings
from telegram import utils as tg_utils


def _greenlet_compat_async_call(
    coro: Coroutine,
    *,
    loop: asyncio.AbstractEventLoop,
) -> tuple[Any | None, Exception | None]:
    """    
    Execute asyncio coroutine in current greenlet and try not to starve other greenlets.
    """

    async def run() -> Any | None:

        task = loop.create_task(coro)
        while not task.done():
            await asyncio.sleep(0.2)
            gevent.sleep(0.1)

        try:
            return task.result(), None
        except Exception as exc:
            return None, exc

    res = loop.run_until_complete(run())

    return res


@shared_task
def schedule_upcoming_reminders(timeframe_sec: int) -> None:
    """Schedules reminders that should be dispatched from now to a given time frame"""

    loop = uvloop.new_event_loop()

    res, exc = _greenlet_compat_async_call(
        tortoise.Tortoise.init(
            db_url=db_settings.connection_string,
            modules={'models': ['db.models']}), loop=loop)
    if exc is not None:
        logger.error(f"Error during orm initialization {exc}")
        return

    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=timeframe_sec)
    reminders, exc = _greenlet_compat_async_call(
        db_queries.get_reminders_within_time(start, end), loop=loop)
    if exc is not None:
        logger.error(f"Error during reminders fetching: {exc}")
        ...

    


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    """"""

    sender.add_periodic_task(
        REMINDERS_CHECK_INTEVAL_SEC,
        schedule_upcoming_reminders.s(REMINDERS_CHECK_INTEVAL_SEC))


@shared_task
def dispatch_reminder(reminder_id: uuid.UUID) -> None:
    """"""
    
    logger.debug("Dispatching reminder...")

    loop = uvloop.new_event_loop()

    logger.debug("Init tortoise...")
    
    res, exc = _greenlet_compat_async_call(
        tortoise.Tortoise.init(
            db_url=db_settings.connection_string,
            modules={'models': ['db.models']}), loop=loop)
    if exc is not None:
        logger.error(f"Error during orm initialization {exc}")
        return

    logger.debug("Initialized tortoise")

    reminder, exc = _greenlet_compat_async_call(
        db_queries.get_reminder(reminder_id), loop=loop)
    if exc is not None:
        logger.error(f"Error during reminder retrieval: {exc}")
        return
        ...  # TODO

    logger.debug(f"Got reminder from db: {reminder}")

    user_id = ...

    status, exc = _greenlet_compat_async_call(
        tg_utils.send_reminders_to_users(user_id), loop=loop)
    if exc is not None:
        logger.error(f"Error during reminder dispatching: {exc}")
        return
        ...  # TODO
    if status != True:
        logger.error(f"Unsuccessfull reminder dispatch request ({status.value})")
        return
        ...  # TODO

    reminder = _greenlet_compat_async_call(
        db_queries.delete_reminder(reminder_id), loop=loop)
    if reminder is None:
        logger.warning(f"Tried to delete unexisting reminder: {reminder_id}")

    logger.debug("Reminder dispatched")
