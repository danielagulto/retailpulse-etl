"""Run the RetailPulse extract-transform-load workflow."""
from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.retailpulse.transform import transform_orders

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "orders.csv"
OUTPUT_DIR = ROOT / "data" / "processed"
DB_PATH = OUTPUT_DIR / "retailpulse.db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("retailpulse")


def run_pipeline() -> dict:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Extracting raw orders from %s", RAW_PATH)
    raw = pd.read_csv(RAW_PATH, dtype={"order_id": "string", "customer_id": "string"})

    logger.info("Transforming and validating %s rows", len(raw))
    clean, rejected, metrics = transform_orders(raw)

    clean.to_csv(OUTPUT_DIR / "clean_orders.csv", index=False)
    rejected.to_csv(OUTPUT_DIR / "rejected_orders.csv", index=False)

    logger.info("Loading %s valid rows into SQLite", len(clean))
    with sqlite3.connect(DB_PATH) as connection:
        clean.to_sql("orders", connection, if_exists="replace", index=False)
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)
        """)
        connection.execute("DROP VIEW IF EXISTS daily_sales")
        connection.execute("""
            CREATE VIEW daily_sales AS
            SELECT order_date,
                   COUNT(DISTINCT order_id) AS order_count,
                   SUM(quantity) AS units_sold,
                   ROUND(SUM(quantity * unit_price), 2) AS revenue
            FROM orders
            GROUP BY order_date
        """)
        connection.commit()

    report = {
        "project": "RetailPulse ETL",
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": str(RAW_PATH.relative_to(ROOT)),
        "database_file": str(DB_PATH.relative_to(ROOT)),
        **metrics,
        "status": "success",
    }
    (OUTPUT_DIR / "data_quality_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    logger.info("Pipeline completed: %s", json.dumps(metrics))
    return report


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2))
