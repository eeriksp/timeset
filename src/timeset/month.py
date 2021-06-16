from __future__ import annotations

from calendar import monthrange
from datetime import timedelta, date

from .timerange import TimeRange
from .daterange import date_range


class CalendarMonth(TimeRange):
    """
    Represent a calendar month.
    """

    def __init__(self, year: int, month: int):
        daterange = date_range(start=date(year, month, 1), end=self._last_date_of_month(year, month))
        super().__init__(start=daterange.start, end=daterange.end)
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
    def _last_date_of_month(year: int, month: int) -> date:
        _, last_day = monthrange(year, month)
        return date(year, month, last_day)
