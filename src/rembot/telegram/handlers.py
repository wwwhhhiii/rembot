import aiogram
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from loguru import logger

from telegram.utils import (
    validate_and_parse_remind_cmd_args,
)


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

    await message.answer("Reminder bot is started")


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
    
    args_valid, args = validate_and_parse_remind_cmd_args(command.args)
    if not args_valid:
        logger.debug(f"Invalid remind command args: {command.args}")
        return

    await message.answer(f"Recieved remind cmd {args}")

