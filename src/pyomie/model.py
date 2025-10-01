from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Generic, NamedTuple, TypeVar

_LOGGER = logging.getLogger(__name__)

OMIEDayHours = list[float]
#: A sequence of quarter-hourly values relating to a single day (up to 96 values).

OMIEDataSeries = dict[str, OMIEDayHours]
#: A dict containing quarter-hourly data for several data series.

_DataT = TypeVar("_DataT")


#: TypeVar used for generic named tuples


class SpotData(NamedTuple):
    """OMIE marginal price market results for a given date.
    
    Note: Data format has evolved from hourly (H1-H24) to quarter-hourly (H1Q1-H24Q4).
    This class supports both formats automatically.
    """

    url: str
    """URL where the data was obtained"""
    market_date: str
    """The date that these results pertain to."""
    header: str
    """File header."""

    energy_total_es_pt: OMIEDayHours
    """Total energy with bilateral contracts in the Iberian market (MWh)"""
    energy_purchases_es: OMIEDayHours
    """Total energy purchases in the Spanish system (MWh)"""
    energy_purchases_pt: OMIEDayHours
    """Total energy purchases in the Portuguese system (MWh)"""
    energy_sales_es: OMIEDayHours
    """Total energy sales in the Spanish system (MWh)"""
    energy_sales_pt: OMIEDayHours
    """Total energy sales in the Portuguese system (MWh)"""
    energy_es_pt: OMIEDayHours
    """Total energy in the Iberian market (MWh)"""
    energy_export_es_to_pt: OMIEDayHours
    """Energy exports from Spain to Portugal (MWh)"""
    energy_import_es_from_pt: OMIEDayHours
    """Energy imports from Portugal to Spain (MWh)"""
    spot_price_es: OMIEDayHours
    """Marginal price in the Spanish system (EUR/MWh)"""
    spot_price_pt: OMIEDayHours
    """Marginal price in the Portuguese system (EUR/MWh)"""


class AdjustmentData(NamedTuple):
    """OMIE adjustment mechanism results for a given date.
    
    Note: Data format has evolved from hourly (H1-H24) to quarter-hourly (H1Q1-H24Q4).
    This class supports both formats automatically.
    """

    url: str
    """URL where the data was obtained"""
    market_date: str
    """The date that these results pertain to."""
    header: str
    """File header."""

    adjustment_price_es: OMIEDayHours
    """Adjustment price in the Spanish system (EUR/MWh)"""
    adjustment_price_pt: OMIEDayHours
    """Adjustment price in the Portuguese system (EUR/MWh)"""
    adjustment_energy: OMIEDayHours
    """Hourly energy subject to the adjustment mechanism for MIBEL consumers (MWh)"""
    adjustment_unit_price: OMIEDayHours
    """Unit adjustment amount (EUR/MWh)"""


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
