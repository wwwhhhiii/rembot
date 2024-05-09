import itertools

from aiogram.utils import keyboard
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)

from telegram.callback_data import UserCmdCallback, UserCmds
from app_models import Reminder


def _get_main_menu_keyboard_markup() -> InlineKeyboardMarkup:

    builder = keyboard.InlineKeyboardBuilder()

    builder.button(
        text="Create reminder",
        callback_data=UserCmdCallback(cmd=UserCmds.CREATE_REMINDER),
    )
    builder.button(
        text="List reminders",
        callback_data=UserCmdCallback(cmd=UserCmds.LIST_REMINDERS),
    )
    builder.button(
        text="Update reminders",
        callback_data=UserCmdCallback(cmd=UserCmds.UPDATE_REMINDER),
    )
    builder.button(
        text="Delete reminder",
        callback_data=UserCmdCallback(cmd=UserCmds.DELETE_REMINDER),
    )

    builder.adjust(2, 2)

    return builder.as_markup()


main_menu_keyboard = _get_main_menu_keyboard_markup()


def get_reminders_as_buttons_markup(reminders: list[Reminder]) -> ReplyKeyboardMarkup:

    rem_time = [r.text for r in reminders]
    if len(rem_time) % 2 != 0:
        rem_time.append(" ")

    half1 = rem_time[: len(rem_time) // 2]
    half2 = rem_time[len(rem_time) // 2 :]

    buttons = [
        [KeyboardButton(text=str(r1)), KeyboardButton(text=str(r2))]
        for r1, r2 in zip(half1, half2)
    ]

    markup = ReplyKeyboardMarkup(keyboard=buttons)

    return markup
