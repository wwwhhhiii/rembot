import uuid
import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, and_, delete, insert

from db.models import DBReminder, DBUser
from app_models import Reminder, User


async def create_user(user: User) -> DBUser | None:
    """Creates new user in database"""

    # stmt =
    # u = await DBUser.create(
    #     id=user.id, tg_id=user.tg_id, username=user.username)

    # return u
    # TODO update to sqlalchemy

    return None


async def create_reminder(reminder: Reminder, user_id: uuid.UUID) -> DBReminder | None:
    """
    Creates new reminder in database.\n
    Binds to existing user from database.
    """

    # user = await DBUser.filter(id=str(user_id)).first()
    # if user is None:
    #     raise RuntimeError(f"User with id {user_id} doesn't exist")

    # rem = await DBReminder.create(
    #     id=reminder.id,
    #     time=reminder.time,
    #     text=reminder.text)
    # await rem.user.add(user)

    # return rem

    # TODO update to sqlalchemy

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
    """"""

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
