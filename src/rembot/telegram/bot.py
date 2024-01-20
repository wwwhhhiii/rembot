from typing import Iterable

import aiogram


def create_bot(token: str, **kwargs) -> aiogram.Bot:
    """Creates telegram bot instance"""

    bot = aiogram.Bot(token, **kwargs)

    return bot


def create_dispatcher(
    include_routers: Iterable[aiogram.Router] = [],
    **kwargs,
) -> aiogram.Dispatcher:
    """Creates telegram updates dispatcher instance"""

    dp = aiogram.Dispatcher(**kwargs)
    dp.include_routers(*include_routers)

    return dp
