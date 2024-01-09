from __future__ import annotations

import csv
import datetime as dt
import logging
from typing import Callable, NamedTuple, TypeVar

from aiohttp import ClientSession

from pyomie.model import (
    AdjustmentData,
    OMIEDataSeries,
    OMIEResults,
    SpotData,
)

DEFAULT_TIMEOUT = dt.timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)


_DataT = TypeVar("_DataT")

_HOURS = list(range(1, 26))
#: Max number of hours in a day (on the day that DST ends).

ADJUSTMENT_END_DATE = dt.date(2024, 1, 1)
#: The date on which the adjustment mechanism is no longer applicable.

# language=Markdown
#
# OMIE market sessions and the values that they influence. Time shown below
# is publication time in the CET timezone plus 10 minutes.
#
# ```
# | Time  | Name        | Spot | Adj  | Spot+1 | Ajd+1 |
# |-------|-------------|------|------|--------|-------|
# | 02:30 | Intraday 4  |  X   |  X   |        |       |
# | 05:30 | Intraday 5  |  X   |  X   |        |       |
# | 10:30 | Intraday 6  |  X   |  X   |        |       |
# | 16:30 | Intraday 1  |      |      |   X    |   X   |
# | 18:30 | Intraday 2  |  X   |  X   |   X    |   X   |
# | 22:30 | Intraday 3  |      |      |   X    |   X   |
# ```
#
# References:
# - https://www.omie.es/en/mercado-de-electricidad
# - https://www.omie.es/sites/default/files/inline-files/intraday_and_continuous_markets.pdf

DateFactory = Callable[[], dt.date]
#: Used by the coordinator to work out the market date to fetch.

OMIEDataT = TypeVar("OMIEDataT")
#: Generic data contained within an OMIE result


class OMIEDayResult(NamedTuple):
    """Data pertaining to a single day exposed in OMIE APIs."""

    url: str
    """URL where the data was obtained"""
    market_date: dt.date
    """The date that these results pertain to."""
    header: str
    """File header."""
    series: OMIEDataSeries
    """Series data for the given day."""


async def _fetch_and_make_results(
    session: ClientSession,
    source: str,
    market_date: dt.date,
    make_result: Callable[[OMIEDayResult], OMIEDataT],
) -> OMIEResults[OMIEDataT] | None:
    async with await session.get(
        source, timeout=DEFAULT_TIMEOUT.total_seconds()
    ) as resp:
        if resp.status == 404:
            return None

        response_text = await resp.text(encoding="iso-8859-1")
        lines = response_text.splitlines()
        header = lines[0]
        csv_data = lines[2:]

        reader = csv.reader(csv_data, delimiter=";", skipinitialspace=True)
        rows = list(reader)
        day_series: OMIEDataSeries = {
            row[0]: [_to_float(row[h]) for h in _HOURS if len(row) > h and row[h]]
            for row in rows
        }

        omie_meta = OMIEDayResult(
            header=header,
            market_date=market_date,
            url=source,
            series=day_series,
        )

        return OMIEResults(
            updated_at=dt.datetime.now(dt.timezone.utc),
            market_date=market_date,
            contents=make_result(omie_meta),
            raw=response_text,
        )


async def spot_price(
    client_session: ClientSession, market_date: dt.date
) -> OMIEResults[SpotData] | None:
    """
    Fetches the marginal price data for a given date.

    :param client_session: the HTTP session to use
    :param market_date: the date to fetch data for
    :return: the SpotData or None
    """
    dc = DateComponents.decompose(market_date)
    source = f"https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_PBC_EV_H_1_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT"

    return await _fetch_and_make_results(
        client_session, source, dc.date, _make_spot_data
    )


async def adjustment_price(
    client_session: ClientSession, market_date: dt.date
) -> OMIEResults[AdjustmentData] | None:
    """
    Fetches the adjustment mechanism data for a given date.

    :param client_session: the HTTP session to use
    :param market_date: the date to fetch data for
    :return: the AdjustmentData or None
    """
    if market_date < ADJUSTMENT_END_DATE:
        dc = DateComponents.decompose(market_date)
        source = f"https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_MAJ_EV_H_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT"

        return await _fetch_and_make_results(
            client_session, source, market_date, _make_adjustment_data
        )

    else:
        # adjustment mechanism ended in 2023
        return None


def _to_float(n: str) -> float:
    return float(n.replace(",", "."))


def _make_spot_data(res: OMIEDayResult) -> SpotData:
    s = res.series
    return SpotData(
        header=res.header,
        market_date=res.market_date.isoformat(),
        url=res.url,
        energy_total_es_pt=s["Energía total con bilaterales del mercado Ibérico (MWh)"],
        energy_purchases_es=s["Energía total de compra sistema español (MWh)"],
        energy_purchases_pt=s["Energía total de compra sistema portugués (MWh)"],
        energy_sales_es=s["Energía total de venta sistema español (MWh)"],
        energy_sales_pt=s["Energía total de venta sistema portugués (MWh)"],
        energy_es_pt=s["Energía total del mercado Ibérico (MWh)"],
        energy_export_es_to_pt=s["Exportación de España a Portugal (MWh)"],
        energy_import_es_from_pt=s["Importación de España desde Portugal (MWh)"],
        spot_price_es=s["Precio marginal en el sistema español (EUR/MWh)"],
        spot_price_pt=s["Precio marginal en el sistema portugués (EUR/MWh)"],
    )


def _make_adjustment_data(res: OMIEDayResult) -> AdjustmentData:
    s = res.series
    return AdjustmentData(
        header=res.header,
        market_date=res.market_date.isoformat(),
        url=res.url,
        adjustment_price_es=s["Precio de ajuste en el sistema español (EUR/MWh)"],
        adjustment_price_pt=s["Precio de ajuste en el sistema portugués (EUR/MWh)"],
        adjustment_energy=s[
            "Energía horaria sujeta al mecanismo de ajuste a los consumidores MIBEL (MWh)"  # noqa: E501
        ],
        adjustment_unit_price=s["Cuantía unitaria del ajuste (EUR/MWh)"],
    )


class DateComponents(NamedTuple):
    """A Date formatted for use in OMIE data file names."""

    date: dt.date
    yy: str
    MM: str
    dd: str
    dd_MM_yy: str

    @staticmethod
    def decompose(a_date: dt.date) -> DateComponents:
        """Creates a `DateComponents` from a `datetime.date`."""
        year = a_date.year
        month = str.zfill(str(a_date.month), 2)
        day = str.zfill(str(a_date.day), 2)
        return DateComponents(
            date=a_date,
            yy=str(year),
            MM=month,
            dd=day,
            dd_MM_yy=f"{day}_{month}_{year}",
        )
