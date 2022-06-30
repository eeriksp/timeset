from __future__ import annotations

from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from .awareness import ensure_aware


@dataclass(frozen=True)
class ContinuousTimeRange:
    """
    Represent a continuous period of time from `start` to `end`.
    """
    start: datetime
    end: datetime

    def __post_init__(self):
        object.__setattr__(self, 'start', ensure_aware(self.start))
        object.__setattr__(self, 'end', ensure_aware(self.end))
        if self.start > self.end:
            raise ValueError("Start cannot be later than end.")

    def __contains__(self, moment: datetime) -> bool:
        return self.start <= moment <= self.end

    @property
    def length(self) -> timedelta:
        return self.end - self.start

    def __and__(self, other: ContinuousTimeRange) -> Optional[ContinuousTimeRange]:
        """
        Return the intersection of `self` (S) and `other` (O): S ∩ O.
        """
        if type(self) != type(other):
            return NotImplemented
        if not has_intersection(self, other):
            return None
        return ContinuousTimeRange(max(self.start, other.start), min(self.end, other.end))

    def __add__(self, other) -> Optional[ContinuousTimeRange]:
        """
        Return the union of `self` (S) and `other` (O): S ∪ O.
        """
        if type(self) != type(other):
            return NotImplemented
        if not has_intersection(self, other):
            return None
        return ContinuousTimeRange(min(self.start, other.start), max(self.end, other.end))

    def __ge__(self, other) -> bool:  # TODO TEST
        """
        Check if `self` (S) is a superset of `other` (O): S ⊇ O.
        """
        return self.start <= other.start and other.end <= self.end

    def __le__(self, other) -> bool:  # TODO TEST
        """
        Check if `self` (S) is a subset of `other` (O): S ⊆ O.
        """
        return other.start <= self.start and self.end <= other.end


def has_intersection(a: ContinuousTimeRange, b: ContinuousTimeRange) -> bool:
    """
    Indicates whether `a` and `b` have an intersection, any points belonging to both sets.
    """
    return b.start in a or b.end in a or a <= b
