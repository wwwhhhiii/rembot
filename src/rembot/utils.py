from typing import Optional
import datetime


def datetime_to_greenwich(
    t: datetime.datetime,
) -> Optional[datetime.datetime]:
    """Localizes datetime to Greenwich datetime (+0 UTC)"""

    offset = t.astimezone().utcoffset()
    if offset is None:
        return None

    return t - offset
