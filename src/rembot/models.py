import datetime
import uuid

from attrs import define


@define
class Reminder:
    """"""

    id: uuid.UUID
    username: str
    time: datetime.datetime
    text: str


@define
class ReminderCreateRequest:
    """"""

    username: str
    time: datetime.datetime
    text: str


@define
class ReminderGetRequest:
    """"""

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
