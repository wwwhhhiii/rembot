import datetime


def datetime_to_greenwich(
    t: datetime.datetime,
) -> datetime.datetime:
    """Localizes datetime to Greenwich datetime (+0 UTC)"""

    return t - t.astimezone().utcoffset()
