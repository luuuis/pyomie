"""Tests for data format detection functionality."""

import pytest

from pyomie.main import get_data_format


def test_format_detection_hourly_exact():
    """Test format detection for exactly 24 hourly values."""
    hourly_data = {"test_series": [1.0] * 24}
    assert get_data_format(hourly_data) == "hourly"


def test_format_detection_hourly_range():
    """Test format detection for hourly data within acceptable range."""
    # Test various counts within the hourly range (20-30 to account for DST)
    for count in [20, 22, 24, 25, 26, 30]:
        hourly_data = {"test_series": [1.0] * count}
        assert get_data_format(hourly_data) == "hourly"


def test_format_detection_quarter_hourly_exact():
    """Test format detection for exactly 96 quarter-hourly values."""
    quarter_hourly_data = {"test_series": [1.0] * 96}
    assert get_data_format(quarter_hourly_data) == "quarter-hourly"


def test_format_detection_quarter_hourly_range():
    """Test format detection for quarter-hourly data within acceptable range."""
    # Test various counts within the quarter-hourly range (90-100)
    for count in [90, 92, 94, 96, 98, 100]:
        quarter_hourly_data = {"test_series": [1.0] * count}
        assert get_data_format(quarter_hourly_data) == "quarter-hourly"


def test_format_detection_unknown_low():
    """Test format detection for values below hourly range."""
    for count in [1, 10, 15, 19]:
        unknown_data = {"test_series": [1.0] * count}
        assert get_data_format(unknown_data) == "unknown"


def test_format_detection_unknown_high():
    """Test format detection for values above quarter-hourly range."""
    for count in [101, 120, 150, 200]:
        unknown_data = {"test_series": [1.0] * count}
        assert get_data_format(unknown_data) == "unknown"


def test_format_detection_unknown_middle():
    """Test format detection for values between hourly and quarter-hourly ranges."""
    for count in [31, 40, 50, 60, 70, 80, 89]:
        unknown_data = {"test_series": [1.0] * count}
        assert get_data_format(unknown_data) == "unknown"


def test_format_detection_empty_data():
    """Test format detection for empty data."""
    assert get_data_format({}) == "unknown"


def test_format_detection_multiple_series():
    """Test format detection when multiple series are present."""
    # Should use the first series for detection
    data = {
        "series1": [1.0] * 24,  # Hourly
        "series2": [2.0] * 96,  # Quarter-hourly
    }
    assert get_data_format(data) == "hourly"  # Should detect based on first series


def test_format_detection_realistic_data():
    """Test format detection with realistic OMIE data structure."""
    # Hourly data structure
    hourly_omie_data = {
        "spot_price_es": [84.08, 79.82, 76.76] + [70.0] * 21,
        "spot_price_pt": [84.08, 79.82, 76.76] + [70.0] * 21,
        "energy_purchases_es": [11833.2] * 24,
        "energy_sales_es": [14296.5] * 24,
    }
    assert get_data_format(hourly_omie_data) == "hourly"

    # Quarter-hourly data structure
    quarter_hourly_omie_data = {
        "spot_price_es": [84.08] * 96,
        "spot_price_pt": [84.08] * 96,
        "energy_purchases_es": [11833.2] * 96,
        "energy_sales_es": [14296.5] * 96,
    }
    assert get_data_format(quarter_hourly_omie_data) == "quarter-hourly"


