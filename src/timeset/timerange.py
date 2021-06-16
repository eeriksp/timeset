from __future__ import annotations

from typing import overload, Optional, Set, FrozenSet
import operator
from functools import reduce
from datetime import datetime, date, timedelta

from .continuous import ContinuousTimeRange


class TimeRange:
    intervals: FrozenSet[ContinuousTimeRange] = frozenset()

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
        if (start and not (end or duration)) or (end and duration):
            raise ValueError("Allowed combination of constructor parameters are:\n  "
                             "* Empty constructor\n  * `start` & `end`\n  * `start` & `duration`")
        if start:
            self.intervals = frozenset({ContinuousTimeRange(start, end or start + duration)})

    def __eq__(self, other: TimeRange) -> bool:
        return self.intervals == other.intervals

    def __repr__(self) -> str:
        return ' + '.join(
            [f"TimeRange(start={repr(p.start)}, end={repr(p.end)})" for p in self.intervals]
        ) or "TimeRange()"

    def __bool__(self) -> bool:
        """
        A TimeRange evaluates to True if its duration is grater than zero.
        """
        return len(self.intervals) != 0

    def __contains__(self, moment: datetime) -> bool:
        return any([moment in p for p in self.intervals])

    def __add__(self, other: TimeRange) -> TimeRange:
        """
        Find the union of the two TimeRange's: A ⋃ B.
        """
        if not isinstance(other, TimeRange):
            return NotImplemented
        intersectionless_periods: Set[ContinuousTimeRange] = set()
        for p in {*self.intervals, *other.intervals}:
            for per in intersectionless_periods:
                if p.intersects_with(per):
                    intersectionless_periods.discard(per)
                    intersectionless_periods.add(p + per)
                    break
            else:
                intersectionless_periods.add(p)
        result = TimeRange()
        result.intervals = intersectionless_periods
        return result

    def __and__(self, other: TimeRange) -> TimeRange:
        """
        Find the intersection of the two TimeRange's: A ⋂ B.
        """
        if not isinstance(other, TimeRange):
            return NotImplemented
        # Compute the Cartesian product and find all intersections
        intersections = {s & o for s in self.intervals for o in other.intervals}
        intersections.discard(None)
        # TODO on next line switch from [] compasion to {} comparison
        #  after TimeRange has been made hashable
        return reduce(operator.add, [TimeRange(t.start, t.end) for t in intersections], TimeRange())

    @property
    def length(self) -> timedelta:
        return sum([p.length for p in self.intervals], start=timedelta())

    @property
    def start(self) -> datetime:  # FIXME ca it be None if TimeRange is empty
        """
        Return the earliest moment in the TimeRange.
        """
        return min({p.start for p in self.intervals})

    @property
    def end(self) -> datetime:  # FIXME ca it be None if TimeRange is empty
        """
        Return the latest moment in the TimeRange.
        """
        return max({p.end for p in self.intervals})

    @property  # TODO TEST
    def start_date(self) -> date:  # FIXME can self.start be None?
        return self.start.date()

    @property  # TODO TEST
    def end_date(self) -> date:  # FIXME can self.end be None?
        return self.end.date()
