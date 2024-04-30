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
from db.util import async_scoped_session_factory
import utils
from telegram import utils as tg_utils


async def create_reminder(request: ReminderCreateRequest) -> RequestExecStatus:
    """Creates a reminder from request for existing or yet non-existing user.

    If `request` contains unknown telegram id - creates new user
    """

    async with async_scoped_session_factory() as session:
        logger.debug(f"Querying for user '{request.user.username}' in database...")
        user = await db_queries.get_user_by_tg_id(
            session,
            telegram_id=request.user.tg_id,
        )
        logger.debug(f"User '{request.user.username}' query result: {user}")
        if user is None:
            logger.debug(
                f"User with id '{request.user.tg_id}' does not exist, creating..."
            )
            user = await db_queries.create_user(
                session,
                id_=uuid.uuid4(),
                telegram_id=request.user.tg_id,
                username=request.user.username,
            )
            logger.debug(f"User '{request.user.tg_id}' has been created")

        request.user.id = user.id

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

        logger.debug(f"Creating reminder for user '{request.user.tg_id}'...")

        try:
            await db_queries.create_reminder(session, reminder)
        except LookupError:
            logger.error(f"Tried to create reminder '{reminder}' for non-existing user")
            return RequestExecStatus.DB_ERROR
        except Exception as e:
            logger.error(f"Database error during reminder creation: {e}")
            return RequestExecStatus.DB_ERROR

        logger.debug(f"Successfully created reminder for user '{request.user.tg_id}'")

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
