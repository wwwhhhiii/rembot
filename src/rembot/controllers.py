import uuid

from loguru import logger

import tasks
from app_models import (
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

    # TODO validate reminder format
    # TODO check if user with tg_id exists, if not - create

    # By this line user should be either determined, either created
    request.user.id = uuid.uuid4()  # TODO replace

    try:
        reminder = Reminder(
            id=uuid.uuid4(),
            user_id=request.user.id,
            time=request.time,
            text=request.text,
        )
    except Exception as e:
        logger.error(f"Invalid reminder create request: {request}")
        return RequestExecStatus.INVALID

    user = User(  # TODO move in other place
        id=uuid.uuid4(), tg_id=request.user.tg_id, username=request.user.username
    )
    await db_queries.create_user(user)
    try:
        await db_queries.create_reminder(reminder, user_id=request.user.id)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return RequestExecStatus.DB_ERROR

    return RequestExecStatus.OK


def get_reminder(request: ReminderGetRequest) -> Reminder | None:
    """"""

    # TODO get reminder by id
    request.reminder_id

    # TODO return success status

    return None


def get_user_reminders(username: str) -> None:
    """"""

    # TODO return paginated reminders

    return None


def update_reminder(request: ReminderUpdateRequest) -> RequestExecStatus:
    """"""

    # TODO load reminder from db, check if exists
    reminder = ...
    if reminder is None:
        ...  # TODO return does not exist status

    # TODO if updated text -> update text in db
    # TODO if updated time -> update time in db -> delete worker, start worker with new time

    # TODO return success status

    return RequestExecStatus.OK


def delete_reminder(request: ReminderDeleteRequest) -> RequestExecStatus:
    """"""

    # TODO load reminder from db, check if exists
    # TODO stop worker, delete reminder from db

    return RequestExecStatus.OK


# async def dispatch_reminder_to_user(request: ...) -> RequestExecStatus:
#     await tg_utils.send_rem_to_user()

#     return RequestExecStatus.OK
