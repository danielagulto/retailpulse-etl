import pandas as pd
import pytest

from src.retailpulse.transform import transform_orders


def sample_data():
    return pd.DataFrame([
        {"order_id": "A1", "order_date": "2026-01-01", "customer_id": "C1",
         "product": " Bottle ", "quantity": "2", "unit_price": "10.50", "country": "Spain"},
        {"order_id": "A2", "order_date": "not-a-date", "customer_id": "C2",
         "product": "Mat", "quantity": "1", "unit_price": "20", "country": "Spain"},
        {"order_id": "A3", "order_date": "2026-01-03", "customer_id": "C3",
         "product": "Shoes", "quantity": "0", "unit_price": "50", "country": "Spain"},
    ])


def test_valid_row_is_normalized():
    clean, rejected, metrics = transform_orders(sample_data())
    assert len(clean) == 1
    assert clean.loc[0, "product"] == "Bottle"
    assert clean.loc[0, "quantity"] == 2
    assert len(rejected) == 2
    assert metrics["valid_rows"] == 1


def test_invalid_rows_include_reasons():
    _, rejected, _ = transform_orders(sample_data())
    reasons = " ".join(rejected["rejection_reason"].tolist())
    assert "invalid_order_date" in reasons
    assert "invalid_quantity" in reasons


def test_exact_duplicates_are_removed():
    raw = sample_data().iloc[[0]]
    duplicated = pd.concat([raw, raw], ignore_index=True)
    clean, rejected, metrics = transform_orders(duplicated)
    assert len(clean) == 1
    assert len(rejected) == 0
    assert metrics["duplicate_rows_removed"] == 1


def test_missing_required_column_raises():
    with pytest.raises(ValueError, match="missing required columns"):
        transform_orders(pd.DataFrame({"order_id": ["A1"]}))
