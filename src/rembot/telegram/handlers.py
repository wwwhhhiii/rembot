import datetime

import aiogram
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from loguru import logger

from telegram.keyboards import get_main_menu_keyboard
from telegram.utils import (
    parse_remind_cmd_args,
)
from controllers import RequestExecStatus, create_reminder
from models import ReminderCreateRequest


router = aiogram.Router(name="rem")


@router.message(Command("start"))
async def cmd_start_handler(
    message: aiogram.types.Message,
) -> None:
    """
    Handles `/start` command.

    ...
    """

    logger.debug(f"Recieved /start command from {message.from_user.username}")

    _settings = {
        "resize_keyboard": True
    }

    await message.answer(
        "Reminder bot is started",
        reply_markup=get_main_menu_keyboard().as_markup(**_settings))


@router.message(Command("remind"))
async def cmd_create_reminder_handler(
    message: aiogram.types.Message,
    command: CommandObject,
) -> None:
    """
    Handles `/remind` command.

    ...
    """

    logger.debug(f"Recieved /remind command from {message.from_user.username}")
    
    args = parse_remind_cmd_args(command.args)
    if args is None:
        logger.debug(f"Invalid remind command args: {command.args}")
        await message.answer(f"Invalid command format")
        return

    req = ReminderCreateRequest(
        username=message.from_user.username or "",
        user_tg_id=message.from_user.id,
        time=args.rem_time.replace(tzinfo=datetime.timezone.utc),
        text=args.text)
    res = await create_reminder(req)

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

