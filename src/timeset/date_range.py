from datetime import datetime, date, timedelta, time
from typing import Optional

from .timerange import TimeRange
from .utils import preclude


# TODO TEST
def daterange(start: date, end: Optional[date] = None, days: Optional[int] = None) -> TimeRange:
    preclude(end is not None and days is not None, TypeError, 'Only one of `end` `days` can be given.')
    if end is not None:
        end_time = end
    elif days is not None:
        end_time = end or start + timedelta(days=days)
    else:
        end_time = start
    return TimeRange(first_moment_in_day(start), last_moment_in_day(end_time))


def first_moment_in_day(d: date, /) -> datetime:
    return datetime.combine(d, time.min)


def last_moment_in_day(d: date, /) -> datetime:
    return datetime.combine(d, time.max)
