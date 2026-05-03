---
name: databricks
description: Databricks-specific patterns for connecting, querying, and loading data in the ai-analyst workspace. Covers Delta Lake, Unity Catalog, Databricks SQL connector, SparkSQL dialect, and best practices for extracting analytics-ready DataFrames. Load whenever the user mentions Databricks, Unity Catalog, Delta tables, or warehouse queries.
---

# Databricks integration skill

## Connection patterns

### Option 1 — Databricks SQL Connector (recommended for analytics)
Use for: running SQL against Databricks SQL warehouse and extracting results as pandas DataFrames.

```python
from databricks import sql
import pandas as pd
import os

def get_databricks_connection():
    """
    Reads connection config from environment variables.
    Set these in .env or Databricks personal access token settings.
    """
    return sql.connect(
        server_hostname = os.environ["DATABRICKS_HOST"],        # e.g. "adb-xxxx.azuredatabricks.net"
        http_path       = os.environ["DATABRICKS_HTTP_PATH"],   # e.g. "/sql/1.0/warehouses/xxxx"
        access_token    = os.environ["DATABRICKS_TOKEN"],       # PAT from user settings
    )


def run_query(sql_query: str, params: dict = None) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""
    with get_databricks_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query, params or [])
            return cursor.fetchall_arrow().to_pandas()
```

### Option 2 — Delta Lake direct read (for file-based access)
Use for: reading Delta tables directly from ADLS/S3 without a SQL warehouse running.

```python
import pandas as pd
from deltalake import DeltaTable

def read_delta_table(table_path: str, columns: list[str] = None,
                     filter_expr: str = None) -> pd.DataFrame:
    """
    Read a Delta table directly from storage.
    table_path: ADLS path, e.g. "abfss://container@account.dfs.core.windows.net/path/to/table"
    """
    storage_options = {
        "account_name": os.environ["AZURE_STORAGE_ACCOUNT"],
        "account_key": os.environ["AZURE_STORAGE_KEY"],
    }
    dt = DeltaTable(table_path, storage_options=storage_options)
    if filter_expr:
        return dt.to_pandas(columns=columns, filters=filter_expr)
    return dt.to_pandas(columns=columns)
```

### Option 3 — MLflow / Databricks workspace SDK
Use for: retrieving experiment results, registered models, or workspace assets.

```python
import mlflow
mlflow.set_tracking_uri("databricks")
# Then use mlflow.search_runs(), mlflow.load_model(), etc.
```

---

## Environment variable setup

Store these in a `.env` file in the project root (gitignored) or in Databricks secrets:

```bash
# .env (never commit this file)
DATABRICKS_HOST=https://adb-xxxx.xx.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxx
DATABRICKS_TOKEN=dapixxxxxxxxxxxxxxxx
AZURE_STORAGE_ACCOUNT=yourstorageaccount
AZURE_STORAGE_KEY=your_key_here
```

Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()  # loads .env file
```

---

## Unity Catalog — naming conventions

Unity Catalog uses three-part names: `catalog.schema.table`

```sql
-- Fully qualified table reference
SELECT * FROM main_catalog.super_analytics.member_balances

-- Or use USE statements
USE CATALOG main_catalog;
USE SCHEMA super_analytics;
SELECT * FROM member_balances LIMIT 100;

-- List all tables in a schema
SHOW TABLES IN main_catalog.super_analytics;

-- Describe a table
DESCRIBE TABLE EXTENDED main_catalog.super_analytics.member_balances;
```

When writing SQL for Databricks Unity Catalog:
- Always qualify table names: `catalog.schema.table`
- Never assume `USE DATABASE` is in scope — be explicit

---

## SparkSQL / Delta Lake dialect specifics

Key differences from ANSI SQL that matter for super analytics:

```sql
-- Date functions (Spark uses its own date functions)
DATEDIFF(end_date, start_date)  -- days between (NOTE: reversed from some dialects)
DATE_TRUNC('month', event_ts)   -- truncate to period
DATE_ADD(event_date, 30)        -- add days
MONTHS_BETWEEN(end_date, start_date)  -- number of months

-- Timestamp with timezone
CONVERT_TIMEZONE('UTC', 'Australia/Melbourne', event_ts)

-- Approximate distinct counts (fast for large tables)
APPROX_COUNT_DISTINCT(member_id)

-- Struct access (nested columns common in Delta tables)
member_profile.age, member_profile.address.suburb

-- Array functions (contribution history often stored as arrays)
ARRAY_AGG(contribution_amount) AS contribution_history
SIZE(contributions_array)
EXPLODE(contributions_array) AS contribution  -- lateral view

-- Window functions (same as ANSI, but PARTITION syntax matters)
ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY snapshot_date DESC)

-- Delta time travel (read historical state of a Delta table)
SELECT * FROM member_balances TIMESTAMP AS OF '2025-12-31'
SELECT * FROM member_balances VERSION AS OF 5

