import datetime
import uuid

from attrs import define


@define
class Reminder:
    """"""

    id: uuid.UUID
    username: str
    reply_to_id: int
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
