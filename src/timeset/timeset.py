from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime, date, timedelta, time
from typing import overload, Optional, Set


@dataclass(frozen=True)
class ContinuousTimeRange:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start cannot be later than end.")

    def __contains__(self, moment: datetime) -> bool:
        return self.start <= moment <= self.end

    @property
    def length(self) -> timedelta:
        return self.end - self.start

    def __and__(self, other: ContinuousTimeRange) -> Optional[ContinuousTimeRange]:
        if type(self) != type(other):
            return NotImplemented
        if not self.intersects_with(other):
            return None
        return ContinuousTimeRange(max(self.start, other.start), min(self.end, other.end))

    def __add__(self, other) -> Optional[ContinuousTimeRange]:
        if type(self) != type(other):
            return NotImplemented
        if not self.intersects_with(other):
            return None
        return ContinuousTimeRange(min(self.start, other.start), max(self.end, other.end))

    def __ge__(self, other) -> bool:  # TODO TEST
        """
        Check if self (S) is a superset of other (O): S ⊇ O
        """
        return self.start <= other.start and other.end <= self.end

    def __le__(self, other) -> bool:  # TODO TEST
        """
        Check if self (S) is a subset of other (O): S ⊆ O
        """
        return other.start <= self.start and self.end <= other.end

    def intersects_with(self, other: ContinuousTimeRange) -> bool:
        return other.start in self or other.end in self or self <= other


class TimeRange:

    @overload
    def __init__(self):
        pass

    @overload
    def __init__(self, start: datetime, end: datetime):
        pass

    @overload
    def __init__(self, cls, start: datetime, duration: timedelta):
        pass

    def __init__(self, start: Optional[datetime] = None,
                 end: Optional[datetime] = None,
                 duration: Optional[timedelta] = None):
        self._periods: Set[ContinuousTimeRange] = set()
        if (start and not (end or duration)) or (end and duration):
            raise ValueError("Allowed combination of constructor parameters are:\n  "
                             "* Empty constructor\n  * `start` & `end`\n  * `start` & `duration`")
        if start:
            self._periods.add(ContinuousTimeRange(start, end or start + duration))

    def __eq__(self, other: TimeRange) -> bool:
        return self._periods == other._periods

    def __repr__(self) -> str:
        return ' + '.join(
            [f"TimeRange(start={repr(p.start)}, end={repr(p.end)})" for p in self._periods]
        ) or "TimeRange()"

    def __bool__(self) -> bool:
        """
        A TimeRange evaluates to True if its duration is grater than zero.
        """
        return len(self._periods) != 0

    def __contains__(self, moment: datetime) -> bool:
        return any([moment in p for p in self._periods])

    def __add__(self, other) -> TimeRange:
        """
        Find the union of the two TimeRange's: A ⋃ B.
        """
        if type(self) != type(other):
            return NotImplemented
        intersectionless_periods: Set[ContinuousTimeRange] = set()
        for p in {*self._periods, *other._periods}:
            for per in intersectionless_periods:
                if p.intersects_with(per):
                    intersectionless_periods.discard(per)
                    intersectionless_periods.add(p + per)
                    break
            else:
                intersectionless_periods.add(p)
        result = TimeRange()
        result._periods = intersectionless_periods
        return result

    # def __and__(self, other: TimeRange) -> Optional[TimeRange]:
    #     """
    #     Find the intersection of the two TimeRange's: A ⋂ B.
    #     """
    #     raise NotImplementedError()

    @property
    def length(self) -> timedelta:
        return sum([p.length for p in self._periods], start=timedelta())

    @property
    def start(self) -> datetime:
        """
        Return the earliest moment in the TimeRange.
        """
        return min({p.start for p in self._periods})

    @property
    def end(self) -> datetime:
        """
        Return the latest moment in the TimeRange.
        """
        return max({p.end for p in self._periods})


class CalendarMonth(TimeRange):
    """
    Represent a calendar month.
    """

    def __init__(self, year: int, month: int):
        start_date = date(year, month, 1)
        end_date = self._last_date_of_month(year, month)
        super().__init__(self._to_datetime(start_date), self._to_datetime(end_date))
        self.year = year
        self.month = month

    def __repr__(self):
        return f'CalendarMonth(year={self.year}, month={self.month})'

    @property
    def next(self) -> CalendarMonth:
        """Return an instance of next month."""
        first_day_in_next_month = self.end.date() + timedelta(days=1)
        return CalendarMonth(first_day_in_next_month.year, first_day_in_next_month.month)

    @property
    def prev(self) -> CalendarMonth:
        """Return an instance of previous month."""
        last_day_in_previous_month = self.start.date() - timedelta(days=1)
        return CalendarMonth(last_day_in_previous_month.year, last_day_in_previous_month.month)

    @staticmethod
    def _last_date_of_month(year: int, month: int) -> datetime.date:
        _, last_day = calendar.monthrange(year, month)
        return date(year, month, last_day)

    @staticmethod
    def _to_datetime(d: date) -> datetime:
        return datetime.combine(d, time.min)
