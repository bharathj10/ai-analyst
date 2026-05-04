---
name: qa-analyst
description: Quality assurance checklist for all analysis outputs — verify numbers, logic, claims, charts, and regulatory statements before anything goes to an exec, trustee, or regulator
---

# QA Analyst Skill

## Context and audience

This skill is invoked as a final gate before any deliverable leaves the team. The audience for QA-reviewed outputs is always high-stakes: trustees, board members, executives, APRA reviewers, or media. A single wrong number, unqualified claim, or mislabelled chart destroys credibility — often in a room where you cannot correct it. The purpose of this skill is to make that impossible.

Load this skill whenever:
- The output-formatter agent is about to produce a final deliverable
- A narrative-writer agent has produced a board paper or trustee report
- Any finding includes a projection, benchmark comparison, or regulatory claim
- The user asks to "QA this", "sense-check", "double-check", or "review before sending"

---

## The five QA dimensions

### 1. Number integrity

Every figure cited in narrative or slide copy must be traceable to the underlying data or calculation.

**Checks:**
- [ ] Every number in the executive summary exists verbatim in the findings JSON or analysis output
- [ ] Percentages sum correctly (e.g., age-band breakdowns must sum to 100%)
- [ ] "vs benchmark" comparisons state which benchmark, which vintage (year), and which source
- [ ] Dollar figures use AUD, comma separators, and consistent precision (either $1.2M or $1,234,567 — never mix in the same document)
- [ ] Growth rates state the base period and end period explicitly ("growth from FY2022 to FY2024" not "recent growth")
- [ ] Sample sizes (n=) match the dataset profile, not a rounded guess
- [ ] Projections state the return assumption, inflation assumption, and time horizon in the body text or footnote — not just in appendix

**Red-flag patterns to catch:**
- "approximately X%" — replace with the exact figure or explain why precision is unavailable
- Round numbers that look too clean (e.g., exactly 50.0%) — verify against data or flag
- KPIs that contradict each other (e.g., "participation fell" in body but chart shows an increase)
- A number cited twice with different values (copy-paste error)

---

### 2. Claim integrity

Every descriptive or inferential claim must be supported by the evidence in the analysis.

**Checks:**
- [ ] Causal language is only used where a causal test was performed ("X causes Y" requires regression or experiment; otherwise use "X is associated with Y" or "X predicts Y")
- [ ] Superlatives are supported ("highest", "lowest", "most" must be compared against a stated peer group)
- [ ] Trend claims cover an explicit time window ("improving over the past 3 years" — state the years)
- [ ] Segment comparisons control for obvious confounders where relevant (e.g., gender gap analysis should note whether age/salary were controlled for)
- [ ] No claims are made about future performance unless explicitly framed as modelled scenarios with stated assumptions
- [ ] "Members are at risk" or similar welfare claims cite the ASFA standard or actuarial threshold used

**Common failures to catch:**
- "significantly higher" used without a statistical test — replace with magnitude ("18 percentage points higher") or perform the test
- Benchmarks from different time periods compared as if contemporaneous
- Finding labelled as "finding" when it is actually a hypothesis or directional observation

---

### 3. Chart integrity

