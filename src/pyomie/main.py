from __future__ import annotations

import csv
import datetime as dt
import logging
from typing import Callable, NamedTuple

from aiohttp import ClientSession

from pyomie.model import OMIEResults

DEFAULT_TIMEOUT = dt.timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)

_HOURS = list(range(25))
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
# | 13:30 | Day-ahead   |      |      |   X    |   X   |
# | 16:30 | Intraday 1  |      |      |   X    |   X   |
# | 18:30 | Intraday 2  |  X   |  X   |   X    |   X   |
# | 22:30 | Intraday 3  |      |      |   X    |   X   |
# ```
#
# References:
# - https://www.omie.es/en/mercado-de-electricidad
# - https://www.omie.es/sites/default/files/inline-files/intraday_and_continuous_markets.pdf

DateFactory = Callable[
    [], dt.date
]  #: Used by the coordinator to work out the market date to fetch.


async def _fetch_to_dict(
    session: ClientSession,
    source: str,
    market_date: dt.date,
    short_names: dict[str, str],
) -> tuple[OMIEResults, str] | None:
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
        hourly_values = {
            row[0]: [
                _to_float(row[h + 1])
                for h in _HOURS
                if len(row) > h + 1 and row[h + 1] != ""
            ]
            for row in rows
        }
        fetched = dt.datetime.now(dt.timezone.utc)

        file_data = {
            "header": header,
            "market_date": market_date.isoformat(),
            "source": source,
        }

        for k in hourly_values:
            hourly = hourly_values[k]
            if k in short_names:
                key = short_names[k]
                file_data.update({f"{key}": hourly})
            else:
                if k:
                    # unknown rows, do not process
                    file_data.update({k: hourly})

        return (
            OMIEResults(
                updated_at=fetched, market_date=market_date, contents=file_data
            ),
            response_text,
        )


async def spot_price(
    client_session: ClientSession, market_date: dt.date
) -> tuple[OMIEResults, str] | None:
    """
    Fetches the marginal price data for a given date.

    :param client_session: the HTTP session to use
    :param market_date: the date to fetch data for
    :return:  an optional tuple containing the parsed and unparsed results
    """
    dc = DateComponents.decompose(market_date)
    source = f"https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_PBC_EV_H_1_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT"

    return await _fetch_to_dict(
        client_session,
        source,
        dc.date,
        {
            "Energía total con bilaterales del mercado Ibérico (MWh)": "energy_with_bilaterals_es_pt",  # noqa: E501
            "Energía total de compra sistema español (MWh)": "energy_purchases_es",
            "Energía total de compra sistema portugués (MWh)": "energy_purchases_pt",
            "Energía total de venta sistema español (MWh)": "energy_sales_es",
            "Energía total de venta sistema portugués (MWh)": "energy_sales_pt",
            "Energía total del mercado Ibérico (MWh)": "energy_es_pt",
            "Exportación de España a Portugal (MWh)": "energy_export_es_to_pt",
            "Importación de España desde Portugal (MWh)": "energy_import_es_from_pt",
            "Precio marginal en el sistema español (EUR/MWh)": "spot_price_es",
            "Precio marginal en el sistema portugués (EUR/MWh)": "spot_price_pt",
        },
    )


async def adjustment_price(
    client_session: ClientSession, market_date: dt.date
) -> tuple[OMIEResults, str] | None:
    """
    Fetches the adjustment mechanism data for a given date.

    :param client_session: the HTTP session to use
    :param market_date: the date to fetch data for
    :return:  an optional tuple containing the parsed and unparsed results
    """
    if market_date < ADJUSTMENT_END_DATE:
        dc = DateComponents.decompose(market_date)
        source = f"https://www.omie.es/sites/default/files/dados/AGNO_{dc.yy}/MES_{dc.MM}/TXT/INT_MAJ_EV_H_{dc.dd_MM_yy}_{dc.dd_MM_yy}.TXT"

        return await _fetch_to_dict(
            client_session,
            source,
            market_date,
            {
                "Precio de ajuste en el sistema español (EUR/MWh)": "adjustment_price_es",  # noqa: E501
                "Precio de ajuste en el sistema portugués (EUR/MWh)": "adjustment_price_pt",  # noqa: E501
                "Energía horaria sujeta al MAJ a los consumidores MIBEL (MWh)": "adjustment_energy",  # noqa: E501
                "Energía horaria sujeta al mecanismo de ajuste a los consumidores MIBEL (MWh)": "adjustment_energy",  # noqa: E501
                "Cuantía unitaria del ajuste (EUR/MWh)": "adjustment_unit_price",
            },
        )

    else:
        # adjustment mechanism ended in 2023
        return None


def _to_float(n: str) -> float | None:
    return n if n is None else float(n.replace(",", "."))


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
