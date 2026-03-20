"""
Standalone example — demonstrates transforms without a running ViewServer engine.

Run with:
    poetry run python -m viewserver_example.standalone
"""

import pandas as pd
from viewserver_example.transforms import (
    add_total,
    filter_active,
    moving_average,
    z_score,
    rank_by,
)


def main():
    # Simulate data that would come from an upstream operator
    df = pd.DataFrame({
        "Identifier": ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA"],
        "price": [150.0, 140.0, 300.0, 130.0, 250.0],
        "qty": [100, 200, 50, 150, 75],
        "active": [True, True, False, True, True],
    })
    print("=== Input DataFrame ===")
    print(df)
    print()

    # Apply transforms in sequence
    df = add_total(df)
    print("=== After add_total ===")
    print(df)
    print()

    df = filter_active(df)
    print("=== After filter_active ===")
    print(df)
    print()

    df = rank_by(df, column="total")
    print("=== After rank_by(total) ===")
    print(df)
    print()

    df = z_score(df, column="price")
    print("=== After z_score(price) ===")
    print(df)
    print()

    # Show what an inline script would look like
    print("=== Equivalent pythonScript config ===")
    script = '''def transform(df):
    df["total"] = df["price"] * df["qty"]
    df = df[df["active"] == True].reset_index(drop=True)
    df["total_Rank"] = df["total"].rank(ascending=False).astype(int)
    return df'''
    print(script)


if __name__ == "__main__":
    main()
