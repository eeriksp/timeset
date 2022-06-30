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

As seen above all the instantiation method create a continuous `TimeSet` consisting of only one interval (or zero intervals). `TimeSet`s which hold multiple intervals are created by adding their parts together using the `+` operator (more on that below).

This is a design decision: we considered `TimeSet(a, b) + TimeSet(c, d)` to be more readable that one longer constructor such as `TimeSet(intervals={[a, b], [c, d]})`.
(If you disagree, feel free to open an issue, this choice is not carved in stone).

### Set operations with `TimeSet`s

Check if two `TimeSet`s are **equal** (if they include the exact same points):

```pycon
>>> TimeSet(start, end) == TimeSet(start, duration=duration)
True
```

Check if a moment is **in** the TimeSet:
```pycon
>>> start in TimeSet(start, end)
True
```

Check if the TimeSet is **empty** (`False` indicates an empty `TimeSet`, `True` indicates a nonempty `TimeSet`):
```pycon
>>> bool(TimeSet(start, end))
True
```

Find the **union (`+`)** of the `TimeSet`s:
```pycon
>>> other_start = end + timedelta(hours=1)
>>> TimeSet(start, end) + TimeSet(other_start , duration=timedelta(hours=1))
TimeSet(start=datetime.datetime(2022, 6, 30, 16, 0), end=datetime.datetime(2022, 6, 30, 17, 0)) + TimeSet(start=datetime.datetime(2022, 6, 30, 12, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
```

Find the **intersection (`&`)** of the `TimeSet`s:
```pycon
>>> other_start = end - timedelta(hours=1)
>>> TimeSet(start, end) & TimeSet(other_start , duration=timedelta(hours=3))
TimeSet(start=datetime.datetime(2022, 6, 30, 14, 0), end=datetime.datetime(2022, 6, 30, 15, 0))
```