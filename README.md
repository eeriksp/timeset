# TimeSet

A Python datastructure for working with overlapping time periods.

## Quickstart

The heart of the `timeset` package is the `TimeSet` class which represents a set of time intervals (e.g. "from `2020-07-10 15:00` to `2020-07-10 16:00` and from `2020-07-10 19:00` to `2020-07-10 19:30`"). A `TimeSet` can of course also contain only one interval or even be empty.

The following code snippets assume these imports and variables:

```pycon
>>> from datetime import datetime, timedelta
>>> from timeset import TimeSet
>>>
>>> start = datetime(2022, 6, 30, 12, 0)
>>> end = datetime(2022, 6, 30, 15, 0)
>>> duration = timedelta(hours=3)
```

### Instantiating a `TimeSet`

There are three ways to instantiate a `TimeSet`:

```pycon
>>> # 1. Instantiate an empty TimeSet
>>> TimeSet()
TimeSet()
>>>
>>> # 2. Instantiate a TimeSet as and interval from `start` to `end`
>>> TimeSet(start=start, end=end)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>> # Or using the shorter notation
>>> TimeSet(start, end)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>>
>>> # 3. Instantiate a TimeSet using `start` and `duration`
>>> TimeSet(start=start, duration=duration)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
>>> # Or using the shorter notation
>>> TimeSet(start, duration=duration)
TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
```

### Set operations with `TimeSet`s

Check if two `TimeSet`s are equal (if they include the exact same points):

```pycon
>>> TimeSet(start, end) == TimeSet(start, duration=duration)
True
```

Check if a moment is in the TimeSet:
```pycon
>>> start in TimeSet(start, end)
True
```