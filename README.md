# RetailPulse — End-to-End ETL Data Pipeline

A Python-based data engineering portfolio project demonstrating automated data extraction, transformation, validation, and loading (ETL) using retail order data.

Built to showcase practical skills relevant to Junior Data Engineer and Data Analytics roles.

## Project Overview

RetailPulse processes raw retail orders through a repeatable ETL pipeline:

1. **Extract:** Reads raw order records from a CSV file.
2. **Transform:** Uses Python and Pandas to standardize values, validate fields, detect duplicates, and identify invalid records.
3. **Load:** Loads validated records into a SQLite database.
4. **Monitor data quality:** Generates a JSON report containing processing metrics and validation results.
5. **Test:** Runs automated tests with pytest to check transformation logic.

The project uses synthetic sample data and is an independent portfolio project. It is not affiliated with any employer or client.

## Verified Execution Results

The pipeline was executed locally, and the automated test suite completed successfully.

| Metric | Result |
|---|---:|
| Raw rows processed | 27 |
| Valid records loaded | 22 |
| Rejected records | 4 |
| Duplicate rows removed | 1 |
| Data quality pass rate | 84.62% |
| Automated tests passed | 4 |
| Automated tests failed | 0 |

The data quality pass rate is calculated from the 22 valid records out of 26 records remaining after duplicate removal.

## Technology Stack

- **Python 3.14** — pipeline execution
- **Pandas** — data transformation and validation
- **SQL / SQLite** — persistent local storage and analytics
- **pytest** — automated testing
- **Docker** — optional containerized execution

## Project Structure

```text
retailpulse-etl/
├── data/
│   ├── raw/
│   │   └── orders.csv
│   └── processed/
│       ├── clean_orders.csv
│       ├── rejected_orders.csv
│       ├── data_quality_report.json
│       └── retailpulse.db
├── sql/
│   └── schema.sql
├── src/
│   └── retailpulse/
│       ├── __init__.py
│       ├── pipeline.py
│       └── transform.py
├── tests/
│   └── test_transform.py
├── .github/
│   └── workflows/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Generated files under `data/processed/` appear after running the pipeline. The `.gitignore` configuration may exclude generated files from Git.

## Getting Started

### Prerequisites

- Python 3.11 or later
- pip

### 1. Clone the repository

```bash
git clone https://github.com/danielagulto/retailpulse-etl.git
cd retailpulse-etl
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the ETL pipeline

```bash
python -m src.retailpulse.pipeline
```

### 5. Run automated tests

```bash
python -m pytest -q
```

Expected test result from the verified local run:

```text
4 passed
```

## Data Quality Rules

The pipeline checks the following fields and conditions:

- Required fields: `order_id`, `order_date`, `customer_id`, `product`, `quantity`, `unit_price`, and `country`.
- Dates must be valid and use the `YYYY-MM-DD` format.
- Quantity must be a positive integer.
- Unit price must be numeric and non-negative.
- Exact duplicate rows are removed.
- Records with missing or invalid required fields are rejected, with rejection reasons recorded in the processed output.

## Generated Outputs

After a successful run, inspect `data/processed/`:

| File | Purpose |
|---|---|
| `clean_orders.csv` | Validated and transformed records |
| `rejected_orders.csv` | Rejected records and their rejection reasons |
| `data_quality_report.json` | Pipeline execution and data quality metrics |
| `retailpulse.db` | SQLite database containing loaded records and analytics objects |

The pipeline rebuilds the `orders` table from the current input on each run, making repeated executions predictable for this sample workflow.

## SQL Analytics Examples

### Revenue by country

```sql
SELECT
    country,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY country
ORDER BY revenue DESC;
```

### Daily revenue

```sql
SELECT *
FROM daily_sales
ORDER BY order_date;
```

### Top products by revenue

```sql
SELECT
    product,
    SUM(quantity) AS units_sold,
    ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;
```

## Skills Demonstrated

- ETL pipeline development
- Python programming and Pandas data processing
- Data cleaning, validation, and duplicate handling
- SQL querying and SQLite data loading
- Data quality metrics and reporting
- Automated testing with pytest
- GitHub-based project documentation

## Future Improvements

- Add PostgreSQL support.
- Schedule recurring pipeline executions.
- Expand data quality checks and test coverage.
- Connect the output to Power BI for an interactive analytics dashboard.
- Explore Azure Data Factory or Microsoft Fabric for cloud-based orchestration.

These are planned improvements, not features claimed as already implemented.

## Portfolio Note

This project uses synthetic sample data for learning and demonstration. It is designed to communicate practical data engineering concepts through a reproducible local workflow.
