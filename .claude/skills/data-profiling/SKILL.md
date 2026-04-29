---
name: data-profiling
description: Use this skill whenever a new dataset is loaded and needs a quick health-check. Produces shape, dtype, missingness, cardinality, and distribution summaries. Trigger on phrases like "profile this data", "what's in this file", "check this dataset", or as the first step of any analysis on unfamiliar data.
---

# Data profiling

## When to use

Any time a dataset is encountered for the first time in a session, before doing any analysis on it.

## Output

A profile report covering:

1. **Shape** — rows, columns, memory footprint
2. **Schema** — column name, dtype, non-null count, null %
3. **Numeric columns** — min, p25, median, mean, p75, max, std
4. **Categorical columns** — cardinality, top 5 values with counts
5. **Datetime columns** — min, max, range
6. **Quality flags** — duplicate rows, columns with >50% nulls, constant columns, suspected ID columns

## Implementation

Use this script as a starting point. Save the output to `outputs/_profile_<dataset>.md`.

```python
import pandas as pd
import numpy as np
from pathlib import Path
import sys

def profile(path: str | Path) -> str:
    path = Path(path)
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    lines = [f"# Profile: {path.name}", ""]
    lines.append(f"- Rows: {len(df):,}")
    lines.append(f"- Columns: {df.shape[1]}")
    lines.append(f"- Memory: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
    lines.append(f"- Duplicate rows: {df.duplicated().sum():,}")
    lines.append("")

    lines.append("## Schema")
    lines.append("| Column | Dtype | Non-null | Null % |")
    lines.append("|---|---|---|---|")
    for col in df.columns:
        nn = df[col].notna().sum()
        pct = (1 - nn / len(df)) * 100
        lines.append(f"| {col} | {df[col].dtype} | {nn:,} | {pct:.1f}% |")
    lines.append("")

    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols):
        lines.append("## Numeric summary")
        lines.append(df[num_cols].describe().to_markdown())
        lines.append("")

    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(cat_cols):
        lines.append("## Categorical summary")
        for col in cat_cols:
            top = df[col].value_counts().head(5)
            lines.append(f"**{col}** (cardinality: {df[col].nunique():,})")
            for val, cnt in top.items():
                lines.append(f"  - {val}: {cnt:,}")
            lines.append("")

    flags = []
    if df.duplicated().sum() > 0:
        flags.append(f"⚠ {df.duplicated().sum():,} duplicate rows")
    high_null = [c for c in df.columns if df[c].isna().mean() > 0.5]
    if high_null:
        flags.append(f"⚠ Columns >50% null: {high_null}")
    constant = [c for c in df.columns if df[c].nunique(dropna=False) == 1]
    if constant:
        flags.append(f"⚠ Constant columns: {constant}")

    if flags:
        lines.append("## Quality flags")
        for f in flags:
            lines.append(f"- {f}")

    return "\n".join(lines)


if __name__ == "__main__":
    print(profile(sys.argv[1]))
```

## Notes

- For datasets > 1GB, sample to 1M rows for the categorical/numeric summary but report exact shape.
- For datetime columns, also report frequency (daily, monthly) by inspecting gaps.
- Always save the profile output before starting analysis — it's the audit trail.
