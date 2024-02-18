import uuid

from db.models import (
    Reminder as ReminderInDB,
    RemUser as UserInDb,
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