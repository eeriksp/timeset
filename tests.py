import unittest
from datetime import datetime

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


if __name__ == '__main__':
    unittest.main()
