---
name: chart-builder
description: Use this skill when creating charts from data. Provides chart-type selection guidance, styling defaults, and reusable matplotlib/plotly templates. Trigger on requests like "make a chart", "visualise", "plot", or as part of any analysis that needs visual output.
---

# Chart builder

## Chart selection

Match chart type to the question:

| Question | Chart |
|---|---|
| How does X change over time? | Line chart |
| How do categories compare? | Horizontal bar (sorted) |
| What's the distribution of X? | Histogram or box plot |
| How does X relate to Y? | Scatter (with trend line if linear) |
| What's the composition of X? | Stacked bar or treemap (avoid pie unless 2-3 slices) |
| How do two distributions compare? | Overlaid density or side-by-side box |
| Cohort over time | Heatmap |

## Title rule

The title states the **conclusion**, not the dimension.

❌ "Member balances by age group"
✅ "Members aged 45-54 hold 42% of total balances"

## Default style — matplotlib

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update({
    "figure.figsize": (12, 7),
    "figure.dpi": 110,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.labelsize": 11,
})

# Australian number formatting helpers
def aud(x, _): return f"${x:,.0f}"
def pct(x, _): return f"{x:.1f}%"
def thousands(x, _): return f"{x:,.0f}"
```

## Standard footer

Every chart needs a source note:

```python
fig.text(
    0.99, 0.01,
    f"Source: {dataset_name} | n={n:,} | {date_range}",
    ha="right", va="bottom", fontsize=8, color="gray", style="italic"
)
```

## Palettes

- **Default sequential:** `viridis`
- **Diverging (good vs bad):** `RdYlGn` (use sparingly — colourblind-unfriendly)
- **Categorical (≤6 series):** `tab10`
- **Brand:** if user provides hex codes, save them in `outputs/_brand.py` for reuse

## Output

- Save as PNG at 1200x800 minimum: `plt.savefig(path, dpi=150, bbox_inches="tight")`
- Filename: `outputs/charts/<YYYY-MM-DD>_<descriptive_name>.png`
- For interactive exploration, use plotly and save as HTML alongside

## Anti-patterns

- 3D charts
- Pie charts with > 4 slices
- Dual y-axes (use small multiples instead)
- Truncated y-axis on bar charts (misleading)
- Rainbow/`jet` colormap
- Charts without units or source notes
