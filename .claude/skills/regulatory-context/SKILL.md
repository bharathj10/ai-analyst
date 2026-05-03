---
name: regulatory-context
description: Australian superannuation regulatory context for analysis — flags when findings have regulatory implications, surfaces relevant APRA/ASIC/ATO rules, and frames analysis within trustee obligations. Load when analysis touches member outcomes, fees, insurance, performance, or governance.
---

# Regulatory context skill

## When to use

Load this skill when analysis findings could intersect with:
- Trustee duties (best financial interests, conflicts of interest)
- APRA prudential obligations (SPS 515 member outcomes, SPS 530 investment governance)
- ASIC disclosure obligations (RG 97 fees, PDS accuracy)
- ATO compliance (contribution caps, TFN, SG)
- Insurance within super (SPS 250, *Protecting Your Super*)
- Retirement income strategy (Retirement Income Covenant)

Do NOT give legal advice. Flag regulatory considerations and recommend trustee/legal review.

---

## Trustee duties (SIS Act s52)

The core obligations every trustee analysis must be conscious of:

1. **Act in the best financial interests of beneficiaries** (amended 2021; "financial" added — clarifies trustees should not pursue non-financial objectives at the cost of member returns without member consent)
2. **Exercise care, skill and diligence** of a prudent superannuation trustee
3. **Maintain undivided loyalty** to beneficiaries (no conflicts of interest)
4. **Keep trust assets separate** from other assets
5. **Not bind discretion** by outside direction
6. **Act with prudence** in formulating investment strategy

### Regulatory red flags in analysis — check for these

| Finding type | Regulatory implication | Framework |
|---|---|---|
| Fund underperforming peers by >0.5% p.a. over 8 years | APRA Performance Test failure risk; member notification required | SPS 515, Pt 2A |
| Members paying fees on zero-balance accounts | "Protecting Your Super" — auto-consolidation/closure required | SIS Act s68AA |
| Insurance eroding low balances | SIS Act obligations to cancel default insurance if balance < $6,000 or inactive 16+ months | SPS 250 |
| Disclosure of fees inconsistent with actual charges | Breach of RG 97; potential misleading PDS | ASIC RG 97 |
| Member not receiving SG contributions | ATO SGC obligation; employer non-compliance | SGC Act 1992 |
| Contribution above concessional cap | Excess CC included in assessable income; ATO admin charge | ITAA 1997 |
| Balance in pension phase exceeding Transfer Balance Cap | Excess must be removed; ATO excess transfer balance tax | ITAA 1997 |
| Investment option not aligned to stated SAA | Potential SPS 530 breach; liquidity risk | SPS 530 |

---

## APRA Heatmap — what it measures

APRA publishes an annual heatmap rating MySuper products on:
- **Investment performance** (net return vs benchmark, 1/5/8 years)
- **Investment fees** (vs peer group)
- **Administration fees** (vs peer group by balance band)
- **Sustainability** (projected member balance at 67 in 10 years)

Traffic light: green (top 25%), yellow, orange, red (bottom 25%). Red = consider trustee action.

When a fund's metric appears in the bottom quartile, APRA expects the trustee to document why and what action is planned (SPS 515 Business Performance Review).

---

## SPS 515 — Strategic planning and member outcomes

Key obligations for analytical work:
1. **Business Performance Review (BPR)** — annual; must assess products against member outcomes and competitors. Analysis you produce may feed into BPR.
2. **Outcomes Assessment** — must demonstrate each product delivers outcomes "not materially inferior" to comparable products
3. **Strategic Plan** — 3+ year documented plan; analysis should link to strategic objectives

What "member outcome" means quantitatively:
- Net return at each balance band ($10k, $50k, $100k, $250k)
- Total cost compared to equivalent products
- Insurance appropriateness
- Ancillary benefits (advice, education)

---

## SPS 530 — Investment governance

Relevant for any asset allocation or return analysis:
- Fund must have documented Investment Governance Framework
- Investment strategy must consider liquidity risk (portion of assets readily realisable within 3 months)
- Stress test liquidity annually (assume 20-30% redemption in stressed market)
- Derivatives: strict governance requirements (only for hedging or efficient portfolio management)
- Unlisted assets valuation: independent, at least annually; more frequently if market conditions change

When unlisted assets >20-25% of portfolio: flag liquidity risk in analysis.

---

## Retirement Income Covenant (from 1 July 2022)

Trustees must formulate, review, and give effect to a **Retirement Income Strategy (RIS)** covering members at or approaching retirement.

The RIS must consider:
- Expected retirement income (from all sources: super + Age Pension + non-super)
- Managing risks: longevity risk, sequencing risk, inflation risk
- Flexible access (some members may need lump sums for health, housing, etc.)

Analytical implications:
- Flag members in pre-retirement cohort (55-65) for RIS-aligned communication
- Retirement income projections should include Age Pension modelling
- Drawdown rate analysis: default 4-5% drawdown is common; actuarially, 5-6% may be sustainable to 90th percentile mortality for a 67-year-old

---

## Insurance within super — SPS 250 key rules

1. **Default insurance** (death + TPD) must be offered for MySuper members unless inappropriate
2. **Opt-out mechanism** required; members can cancel at any time
3. **Protecting Your Super (2019):** Cancel insurance if:
   - Account balance < $6,000, OR
   - No contributions in 16+ months (inactive) AND member has not confirmed they want insurance
4. **Occupational rating** — must price appropriately for risk (e.g., white collar vs blue collar vs hazardous)
5. **Group insurance arrangements** — trustees must annually review whether terms remain in members' best financial interests

Analytical flags:
- Members with large insurance premiums relative to balance (premium drain analysis)
- Young members (<25) who may have inappropriate default cover
- Members who qualified for inactivation-based cancellation but were retained

---

## ATO compliance quick reference

### Superannuation Guarantee (SG) obligations
- Employer must pay SG on employee's OTE (not total package, unless agreed otherwise)
- Due: 28 days after end of each quarter (Jan, Apr, Jul, Oct) → **Payday Super from 1 Jul 2026: due same day as salary**
- Shortfall → SGC (Superannuation Guarantee Charge): SG amount + nominal interest + administration charge; not tax-deductible
- Underpayment to specific employees is common; payroll data analysis can surface this

### Contribution cap breaches
- CC excess → included in assessable income at marginal rate; ATO issues excess CC determination; member has 60 days to decide: pay tax from super or personally
- NCC excess → 47% tax unless returned within 85-day election window
- Analytical flag: any member with multiple employer records (new and old job in same year) may breach CC without realising

### SMSF-specific
- Annual return and audit required; ATO administers
- Non-arm's-length income (NALI) rules: artificially low or high related-party transactions → taxed at 45%
- In-house asset rule: max 5% of fund assets in investments with related parties

---

## How to flag regulatory context in analysis outputs

Add a **Regulatory considerations** section (before Caveats) in any report that touches the above topics:

```markdown
## Regulatory considerations

The following findings may have regulatory implications. These are observations only —
trustee and legal teams should assess and respond appropriately.

- [Finding X]: [Relevant framework — e.g., "Members with premium drain >50% of contribution
  may trigger SPS 250 review obligations."]
- [Finding Y]: [Relevant framework]

This analysis does not constitute legal or compliance advice.
```

Always be specific: cite the framework (SPS 515, RG 97, SIS Act s52) not just "regulatory issues".
