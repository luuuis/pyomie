import datetime as dt
import json

import pytest
from aiohttp import ClientResponseError
from deepdiff.diff import DeepDiff

from pyomie.main import spot_price

from .fixture import read_file


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code", [404, 403, 500, 502, 503])
async def test_spot_price_http_error(session, mock_server, status_code):
    mock_server.get(
        "https://www.omie.es/sites/default/files/dados/AGNO_2970/MES_01/TXT/INT_PBC_EV_H_1_01_01_2970_01_01_2970.TXT",
        status=status_code,
    )

    with pytest.raises(ClientResponseError) as e_info:
        await spot_price(session, dt.date(2970, 1, 1))

    exc = e_info.value
    assert exc.status == status_code


@pytest.mark.asyncio
async def test_spot_price_24h_day(session):
    with pytest.raises(ValueError) as e_info:
        await spot_price(session, dt.date(2024, 9, 30))

    exc = e_info.value
    assert str(exc) == "Dates earlier than 2025-10-01 are not supported."


@pytest.mark.asyncio
async def test_spot_price_96q_day(session, mock_server):
    mock_server.get(
        "https://www.omie.es/sites/default/files/dados/AGNO_2025/MES_10/TXT/INT_PBC_EV_H_1_01_10_2025_01_10_2025.TXT",
        status=200,
        body=read_file("INT_PBC_EV_H_1_01_10_2025_01_10_2025.TXT").encode("iso8859-1"),
    )

    result = await spot_price(session, dt.date(2025, 10, 1))
    assert result is not None

    fixture_contents = json.loads(
        read_file("INT_PBC_EV_H_1_01_10_2025_01_10_2025.json")
    )

    diff = DeepDiff(
        t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
    )
    assert str(diff) == "{}"
