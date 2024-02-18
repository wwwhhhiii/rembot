import datetime
import uuid

from attrs import define


@define
class User:
    """"""

    id: uuid.UUID
    tg_id: int
    username: str


@define
class Reminder:
    """"""

    id: uuid.UUID
    time: datetime.datetime
    text: str


@define
class ReminderCreateRequest:
    """"""

    username: str
    user_tg_id: int
    time: datetime.datetime
    text: str


@define
class ReminderGetRequest:
    """"""

    user_tg_id: int
    username: str
    reminder_id: uuid


@define
class ReminderUpdateRequest:
    """"""

    ...


@define
class ReminderDeleteRequest:
    """"""

    ...