-- MERGE (upsert pattern — common for member data ETL)
MERGE INTO target_table t
USING source_table s ON t.member_id = s.member_id
WHEN MATCHED THEN UPDATE SET t.balance = s.balance
WHEN NOT MATCHED THEN INSERT *;
```

---

## Standard query templates for super analytics

### Member snapshot extract
```sql
WITH latest_snapshot AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY snapshot_date DESC) AS rn
    FROM   catalog.schema.member_balances
    WHERE  snapshot_date >= DATE_ADD(CURRENT_DATE(), -90)  -- last 90 days
),
base AS (
    SELECT
        member_id,
        snapshot_date,
        balance_aud,
        employer_contribution_ytd,
        voluntary_contribution_ytd,
        salary_sacrifice_ytd,
        salary_aud,
        FLOOR(DATEDIFF(snapshot_date, date_of_birth) / 365.25) AS age_years,
        investment_option_code,
        last_login_date,
        DATEDIFF(CURRENT_DATE(), last_login_date) AS last_login_days_ago
    FROM latest_snapshot
    WHERE rn = 1
      AND account_status = 'ACTIVE'
)
SELECT * FROM base
LIMIT 1000  -- always add limit for first run
;
```

### Contribution trend by month
```sql
SELECT
    DATE_TRUNC('month', contribution_date)  AS month,
    age_band,
    COUNT(DISTINCT member_id)               AS n_members,
    SUM(employer_contribution_aud)          AS total_employer,
    SUM(salary_sacrifice_aud)               AS total_ss,
    SUM(voluntary_ncc_aud)                  AS total_ncc,
    AVG(salary_sacrifice_aud)               AS mean_ss,
    PERCENTILE_APPROX(salary_sacrifice_aud, 0.5) AS median_ss
FROM catalog.schema.contributions
WHERE contribution_date >= ADD_MONTHS(CURRENT_DATE(), -24)
  AND contribution_type IN ('EMPLOYER_SG', 'SALARY_SACRIFICE', 'VOLUNTARY_NCC')
GROUP BY 1, 2
ORDER BY 1, 2
;
```

### Fund-level flow analysis
```sql
SELECT
    DATE_TRUNC('quarter', transaction_date) AS quarter,
    SUM(CASE WHEN transaction_type = 'CONTRIBUTION' THEN amount_aud ELSE 0 END) AS inflows,
    SUM(CASE WHEN transaction_type IN ('BENEFIT_PAYMENT', 'ROLLOVER_OUT') THEN amount_aud ELSE 0 END) AS outflows,
    SUM(CASE WHEN transaction_type = 'CONTRIBUTION' THEN amount_aud ELSE 0 END)
        - SUM(CASE WHEN transaction_type IN ('BENEFIT_PAYMENT', 'ROLLOVER_OUT') THEN amount_aud ELSE 0 END)
        AS net_flow,
    COUNT(DISTINCT CASE WHEN transaction_type = 'ROLLOVER_OUT' THEN member_id END) AS members_rolling_out
FROM catalog.schema.transactions
WHERE transaction_date >= ADD_MONTHS(CURRENT_DATE(), -12)
GROUP BY 1
ORDER BY 1
;
```

---

## Performance best practices for super analytics queries

1. **Partition pruning**: Super data is almost always partitioned by `snapshot_date` or `member_cohort`. Always filter on the partition column.

   ```sql
   -- GOOD: hits only 1 partition
   WHERE snapshot_date = '2026-03-31'
   
   -- BAD: full table scan
   WHERE YEAR(snapshot_date) = 2026 AND MONTH(snapshot_date) = 3
   ```

2. **Z-ordering**: If your Databricks table is Z-ordered on `member_id` and `snapshot_date`, use both columns in your filters.

3. **LIMIT on first exploration**: Always add `LIMIT 1000` when running exploratory queries. Remove for the final extract only.

4. **Avoid UDFs** where native Spark functions exist — they break the Catalyst optimizer.

5. **Count before collect**: For large tables, run `SELECT COUNT(*) ...` first to understand volume before `SELECT *`.

6. **Parquet/Delta for saves**: Save extracted DataFrames to `data/processed/*.parquet` for local reuse — avoid repeated warehouse queries.

---

## Saving to processed/ and reusing

```python
import pandas as pd
from pathlib import Path

def extract_and_save(query: str, output_name: str) -> pd.DataFrame:
    """Run a Databricks query, save parquet, return DataFrame."""
    cache_path = Path(f"data/processed/{output_name}.parquet")

    if cache_path.exists():
        print(f"Loading cached: {cache_path}")
        return pd.read_parquet(cache_path)

    print(f"Querying Databricks...")
    df = run_query(query)
    df.to_parquet(cache_path, index=False)
    print(f"Saved: {cache_path} ({len(df):,} rows)")
    return df
```

---

## Common Databricks errors and fixes

| Error | Likely cause | Fix |
|---|---|---|
| `DATABRICKS_HOST not set` | .env not loaded | `load_dotenv()` before connection |
| `AnalysisException: Table not found` | Wrong catalog/schema prefix | Use `SHOW TABLES IN catalog.schema` to verify |
| `PERMISSION_DENIED` | PAT doesn't have SELECT on table | Request Unity Catalog data access from DBA |
| `RESOURCE_EXHAUSTED` | SQL warehouse is idle/stopped | Start the warehouse in Databricks UI first |
| `Py4JJavaError` in delta-rs | Storage credentials wrong | Check AZURE_STORAGE_KEY or SAS token validity |
| `ArrowInvalid: Schema mismatch` | Decimal precision difference | Cast to `DOUBLE` in SQL before fetching |
| `MemoryError` | Query returns too many rows | Add `LIMIT` or filter; sample first |

---

## Installing dependencies

```bash
# Install databricks-sql-connector and delta-rs
uv pip install databricks-sql-connector deltalake python-dotenv

# Or with pip
pip install databricks-sql-connector deltalake python-dotenv
```

Add to `requirements.txt`:
```
databricks-sql-connector>=3.0.0
deltalake>=0.17.0
python-dotenv>=1.0.0
```
