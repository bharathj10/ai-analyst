# Project: Retirement Adequacy Assessment

**Business question:** Are our members on track for a comfortable retirement? Where are the biggest gaps, and what should we do about it?

**Owner:** Analytics & Insights
**Audience:** Trustee board — June 2026 meeting
**Data source:** `data/super_members_2026Q1.csv` (5,000 synthetic members, snapshot 31 March 2026)
**Time range:** Q1 2026 snapshot; projections to age 67
**Active project folder:** `projects/retirement-adequacy/`

## Analytical scope

1. Retirement adequacy by age band × balance quartile cohort
2. Gap to ASFA comfortable standard ($51,630 p.a. single / $72,663 couple)
3. Age Pension dependency estimate
4. Gender gap in projected retirement balances
5. Salary sacrifice participation benchmarked against APRA industry medians
6. Regulatory considerations (SPS 515 member outcomes obligations)

## Assumptions

- Projection rate: 7.5% p.a. net (base), 5.5% (downside), 9.5% (upside)
- Inflation: 2.5% p.a.
- Retirement age: 67
- SG rate: 11.5% FY2025, 12.0% FY2026+
- Fees: use `annual_fees_aud` from dataset
- Current salary sacrifice continued at observed rate

## Outputs

All outputs saved under `projects/retirement-adequacy/outputs/`.
Charts under `projects/retirement-adequacy/outputs/charts/`.
