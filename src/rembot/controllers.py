import uuid

from loguru import logger

import tasks
from models import (
    User,
    Reminder,
    RequestExecStatus,
    ReminderCreateRequest,
    ReminderGetRequest,
    ReminderUpdateRequest,
    ReminderDeleteRequest,
)
from db import queries as db_queries
import utils
from telegram import utils as tg_utils


async def create_reminder(request: ReminderCreateRequest) -> RequestExecStatus:
    """"""

    try:
        reminder = Reminder(
            id=uuid.uuid4(),
            time=request.time,
            text=request.text)
    except Exception as e:
        logger.error(f"Invalid reminder create request: {request}")
        return RequestExecStatus.INVALID

    user = User(  # TODO move in other place
        id=uuid.uuid4(),
        tg_id=request.user_tg_id,
        username=request.username)
    await db_queries.create_user(user)
    try:
        await db_queries.create_reminder(reminder, user_id=user.id)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return RequestExecStatus.DB_ERROR

    # try:
    #     tasks.dispatch_reminder.apply_async(
    #         (reminder.id,),
    #         eta=utils.datetime_to_greenwich(reminder.time))
    #     logger.debug(reminder.time)
    # except Exception as e:
    #     logger.error(f"Task error: {e}")
    #     return RequestExecStatus.TASK_ERROR

    return RequestExecStatus.OK


def get_reminder(request: ReminderGetRequest) -> RequestExecStatus:
    """"""

    # TODO get reminder by id
    request.reminder_id

    # TODO return success status


def get_user_reminders(username: str) -> ...:
    """"""

    # TODO return paginated reminders


def update_reminder(request: ReminderUpdateRequest) -> RequestExecStatus:
    """"""

    # TODO load reminder from db, check if exists
    reminder = ...
    if reminder is None:
        ...  # TODO return does not exist status

    # TODO if updated text -> update text in db
    # TODO if updated time -> update time in db -> delete worker, start worker with new time

    # TODO return success status


def delete_reminder(request: ReminderDeleteRequest) -> RequestExecStatus:
    """"""

    # TODO load reminder from db, check if exists
    # TODO stop worker, delete reminder from db


async def dispatch_reminder_to_user(request: ...) -> RequestExecStatus:
    await tg_utils.send_rem_to_user()