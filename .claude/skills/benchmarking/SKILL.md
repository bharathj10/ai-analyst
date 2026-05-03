---
name: benchmarking
description: Industry benchmarking methodology for financial services and superannuation analysis. Provides frameworks for comparing fund performance, fees, member outcomes, and engagement metrics against APRA data and industry peers.
---

# Benchmarking skill

## When to use

Any time an analysis needs to be contextualised against:
- Industry medians or percentiles (APRA-published data)
- Peer group (industry funds vs retail vs public sector)
- Time series baseline (fund's own history)
- International comparisons (global pension systems)
- Internal targets or strategic plan KPIs

Benchmarking without context is noise. Every number should have a comparator.

---

## Benchmark hierarchy (use in order of preference)

1. **APRA published data** — authoritative, primary source for Australian super
2. **Association research** (ASFA, AIST, FSC) — industry surveys, often more granular
3. **Commercial ratings** (SuperRatings, Rainmaker, Chant West) — member surveys, fund rankings
4. **Peer comparable** — funds of similar size, member profile, or product type
5. **Internal target** — fund's own strategic plan KPI (document the source)
6. **International** — only for structural/design comparisons; not apples-to-apples

---

## Key APRA benchmarks to reference

### Investment returns (MySuper balanced options, net of fees and tax)
| Period | Industry fund median | Retail fund median |
|---|---|---|
| 1 year (FY2024) | ~8.5% | ~7.8% |
| 3 year p.a. | ~5.5% | ~4.9% |
| 5 year p.a. | ~6.8% | ~6.0% |
| 7 year p.a. | ~7.4% | ~6.6% |
| 10 year p.a. | ~7.9% | ~7.0% |

*Note: Always fetch current APRA data for live analysis. These are indicative for framing questions.*

### Fee benchmarks (MySuper, $50k balance)
| Sector | Total fees median |
|---|---|
| Industry funds | ~0.70–0.90% p.a. |
| Retail funds | ~1.00–1.40% p.a. |
| Public sector | ~0.45–0.70% p.a. |
| SMSF | ~1.50–2.00% p.a. (on small balances) |

APRA Performance Test threshold: >0.5% p.a. underperformance for 8 years → mandatory member notification.

### Member metrics (industry averages)
| Metric | Typical range |
|---|---|
| Average account balance (all ages) | ~$115,000 |
| Median account balance (all ages) | ~$72,000 |
| Average balance at retirement | ~$200,000 (men) / ~$160,000 (women) |
| Member churn rate (annual) | ~3–5% |
| Salary sacrifice participation | ~20–25% of members |
| Active engagement (login last 12mo) | ~30–40% |
| Insurance opt-out rate | ~10–15% (post Protecting Your Super) |

---

## How to structure a benchmarking analysis

### Step 1 — Define the comparison universe
State clearly:
- What is being compared (e.g., "salary sacrifice participation rate")
- The subject (e.g., "our fund's 35-44 age cohort")
- The comparator (e.g., "APRA industry fund median for that age band")
- The time period (e.g., "FY2025 Q1")
- The data source for the comparator (cite it)

### Step 2 — Check unit compatibility
Common traps:
- Return figures: gross vs net of fees; net of fees only vs net of fees and tax
- Balance figures: mean vs median (super is right-skewed; mean > median significantly)
- Fee figures: investment fee only vs total cost of product (RG 97)
- Coverage: all members vs active members only; employed vs unemployed

### Step 3 — Calculate the gap and direction
```python
gap = subject_value - benchmark_value
gap_pct = (subject_value / benchmark_value - 1) * 100
direction = "above" if gap > 0 else "below"
```

### Step 4 — Contextualise with confidence
Always state:
- Sample size (flag n < 100 as low confidence)
- Time period
- Whether the gap is statistically significant
- Possible confounders (e.g., our fund has older average member age → naturally higher balance)

### Step 5 — Rank or tier if comparing multiple groups

Use percentile ranking when data allows:
```python
import scipy.stats as stats
percentile_rank = stats.percentileofscore(peer_values, subject_value)
```

Or qualitative tiers:
- **Top quartile** (>75th pctile)
- **Above median** (50-75th pctile)
- **Below median** (25-50th pctile)
- **Bottom quartile** (<25th pctile)

---

## Output format for benchmarking

### Single metric benchmark
```
[Metric]: [Subject value] vs [Benchmark value] ([Source])
→ [X]% above/below benchmark
→ Context: [1-2 sentence explanation of what drives the gap]
```

### Multi-metric dashboard (markdown table)
| Metric | Our Fund | APRA Median | Gap | Tier |
|---|---|---|---|---|
| 10yr net return | 8.2% | 7.9% | +0.3% | Above median |
| Total fees ($50k bal) | 0.78% | 0.82% | -0.04% | Above median |
| Salary sacrifice rate | 18.4% | 22.1% | -3.7pp | Below median |
| NPS | +42 | +35 | +7 | Top quartile |

### Trend benchmarking
Plot fund metric alongside industry median over time. Use dual series: fund in solid line (brand colour), benchmark as dashed grey line. Label the gap at the latest data point.

---

## International benchmarking — caveats

Use international comparisons for structural/design arguments only (contribution rates, coverage, adequacy). Do not directly compare investment returns across countries due to:
- Different tax treatment (some report gross, some net)
- Currency effects
- Different asset allocation norms
- Different reporting periods

Safe international comparisons:
- Contribution rate (% of salary) — Australia 12% vs Netherlands ~17% vs US 3-6% voluntary
- System adequacy (Mercer Index score)
- Coverage rate (% of workforce)
- Replacement rate (% of pre-retirement income)

---

## Common benchmarking errors to avoid

- Comparing mean to median without noting the difference
- Using a peer group that doesn't match the fund's profile (large fund vs small fund)
- Ignoring survivorship bias in long-run return comparisons (closed/merged funds excluded)
- Treating external benchmarks as current when they may be 12-18 months stale
- Confusing investment return benchmark (e.g. CPI+3%) with peer comparison benchmark
