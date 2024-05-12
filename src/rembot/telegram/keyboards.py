import itertools

from aiogram.utils import keyboard
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)

from telegram.callback_data import (
    UserCmdCallback,
    UserCmds,
    ReminderToUpdateChoice,
)
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


def get_reminders_to_update_keyboard(reminders: list[Reminder]) -> InlineKeyboardMarkup:

    # if len(reminders) % 2 != 0:
    #     ...
    #     # reminders.append(" ")  # TODO

    # half1 = reminders[: len(reminders) // 2]
    # half2 = reminders[len(reminders) // 2 :]

    # buttons = []

    # for rem1, rem2 in zip(half1, half2):
    #     row = [
    #         InlineKeyboardButton(
    #             text=rem1.text,
    #             callback_data=ReminderToUpdateChoice(
    #                 id_=rem1.id, time=rem1.time, text=rem1.text).pack(),
    #         ),
    #         InlineKeyboardButton(
    #             text=rem2.text,
    #             callback_data=ReminderToUpdateChoice(
    #                 id_=rem2.id, time=rem2.time, text=rem2.text).pack(),
    #         ),
    #     ]
    #     buttons.append(row)

    # markup = InlineKeyboardMarkup(keyboard=buttons)
    # TODO adjust by number of columns

    builder = keyboard.InlineKeyboardBuilder()

    for r in reminders:
        builder.button(
            text=r.text,
            callback_data=ReminderToUpdateChoice(id_=r.id, time=r.time),
        )

    return builder.as_markup()


def _get_reminder_property_choice_keyboard() -> InlineKeyboardMarkup:

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Time"), KeyboardButton(text="Text")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return markup


reminder_prop_choice_keyboard = _get_reminder_property_choice_keyboard()
