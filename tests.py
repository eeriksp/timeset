import unittest
from datetime import datetime, timedelta

from timeset import TimeRange

start = datetime(2021, 5, 20, 12, 12)
end = datetime(2021, 5, 20, 14, 12)
string_repr = "TimeRange(start=datetime.datetime(2021, 5, 20, 12, 12), end=datetime.datetime(2021, 5, 20, 14, 12))"


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
        self.assertTrue(datetime(2021, 5, 20, 12, 19) in t)


if __name__ == '__main__':
    unittest.main()
