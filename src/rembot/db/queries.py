import uuid
import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, and_

from db.models import (
    Reminder as ReminderInDB,
    User as UserInDb,
)
from models import Reminder, User


async def create_user(user: User) -> UserInDb:
    """Creates new user in database"""

    u = await UserInDb.create(
        id=user.id, tg_id=user.tg_id, username=user.username)

    return u


async def create_reminder(
    reminder: Reminder, user_id: uuid.UUID) -> ReminderInDB:
    """
    Creates new reminder in database.\n
    Binds to existing user from database.
    """

    user = await UserInDb.filter(id=str(user_id)).first()
    if user is None:
        raise RuntimeError(f"User with id {user_id} doesn't exist")

    rem = await ReminderInDB.create(
        id=reminder.id,
        time=reminder.time,
        text=reminder.text)
    await rem.user.add(user)

    return rem


async def get_reminder(id: uuid.UUID) -> Reminder | None:

    reminder = await ReminderInDB.filter(id=str(id)).first()
    if reminder is None:
        return None
    
    return Reminder(id=reminder.id, time=reminder.time, text=reminder.text)

    
async def get_reminders_within_time(
    session_factory: async_sessionmaker[AsyncSession],
    start: datetime.datetime,
    end: datetime.datetime,
) -> list[Reminder]:
    """"""

    async with session_factory() as session:
        async with session.begin():
            stmt = (
                select(ReminderInDB).\
                filter(and_((ReminderInDB.time > start), (ReminderInDB.time < end)))
            )
            reminders = await session.scalars(stmt)
    
            return [Reminder(rec.id, rec.time, rec.text) for rec in reminders]


async def delete_reminder(id: uuid.UUID) -> Reminder | None:

    reminder = await ReminderInDB.filter(id=str(id)).first()
    if reminder is None:
        return None

    await ReminderInDB.delete(id=str(id))

    return Reminder(id=reminder.id, time=reminder.time, text=reminder.text)
