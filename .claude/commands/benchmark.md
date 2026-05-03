---
description: Benchmark a fund metric against APRA industry data or peer group
argument-hint: <metric or dataset path> [vs <comparator>]
---

You're being asked to benchmark: $ARGUMENTS

Run this as a two-agent workflow:
1. **research-agent** — fetch current APRA benchmark data for the relevant metric (state which APRA publication to use: AFLSS, quarterly stats, heatmap)
2. **super-specialist** — compute the gap between the subject metric and the benchmark; produce the benchmarking table and dollar-impact analysis

Output format: a benchmarking table (subject vs APRA median vs top-quartile threshold), gap analysis in both percentage points and dollar terms, and a tier classification (top quartile / above median / below median / bottom quartile).

Save to `outputs/YYYY-MM-DD_benchmark_<metric>.md`.
