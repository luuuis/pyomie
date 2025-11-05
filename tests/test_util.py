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
