import datetime
import uuid

import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from src.rembot.db import queries
from src.rembot.db.settings import db_settings
from src.rembot.db.models import User, Reminder


engine = create_async_engine(db_settings.connection_string)
session_factory = async_sessionmaker(engine)


@pytest.mark.asyncio
async def test_get_reminders_in_timeframe() -> None:
    
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
                    User(
                        tg_id=00000,
                        username="000",
                        reminders=[
                            Reminder(time=out1, text="I'm out"),
                            Reminder(time=in1, text="I'm in"),
                        ],
                    ),
                    User(
                        tg_id=11111,
                        username="111",
                        reminders=[
                            Reminder(time=in2, text="I'm in"),
                            Reminder(time=out2, text="I'm out")
                        ],
                    ),
                ]
            )

    res = await queries.get_reminders_within_time(
        session_factory, start, end)
    
    in_time = set((in1, in2))
    got_time = set([rem.time for rem in res])

    assert got_time == in_time
