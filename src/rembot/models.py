import datetime
import uuid
import enum

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
    time: datetime.datetime  # TODO add time validation at init
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


class RequestExecStatus(int, enum.Enum):
    OK = enum.auto()
    INVALID = enum.auto()
    DB_ERROR = enum.auto()
    TASK_ERROR = enum.auto()
