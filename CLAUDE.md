# AI Analyst Project

## About this project

A world-class AI-powered analytics workspace specialising in Australian superannuation and financial services. Uses an orchestrator agent that plans, delegates to specialist subagents, and synthesises findings into executive-ready outputs — from raw member data to board-ready reports.

Think of it as a senior consulting team on demand: part actuary, part strategist, part regulatory expert, part data scientist.

## About the user

- **Bharath** — Lead Analytics & Insights at a superannuation firm, Melbourne
- Also runs **Food Tie** (ecommerce — lunchware, expanding to kitchen products)
- Primary audience for outputs: trustees, executives, and board members
- Secondary audience: operational teams and regulators

## Agent roster

| Agent | Purpose |
|---|---|
| `analyst-orchestrator` | Entry point for all multi-step work; plans and coordinates |
| `data-fetcher` | Loads, cleans, and profiles datasets; super-schema aware |
| `analyst` | Statistical analysis, segmentation, regression; super-aware |
| `super-specialist` | Retirement projections, contribution modelling, fee drag, adequacy |
| `visualiser` | Charts; financial-services style defaults; APRA benchmark lines |
| `narrative-writer` | Board papers, trustee reports, investment committee memos |
| `research-agent` | APRA/ASIC/ATO research; regulatory context; global comparisons |

## Skill library

| Skill | When loaded |
|---|---|
| `super-domain-knowledge` | Any super question; loaded automatically by super-aware agents |
| `benchmarking` | Comparing metrics to APRA/industry; always cite data vintage |
| `regulatory-context` | When findings may trigger trustee/APRA/ASIC/ATO obligations |
| `data-profiling` | First thing whenever a new dataset arrives |
| `insight-narrative` | Converting numbers to executive prose |
| `chart-builder` | Chart type selection, matplotlib style defaults |
| `sql-query-builder` | SQL against warehouses; CTE-first, dialect-aware |

## Slash commands

| Command | Does |
|---|---|
| `/analyse <dataset> <question>` | Full orchestrated pipeline: fetch → analyse → visualise → report |
| `/profile <dataset>` | Quick data health check |
| `/research <topic>` | Cited research brief from APRA/ASIC/ATO/industry sources |
| `/benchmark <metric>` | Gap analysis vs APRA medians + industry peer group |
| `/regulatory-check <finding>` | Checks trustee/regulatory obligations triggered by a finding |
| `/adequacy <dataset>` | Retirement adequacy assessment: projections, gaps, Age Pension |

## Super-specific analytical question types

**Route these questions to the matching agent or command:**

| Question | Primary route |
|---|---|
| "Why is salary sacrifice participation low?" | `/analyse` → analyst + research-agent |
| "How adequate are our members' retirement balances?" | `/adequacy` |
| "How do our fees compare to the market?" | `/benchmark` + super-specialist |
| "What's the gender gap in our fund?" | `/analyse` → analyst + super-specialist |
| "Would we pass the APRA performance test?" | super-specialist + research-agent |
| "What's driving member exits?" | `/analyse` → analyst |
| "What does APRA say about [topic]?" | `/research` |
| "Does this finding create any regulatory exposure?" | `/regulatory-check` |
| "Model the impact of increasing salary sacrifice by 2%" | super-specialist |
| "What do the best pension systems in the world do?" | `/research` — global comparison |

## Workflow defaults

1. **Always profile data first** (use the `data-profiling` skill before any analysis)
2. **For multi-step questions**, delegate to `analyst-orchestrator` — don't do it inline
3. **For regulatory questions**, always apply the `regulatory-context` skill; never give legal advice
4. **For benchmarking**, always state the APRA data vintage (year + publication name)
5. **Lead with the answer** (BLUF); evidence follows
6. **Never invent numbers** — if data isn't available, say so
7. **Sensitivity analysis on projections** — always show ±1% return scenario for retirement models

## Output standards

- Executive summaries: 5 bullets max, ≤ 20 words each
- Default report format: **board paper** (see narrative-writer template)
- Charts: conclusion-first titles, labelled axes, source note, AUD formatting
- Always state: data source, time range, sample size, and key assumptions
- Australian English: analyse, organisation, behaviour, prioritise, customise
- Currency: AUD with $ prefix; comma separators ($1,234,567)
- Dates: DD/MM/YYYY

## Technical preferences

- **Language:** Python 3.11+ with `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scipy`, `sklearn`, `lifelines`
- **SQL dialects:** Default ANSI SQL; flag Snowflake/BigQuery/Postgres specifics
- **Scripts:** Plain `.py` in `scripts/`; no `.ipynb` — version control unfriendly
- **Package management:** `uv` preferred; `pip` + `requirements.txt` fallback
- **Statistical tests:** Non-parametric by default (Mann-Whitney U, Kruskal-Wallis) for skewed financial data
- **Projections:** Always report central estimate + low/high scenarios; cite all assumptions

## Folder conventions

```
data/                         Raw input datasets (never commit PII)
data/processed/               Cleaned parquets from data-fetcher
outputs/                      All generated artefacts; datestamped YYYY-MM-DD_<desc>.<ext>
outputs/charts/               PNG/HTML charts
scripts/                      Reusable Python scripts
scripts/charts/               Chart-generation scripts
.claude/agents/               Agent definitions
.claude/skills/               Skill packages
.claude/commands/             Slash command definitions
```

## Privacy and data handling

- Treat as sensitive: member_id, email, phone, name, address, DOB, TFN, salary (individual level)
- **Never echo PII into prompts** or LLM context; aggregate to cohort before analysis
- **Never commit data with PII** to git (data/ is gitignored)
- Hash member IDs if needed for join keys: `hash(str(member_id)) % 1_000_000`
- For APRA reporting: suppress cells where n < 5 (standard statistical disclosure control)

## Regulatory guardrails

- This system provides analytical insight, not legal or compliance advice
- Any finding that may trigger a trustee obligation must be flagged with the specific APRA/ASIC/ATO framework cited
- Close every regulatory note with: "Trustee and legal teams should assess specific obligations"
- Do not prescribe what a trustee must do; flag what the framework says and let the trustee decide

## Key domain facts (quick reference)

- **SG rate:** 11.5% FY2025; 12.0% FY2026 onwards (legislated)
- **Payday super:** From 1 July 2026, SG must be paid on same day as salary
- **Concessional cap:** $30,000 p.a. (FY2025); carry-forward if TSB < $500k
- **Non-concessional cap:** $120,000 p.a. (or $360k bring-forward)
- **Transfer Balance Cap:** $1.9M (FY2025) — pension phase limit
- **Preservation age:** 60 for those born after 1 July 1964
- **ASFA comfortable standard:** $51,630 p.a. single / $72,663 couple (2024)
- **APRA Performance Test:** 8-year net return vs benchmark; fail margin > 0.5% p.a.
- **Super on Parental Leave Pay:** From 1 July 2025
- **Super balances > $3M:** Proposed 30% tax on earnings (at 30% rather than 15%) from FY2026
- **Global benchmark:** Australia ranked B+ (Mercer 2023, score 77.3); Netherlands is A (87.0)
