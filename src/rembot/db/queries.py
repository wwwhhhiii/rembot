import uuid
import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, insert
from sqlalchemy.orm import selectinload, load_only

from db.models import DBReminder, DBUser
from app_models import Reminder, User


async def create_user(
    session: AsyncSession,
    id_: uuid.UUID,
    telegram_id: int,
) -> User:
    """Creates new user in database

    Returns user database model instance
    """

    async with session.begin() as transaction:
        user = DBUser(id=id_, tg_id=telegram_id)
        session.add(user)  # TODO catch errors

        created_user = User(id=user.id, tg_id=user.tg_id)

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

        user = User(id=res.id, tg_id=res.tg_id)

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
    """Creates new reminder and writes it to database.\n
    Binds this reminder to existing user from database by user id.

    raises `LookupError` when user with user id from reminder is not found in database.
    """

    async with session.begin() as transaction:
        user = await session.scalar(select(DBUser).where(DBUser.id == reminder.user_id))
        if user is None:
            raise LookupError(f"User with id {reminder.user_id} not found")

        rem = DBReminder(
            time=reminder.time, text=reminder.text, user_id=reminder.user_id
        )
        session.add(rem)  # TODO returning insert

    return None


async def get_reminder_by_id(
    session: AsyncSession,
    id_: uuid.UUID,
) -> Reminder | None:

    stmt = select(Reminder).where(Reminder.id == id_)
    async with session.begin() as transaction:
        reminder = await session.scalar(stmt)

        if reminder is None:
            return None

        return Reminder(
            id=reminder.id,
            user_id=reminder.user_id,
            time=reminder.time,
            text=reminder.text,
        )


async def get_user_reminders(
    session: AsyncSession,
    user_tg_id: int,
) -> list[Reminder] | None:
    """
    Returns `None` if user is not found
    """

    # TODO mb generator with limit

    async with session.begin() as transaction:
        stmt = (
            select(DBUser)
            .where(DBUser.tg_id == user_tg_id)
            .options(
                selectinload(DBUser.reminders),
            )
        )
        user = await session.scalar(stmt)
        if user is None:
            return None

        return [Reminder(r.id, r.user_id, r.time, r.text) for r in user.reminders]


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


async def update_reminder(
    session: AsyncSession,
    id_: uuid.UUID,
    time: datetime.datetime | None,
    text: str | None,
) -> None:
    """"""

    if time is None and text is None:
        raise ValueError  # TODO

    update_obj: dict[str, uuid.UUID | datetime.datetime | str] = {
        "id": id_,
    }
    if time is not None:
        update_obj["time"] = time
    if text is not None:
        update_obj["text"] = text

    async with session.begin() as transaction:
        await session.execute(
            update(DBReminder),
            [
                update_obj,
            ],
        )

    return


async def delete_reminder(id: uuid.UUID) -> Reminder | None:

    # reminder = await DBReminder.filter(id=str(id)).first()
    # if reminder is None:
    #     return None

    # await DBReminder.delete(id=str(id))

    # return Reminder(id=reminder.id, time=reminder.time, text=reminder.text)

    # TODO update to sqlalchemy

    return None
