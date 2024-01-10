from __future__ import annotations

import asyncio
import datetime as dt
import json
import sys
from typing import Awaitable, Callable, NamedTuple, TypeVar

import aiohttp
import typer
from aiohttp import ClientSession

from pyomie.main import adjustment_price, spot_price
from pyomie.model import OMIEResults

_NamedTupleT = TypeVar("_NamedTupleT", bound=NamedTuple)

app = typer.Typer(add_completion=False)

_DATE_DEFAULT = "today's date"


def _parse_date_arg(a_date: str) -> dt.date:
    if a_date is _DATE_DEFAULT:
        return dt.date.today()
    else:
        return dt.date.fromisoformat(a_date)


@app.command()
def spot(
    date: dt.date = typer.Argument(  # noqa: B008
        default=_DATE_DEFAULT,
        help="Date to fetch in YYYY-MM-DD format",
        parser=_parse_date_arg,
    ),
    csv: bool = typer.Option(
        default=False, help="Print the CSV as returned by OMIE, without parsing."
    ),
) -> None:
    """Fetch the OMIE spot price data."""
    _fetch_and_print(spot_price, date, csv)


@app.command()
def adjustment(
    date: dt.date = typer.Argument(  # noqa: B008
        default=_DATE_DEFAULT,
        help="Date to fetch in YYYY-MM-DD format",
        parser=_parse_date_arg,
    ),
    csv: bool = typer.Option(
        default=False, help="Print the CSV as returned by OMIE, without parsing."
    ),
) -> None:
    """Fetch the OMIE adjustment mechanism data (2022-06-14 to 2023-12-31)."""
    _fetch_and_print(adjustment_price, date, csv)


def _fetch_and_print(
    fetch_omie_data: Callable[
        [ClientSession, dt.date], Awaitable[OMIEResults[_NamedTupleT] | None]
    ],
    market_date: dt.date,
    print_raw: bool,
) -> None:
    async def fetch_and_print() -> None:
        async with aiohttp.ClientSession() as session:
            fetched_data = await fetch_omie_data(session, market_date)
            if fetched_data:
                # noinspection PyProtectedMember
                sys.stdout.write(
                    fetched_data.raw
                    if print_raw
                    else json.dumps(fetched_data.contents._asdict())
                )

    asyncio.get_event_loop().run_until_complete(fetch_and_print())


if __name__ == "__main__":
    app()
