# RetailPulse — End-to-End ETL Data Pipeline

A portfolio project demonstrating core Junior Data Engineer skills relevant to data engineering and analytics roles.

## What it does

1. **Extracts** raw retail orders from `data/raw/orders.csv`.
2. **Transforms** records with Python and Pandas: standardizes text, validates dates and numeric fields, removes exact duplicates, and separates invalid records.
3. **Loads** valid, cleaned records into a SQLite database (no database server needed).
4. Produces a **data quality report** and SQL analytics tables/views.
5. Includes automated tests and a Docker option.

> This is a learning/portfolio project using synthetic sample data. It is not affiliated with KPMG and does not claim production deployment.

## Tech stack

- Python 3.11+
- Pandas
- SQL / SQLite
- pytest
- Docker (optional)

## Project structure

```text
retailpulse-etl/
├── data/
│   ├── raw/orders.csv
│   └── processed/                 # generated outputs
├── sql/schema.sql
├── src/retailpulse/
│   ├── __init__.py
│   ├── pipeline.py
│   └── transform.py
├── tests/test_transform.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run locally (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.retailpulse.pipeline
pytest -q
```

On Windows, activate the virtual environment with `.venv\\Scripts\\activate`.

## Expected outputs

After running the pipeline, check `data/processed/` for:
- `retailpulse.db` — SQLite database with `orders` table and `daily_sales` view
- `clean_orders.csv` — valid transformed records
- `rejected_orders.csv` — invalid records with rejection reasons
- `data_quality_report.json` — run metrics and validation counts

The pipeline is designed to be re-runnable: the `orders` table is rebuilt on each run from the current input file, avoiding accidental duplicate loads.

## Data quality rules

- `order_id`, `order_date`, `customer_id`, `product`, `quantity`, `unit_price`, and `country` are required.
- `order_date` must be a valid date in ISO format (`YYYY-MM-DD`).
- `quantity` must be a positive integer.
- `unit_price` must be numeric and non-negative.
- Exact duplicate rows are dropped; rows with missing/invalid required fields are rejected.

## Useful SQL examples

```sql
-- Revenue by country
SELECT country, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY country
ORDER BY revenue DESC;

-- Daily revenue view
SELECT * FROM daily_sales ORDER BY order_date;

-- Top products
SELECT product, SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;
```

## Next improvements

- Replace the local SQLite database with PostgreSQL.
- Add a scheduled run (cron or GitHub Actions).
- Add structured logging and a REST health endpoint.
- Connect the database to Power BI and build a dashboard.
- Deploy the pipeline to Azure Data Factory / Microsoft Fabric as a follow-on project.

## Portfolio talking points

Be prepared to explain the extract-transform-load stages, validation rules, rejected-record handling, idempotent loading strategy, SQL view, and test coverage. Only describe features you have personally run and verified.
