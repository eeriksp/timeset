from datetime import datetime, date, timedelta, time
from typing import Optional

from .timerange import TimeRange
from .utils import preclude


# TODO TEST
def date_range(start: date, end: Optional[date] = None, days: Optional[int] = None) -> TimeRange:
    preclude(end is None and days is None, TypeError, 'Either `end` or duration as `days` must be given.')
    preclude(end is not None and days is not None, TypeError, 'Only one of `end` `days` can be given.')
    end = end or start + timedelta(days=days)
    return TimeRange(first_moment_in_day(start), last_moment_in_day(end))


def first_moment_in_day(d: date, /) -> datetime:
    return datetime.combine(d, time.min)


def last_moment_in_day(d: date, /) -> datetime:
    return datetime.combine(d, time.max)
