"""
Unit tests for transform functions.

These run without viewserver_python or a running engine — pure pandas tests.

    poetry run pytest
"""

import pandas as pd
import numpy as np
import pytest

from viewserver_example.transforms import (
    identity,
    add_total,
    filter_active,
    moving_average,
    z_score,
    rank_by,
    pct_change,
    squared,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Identifier": ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"],
        "price": [150.0, 140.0, 300.0, 130.0, 250.0],
        "qty": [100, 200, 50, 150, 75],
        "active": [True, True, False, True, True],
        "Value": [10.0, 20.0, 30.0, 40.0, 50.0],
    })


class TestIdentity:
    def test_returns_same_data(self, sample_df):
        result = identity(sample_df)
        pd.testing.assert_frame_equal(result, sample_df)


class TestAddTotal:
    def test_adds_total_column(self, sample_df):
        result = add_total(sample_df)
        assert "total" in result.columns
        assert list(result["total"]) == [15000.0, 28000.0, 15000.0, 19500.0, 18750.0]

    def test_no_price_column(self):
        df = pd.DataFrame({"name": ["a"]})
        result = add_total(df)
        assert "total" not in result.columns


class TestFilterActive:
    def test_removes_inactive_rows(self, sample_df):
        result = filter_active(sample_df)
        assert len(result) == 4
        assert "MSFT" not in result["Identifier"].values

    def test_no_active_column(self):
        df = pd.DataFrame({"name": ["a", "b"]})
        result = filter_active(df)
        assert len(result) == 2


class TestMovingAverage:
    def test_adds_ma_column(self, sample_df):
        result = moving_average(sample_df, column="Value", window=3)
        assert "Value_MA3" in result.columns
        assert len(result) == 5

    def test_missing_column(self, sample_df):
        result = moving_average(sample_df, column="nonexistent")
        assert "nonexistent_MA5" not in result.columns


class TestZScore:
    def test_adds_zscore_column(self, sample_df):
        result = z_score(sample_df, column="Value")
        assert "Value_ZScore" in result.columns
        # Mean z-score should be ~0
        assert abs(result["Value_ZScore"].mean()) < 1e-10


class TestRankBy:
    def test_adds_rank_column(self, sample_df):
        result = rank_by(sample_df, column="Value")
        assert "Value_Rank" in result.columns
        # Highest value (50) should be rank 1
        tsla_row = result[result["Identifier"] == "TSLA"]
        assert tsla_row["Value_Rank"].iloc[0] == 1


class TestPctChange:
    def test_adds_pct_change_column(self, sample_df):
        result = pct_change(sample_df, column="Value")
        assert "Value_PctChange" in result.columns
        assert result["Value_PctChange"].iloc[0] == 0  # first row filled with 0


class TestSquared:
    def test_adds_squared_column(self, sample_df):
        result = squared(sample_df, column="Value")
        assert "Value_Squared" in result.columns
        assert list(result["Value_Squared"]) == [100.0, 400.0, 900.0, 1600.0, 2500.0]


class TestPipeline:
    """Test composing multiple transforms in sequence."""

    def test_full_pipeline(self, sample_df):
        df = sample_df.copy()
        df = add_total(df)
        df = filter_active(df)
        df = rank_by(df, column="total")
        df = z_score(df, column="price")

        assert len(df) == 4  # MSFT filtered out
        assert "total" in df.columns
        assert "total_Rank" in df.columns
        assert "price_ZScore" in df.columns
