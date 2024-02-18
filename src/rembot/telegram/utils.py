from dataclasses import dataclass
from typing import Iterable
import re
import datetime
import functools

from loguru import logger


@dataclass
class RemCmdArgs:
    rem_time: datetime.datetime
    text: str


def tomorrow_date_factory() -> datetime.datetime:
    return datetime.datetime.today() + datetime.timedelta(days=1)


SPECIAL_WORDS_TO_DATE_FACTORY = {
    "сегодня": functools.partial(datetime.datetime.today),
    "завтра": tomorrow_date_factory,
    "today": functools.partial(datetime.datetime.today),
    "tomorrow": tomorrow_date_factory,
}


def _get_remind_cmd_args_regex(
    special_words: Iterable[str],
) -> re.Pattern:
    """Compiles case-insensitive arguments regex.
    
    Arguments: date time text
    """

    DATE_REGEX = r"(\d{1,2}).(\d{1,2})"
    DAYS = [DATE_REGEX, *special_words]
    DAY_REGEX = "|".join(DAYS)
    TIME_REGEX = r"(\d{1,2}):(\d{2})"  # TODO add 00 default after ":" if no given
    REMIND_TEXT_REGEX = ".{1,200}"
    SPACING_REGEX = " {1,5}"

    time_regex = f"^({DAY_REGEX})" + SPACING_REGEX + f"({TIME_REGEX})" + SPACING_REGEX + f"({REMIND_TEXT_REGEX})$"
    logger.debug(f"Time regex: {time_regex}")

    return re.compile(time_regex, flags=re.IGNORECASE)


REMIND_CMD_ARGS_PARSE_REGEX = _get_remind_cmd_args_regex(
    special_words=SPECIAL_WORDS_TO_DATE_FACTORY.keys())


def parse_remind_cmd_args(args_str: str | None) -> RemCmdArgs | None:
    """"""

    if args_str is None:
        return None

    match = re.match(REMIND_CMD_ARGS_PARSE_REGEX, args_str)
    if match is None:
        return None

    year = datetime.datetime.now().year

    date = match.group(1)
    dt_func = SPECIAL_WORDS_TO_DATE_FACTORY.get(date)
    date_is_special_word = dt_func is not None
    if date_is_special_word:
        date = dt_func()
    else:
        day, month = int(match.group(2)), int(match.group(3))
        date = datetime.date(year, month, day)

    hour = int(match.group(5))
    minute = match.group(6)
    minute = int(minute) if minute is not None else 0
    text = match.group(7)

    rem_time = datetime.datetime(
        year=year,
        month=date.month,
        day=date.day,
        hour=hour,
        minute=minute,)

    args = RemCmdArgs(rem_time=rem_time, text=text)

    return args
