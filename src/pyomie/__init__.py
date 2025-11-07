__version__ = "1.1.3"

import datetime as dt
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

QUARTER_HOURLY_START_DATE = dt.date(2025, 10, 1)
#: The date on which the SDAC changed over to quarter-hourly pricing.
