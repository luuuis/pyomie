from __future__ import annotations

import asyncio
import datetime as dt
import json
import sys
from typing import Awaitable, Callable

import aiohttp
import typer
from aiohttp import ClientSession

from pyomie.main import adjustment_price, spot_price
from pyomie.model import OMIEResults

app = typer.Typer()

_DATE_DEFAULT = "today's date"


def _parse_iso8601_date(a_date: str) -> dt.date:
    if a_date is _DATE_DEFAULT:
        return dt.date.today()
    else:
        return dt.date.fromisoformat(a_date)


@app.command()
def spot(
    date: dt.date = typer.Argument(  # noqa: B008
        default=_DATE_DEFAULT,
        help="Date to fetch in YYYY-MM-DD format",
        parser=_parse_iso8601_date,
    ),
    csv: bool = typer.Option(
        default=False, help="Print the CSV as returned by OMIE, without parsing."
    ),
) -> None:
    """Fetches the OMIE spot price data."""
    _sync_fetch_and_print(spot_price, date, csv)


@app.command()
def adjustment(
    date: dt.date = typer.Argument(  # noqa: B008
        default=_DATE_DEFAULT,
        help="Date to fetch in YYYY-MM-DD format",
        parser=_parse_iso8601_date,
    ),
    csv: bool = typer.Option(
        default=False, help="Print the CSV as returned by OMIE, without parsing."
    ),
) -> None:
    """Fetches the OMIE adjustment mechanism data."""
    _sync_fetch_and_print(adjustment_price, date, csv)


def _sync_fetch_and_print(
    fetch_omie_data: Callable[
        [ClientSession, dt.date], Awaitable[tuple[OMIEResults, str] | None]
    ],
    market_date: dt.date,
    raw: bool,
) -> None:
    async def fetch_and_print() -> None:
        async with aiohttp.ClientSession() as session:
            fetched_data = await fetch_omie_data(session, market_date)
            if fetched_data:
                parsed, unparsed = fetched_data
                sys.stdout.write(unparsed if raw else json.dumps(parsed.contents))

    asyncio.get_event_loop().run_until_complete(fetch_and_print())


if __name__ == "__main__":
    app()
