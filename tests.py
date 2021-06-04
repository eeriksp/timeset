import unittest
from datetime import datetime, timedelta

from timeset import TimeRange, ContinuousTimeRange

date = (2021, 5, 20)
start = datetime(*date, 12, 12)
end = datetime(*date, 14, 12)
string_repr = "TimeRange(start=datetime.datetime(2021, 5, 20, 12, 12), end=datetime.datetime(2021, 5, 20, 14, 12))"


class ContinuousTimeRangeTest(unittest.TestCase):

    def setUp(self) -> None:
        self.timerange = ContinuousTimeRange(start, end)

    def test_initialization(self):
        with self.assertRaisesRegex(ValueError, "Start cannot be later than end."):
            ContinuousTimeRange(end, start)

    def test_contains(self):
        self.assertTrue(datetime(*date, 13, 12) in self.timerange)
        # Assert that endpoints are included
        self.assertTrue(start in self.timerange)
        self.assertTrue(end in self.timerange)

    def test_does_not_contain(self):
        self.assertFalse(datetime(*date, 22, 12) in self.timerange)

    def test_as_timedelta(self):
        self.assertEqual(ContinuousTimeRange(start, start).as_timedelta, timedelta(hours=0))
        self.assertEqual(self.timerange.as_timedelta, timedelta(hours=2))

    def test_intersection(self):
        union1 = self.timerange & ContinuousTimeRange(datetime(*date, 13, 12), datetime(*date, 22, 12))
        self.assertEqual(union1, ContinuousTimeRange(datetime(*date, 13, 12), end))

        union2 = self.timerange & ContinuousTimeRange(start, start)
        self.assertEqual(union2, ContinuousTimeRange(start, start))

    def test_union(self):
        union1 = self.timerange + ContinuousTimeRange(datetime(*date, 13, 12), datetime(*date, 15, 12))
        self.assertEqual(union1, ContinuousTimeRange(start, datetime(*date, 15, 12)))

        union2 = self.timerange + ContinuousTimeRange(start, start)
        self.assertEqual(union2, ContinuousTimeRange(start, end))

    def test_intersects_with(self):
        self.assertTrue(self.timerange.intersects_with(
            ContinuousTimeRange(datetime(*date, 13, 12), datetime(*date, 15, 12))))

    def test_does_not_intersect_with(self):
        self.assertFalse(self.timerange.intersects_with(
            ContinuousTimeRange(datetime(*date, 18, 12), datetime(*date, 19, 12))))


class TimeRangeInitializationTest(unittest.TestCase):
    def test_empty_initialization(self):
        t = TimeRange()
        self.assertEqual(str(t), "TimeRange()")

    def test_initialization_with_start_and_end(self):
        t = TimeRange(start=start, end=end)
        self.assertEqual(str(t), string_repr)

    def test_initialization_with_start_and_duration(self):
        t = TimeRange(start=start, duration=timedelta(hours=8))
        self.assertEqual(t.as_timedelta, timedelta(hours=8))
        self.assertTrue(start in t)
        self.assertTrue(start + timedelta(hours=8) in t)

    def test_start_end_integrity(self):
        with self.assertRaises(ValueError):
            TimeRange(start=end, end=start)


class TimeRangeBooleanTest(unittest.TestCase):
    def test_bool_true(self):
        t = TimeRange(start=start, end=end)
        self.assertTrue(t)

    def test_bool_false(self):
        t = TimeRange()
        self.assertFalse(t)


class TimeRangeTimedeltaTest(unittest.TestCase):
    def test_timedelta_two_hours(self):
        t = TimeRange(start=start, end=end)
        self.assertEqual(t.as_timedelta, timedelta(hours=2))

    def test_timedelta_zero(self):
        t = TimeRange()
        self.assertEqual(t.as_timedelta, timedelta(hours=0))


class TimeRangeContainsTest(unittest.TestCase):
    def test_contains(self):
        t = TimeRange(start=start, end=end)
        self.assertTrue(datetime(2021, 5, 20, 12, 13) in t)

    def test_does_not_contain(self):
        t = TimeRange(start=start, end=end)
        self.assertFalse(datetime(2021, 5, 20, 16, 12) in t)


class TimeRangeAdditionTest(unittest.TestCase):
    def test_no_overlap(self):
        t1 = TimeRange(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeRange(start=datetime(*date, 16), duration=timedelta(hours=2))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=4))

    def test_one_contains_another(self):
        t1 = TimeRange(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeRange(start=datetime(*date, 13), duration=timedelta(hours=1))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=2))

    def test_overlap(self):
        t1 = TimeRange(start=datetime(*date, 12), duration=timedelta(hours=3))
        t2 = TimeRange(start=datetime(*date, 13), duration=timedelta(hours=3))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=4))


if __name__ == '__main__':
    unittest.main()
