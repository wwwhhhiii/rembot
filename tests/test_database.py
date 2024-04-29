import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from src.rembot.db import queries
from src.rembot.db.settings import db_settings
from src.rembot.db.models import DBUser, DBReminder


engine = create_async_engine(db_settings.connection_string)
session_factory = async_sessionmaker(engine)


@pytest.mark.asyncio  # type: ignore[misc]
async def test_get_reminders_in_timeframe() -> None:
    """Test that ensures that reminders are collected in a specific time frame"""

    start = datetime.datetime(year=2000, month=2, day=16, hour=1)
    end = start + datetime.timedelta(hours=5)

    out1 = start - datetime.timedelta(hours=1)
    in1 = start + datetime.timedelta(hours=1)
    in2 = start + datetime.timedelta(hours=3)
    out2 = start + datetime.timedelta(hours=6)

    async with session_factory() as session:
        async with session.begin():
            session.add_all(
                [
                    DBUser(
                        tg_id=00000,
                        username="000",
                        reminders=[
                            DBReminder(time=out1, text="I'm out"),
                            DBReminder(time=in1, text="I'm in"),
                        ],
                    ),
                    DBUser(
                        tg_id=11111,
                        username="111",
                        reminders=[
                            DBReminder(time=in2, text="I'm in"),
                            DBReminder(time=out2, text="I'm out"),
                        ],
                    ),
                ]
            )

    async with session_factory() as session:
        res = await queries.get_reminders_within_time(session, start, end)

    in_time = set((in1, in2))
    got_time = set([rem.time for rem in res])

    assert got_time == in_time
