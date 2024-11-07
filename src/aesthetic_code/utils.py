from pptx.util import Length


def unit_conversion(value: Length | None, unit: str) -> int | float:
    if value is None:
        raise ValueError("Value cannot be None")

    if unit == "cm":
        return value.cm
    elif unit == "inches" or unit == "in" or unit == "inch":
        return value.inches
    elif unit == "pt":
        return value.pt
    elif unit == "emu":
        return value.emu
    else:
        raise ValueError(f"Invalid measurement unit: {unit}")


def interval_minus_interval(interval1: tuple, interval2: tuple) -> list[tuple]:
    """
    Subtract intervals from another interval.
    interval1 - interval2
    """
    if interval1[1] < interval2[0] or interval2[1] < interval1[0]:
        return [interval1]
    elif interval1[0] <= interval2[0] and interval1[1] >= interval2[1]:
        return [(interval1[0], interval2[0]), (interval2[1], interval1[1])]
    elif interval1[0] <= interval2[0]:
        return [(interval1[0], interval2[0])]
    elif interval1[1] >= interval2[1]:
        return [(interval2[1], interval1[1])]
    else:
        return [interval1]


def intervals_minus_interval(intervals: list[tuple], interval: tuple) -> list[tuple]:
    """
    Subtract an interval from a list of intervals.
    intervals - interval
    """
    result = []
    for i in intervals:
        result.extend(interval_minus_interval(i, interval))
    return result
