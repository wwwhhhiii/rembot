import datetime
import uuid
from enum import Enum, auto

from aiogram import filters


class UserCmds(str, Enum):

    CREATE_REMINDER = "create-reminder"
    LIST_REMINDERS = "list-reminders"
    UPDATE_REMINDER = "update-reminder"
    DELETE_REMINDER = "delete-reminder"


class UserCmdCallback(filters.callback_data.CallbackData, prefix="user"):  # type: ignore
    """"""

    cmd: UserCmds


class ListRemindersCallback(filters.callback_data.CallbackData, prefix="rem"):  # type: ignore
    """"""

    ...


class ReminderToUpdateChoice(
    filters.callback_data.CallbackData,  # type: ignore
    prefix="rem",
    sep="&",
):
    """"""

    id_: uuid.UUID
    time: datetime.datetime


class ReminderUpdateCancelChoice(
    filters.callback_data.CallbackData, prefix="rem"  # type: ignore
):

    ...


class ReminderEditMenuOpts(int, Enum):

    UPD_TIME = auto()
    UPD_TXT = auto()
    CONFIRM = auto()
    CANCEL = auto()


class ReminderEditMenu(filters.callback_data.CallbackData, prefix="rem"):  # type: ignore
    """"""

    opt: ReminderEditMenuOpts


class UpdateReminderCallback(filters.callback_data.CallbackData, prefix="rem"):  # type: ignore
    """"""

    id_: uuid.UUID
    time: datetime.datetime | None
    text: str | None
