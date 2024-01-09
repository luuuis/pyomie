import datetime as dt
import json

import aiohttp
import pytest
from aioresponses import aioresponses
from deepdiff.diff import DeepDiff

from pyomie.main import adjustment_price, spot_price

from .fixture import read_file


@pytest.mark.asyncio
async def test_spot_price_404():
    async with aiohttp.ClientSession() as session:
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_1970/MES_01/TXT/INT_PBC_EV_H_1_01_01_1970_01_01_1970.TXT",
                status=404,
            )

            resp = await spot_price(session, dt.date(1970, 1, 1))
            assert resp is None


@pytest.mark.asyncio
async def test_spot_price_24h_day():
    async with aiohttp.ClientSession() as session:
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2024/MES_01/TXT/INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT",
                status=200,
                body=read_file("INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT").encode(
                    "iso8859-1"
                ),
            )

            result = await spot_price(session, dt.date(2024, 1, 7))
            assert result is not None

            fixture_contents = json.loads(
                read_file("INT_PBC_EV_H_1_07_01_2024_07_01_2024.json")
            )

            diff = DeepDiff(
                t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
            )
            assert str(diff) == "{}"


@pytest.mark.asyncio
async def test_adjustment_price_404():
    async with aiohttp.ClientSession() as session:
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2023/MES_12/TXT/INT_MAJ_EV_H_31_12_2023_31_12_2023.TXT",
                status=404,
            )
            resp = await adjustment_price(session, dt.date(2023, 12, 31))
            assert resp is None


@pytest.mark.asyncio
async def test_adjustment_price_ended():
    async with aiohttp.ClientSession() as session:
        with aioresponses():
            # no HTTP should be done, don't train the mock.
            resp = await adjustment_price(session, dt.date(2024, 1, 7))
            assert resp is None


@pytest.mark.asyncio
async def test_adjustment_price_24h_day():
    async with aiohttp.ClientSession() as session:
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2023/MES_06/TXT/INT_MAJ_EV_H_15_06_2023_15_06_2023.TXT",
                status=200,
                body=read_file("INT_MAJ_EV_H_15_06_2023_15_06_2023.TXT").encode(
                    "iso8859-1"
                ),
            )

            result = await adjustment_price(session, dt.date(2023, 6, 15))
            assert result is not None

            fixture_contents = json.loads(
                read_file("INT_MAJ_EV_H_15_06_2023_15_06_2023.json")
            )

            diff = DeepDiff(
                t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
            )
            assert str(diff) == "{}"
