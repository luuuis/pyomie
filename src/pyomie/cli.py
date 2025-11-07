from __future__ import annotations

import asyncio
import datetime as dt
import json
import logging
import sys
from typing import Awaitable, Callable, NamedTuple, TypeVar

import aiohttp
import typer
from aiohttp import ClientSession

from . import LOGGER, QUARTER_HOURLY_START_DATE
from .main import spot_price
from .model import OMIEResults

_NamedTupleT = TypeVar("_NamedTupleT", bound=NamedTuple)

app = typer.Typer(add_completion=False)

_DATE_DEFAULT = "today's date"


def _parse_date_arg(a_date: str) -> dt.date:
    date = dt.date.fromisoformat(a_date) if a_date != _DATE_DEFAULT else dt.date.today()
    if date < QUARTER_HOURLY_START_DATE:
        raise typer.BadParameter(
            f"Dates earlier than {QUARTER_HOURLY_START_DATE} are not supported."
        )

    return date


@app.command()
def spot(
    date: dt.date = typer.Argument(  # noqa: B008
        default=_DATE_DEFAULT,
        help="Date to fetch in YYYY-MM-DD format",
        parser=_parse_date_arg,
    ),
    csv: bool = typer.Option(
        False,
        "--csv",
        is_flag=True,
        help="Print the CSV as returned by OMIE, without parsing.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        is_flag=True,
        help="Verbose mode.",
    ),
) -> None:
    """Fetch the OMIE spot price data."""
    _configure_logging(verbose)
    _fetch_and_print(spot_price, date, csv, verbose)


def _fetch_and_print(
    fetch_omie_data: Callable[
        [ClientSession, dt.date], Awaitable[OMIEResults[_NamedTupleT] | None]
    ],
    market_date: dt.date,
    print_raw: bool,
    verbose: bool,
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

    try:
        asyncio.get_event_loop().run_until_complete(fetch_and_print())
    except Exception as e:
        if verbose:
            raise
        else:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(code=1) from e


def _configure_logging(verbose: bool) -> None:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s %(message)s")
    handler.setFormatter(formatter)
    LOGGER.setLevel(logging.DEBUG if verbose else logging.WARNING)
    LOGGER.addHandler(handler)


if __name__ == "__main__":
    app()
