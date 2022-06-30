import unittest
from unittest import TestCase
from datetime import datetime, timedelta

from .interval import TimeInterval, has_intersection
from .timeset import TimeSet
from .date_range import daterange
from .month import CalendarMonth

date = (2021, 5, 20)
start = datetime(*date, 12, 12)
end = datetime(*date, 14, 12)
string_repr = "TimeSet(start=datetime.datetime(2021, 5, 20, 12, 12), end=datetime.datetime(2021, 5, 20, 14, 12))"


class ContinuousTimeRangeTest(unittest.TestCase):

    def setUp(self) -> None:
        self.timerange = TimeInterval(start, end)

    def test_initialization(self):
        with self.assertRaisesRegex(ValueError, "Start cannot be later than end."):
            TimeInterval(end, start)

    def test_contains(self):
        self.assertTrue(datetime(*date, 13, 12) in self.timerange)
        # Assert that endpoints are included
        self.assertTrue(start in self.timerange)
        self.assertTrue(end in self.timerange)

    def test_does_not_contain(self):
        self.assertFalse(datetime(*date, 22, 12) in self.timerange)

    def test_as_timedelta(self):
        self.assertEqual(TimeInterval(start, start).length, timedelta(hours=0))
        self.assertEqual(self.timerange.length, timedelta(hours=2))

    def test_intersection(self):
        union1 = self.timerange & TimeInterval(datetime(*date, 13, 12), datetime(*date, 22, 12))
        self.assertEqual(union1, TimeInterval(datetime(*date, 13, 12), end))

        union2 = self.timerange & TimeInterval(start, start)
        self.assertEqual(union2, TimeInterval(start, start))

    def test_union(self):
        union1 = self.timerange + TimeInterval(datetime(*date, 13, 12), datetime(*date, 15, 12))
        self.assertEqual(union1, TimeInterval(start, datetime(*date, 15, 12)))

        union2 = self.timerange + TimeInterval(start, start)
        self.assertEqual(union2, TimeInterval(start, end))

    def test_intersects_with(self):
        # Partial intersection
        self.assertTrue(has_intersection(self.timerange,
                                         TimeInterval(datetime(*date, 13, 12), datetime(*date, 15, 12))))

        # Self contains other
        self.assertTrue(has_intersection(self.timerange,
                                         TimeInterval(datetime(*date, 12, 19), datetime(*date, 13, 12))))

        # Other contains self
        self.assertTrue(has_intersection(self.timerange,
                                         TimeInterval(datetime(*date, 11, 12), datetime(*date, 18, 12))))

    def test_does_not_intersect_with(self):
        self.assertFalse(has_intersection(self.timerange,
                                          TimeInterval(datetime(*date, 18, 12), datetime(*date, 19, 12))))

    def test_equality(self):
        self.assertTrue(self.timerange == TimeInterval(self.timerange.start, self.timerange.end))

    def test_inequality(self):
        self.assertFalse(self.timerange != TimeInterval(self.timerange.start, self.timerange.end))
        self.assertFalse(self.timerange == TimeInterval(self.timerange.start, self.timerange.start))

    def test_superset(self):
        # Is superset
        self.assertTrue(self.timerange >= TimeInterval(datetime(*date, 13, 12), datetime(*date, 13, 14)))
        # Is superset (one edge in common)
        self.assertTrue(self.timerange >= TimeInterval(datetime(*date, 12, 12), datetime(*date, 13, 14)))
        # Is not superset (actually self is subset)
        self.assertFalse(self.timerange >= TimeInterval(datetime(*date, 12, 12), datetime(*date, 22, 14)))
        # Is not superset (no intersection)
        self.assertFalse(self.timerange >= TimeInterval(datetime(*date, 18, 12), datetime(*date, 22, 14)))

    def test_subset(self):
        # Is subset
        self.assertTrue(self.timerange <= TimeInterval(datetime(*date, 10, 12), datetime(*date, 18, 14)))
        # Is subset (one edge in common)
        self.assertTrue(self.timerange <= TimeInterval(datetime(*date, 12, 12), datetime(*date, 18, 14)))
        # Is not subset (actually self is superset)
        self.assertFalse(self.timerange <= TimeInterval(datetime(*date, 12, 12), datetime(*date, 13, 14)))
        # Is not subset (no intersection)
        self.assertFalse(self.timerange <= TimeInterval(datetime(*date, 18, 12), datetime(*date, 22, 14)))


class TimeRangeInitializationTest(unittest.TestCase):
    def test_empty_initialization(self):
        t = TimeSet()
        self.assertEqual(str(t), "TimeSet()")

    def test_initialization_with_start_and_end(self):
        t = TimeSet(start=start, end=end)
        self.assertEqual(str(t), string_repr)

    def test_initialization_with_start_and_end_as_dates(self):
        string = "TimeSet(start=datetime.datetime(2021, 5, 20, 0, 0), end=datetime.datetime(2021, 5, 21, 23, 59, 59, 999999))"
        self.assertEqual(str(daterange(start=datetime(2021, 5, 20), end=datetime(2021, 5, 21))), string)

    def test_initialization_with_start_and_duration(self):
        t = TimeSet(start=start, duration=timedelta(hours=8))
        self.assertEqual(t.length, timedelta(hours=8))
        self.assertTrue(start in t)
        self.assertTrue(start + timedelta(hours=8) in t)

    def test_initialization_with_start_and_duration_from_dates(self):
        string = "TimeSet(start=datetime.datetime(2021, 5, 20, 0, 0), end=datetime.datetime(2021, 5, 21, 23, 59, 59, 999999))"
        self.assertEqual(str(daterange(start=datetime(2021, 5, 20), days=1)), string)

    def test_start_end_integrity(self):
        with self.assertRaises(ValueError):
            TimeSet(start=end, end=start)


