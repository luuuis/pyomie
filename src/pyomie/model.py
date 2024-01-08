from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Generic, NamedTuple, TypeVar

_LOGGER = logging.getLogger(__name__)

OMIEDayHours = list[float]
#: A sequence of hourly values relating to a single day.

OMIEDataSeries = dict[str, OMIEDayHours]
#: A dict containing hourly data for several data series.

_DataT = TypeVar("_DataT")


#: TypeVar used for generic named tuples


class SpotData(NamedTuple):
    """OMIE marginal price market results for a given date."""

    url: str
    """URL where the data was obtained"""
    market_date: str
    """The date that these results pertain to."""
    header: str
    """File header."""

    energy_total_es_pt: OMIEDayHours
    energy_purchases_es: OMIEDayHours
    energy_purchases_pt: OMIEDayHours
    energy_sales_es: OMIEDayHours
    energy_sales_pt: OMIEDayHours
    energy_es_pt: OMIEDayHours
    energy_export_es_to_pt: OMIEDayHours
    energy_import_es_from_pt: OMIEDayHours
    spot_price_es: OMIEDayHours
    spot_price_pt: OMIEDayHours


class AdjustmentData(NamedTuple):
    """OMIE marginal price (spot) market results for a given date."""

    url: str
    """URL where the data was obtained"""
    market_date: str
    """The date that these results pertain to."""
    header: str
    """File header."""

    adjustment_price_es: OMIEDayHours
    adjustment_price_pt: OMIEDayHours
    adjustment_energy: OMIEDayHours
    adjustment_unit_price: OMIEDayHours


class OMIEResults(NamedTuple, Generic[_DataT]):
    """OMIE market results for a given date."""

    updated_at: datetime
    """The fetch date/time."""

    market_date: date
    """The day that the data relates to."""

    contents: _DataT
    """The data fetched from OMIE."""

    raw: str
    """The raw text as returned from OMIE."""
