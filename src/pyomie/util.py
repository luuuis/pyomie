import datetime as dt

from zoneinfo import ZoneInfo

from pyomie.model import OMIEDayHours

_CET = ZoneInfo("CET")


def localize_hourly_data(
    date: dt.date,
    hourly_data: OMIEDayHours,
) -> dict[str, float]:
    """
    Localize incoming hourly data to the CET timezone.

    This is especially useful on days that are DST boundaries and
    that may have 23 or 25 hours.

    :param date: the date that the values relate to
    :param hourly_data: the hourly values
    :return: a dict containing the hourly values indexed by their starting
             time (ISO8601 formatted)
    """
    hours_in_day = len(
        hourly_data
    )  # between 23 and 25 (inclusive) due to DST changeover
    midnight = dt.datetime(date.year, date.month, date.day, tzinfo=_CET).astimezone(
        dt.timezone.utc
    )

    return {
        (midnight + dt.timedelta(hours=h)).astimezone(_CET).isoformat(): hourly_data[h]
        for h in range(hours_in_day)
    }
