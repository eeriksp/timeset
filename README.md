# TimeSet

A Python datastructure for working with overlapping time periods.

## Quickstart

The heart of the `timeset` package is the `TimeSet` class which represents a set of time intervals (e.g. "from `2020-07-10 15:00` to `2020-07-10 16:00` and from `2020-07-10 19:00` to `2020-07-10 19:30`"). A `TimeSet` can of course also contain only one interval or even be empty.

There are three ways to instantiate a `TimeSet`:

```pycon
>>> from datetime import datetime, timedelta
>>> from timeset import TimeSet
>>>
>>> # 1. Instantiate an empty TimeSet
>>> TimeSet()
TimeSet()
>>>
>>> # 2. Instantiate a TimeSet as and interval from `start` to `end`
>>> start = datetime(2022, 6, 30, 12, 0)
>>> end = datetime(2022, 6, 30, 15, 0)
>>> TimeSet(start=start, end=end)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>> # Or using the shorter notation
>>> TimeSet(start, end)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>>
>>> # 3. Instantiate a TimeSet using `start` and `duration`
>>> TimeSet(start=start, duration=timedelta(hours=3))
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>> # Or using the shorter notation
>>> TimeSet(start, duration=timedelta(hours=3))
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
```


