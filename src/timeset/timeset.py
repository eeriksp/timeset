from __future__ import annotations

from typing import overload, Optional, Set, FrozenSet
import operator
from functools import reduce
from datetime import datetime, date, timedelta

from .interval import TimeInterval, has_intersection


class TimeSet:
    intervals: FrozenSet[TimeInterval] = frozenset()

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
            self.intervals = frozenset({TimeInterval(start, end or start + duration)})

    def __eq__(self, other: TimeSet) -> bool:
        return self.intervals == other.intervals

    def __repr__(self) -> str:
        return ' + '.join(
            [f"TimeSet(start={repr(p.start)}, end={repr(p.end)})" for p in self.intervals]
        ) or "TimeSet()"

    def __bool__(self) -> bool:
        """
        A TimeSet evaluates to True if its duration is grater than zero.
        """
        return len(self.intervals) != 0

    def __contains__(self, moment: datetime) -> bool:
        return any([moment in p for p in self.intervals])

    def __add__(self, other: TimeSet) -> TimeSet:
        """
        Return the union of `self` (S) and `other` (O): S ∪ O.
        """
        if not isinstance(other, TimeSet):
            return NotImplemented
        intersectionless_periods: Set[TimeInterval] = set()
        for p in {*self.intervals, *other.intervals}:
            for per in intersectionless_periods:
                if has_intersection(p, per):
                    intersectionless_periods.discard(per)
                    intersectionless_periods.add(p + per)
                    break
            else:
                intersectionless_periods.add(p)
        result = TimeSet()
        result.intervals = intersectionless_periods
        return result

    def __and__(self, other: TimeSet) -> TimeSet:
        """
        Return the intersection of `self` (S) and `other` (O): S ∩ O.
        """
        if not isinstance(other, TimeSet):
            return NotImplemented
        # Compute the Cartesian product and find all intersections
        intersections = {s & o for s in self.intervals for o in other.intervals}
        intersections.discard(None)
        # TODO on next line switch from [] compasion to {} comparison
        #  after TimeRange has been made hashable
        return reduce(operator.add, [TimeSet(t.start, t.end) for t in intersections], TimeSet())

    @property
    def length(self) -> timedelta:
        return sum([p.length for p in self.intervals], start=timedelta())

    @property
    def start(self) -> Optional[datetime]:
        """
        Return the earliest moment in the TimeRange.
        """
        return min({p.start for p in self.intervals}) if self else None

    @property
    def end(self) -> Optional[datetime]:
        """
        Return the latest moment in the TimeRange.
        """
        return max({p.end for p in self.intervals}) if self else None

    @property
    def start_date(self) -> Optional[date]:
        return self.start.date() if self else None

    @property
    def end_date(self) -> Optional[date]:
        return self.end.date() if self else None
