import aiogram
from aiogram.filters import CommandStart
from loguru import logger


router = aiogram.Router()


@router.message(CommandStart)
async def cmd_start_handler(
    message: aiogram.types.Message,
) -> None:
    """
    Handles `/start` command.

    ...
    """

    logger.debug(f"Recieved /start command from {message.from_user.username}")

    await message.answer("Reminder bot is started")


async def cmd_create_reminder_handler(
    message: aiogram.types.Message,
) -> None:
    """
    Handles `/remind` command.

    ...
    """

    ...