class TimeRangeBooleanTest(unittest.TestCase):
    def test_bool_true(self):
        t = TimeSet(start=start, end=end)
        self.assertTrue(t)

    def test_bool_false(self):
        t = TimeSet()
        self.assertFalse(t)


class TimeRangeTimedeltaTest(unittest.TestCase):
    def test_timedelta_two_hours(self):
        t = TimeSet(start=start, end=end)
        self.assertEqual(t.length, timedelta(hours=2))

    def test_timedelta_zero(self):
        t = TimeSet()
        self.assertEqual(t.length, timedelta(hours=0))


class TimeRangeContainsTest(unittest.TestCase):
    def test_contains(self):
        t = TimeSet(start=start, end=end)
        self.assertTrue(datetime(2021, 5, 20, 12, 13) in t)

    def test_does_not_contain(self):
        t = TimeSet(start=start, end=end)
        self.assertFalse(datetime(2021, 5, 20, 16, 12) in t)


class TimeRangeAdditionTest(unittest.TestCase):
    def test_no_overlap(self):
        t1 = TimeSet(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeSet(start=datetime(*date, 16), duration=timedelta(hours=2))
        self.assertEqual((t1 + t2).length, timedelta(hours=4))

    def test_one_contains_another(self):
        t1 = TimeSet(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeSet(start=datetime(*date, 13), duration=timedelta(hours=1))
        self.assertEqual((t1 + t2).length, timedelta(hours=2))

    def test_overlap(self):
        t1 = TimeSet(start=datetime(*date, 12), duration=timedelta(hours=3))
        t2 = TimeSet(start=datetime(*date, 13), duration=timedelta(hours=3))
        self.assertEqual((t1 + t2).length, timedelta(hours=4))


class TimeRangeStartEndTest(TestCase):
    compound_timerange = TimeSet(start, datetime(*date, 13, 12)) + TimeSet(datetime(*date, 13, 22), end)

    def test_start(self):
        self.assertEqual(self.compound_timerange.start, start)

    def test_empty_timerange_start(self):
        self.assertEqual(TimeSet().start, None)

    def test_end(self):
        self.assertEqual(self.compound_timerange.end, end)

    def test_empty_timerange_end(self):
        self.assertEqual(TimeSet().end, None)

    def test_start_date(self):
        self.assertEqual(self.compound_timerange.start_date, start.date())

    def test_empty_timerange_start_date(self):
        self.assertEqual(TimeSet().start_date, None)

    def test_end_date(self):
        self.assertEqual(self.compound_timerange.end_date, end.date())

    def test_empty_timerange_end_date(self):
        self.assertEqual(TimeSet().end_date, None)


class TimeRangeIntersectionTest(TestCase):
    def test_intersection(self):
        t1 = TimeSet(start=datetime(*date, 12), end=datetime(*date, 14))
        t2 = TimeSet(start=datetime(*date, 13), end=datetime(*date, 15))
        self.assertEqual(t1 & t2, TimeSet(start=datetime(*date, 13), end=datetime(*date, 14)))

    def test_no_intersection(self):
        t1 = TimeSet(start=datetime(*date, 12), end=datetime(*date, 14))
        t2 = TimeSet(start=datetime(*date, 18), end=datetime(*date, 20))
        self.assertEqual(t1 & t2, TimeSet())

    def test_one_moment_intersection(self):
        t1 = TimeSet(start=datetime(*date, 12), end=datetime(*date, 14))
        t2 = TimeSet(start=datetime(*date, 14), end=datetime(*date, 20))
        self.assertEqual(t1 & t2, TimeSet(start=datetime(*date, 14), end=datetime(*date, 14)))


class CalendarMonthTest(TestCase):
    def test_init(self):
        month = CalendarMonth(year=2021, month=10)
        self.assertEqual(month.year, 2021)
        self.assertEqual(month.month, 10)
        self.assertTrue(datetime(2021, 9, 1) not in month)
        self.assertTrue(datetime(2021, 10, 10) in month)
        self.assertTrue(datetime(2021, 11, 1) not in month)

    def test_next(self):
        month = CalendarMonth(year=2021, month=11)
        self.assertEqual(month.next, CalendarMonth(year=2021, month=12))
        self.assertEqual(month.next.next, CalendarMonth(year=2022, month=1))

    def test_prev(self):
        month = CalendarMonth(year=2021, month=2)
        self.assertEqual(month.prev, CalendarMonth(year=2021, month=1))
        self.assertEqual(month.prev.prev, CalendarMonth(year=2020, month=12))


if __name__ == '__main__':
    unittest.main()
