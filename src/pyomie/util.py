import datetime as dt
from zoneinfo import ZoneInfo

from pyomie.model import OMIEDayQuarters

_CET = ZoneInfo("CET")
_UTC = ZoneInfo("Etc/UTC")


def localize_quarter_hourly_data(
    date: dt.date,
    quarter_hourly_data: OMIEDayQuarters,
) -> dict[str, float]:
    """
    Localize incoming quarter-hourly data to the CET timezone.

    This is especially useful on days that are DST boundaries and
    that may have 23 or 25 hours to avoid any ambiguities in the data.

    The quarter-hours are stepped forward in real elapsed time from the
    market day's local midnight, so each key carries the UTC offset that
    is in effect at its own instant: the repeated hour of a fall-back day
    is served by both of its occurrences, and the missing hour of a
    spring-forward day simply never appears.

    :param date: the date that the values relate to
    :param quarter_hourly_data: the quarter-hourly values
    :return: a dict containing the hourly values indexed by their starting
             time (ISO8601 formatted)
    """
    midnight = dt.datetime(date.year, date.month, date.day, tzinfo=_CET)
    # Adding a timedelta to a CET-aware datetime moves the wall clock and
    # keeps the offset that ZoneInfo resolves for the resulting wall time,
    # so on a boundary day every key after the transition lands on the wrong
    # instant. Stepping in UTC keeps the quarter-hours real instead.
    day_start = midnight.astimezone(_UTC)
    quarter_hour = dt.timedelta(minutes=15)

    return {
        (day_start + quarter_hour * qh).astimezone(_CET).isoformat(): datum
        for qh, datum in enumerate(quarter_hourly_data)
    }
