from typing import Iterable, Mapping, Any

import aiogram


def create_bot(token: str, **kwargs: Mapping[str, Any]) -> aiogram.Bot:
    """Creates telegram bot instance"""

    bot = aiogram.Bot(token, **kwargs)

    return bot


def create_dispatcher(
    include_routers: Iterable[aiogram.Router] = [],
    **kwargs: Mapping[str, Any],
) -> aiogram.Dispatcher:
    """Creates telegram updates dispatcher instance"""

    dp = aiogram.Dispatcher(**kwargs)
    dp.include_routers(*include_routers)

    return dp
