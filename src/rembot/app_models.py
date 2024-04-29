from dataclasses import dataclass
import datetime
import uuid
import enum


@dataclass
class User:
    """"""

    id: uuid.UUID
    tg_id: int
    username: str


@dataclass
class Reminder:
    """"""

    id: uuid.UUID
    user_id: uuid.UUID
    time: datetime.datetime  # TODO add time validation at init
    text: str


@dataclass
class ReminderCreateRequest:
    """"""

    user: User
    time: datetime.datetime
    text: str


@dataclass
class ReminderGetRequest:
    """"""

    user_tg_id: int
    username: str
    reminder_id: uuid.UUID


@dataclass
class ReminderUpdateRequest:
    """"""

    ...


@dataclass
class ReminderDeleteRequest:
    """"""

    ...


class RequestExecStatus(int, enum.Enum):
    OK = enum.auto()
    INVALID = enum.auto()
    DB_ERROR = enum.auto()
    TASK_ERROR = enum.auto()
