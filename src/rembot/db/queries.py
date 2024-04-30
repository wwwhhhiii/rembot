import uuid
import datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from db.models import DBReminder, DBUser
from app_models import Reminder, User


async def create_user(
    session: AsyncSession,
    id_: uuid.UUID,
    telegram_id: int,
    username: str,
) -> User:
    """Creates new user in database

    Returns user database model instance
    """

    async with session.begin() as transaction:
        user = DBUser(id=id_, tg_id=telegram_id, username=username)
        session.add(user)  # TODO catch errors

        created_user = User(id=user.id, tg_id=user.tg_id, username=username)

    return created_user


async def get_user_by_tg_id(
    session: AsyncSession,
    telegram_id: int,
) -> User | None:
    """Selects user from database by its telegram id.

    If no user was found - returns `None`
    """

    stmt = select(DBUser).where(DBUser.tg_id == telegram_id)

    async with session.begin() as transaction:
        res = await session.scalar(stmt)
        if res is None:
            return None

        user = User(id=res.id, tg_id=res.tg_id, username=res.username)

    return user


async def get_user_by_id(
    session: AsyncSession,
    id_: uuid.UUID,
) -> User | None:
    """"""


async def create_reminder(
    session: AsyncSession,
    reminder: Reminder,
) -> None:
    """Creates new reminder in database.\n
    Binds to existing user from database.

    raises `LookupError` when user not found
    """

    async with session.begin() as transaction:
        user = await session.scalar(select(DBUser).where(DBUser.id == reminder.user_id))
        if user is None:
            raise LookupError(f"User with id {reminder.user_id} not found")

        rem = DBReminder(
            time=reminder.time, text=reminder.text, user_id=reminder.user_id
        )
        session.add(rem)  # TODO catch errors

    return None


async def get_reminder(id: uuid.UUID) -> Reminder | None:

    # reminder = await DBReminder.filter(id=str(id)).first()
    # if reminder is None:
    #     return None

    # return Reminder(id=reminder.id, time=reminder.time, text=reminder.text)

    # TODO update to sqlalchemy

    return None


async def get_reminders_within_time(
    session: AsyncSession,
    start: datetime.datetime,
    end: datetime.datetime,
) -> list[Reminder]:
    """Queries reminders from database within given time frame"""

    async with session.begin():
        stmt = select(DBReminder).filter(
            and_((DBReminder.time > start), (DBReminder.time < end))
        )
        reminders = await session.scalars(stmt)

        return [Reminder(rec.id, rec.user_id, rec.time, rec.text) for rec in reminders]


async def delete_reminder(id: uuid.UUID) -> Reminder | None:

    # reminder = await DBReminder.filter(id=str(id)).first()
    # if reminder is None:
    #     return None

    # await DBReminder.delete(id=str(id))

    # return Reminder(id=reminder.id, time=reminder.time, text=reminder.text)

    # TODO update to sqlalchemy

    return None
