"""
Databricks connector utility for the AI Analyst workspace.

Provides a clean interface for the data-fetcher agent to query
Databricks SQL warehouses and Unity Catalog tables.

Usage:
    # Test connection
    python scripts/databricks_connector.py --test

    # Run a query and save to parquet
    python scripts/databricks_connector.py --query "SELECT * FROM catalog.schema.table LIMIT 1000" --output data/processed/extract.parquet

    # Describe a table
    python scripts/databricks_connector.py --describe catalog.schema.table
"""

from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

import pandas as pd


def _load_env():
    """Load .env file if present."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def get_connection():
    """Return a live Databricks SQL connection."""
    _load_env()

    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    http_path = os.environ.get("DATABRICKS_HTTP_PATH", "")
    token = os.environ.get("DATABRICKS_TOKEN", "")

    if not all([host, http_path, token]):
        missing = [k for k, v in [
            ("DATABRICKS_HOST", host),
            ("DATABRICKS_HTTP_PATH", http_path),
            ("DATABRICKS_TOKEN", token),
        ] if not v]
        raise EnvironmentError(
            f"Missing Databricks credentials: {missing}. "
            f"Copy .env.example to .env and fill in your values."
        )

    try:
        from databricks import sql
    except ImportError:
        raise ImportError(
            "databricks-sql-connector not installed. "
            "Run: pip install databricks-sql-connector"
        )

    return sql.connect(
        server_hostname=host.replace("https://", ""),
        http_path=http_path,
        access_token=token,
    )


def run_query(sql_query: str) -> pd.DataFrame:
    """Execute a SQL query against the Databricks warehouse and return a DataFrame."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            return cursor.fetchall_arrow().to_pandas()


def describe_table(table_path: str) -> pd.DataFrame:
    """Return schema information for a Unity Catalog table."""
    return run_query(f"DESCRIBE TABLE EXTENDED {table_path}")


def list_tables(schema_path: str) -> pd.DataFrame:
    """List all tables in a Unity Catalog schema (e.g. 'catalog.schema')."""
    return run_query(f"SHOW TABLES IN {schema_path}")


def extract_and_save(
    sql_query: str,
    output_path: str | Path,
    *,
    use_cache: bool = True,
    print_profile: bool = True,
) -> pd.DataFrame:
    """
    Run a Databricks query, save result to parquet, and return the DataFrame.
    If use_cache=True and the parquet already exists, loads it instead of re-querying.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if use_cache and output_path.exists():
        print(f"[cache] Loading: {output_path}")
        df = pd.read_parquet(output_path)
    else:
        print(f"[databricks] Running query...")
        df = run_query(sql_query)
        df.to_parquet(output_path, index=False)
        print(f"[saved] {output_path} ({len(df):,} rows × {df.shape[1]} cols)")

    if print_profile:
        print(f"\nShape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"Columns: {list(df.columns)}")
        null_cols = [c for c in df.columns if df[c].isna().any()]
        if null_cols:
            print(f"Columns with nulls: {null_cols}")

    return df


def test_connection() -> bool:
    """Verify the Databricks connection works. Returns True on success."""
    try:
        df = run_query("SELECT current_catalog(), current_schema(), current_user()")
        row = df.iloc[0]
        print(f"Connection OK")
        print(f"  Catalog: {row.iloc[0]}")
        print(f"  Schema:  {row.iloc[1]}")
        print(f"  User:    {row.iloc[2]}")
        return True
    except Exception as e:
        print(f"Connection FAILED: {e}")
        return False


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Databricks connector utility")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--query", type=str, help="SQL query to run")
    parser.add_argument("--output", type=str, help="Output parquet path for --query")
    parser.add_argument("--describe", type=str, metavar="TABLE", help="Describe a table")
    parser.add_argument("--list-tables", type=str, metavar="SCHEMA", help="List tables in schema")
    parser.add_argument("--no-cache", action="store_true", help="Bypass parquet cache")
    args = parser.parse_args()

    if args.test:
        sys.exit(0 if test_connection() else 1)

    elif args.describe:
        df = describe_table(args.describe)
        print(df.to_string(index=False))

    elif args.list_tables:
        df = list_tables(args.list_tables)
        print(df.to_string(index=False))

    elif args.query:
        if args.output:
            extract_and_save(
                args.query,
                args.output,
                use_cache=not args.no_cache,
            )
        else:
            df = run_query(args.query)
            print(df.to_string(index=False))

    else:
        parser.print_help()
