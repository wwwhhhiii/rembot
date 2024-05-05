from aiogram.utils import keyboard

from telegram.callback_data import UserCmdCallback, UserCmds


def get_main_menu_keyboard() -> keyboard.InlineKeyboardBuilder:
    """"""

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
        text="Update reminder",
        callback_data=UserCmdCallback(cmd=UserCmds.UPDATE_REMINDER),
    )
    builder.button(
        text="Delete reminder",
        callback_data=UserCmdCallback(cmd=UserCmds.DELETE_REMINDER),
    )

    builder.adjust(2, 2)

    return builder
