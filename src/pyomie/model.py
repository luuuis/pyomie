from __future__ import annotations

import logging
from datetime import date, datetime
from typing import NamedTuple, Union

_LOGGER = logging.getLogger(__name__)

OMIEFile = dict[str, Union[float, list[float]]]
#: A dict parsed from one of the OMIE CSV file.


class OMIEResults(NamedTuple):
    """OMIE market results for a given date."""

    updated_at: datetime
    """The fetch date/time."""

    market_date: date
    """The day that the data relates to."""

    contents: OMIEFile
    """Data fetched from OMIE."""
