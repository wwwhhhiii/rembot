import uuid
import enum

from loguru import logger
from attrs import asdict

from tasks import exec_reminder
from models import (
    User,
    Reminder,
    ReminderCreateRequest,
    ReminderGetRequest,
    ReminderUpdateRequest,
    ReminderDeleteRequest,
)
from db import queries as db_queries


class RequestExecStatus(int, enum.Enum):
    OK = enum.auto()
    INVALID = enum.auto()
    DB_ERROR = enum.auto()
    TASK_ERROR = enum.auto()


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


    user = User(
        id=uuid.uuid4(),
        tg_id=request.user_tg_id,
        username=request.username)
    await db_queries.create_user(user)
    try:
        await db_queries.create_reminder(reminder, user_id=user.id)
    except Exception as e:
        logger.error(f"Database error: {e}")
        return RequestExecStatus.DB_ERROR

    try:
        exec_reminder.delay(asdict(reminder))
    except Exception as e:
        logger.error(f"Task error: {e}")
        return RequestExecStatus.TASK_ERROR

    return RequestExecStatus.OK


def get_reminder(request: ReminderGetRequest) -> ...:
    """"""

    # TODO get reminder by id
    request.reminder_id

    # TODO return success status


def get_user_reminders(username: str) -> ...:
    """"""

    # TODO return paginated reminders


def update_reminder(request: ReminderUpdateRequest) -> ...:
    """"""

    # TODO load reminder from db, check if exists
    reminder = ...
    if reminder is None:
        ...  # TODO return does not exist status

    # TODO if updated text -> update text in db
    # TODO if updated time -> update time in db -> delete worker, start worker with new time
    res = exec_reminder.delay(reminder)

    # TODO return success status


def delete_reminder(request: ReminderDeleteRequest) -> ...:
    """"""

    # TODO load reminder from db, check if exists
    # TODO stop worker, delete reminder from db


def dispatch_reminder_to_user(request: ...) -> ...:
    ...