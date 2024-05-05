import datetime
from enum import Enum

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
