"""Validation and transformation functions for the RetailPulse pipeline."""
from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "product",
    "quantity", "unit_price", "country",
]


def transform_orders(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Return (clean, rejected, metrics) dataframes and basic quality metrics."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if missing_columns:
        raise ValueError(f"Input is missing required columns: {missing_columns}")

    df = raw[REQUIRED_COLUMNS].copy()
    rows_read = len(df)

    # Normalize text before checking required values.
    for col in ["order_id", "customer_id", "product", "country"]:
        df[col] = df[col].astype("string").str.strip()

    # Drop exact duplicate rows deterministically.
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicate_rows_removed = before_dedup - len(df)

    parsed_dates = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
    quantities = pd.to_numeric(df["quantity"], errors="coerce")
    prices = pd.to_numeric(df["unit_price"], errors="coerce")

    reasons = []
    for idx in df.index:
        row_reasons = []
        for col in ["order_id", "customer_id", "product", "country"]:
            if pd.isna(df.at[idx, col]) or str(df.at[idx, col]).strip() == "":
                row_reasons.append(f"missing_{col}")
        if pd.isna(parsed_dates.loc[idx]):
            row_reasons.append("invalid_order_date")
        if pd.isna(quantities.loc[idx]) or quantities.loc[idx] <= 0 or float(quantities.loc[idx]) % 1 != 0:
            row_reasons.append("invalid_quantity")
        if pd.isna(prices.loc[idx]) or prices.loc[idx] < 0:
            row_reasons.append("invalid_unit_price")
        reasons.append(";".join(row_reasons))

    df["rejection_reason"] = reasons
    rejected = df[df["rejection_reason"] != ""].copy()
    clean = df[df["rejection_reason"] == ""].copy()

    clean["order_date"] = parsed_dates.loc[clean.index].dt.strftime("%Y-%m-%d")
    clean["quantity"] = quantities.loc[clean.index].astype(int)
    clean["unit_price"] = prices.loc[clean.index].astype(float).round(2)
    clean = clean.drop(columns=["rejection_reason"]).reset_index(drop=True)

    rejected["rejection_reason"] = rejected["rejection_reason"].astype(str)
    rejected = rejected.reset_index(drop=True)

    metrics = {
        "rows_read": int(rows_read),
        "duplicate_rows_removed": int(duplicate_rows_removed),
        "valid_rows": int(len(clean)),
        "rejected_rows": int(len(rejected)),
        "data_quality_pass_rate_pct": round((len(clean) / max(rows_read - duplicate_rows_removed, 1)) * 100, 2),
    }
    return clean, rejected, metrics
