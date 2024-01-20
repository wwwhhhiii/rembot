import uvloop

from settings.bot import bot_settings
from telegram.bot import create_bot, create_dispatcher
from telegram.handlers import router


async def main() -> None:
    
    bot = create_bot(bot_settings.token)
    dispatcher = create_dispatcher(include_routers=[router,])
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
