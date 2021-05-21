from dataclasses import dataclass
from datetime import datetime
from typing import overload, Optional, Set


@dataclass(frozen=True)
class ContinuousTimeRange:
    start: datetime
    end: datetime


class TimeRange:

    @overload
    def __init__(self):
        pass

    @overload
    def __init__(self, start: datetime, end: datetime):
        pass

    def __init__(self, start: Optional[datetime] = None, end: Optional[datetime] = None):
        self.periods: Set[ContinuousTimeRange] = set()
        if start and end:
            self.periods.add(ContinuousTimeRange(start, end))
        elif start or end:
            raise ValueError("A `TimeRange` must have either none or both `start` and `end` specified.")

    def __str__(self) -> str:
        return ' + '.join(
            [f"TimeRange(start={repr(p.start)}, end={repr(p.end)})" for p in self.periods]
        ) or "TimeRange()"
