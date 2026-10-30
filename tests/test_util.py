import datetime as dt

from pyomie.model import OMIEDayQuarters
from pyomie.util import localize_quarter_hourly_data

PRICES: OMIEDayQuarters = [1, 2, 3, 4, 5]


def test_localize_quarter_hourly_data():
    two_hours_prices: OMIEDayQuarters = [0.0, 0.25, 0.50, 0.75, 1.0, 1.25, 1.50, 1.75]
    two_hours = localize_quarter_hourly_data(dt.date(2024, 4, 20), two_hours_prices)
    assert two_hours == {
        "2024-04-20T00:00:00+02:00": 0.0,
        "2024-04-20T00:15:00+02:00": 0.25,
        "2024-04-20T00:30:00+02:00": 0.5,
        "2024-04-20T00:45:00+02:00": 0.75,
        "2024-04-20T01:00:00+02:00": 1.0,
        "2024-04-20T01:15:00+02:00": 1.25,
        "2024-04-20T01:30:00+02:00": 1.5,
        "2024-04-20T01:45:00+02:00": 1.75,
    }

    date = dt.date(2025, 10, 2)

    # pattern [h.0, h.25, h.5, h.75] repeats for every hour
    full_day_prices: OMIEDayQuarters = [
        price for h in range(24) for price in [h, h + 0.25, h + 0.5, h + 0.75]
    ]
    full_day = localize_quarter_hourly_data(date, full_day_prices)

    assert len(full_day) == 96
    for isodatetime, price in full_day.items():
        start_time = dt.datetime.fromisoformat(isodatetime)

        assert start_time.date() == date

        # expected hour+minute is encoded into the price
        assert start_time.hour == int(price)
        assert start_time.minute / 60 == price % 1


def _localized_quarter_hours(date: dt.date, quarter_hours: int) -> dict[str, float]:
    """
    Localize placeholder values for `date` and check their keys are real instants.

    Returns the localized data so each caller can assert the instants of
    specific quarter-hours as well.
    """
    prices: OMIEDayQuarters = [qh / 4 for qh in range(quarter_hours)]
    localized = localize_quarter_hourly_data(date, prices)

    # every value of the day must get its own key, in the order given
    assert len(localized) == quarter_hours
    assert list(localized.values()) == prices

    # the keys must be real instants, strictly increasing and 15 minutes apart
    instants = [dt.datetime.fromisoformat(iso) for iso in localized]
    first = instants[0]
    assert all(
        instant - first == dt.timedelta(minutes=15) * qh
        for qh, instant in enumerate(instants)
    )

    return localized


def test_localize_quarter_hourly_data_on_dst_fall_back_day():
    """A 25-hour CET day (2026-10-25) must serve all of its 100 quarter-hours."""
    keys = list(_localized_quarter_hours(dt.date(2026, 10, 25), 25 * 4))

    # qh 11 and qh 12 straddle the 03:00+02:00 -> 02:00+01:00 change: the
    # repeated hour is served twice, once under each offset. The buggy keys
    # jumped from 00:45Z to 02:00Z, leaving 01:00-01:45Z unaddressed.
    assert keys[11] == "2026-10-25T02:45:00+02:00"
    assert keys[12] == "2026-10-25T02:00:00+01:00"

    # every later key carries the offset in effect at its own instant, so it
    # is one hour earlier in UTC than the wall-clock arithmetic produced
    assert keys[71] == "2026-10-25T16:45:00+01:00"

    # the day ends at its local midnight minus one quarter-hour, not later:
    # the 4 keys past 23:00Z the buggy code produced were the next day's
    assert keys[-1] == "2026-10-25T23:45:00+01:00"


def test_localize_quarter_hourly_data_on_dst_spring_forward_day():
    """A 23-hour CET day (2027-03-28) has only 92 quarter-hours to serve."""
    keys = list(_localized_quarter_hours(dt.date(2027, 3, 28), 23 * 4))

    # 02:00-02:45 local does not exist on this day, so the 8th quarter-hour
    # is already summer time; the buggy code reused the skipped hour instead,
    # which collapsed the day's 92 values onto 88 instants
    assert keys[7] == "2027-03-28T01:45:00+01:00"
    assert keys[8] == "2027-03-28T03:00:00+02:00"

    assert keys[-1] == "2027-03-28T23:45:00+02:00"
    assert not any(dt.datetime.fromisoformat(key).hour == 2 for key in keys)
