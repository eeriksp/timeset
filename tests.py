import unittest
from datetime import datetime, timedelta

from timeset import TimeRange, ContinuousTimeRange

date = (2021, 5, 20)
start = datetime(*date, 12, 12)
end = datetime(*date, 14, 12)
string_repr = "TimeRange(start=datetime.datetime(2021, 5, 20, 12, 12), end=datetime.datetime(2021, 5, 20, 14, 12))"


class ContinuousTimeRangeTest(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaisesRegex(ValueError, "Start cannot be later than end."):
            ContinuousTimeRange(end, start)

    def test_contains(self):
        timerange= ContinuousTimeRange(start, end)
        self.assertTrue(datetime(*date, 13, 12) in timerange)
        # Assert that endpoints are included
        self.assertTrue(start in timerange)
        self.assertTrue(end in timerange)

class TimeRangeInitializationTest(unittest.TestCase):
    def test_initialization_with_start_and_end(self):
        t = TimeRange(start=start, end=end)
        self.assertEqual(str(t), string_repr)

    def test_empty_initialization(self):
        t = TimeRange()
        self.assertEqual(str(t), "TimeRange()")

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
        t1 = TimeRange.with_duration(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeRange.with_duration(start=datetime(*date, 16), duration=timedelta(hours=2))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=4))

    def test_one_contains_another(self):
        t1 = TimeRange.with_duration(start=datetime(*date, 12), duration=timedelta(hours=2))
        t2 = TimeRange.with_duration(start=datetime(*date, 13), duration=timedelta(hours=1))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=2))

    def test_overlap(self):
        t1 = TimeRange.with_duration(start=datetime(*date, 12), duration=timedelta(hours=3))
        t2 = TimeRange.with_duration(start=datetime(*date, 13), duration=timedelta(hours=3))
        self.assertEqual((t1 + t2).as_timedelta, timedelta(hours=4))


if __name__ == '__main__':
    unittest.main()
