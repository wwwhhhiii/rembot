import uuid
import datetime

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


async def create_reminder(
    user_tg_id: int,
    reminder_time: datetime.datetime,
    reminder_text: str,
) -> RequestExecStatus:
    """Creates a reminder from request for existing or yet non-existing user.

    If `request` contains unknown telegram id - creates new user
    """

    # TODO validate reminder data
    # logger.error(f"Invalid reminder create request: {request}")
    # return RequestExecStatus.INVALID

    async with async_scoped_session_factory() as db_session:
        logger.debug(f"Querying for user '{user_tg_id}' in database...")
        user = await db_queries.get_user_by_tg_id(
            db_session,
            telegram_id=user_tg_id,
        )
        logger.debug(f"User '{user_tg_id}' query result: {user}")
        if user is None:
            logger.debug(f"User with id '{user_tg_id}' does not exist, creating...")
            user = await db_queries.create_user(
                db_session,
                id_=uuid.uuid4(),
                telegram_id=user_tg_id,
            )
            logger.debug(f"User '{user_tg_id}' has been created")

        reminder = Reminder(
            id=uuid.uuid4(),
            user_id=user.id,
            time=reminder_time,
            text=reminder_text,
        )

        logger.debug(f"Creating reminder for user '{user_tg_id}'...")

        try:
            await db_queries.create_reminder(db_session, reminder)
        except LookupError:
            logger.error(f"Tried to create reminder '{reminder}' for non-existing user")
            return RequestExecStatus.DB_ERROR
        except Exception as e:
            logger.error(f"Database error during reminder creation: {e}")
            return RequestExecStatus.DB_ERROR

        logger.debug(f"Successfully created reminder for user '{user_tg_id}'")

        return RequestExecStatus.OK


async def get_reminder(request: ReminderGetRequest) -> Reminder | None:
    """"""

    async with async_scoped_session_factory() as db_session:
        reminder = await db_queries.get_reminder_by_id(
            db_session, id_=request.reminder_id
        )

    return reminder


async def get_user_reminders(user_tg_id: int) -> list[Reminder] | None:
    """"""

    async with async_scoped_session_factory() as db_session:
        reminders = await db_queries.get_user_reminders(
            db_session, user_tg_id=user_tg_id
        )

    return reminders


async def update_reminder(
    id_: uuid.UUID,
    time: datetime.datetime | None,
    text: str | None,
) -> None:
    """"""

    async with async_scoped_session_factory() as session:
        reminder = await db_queries.get_reminder_by_id(session, id_=id_)

        if reminder is None:
            return None

        await db_queries.update_reminder(session, id_=id_, time=time, text=text)

    return


def delete_reminder(request: ReminderDeleteRequest) -> RequestExecStatus:
    """"""

    # TODO load reminder from db, check if exists
    # TODO stop worker, delete reminder from db

    return RequestExecStatus.OK


# async def dispatch_reminder_to_user(request: ...) -> RequestExecStatus:
#     await tg_utils.send_rem_to_user()

#     return RequestExecStatus.OK