**Checks:**
- [ ] Every chart has a title that states the conclusion (not the dimension)
- [ ] Axes are labelled with units (%, $, years, #members)
- [ ] Y-axis starts at zero for bar/column charts unless explicitly justified (with a note)
- [ ] Source note present on every chart: "Source: [dataset name] | n=X | [date] | Analytics & Insights"
- [ ] Colour is not the sole differentiator (use labels, patterns, or direct annotation for accessibility)
- [ ] APRA benchmark reference lines are labelled with the benchmark name and year
- [ ] No chart shows more than 5–6 series (beyond that, break into separate charts or use a table)
- [ ] Chart caption states what the chart shows — the conclusion the reader should draw

**Common failures:**
- Dual-axis charts where the two scales mislead the relationship — use two separate charts instead
- Pie charts with more than 5 slices — use a bar chart
- Truncated y-axis inflating the appearance of change

---

### 4. Regulatory and compliance integrity

Any regulatory claim carries trustee and legal risk if wrong. This dimension is non-negotiable.

**Checks:**
- [ ] Every APRA/ASIC/ATO citation includes the specific standard or section (e.g., SPS 515, s52 SIS Act — not just "APRA regulations")
- [ ] Regulatory thresholds cited are the current legislated values (verify against `super-domain-knowledge` skill)
- [ ] The APRA Performance Test logic is correct: 8-year net return, vs Strategic Asset Allocation benchmark, fail margin > 0.5% p.a.
- [ ] Contribution cap figures match the correct financial year
- [ ] SG rate cited matches the correct financial year (11.5% FY2025; 12.0% FY2026+)
- [ ] The document closes regulatory observations with: "Trustee and legal teams should assess specific obligations"
- [ ] The document does not prescribe what the trustee must do — it flags the framework and defers

**Automatic red flags — stop and verify before proceeding:**
- Any claim that the fund is compliant or non-compliant (that is a legal determination, not an analytical one)
- Use of "breach" without "potential" qualifier unless an actual breach has been formally determined
- Citing preservation rules without confirming the member's date of birth cohort

---

### 5. Document completeness and formatting

**Checks:**
- [ ] Classification marking on every page (CONFIDENTIAL — INTERNAL USE ONLY or equivalent)
- [ ] Source note states: dataset name, n=, date of extract, and team name
- [ ] Time range of data is stated in the document header or executive summary
- [ ] No placeholder text remaining ("TBC", "TODO", "[INSERT]", "DRAFT")
- [ ] Australian English throughout: analyse, organisation, behaviour, prioritise, customise, recognise
- [ ] Dates in DD/MM/YYYY format
- [ ] Currency formatted as AUD ($X,XXX,XXX or $X.XM)
- [ ] Consistent heading hierarchy (no skipped heading levels)
- [ ] Recommendations include: owner, timeframe, and priority — not just the action

---

## QA output format

When completing a QA pass, produce a structured sign-off block:

```
## QA Sign-off

**Reviewer:** [agent or analyst name]
**Date:** DD/MM/YYYY
**Status:** PASS / PASS WITH NOTES / HOLD — ISSUES FOUND

### Numbers verified
- [x] Executive summary figures verified against findings JSON
- [x] Benchmark comparisons cite vintage and source
- [ ] ⚠ Projection on slide 4 does not state return assumption — added to caveats

### Claims verified
- [x] No unsupported causal language
- [x] Trend claims have explicit time windows

### Charts verified
- [x] All charts have conclusion-first titles
- [ ] ⚠ Figure 2 y-axis starts at 40% — annotation added to explain truncation

### Regulatory verified
- [x] SG rate and contribution caps match FY2025 values
- [x] Regulatory observations close with trustee deferral language

### Formatting verified
- [x] Classification marking on all pages
- [x] Australian English throughout
- [x] No placeholder text

### Issues requiring action before release
1. [Issue 1 — specific, with fix]
2. [Issue 2 — specific, with fix]
```

If status is **HOLD**, the output must not be delivered until every issue is resolved and QA is re-run.

---

## Quick QA checklist (one-pass scan)

Copy this before every send:

```
Numbers:  [ ] All figures traceable  [ ] Percentages sum  [ ] n= stated  [ ] Benchmarks cited with vintage
Claims:   [ ] No unsupported causality  [ ] Superlatives justified  [ ] Time windows explicit
Charts:   [ ] Conclusion titles  [ ] Axes labelled  [ ] Source notes  [ ] No misleading scales
Regulatory: [ ] Specific standards cited  [ ] Caps/rates match FY  [ ] Trustee deferral language
Format:   [ ] Classification  [ ] No placeholders  [ ] AU English  [ ] DD/MM/YYYY  [ ] AUD
```
