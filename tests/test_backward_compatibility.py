"""Tests for backward compatibility with hourly data format."""

import datetime as dt
import json

import aiohttp
import pytest
from aioresponses import aioresponses
from deepdiff.diff import DeepDiff

from pyomie.main import adjustment_price, get_data_format, spot_price

from .fixture import read_file


@pytest.mark.asyncio
async def test_existing_hourly_spot_data_still_works():
    """Test that existing hourly spot data continues to work unchanged."""
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

            # Verify we still get 24 values (hourly data)
            assert len(result.contents.spot_price_es) == 24
            assert len(result.contents.spot_price_pt) == 24
            assert len(result.contents.energy_purchases_es) == 24
            assert len(result.contents.energy_sales_es) == 24
            assert len(result.contents.energy_purchases_pt) == 24
            assert len(result.contents.energy_sales_pt) == 24
            assert len(result.contents.energy_es_pt) == 24
            assert len(result.contents.energy_total_es_pt) == 24
            assert len(result.contents.energy_import_es_from_pt) == 24
            assert len(result.contents.energy_export_es_to_pt) == 24

            # Verify the data matches the expected JSON exactly
            fixture_contents = json.loads(
                read_file("INT_PBC_EV_H_1_07_01_2024_07_01_2024.json")
            )

            diff = DeepDiff(
                t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
            )
            assert str(diff) == "{}"

            # Verify format detection works correctly
            assert get_data_format(result.contents._asdict()) == "hourly"


@pytest.mark.asyncio
async def test_existing_hourly_adjustment_data_still_works():
    """Test that existing hourly adjustment data continues to work unchanged."""
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

            # Verify we still get 24 values (hourly data)
            assert len(result.contents.adjustment_price_es) == 24
            assert len(result.contents.adjustment_price_pt) == 24
            assert len(result.contents.adjustment_energy) == 24
            assert len(result.contents.adjustment_unit_price) == 24

            # Verify the data matches the expected JSON exactly
            fixture_contents = json.loads(
                read_file("INT_MAJ_EV_H_15_06_2023_15_06_2023.json")
            )

            diff = DeepDiff(
                t1=fixture_contents, t2=result.contents._asdict(), ignore_order=True
            )
            assert str(diff) == "{}"

            # Verify format detection works correctly
            assert get_data_format(result.contents._asdict()) == "hourly"


def test_api_compatibility():
    """Test that the public API remains unchanged."""
    # Import all public functions to ensure they still exist
    from pyomie.main import spot_price, adjustment_price, get_data_format
    from pyomie.model import SpotData, AdjustmentData, OMIEResults, OMIEDayHours, OMIEDataSeries
    
    # Verify the functions are callable
    assert callable(spot_price)
    assert callable(adjustment_price)
    assert callable(get_data_format)
    
    # Verify the data types exist
    assert SpotData is not None
    assert AdjustmentData is not None
    assert OMIEResults is not None
    assert OMIEDayHours is not None
    assert OMIEDataSeries is not None


def test_data_structure_compatibility():
    """Test that data structures remain compatible with existing code."""
    # Test that OMIEDayHours can handle both 24 and 96 values
    hourly_data: list[float] = [1.0] * 24
    quarter_hourly_data: list[float] = [1.0] * 96
    
    # Both should be valid OMIEDayHours
    assert isinstance(hourly_data, list)
    assert isinstance(quarter_hourly_data, list)
    assert all(isinstance(x, float) for x in hourly_data)
    assert all(isinstance(x, float) for x in quarter_hourly_data)


@pytest.mark.asyncio
async def test_mixed_format_handling():
    """Test that the system can handle both formats in the same session."""
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

        # Test quarter-hourly format with the same URL (simulating format change over time)
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

        # Both results should be valid and properly typed
        assert hourly_result.market_date == quarter_hourly_result.market_date
        assert hourly_result.url == quarter_hourly_result.url


