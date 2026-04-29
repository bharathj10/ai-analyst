---
name: sql-query-builder
description: Use this skill when writing SQL against a data warehouse. Helps construct queries that are dialect-aware, performant, and safe. Trigger on requests like "query the warehouse", "write SQL to get", "extract data from <database>", or any time a SQL query needs to be authored or reviewed.
---

# SQL query builder

## When to use

Any time SQL needs to be written or reviewed. Especially when the user mentions a specific warehouse (Snowflake, BigQuery, Postgres, Redshift, Databricks).

## Workflow

1. **Confirm dialect first.** Ask if not stated. Default to ANSI SQL but flag dialect-specific functions.
2. **Confirm the table(s) and columns** before writing the query. If schema isn't known, suggest the user run `DESCRIBE <table>` or equivalent first.
3. **Build the query incrementally**:
   - Start with the FROM clause
   - Add filters (WHERE)
   - Add joins
   - Add aggregations (GROUP BY)
   - Add ordering and limits
4. **Always add a LIMIT** on first run (default 1000) so the user can sanity-check before pulling full data.
5. **Format with readable indentation** — CTEs over deeply nested subqueries.

## Patterns to use

### CTE-first style
```sql
WITH base AS (
    SELECT ...
    FROM raw_table
    WHERE event_date >= DATE '2025-01-01'
),
enriched AS (
    SELECT b.*, dim.category
    FROM base b
    LEFT JOIN dimension dim USING (id)
)
SELECT ...
FROM enriched
```

### Date filtering — be explicit about timezones
- Snowflake: `event_ts >= TIMESTAMP '2025-01-01 00:00:00'`
- BigQuery: `DATE(event_ts, "Australia/Melbourne") >= '2025-01-01'`
- Postgres: `event_ts AT TIME ZONE 'Australia/Melbourne' >= '2025-01-01'`

### Window functions for ranking and running totals
Prefer over self-joins.

## Anti-patterns to avoid

- `SELECT *` in production queries — always enumerate columns
- `WHERE function(column) = value` — non-sargable, prevents index use
- Implicit type casts in joins
- Cartesian joins from missing ON conditions
- `GROUP BY` with column position (`GROUP BY 1, 2`) — use names

## Safety

- For any DELETE/UPDATE/DROP, **always show the equivalent SELECT first** for the user to verify the affected rows
- Wrap destructive operations in transactions where the dialect supports it
- Never write queries that could expose PII unmasked
