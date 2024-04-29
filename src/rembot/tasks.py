import asyncio
import uuid
from typing import Coroutine, Any, Callable, Optional
import datetime
import time

from loguru import logger

from db import queries as db_queries
from db.settings import db_settings
from db.models import DBReminder
from app_models import Reminder
from db.util import async_scoped_session_factory
from telegram import utils as tg_utils


async def execute_periodically(
    func: Callable[..., Any],
    preiod_sec: int,
    *func_args: tuple[Any],
    **func_kwds: dict[str, Any],
) -> None:

    while True:
        await asyncio.sleep(preiod_sec)

        try:
            res = await func(*func_args, **func_kwds)
        except Exception as e:
            logger.error(f"Exception during periodic task execution: {e}")


async def on_reminder_dispatch_cleanup(reminder_id: uuid.UUID) -> Optional[Reminder]:
    """"""

    reminder = await db_queries.delete_reminder(id=reminder_id)

    return reminder


async def dispatch_reminder_after(
    reminder_id: uuid.UUID, after_sec: int
) -> Optional[Reminder]:
    """"""

    await asyncio.sleep(after_sec)
    # TODO load fresh reminder
    reminder = await db_queries.get_reminder(reminder_id)
    if reminder is None:
        return None
    # TODO dispatch
    await tg_utils.send_reminders_to_users(user_id=reminder.user_id)
    reminder = await on_reminder_dispatch_cleanup(reminder.id)

    return reminder


async def schedule_upcoming_reminders(timeframe_sec: int) -> None:
    """Schedules reminders that should be dispatched in a timedelta
    from now to a given time frame.

    This task is intended to be called periodically
    """

    logger.debug(f"Running scheduling task...")

    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=timeframe_sec)

    logger.info(f"Collecting upcoming reminders in a {start}-{end} timeframe...")

    async with async_scoped_session_factory() as session:
        reminders = await db_queries.get_reminders_within_time(session, start, end)

    logger.info(f"Collected {len(reminders)} upcoming reminders")
    logger.debug(f"Scheduling reminders for dispatch...")

    reminder_tasks = []
    for rem in reminders:
        rem_left_sec = int(time.mktime(rem.time.timetuple()) - time.time())
        reminder_tasks.append(
            asyncio.create_task(dispatch_reminder_after(rem.id, rem_left_sec))
        )

    await asyncio.gather(*reminder_tasks)
