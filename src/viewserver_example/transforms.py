"""
Reusable DataFrame transform functions for ViewServer Python operators.

Each function takes a pandas DataFrame and returns a pandas DataFrame.
These can be used with engine.register_python_operator() or as inline
scripts in pythonScript operator configs.
"""

import pandas as pd
import numpy as np


def identity(df: pd.DataFrame) -> pd.DataFrame:
    """Passthrough — returns the input unchanged."""
    return df


def add_total(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'total' column = price * qty."""
    if "price" in df.columns and "qty" in df.columns:
        df["total"] = df["price"] * df["qty"]
    return df


def filter_active(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only rows where 'active' is True."""
    if "active" in df.columns:
        return df[df["active"] == True].reset_index(drop=True)  # noqa: E712
    return df


def moving_average(df: pd.DataFrame, column: str = "Value", window: int = 5) -> pd.DataFrame:
    """Add a rolling average column."""
    if column in df.columns:
        df[f"{column}_MA{window}"] = df[column].rolling(window=window, min_periods=1).mean()
    return df


def z_score(df: pd.DataFrame, column: str = "Value") -> pd.DataFrame:
    """Add a z-score column."""
    if column in df.columns:
        mean = df[column].mean()
        std = df[column].std()
        if std and std > 0:
            df[f"{column}_ZScore"] = (df[column] - mean) / std
        else:
            df[f"{column}_ZScore"] = 0.0
    return df


def rank_by(df: pd.DataFrame, column: str = "Value") -> pd.DataFrame:
    """Add a rank column."""
    if column in df.columns:
        df[f"{column}_Rank"] = df[column].rank(ascending=False).astype(int)
    return df


def pct_change(df: pd.DataFrame, column: str = "Value") -> pd.DataFrame:
    """Add a percentage change column."""
    if column in df.columns:
        df[f"{column}_PctChange"] = df[column].pct_change().fillna(0)
    return df


def squared(df: pd.DataFrame, column: str = "Value") -> pd.DataFrame:
    """Add a squared column."""
    if column in df.columns:
        df[f"{column}_Squared"] = df[column] ** 2
    return df
