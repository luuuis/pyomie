import datetime as dt

from zoneinfo import ZoneInfo

from pyomie.model import OMIEDayQuarters

_CET = ZoneInfo("CET")


def localize_quarter_hourly_data(
    date: dt.date,
    quarter_hourly_data: OMIEDayQuarters,
) -> dict[str, float]:
    """
    Localize incoming quarter-hourly data to the CET timezone.

    This is especially useful on days that are DST boundaries and
    that may have 23 or 25 hours to avoid any ambiguities in the data.

    :param date: the date that the values relate to
    :param quarter_hourly_data: the quarter-hourly values
    :return: a dict containing the hourly values indexed by their starting
             time (ISO8601 formatted)
    """
    midnight = dt.datetime(date.year, date.month, date.day, tzinfo=_CET)

    return {
        (midnight + dt.timedelta(minutes=15 * qh)).isoformat(): datum
        for qh, datum in enumerate(quarter_hourly_data)
    }
