import datetime
import uuid

import aiogram
from aiogram import F
from aiogram.filters import Command
import aiogram.filters
import aiogram.filters.callback_data
from aiogram.filters.command import CommandObject
from loguru import logger

from telegram.keyboards import get_main_menu_keyboard
from telegram.callback_data import UserCmdCallback, UserCmds
from telegram.utils import (
    parse_remind_cmd_args,
)
from controllers import RequestExecStatus, create_reminder, get_user_reminders
from app_models import ReminderCreateRequest, User


router = aiogram.Router(name="rem")


@router.message(Command("start"))  # type: ignore
async def cmd_start(
    message: aiogram.types.Message,
) -> None:
    """
    Handles `/start` command.

    ...
    """

    if message.from_user is not None:
        logger.debug(f"Recieved /start command from {message.from_user.username}")

    settings = {"resize_keyboard": True}

    await message.answer(
        "Reminder bot is started",
        reply_markup=get_main_menu_keyboard().as_markup(**settings),
    )


@router.message(Command("remind"))  # type: ignore
async def cmd_create_reminder(
    message: aiogram.types.Message,
    command: CommandObject,
) -> None:
    """
    Handles `/remind` command.

    ...
    """

    fromuser = message.from_user
    if fromuser is None:
        logger.debug(f"Unable to get user of the message")
        return

    logger.debug(f"Recieved /remind command from {message.from_user.username}")

    args = parse_remind_cmd_args(command.args)
    if args is None:
        logger.debug(f"Invalid remind command args: {command.args}")
        await message.answer(f"Invalid command format")
        return

    res = await create_reminder(
        user_tg_id=fromuser.id, reminder_time=args.rem_time, reminder_text=args.text
    )

    if res == RequestExecStatus.OK:
        date = args.rem_time.date()
        answer = (
            f"Reminder has been successfully set.\n"
            f"Time: {date.day}.{date.month} {args.rem_time.hour}:{args.rem_time.minute}\n"
            f"Text: {args.text}"
        )
        await message.answer(answer)
    else:
        await message.answer(f"Something went wrong ({res.name})")


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.CREATE_REMINDER))  # type: ignore
async def clb_create_reminder(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    await query.answer("Not implemented")


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.LIST_REMINDERS))  # type: ignore
async def clb_list_reminders(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    reminders = await get_user_reminders(query.from_user.id)

    if reminders is None:
        await query.message.answer("Unknown user")
        return

    if len(reminders) == 0:
        await query.message.answer("No reminders were set yet")
        return

    await query.message.answer("\n".join(map(str, reminders)))


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.UPDATE_REMINDER))  # type: ignore
async def clb_update_reminder(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    await query.answer("Not implemented")


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.DELETE_REMINDER))  # type: ignore
async def clb_delete_reminder(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    await query.answer("Not implemented")
