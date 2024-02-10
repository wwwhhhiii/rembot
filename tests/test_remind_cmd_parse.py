import datetime

import pytest

from src.rembot.telegram.utils import parse_remind_cmd_args


def test_valid_cmd() -> None:
    cmd = "16.02  1:00   qwerty asdf"
    res = parse_remind_cmd_args(cmd)

    assert res is not None


def test_invalid_cmd() -> None:
    cmd = "aswd      12    fewffffffff"
    res = parse_remind_cmd_args(cmd)

    assert res is None


def test_tomorrow_special_words() -> None:
    txt = "qweqwfew fewfe efe"
    cmd = f"завтра   16:31  {txt}"
    res = parse_remind_cmd_args(cmd)
    
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    cmd_datetime = datetime.datetime(
        year=tomorrow.year,
        month=tomorrow.month,
        day=tomorrow.day,
        hour=16,
        minute=31,
        second=0)

    assert res.rem_time == cmd_datetime

