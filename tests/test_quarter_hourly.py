"""Tests for quarter-hourly data format support."""

import datetime as dt
import json

import aiohttp
import pytest
from aioresponses import aioresponses
from deepdiff.diff import DeepDiff

from pyomie.main import adjustment_price, get_data_format, spot_price

from .fixture import read_file


@pytest.mark.asyncio
async def test_spot_price_quarter_hourly():
    """Test that quarter-hourly spot price data is parsed correctly."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2024/MES_01/TXT/INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT",
                status=200,
                body=read_file("INT_PBC_EV_H_1_07_01_2024_QUARTER_HOURLY.TXT").encode(
                    "iso8859-1"
                ),
            )

            result = await spot_price(session, dt.date(2024, 1, 7))
            assert result is not None

            # Verify we have 96 values (quarter-hourly data)
            assert len(result.contents.spot_price_es) == 96
            assert len(result.contents.spot_price_pt) == 96
            assert len(result.contents.energy_purchases_es) == 96

            # Load expected data and compare
            fixture_contents = json.loads(
                read_file("INT_PBC_EV_H_1_07_01_2024_QUARTER_HOURLY.json")
            )

            diff = DeepDiff(
                t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
            )
            assert str(diff) == "{}"


def test_get_data_format_hourly():
    """Test format detection for hourly data."""
    hourly_data = {
        "spot_price_es": [84.08] * 24,
        "energy_purchases_es": [11833.2] * 24,
    }
    assert get_data_format(hourly_data) == "hourly"


def test_get_data_format_quarter_hourly():
    """Test format detection for quarter-hourly data."""
    quarter_hourly_data = {
        "spot_price_es": [84.08] * 96,
        "energy_purchases_es": [11833.2] * 96,
    }
    assert get_data_format(quarter_hourly_data) == "quarter-hourly"


def test_get_data_format_unknown():
    """Test format detection for unknown data."""
    unknown_data = {
        "spot_price_es": [84.08] * 10,  # Neither 24 nor 96
    }
    assert get_data_format(unknown_data) == "unknown"


def test_get_data_format_empty():
    """Test format detection for empty data."""
    assert get_data_format({}) == "unknown"


def test_get_data_format_dst_day():
    """Test format detection for DST day (25 hours)."""
    dst_data = {
        "spot_price_es": [84.08] * 25,  # DST day has 25 hours
    }
    assert get_data_format(dst_data) == "hourly"  # Should still be detected as hourly


@pytest.mark.asyncio
async def test_backward_compatibility_hourly():
    """Test that old hourly format still works."""
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

            # Verify we have 24 values (hourly data)
            assert len(result.contents.spot_price_es) == 24
            assert len(result.contents.spot_price_pt) == 24
            assert len(result.contents.energy_purchases_es) == 24

            # Verify format detection
            assert get_data_format(result.contents._asdict()) == "hourly"


@pytest.mark.asyncio
async def test_quarter_hourly_vs_hourly_detection():
    """Test that the parser correctly distinguishes between hourly and quarter-hourly formats."""
    async with aiohttp.ClientSession() as session:
        # Test hourly format
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2024/MES_01/TXT/INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT",
                status=200,
                body=read_file("INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT").encode(
                    "iso8859-1"
                ),
            )

            hourly_result = await spot_price(session, dt.date(2024, 1, 7))
            assert hourly_result is not None
            assert len(hourly_result.contents.spot_price_es) == 24

        # Test quarter-hourly format
        with aioresponses() as m:
            m.get(
                "https://www.omie.es/sites/default/files/dados/AGNO_2024/MES_01/TXT/INT_PBC_EV_H_1_07_01_2024_07_01_2024.TXT",
                status=200,
                body=read_file("INT_PBC_EV_H_1_07_01_2024_QUARTER_HOURLY.TXT").encode(
                    "iso8859-1"
                ),
            )

            quarter_hourly_result = await spot_price(session, dt.date(2024, 1, 7))
            assert quarter_hourly_result is not None
            assert len(quarter_hourly_result.contents.spot_price_es) == 96


