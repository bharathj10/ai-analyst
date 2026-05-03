---
description: Run a retirement adequacy assessment on a member dataset — projects balances to retirement, gaps to ASFA standard, Age Pension dependency
argument-hint: <dataset path> [retirement age, default 67]
---

You're being asked to run a retirement adequacy assessment.

**Dataset:** `$1`
**Retirement age:** ${2:-67}

Use the following three-agent workflow:
1. **data-fetcher** — load and profile the dataset; derive `age_band`, `balance_quartile`, `is_voluntary_contributor`, `years_to_retirement`
2. **super-specialist** — for each age band × balance quartile cohort, run `project_balance()` and `income_sustainability()` from the calculation engine; compare to ASFA comfortable ($51,630 p.a. single) and modest ($32,030 p.a. single) standards; calculate Age Pension eligibility using the assets test approximation; identify % adequate / borderline / inadequate per cohort
3. **narrative-writer** — produce a board paper format report with: adequacy heatmap table, gap distribution, Age Pension dependency estimate, gender breakdown if gender column exists, and 3-5 specific recommendations

Key outputs:
- `outputs/YYYY-MM-DD_adequacy_assessment.md` (board paper)
- `outputs/charts/YYYY-MM-DD_adequacy_heatmap.png`
- `outputs/charts/YYYY-MM-DD_projected_balance_by_age_band.png`
- `outputs/YYYY-MM-DD_adequacy_results.json`

Flag the cohorts with the highest adequacy risk. State all projection assumptions explicitly.
