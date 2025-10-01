from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Generic, NamedTuple, TypeVar

_LOGGER = logging.getLogger(__name__)

OMIEDayQuarters = list[float]
#: A sequence of quarter-hourly values relating to a single day.

OMIEDataSeries = dict[str, OMIEDayQuarters]
#: A dict containing quarter-hourly data for several data series.

_DataT = TypeVar("_DataT")
#: TypeVar used for generic named tuples


class SpotData(NamedTuple):
    """OMIE spot price market results for a given date (quarter-hourly)."""

    url: str
    """URL where the data was obtained"""
    market_date: str
    """The date that these results pertain to."""
    header: str
    """File header."""

    es_pt_total_power: OMIEDayQuarters
    """Total power including bilateral contracts on the Iberian market (MW)."""
    es_purchases_power: OMIEDayQuarters
    """Total power of purchases in Spain (MW)."""
    pt_purchases_power: OMIEDayQuarters
    """Total power of purchases in Portugal (MW)."""
    es_sales_power: OMIEDayQuarters
    """Total power of sales in Spain (MW)."""
    pt_sales_power: OMIEDayQuarters
    """Total power of sales in Portugal (MW)."""
    es_pt_power: OMIEDayQuarters
    """Total power on the Iberian market (MW)."""
    es_to_pt_exports_power: OMIEDayQuarters
    """Exports from Spain to Portugal (MW)."""
    es_from_pt_imports_power: OMIEDayQuarters
    """Imports from Portugal to Spain (MW)."""
    es_spot_price: OMIEDayQuarters
    """Spot price in Spain (EUR/MWh)."""
    pt_spot_price: OMIEDayQuarters
    """Spot price in Portugal (EUR/MWh)."""


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
