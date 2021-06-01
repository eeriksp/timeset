from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
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
    def as_timedelta(self) -> timedelta:
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

    def intersects_with(self, other: ContinuousTimeRange) -> bool:
        return other.start in self or other.end in self


class TimeRange:

    @overload
    def __init__(self):
        pass

    @overload
    def __init__(self, start: datetime, end: datetime):
        pass

    def __init__(self, start: Optional[datetime] = None, end: Optional[datetime] = None):
        self._periods: Set[ContinuousTimeRange] = set()
        if start and end:
            self._periods.add(ContinuousTimeRange(start, end))
        elif start or end:
            raise ValueError("A `TimeRange` must have either none or both `start` and `end` specified.")

    def __repr__(self) -> str:
        return ' + '.join(
            [f"TimeRange(start={repr(p.start)}, end={repr(p.end)})" for p in self._periods]
        ) or "TimeRange()"

    def __bool__(self) -> bool:
        return len(self._periods) != 0

    def __contains__(self, moment: datetime) -> bool:
        return any([moment in p for p in self._periods])

    def __add__(self, other) -> TimeRange:
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

    @classmethod
    def with_duration(cls, start: datetime, duration: timedelta) -> TimeRange:
        return cls(start, start + duration)

    @property
    def as_timedelta(self) -> timedelta:
        return sum([p.as_timedelta for p in self._periods], start=timedelta())
