# AI Analyst — Team Guide

**Version:** 2.0 | **Maintained by:** Bharath (Analytics & Insights) | **Last updated:** May 2026

---

## What is this?

The AI Analyst is a multi-agent analytics system that takes a business question and a dataset — or a Databricks table — and produces a complete analytical deliverable: statistical findings, charts, a written report, and a presentation deck. It is purpose-built for Australian superannuation analytics but handles any structured data question.

Think of it as a senior analyst you can brief in plain English. It knows the SIS Act, contribution rules, APRA benchmarks, and global pension systems. It writes in Australian English and formats outputs for board and executive audiences.

**What it replaces:** the 1-3 day cycle of manually extracting data, writing Python, building charts, formatting slides, and writing up findings. Most analyses run in under 30 minutes.

**What it does not replace:** your judgement. Every output should be reviewed before it goes to stakeholders. The system is a force multiplier, not an autonomous decision-maker.

---

## Quick start (3 steps)

### Step 1 — Open the project
```bash
cd ~/Projects/ai-analyst
source .venv/bin/activate   # activate Python environment
claude                       # launch Claude Code
```

### Step 2 — Ask a question or run a command
```
/analyse data/your_file.csv "what's driving low salary sacrifice participation among 25-34 year-olds?"
```

### Step 3 — Collect your outputs
Everything lands in `outputs/` with today's date prefix:
- `YYYY-MM-DD_<topic>.md` — the written report
- `YYYY-MM-DD_<topic>_deck.pptx` — the slide deck
- `YYYY-MM-DD_<topic>_report.docx` — the Word document
- `outputs/charts/` — all charts as PNGs

---

## Slash command reference

| Command | What it does | Example |
|---|---|---|
| `/analyse <file> <question>` | Full pipeline: profile → analyse → charts → report → deck | `/analyse data/members.csv "what's the gender gap in balances?"` |
| `/profile <file>` | Quick data health check — shape, nulls, duplicates, flags | `/profile data/members.csv` |
| `/adequacy <file>` | Retirement adequacy assessment — projections, ASFA gaps, Age Pension dependency | `/adequacy data/members.csv` |
| `/research <topic>` | Cited research brief from APRA, ASIC, ATO, industry sources | `/research "APRA performance test methodology"` |
| `/benchmark <metric>` | Gap vs APRA industry medians, peer group, dollar impact | `/benchmark "our fund's 10yr net return of 8.1%"` |
| `/regulatory-check <finding>` | Flags trustee/APRA/ASIC obligations triggered by a finding | `/regulatory-check "members with insurance premium >20% of employer contribution"` |
| `/format <findings file>` | Converts analysis findings into PPTX + Word + Markdown | `/format outputs/2026-05-01_findings.json` |

---

## Common workflows

### "I have a CSV and a question"
```
/analyse data/your_file.csv "your question in plain English"
```
The orchestrator plans the work, runs each specialist agent in sequence, and assembles a full deliverable. For most datasets: under 20 minutes.

### "I want to query Databricks directly"
See [Databricks connection setup](#databricks-connection-setup) below. Once configured:
```
Analyse member contribution patterns for FY2025 from the Unity Catalog table
main_catalog.super_analytics.member_contributions — focus on salary sacrifice
by age band and compare to the APRA industry benchmark.
```
The data-fetcher agent connects to your SQL warehouse, extracts the data, profiles it, and passes it to the analyst. No manual extract needed.

### "I need a board paper on X"
Either run `/analyse` first, then ask for a board paper format:
```
/analyse data/members.csv "retirement adequacy by age cohort"
```
Or, if you already have findings:
```
Turn the findings at outputs/2026-05-01_findings.json into a board paper for the June trustee meeting.
```
The narrative-writer will produce a document in the correct board paper format with executive summary, key findings with charts, regulatory considerations, and recommendations.

### "What does APRA say about [topic]?"
```
/research "APRA SPS 515 member outcomes assessment requirements"
```
Returns a cited research brief with specific regulation references, current APRA guidance, and any recent changes.

### "How do we compare to the market?"
```
/benchmark "our fund's salary sacrifice participation rate of 18.4% for 35-44 year-olds"
```
Returns a benchmarking table against APRA industry medians, tier classification (top quartile / above median / etc.), and the dollar impact of the gap.

### "Does this finding create a compliance issue?"
```
/regulatory-check "237 members have insurance premiums exceeding 30% of their employer contribution"
```
Returns the specific APRA/ASIC/ATO frameworks that apply, what the trustee obligation is, and the recommended action.

### "What would happen if we increased salary sacrifice by 2%?"
```
Model the impact of increasing salary sacrifice by 2% of salary for all members
aged 30-44 who are not currently participating. Project the change in retirement
balance at age 67 and the reduction in Age Pension dependency.
```
The super-specialist agent runs the projection calculations and returns a sensitivity analysis with central estimate and low/high scenarios.

### "I want to understand the global context"
```
/research "how do other countries handle retirement income adequacy — focus on Netherlands, Canada, and UK vs Australia"
```
Returns a comparative research brief using the Mercer Global Pension Index data and OECD statistics.

---

## Databricks connection setup

The system connects to Databricks via the SQL connector. One-time setup per machine:

### 1. Install the connector
```bash
pip install databricks-sql-connector python-dotenv
```

### 2. Create your credentials file
Copy the template and fill in your details:
```bash
cp .env.example .env
```

Edit `.env` with your actual values (never commit this file):
```
DATABRICKS_HOST=https://adb-xxxx.xx.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxx
DATABRICKS_TOKEN=dapixxxxxxxxxxxxxxxx
```

**Where to find these values:**
- `DATABRICKS_HOST`: Your Databricks workspace URL (from browser address bar, just the `https://...azuredatabricks.net` part)
- `DATABRICKS_HTTP_PATH`: Databricks workspace → SQL Warehouses → your warehouse → Connection Details tab → HTTP Path
- `DATABRICKS_TOKEN`: Databricks workspace → Settings → Developer → Access Tokens → Generate New Token

### 3. Test the connection
```bash
python scripts/databricks_connector.py --test
```
Should print: `Connection OK | Workspace: ...`

### 4. Ask questions against live data
Once connected, you can reference Databricks tables directly in your prompts:
```
Profile the table main_catalog.super_analytics.member_snapshot_2025q4
```
```
/analyse main_catalog.super_analytics.member_snapshot_2025q4 "what's driving member exits?"
```

The data-fetcher agent automatically uses the Databricks connector when a table path (containing `.`) is detected instead of a local file path.

### Unity Catalog table naming
All tables use three-part names: `catalog.schema.table`

Common schemas in a super fund context:
| Schema | Contents |
|---|---|
| `super_analytics.member_*` | Member snapshots, profiles, demographics |
| `super_analytics.contributions_*` | Contribution transactions, SG, voluntary |
| `super_analytics.balances_*` | Account balance history |
| `super_analytics.investments_*` | Investment option holdings, performance |
| `super_analytics.insurance_*` | Insurance premium and claims data |
| `super_analytics.engagement_*` | Logins, app usage, comms history |

---

## Output formats explained

### Markdown report (`.md`)
The primary analytical output. Contains executive summary, numbered findings with charts embedded, regulatory flags, recommendations, caveats, and appendix. Readable in any text editor, GitHub, or VS Code. Best for: internal sharing, source document.

### PowerPoint deck (`.pptx`)
Consultant-quality slide deck. Contains: cover, executive summary, one slide per major finding (chart + key insight panel), action cards, caveats, back cover. Built from `scripts/build_deck.py`. Best for: board meetings, presentations, anything you'll project.

### Word report (`.docx`)
Formal document with running headers/footers, KPI strips, premium table styles, callout boxes, and appendix. Built from `scripts/build_report.py`. Best for: formal reports, documents that will be annotated or redlined, regulatory submissions.

### Findings JSON (`_findings.json`)
Machine-readable results file used by downstream agents. Contains all statistics, confidence intervals, benchmarks, and flags. Best for: reusing findings in further analysis, building further prompts on top of.

---

## Governance and review checklist

Before sharing any output externally (to the board, regulators, or external parties):

- [ ] **Numbers verified** — spot-check at least 3 key figures against the source data
- [ ] **Sample sizes** — confirm n > 30 for any segment cited in findings
- [ ] **Benchmarks current** — APRA benchmark data cited with its vintage (year + publication)
- [ ] **Regulatory flags** — any `/regulatory-check` flags reviewed by compliance team
- [ ] **Classification correct** — confirm "CONFIDENTIAL" marking appropriate for the audience
- [ ] **No PII** — confirm no member identifiers, names, or sensitive details in outputs
- [ ] **Assumptions stated** — all projection assumptions (return rate, inflation, retirement age) are visible in the document
- [ ] **Australian English** — final spell-check for analyse/analyze, behaviour/behavior, etc.

---

## Understanding the agents

You don't need to know which agent does what to use the system — the orchestrator handles routing. But for debugging or extending the system:

| Agent | Triggered by | Does |
|---|---|---|
| `analyst-orchestrator` | Any multi-step analytical question | Plans, coordinates, synthesises |
| `data-fetcher` | New dataset or Databricks table | Loads, profiles, cleans, saves parquet |
| `analyst` | Clean dataset + analytical question | Statistics, regression, segmentation |
| `super-specialist` | Projections, adequacy, fee/insurance models | Quantitative super calculations |
| `visualiser` | Findings JSON + chart request | Creates publication-quality charts |
| `narrative-writer` | Findings + charts | Board papers, trustee reports, memos |
| `research-agent` | Regulatory or industry questions | Web research, cited briefs |
| `investment-analyst` | Investment performance questions | Attribution, APRA test, SAA drift |
| `output-formatter` | Any completed analysis | PPTX + Word + Markdown packaging |

---

## Common question types and what to expect

| Question type | Time | Output |
|---|---|---|
| Quick data profile | < 2 min | Markdown health check report |
| Segmentation analysis (e.g. participation by age) | 10-15 min | Report + 3-5 charts + deck |
| Retirement adequacy assessment | 15-20 min | Board paper + adequacy heatmap |
| Regulatory research brief | 5-8 min | Cited research document |
| Benchmarking vs APRA | 5-8 min | Benchmarking table + gap analysis |
| Full multi-dataset investigation | 30-45 min | Report + charts + deck + Word doc |

Times assume local data files. Databricks queries add 2-5 minutes for data extraction.

---

## Data handling rules

1. **Never commit data files** — `data/` is in `.gitignore`. Raw member data stays on local disk only.
2. **No PII in prompts** — never paste member IDs, names, emails, or TFNs into a prompt. Use aggregate data only.
3. **Parquet for processed data** — cleaned datasets go to `data/processed/` as parquet. Faster and more compact than CSV.
4. **Databricks credentials** — keep `.env` file local, never commit. Rotate tokens every 90 days.
5. **Output files** — `outputs/` can be committed (no PII in charts/reports). Datestamp everything.

---

## Extending the system

### Adding a new agent
Create `.claude/agents/your-agent.md` with a frontmatter block:
```markdown
---
name: your-agent
description: When to use this agent (this text is how the orchestrator decides to call it)
tools: Read, Write, Bash, Glob
skills:
  - skill-name
---
# Role...
```

### Adding a new skill
Create `.claude/skills/your-skill/SKILL.md`. Skills are reference documents loaded into agent context on demand. Good for: domain knowledge, coding patterns, style guides.

### Adding a slash command
Create `.claude/commands/your-command.md`:
```markdown
---
description: One-line description
argument-hint: <arg1> [optional-arg2]
---
What to do with $1 and $2...
```

### Modifying the output templates
- Slide deck design: `scripts/build_deck.py` — edit the colour system (class `C`) or slide constructors
- Word report design: `scripts/build_report.py` — edit callout styles, heading styles, or table formatting
- Both are parametric — you pass a config object, they produce the file. No design changes needed per analysis.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: pandas` | `source .venv/bin/activate` — Python env not active |
| `Databricks connection refused` | Check warehouse is running in Databricks UI; verify `.env` values |
| `PermissionError` on table | Request Unity Catalog SELECT permission from your DBA |
| Agent produces wrong chart type | Add chart type guidance to the prompt: "use a horizontal bar chart sorted by value" |
| Deck font looks wrong | Calibri must be installed. On Mac: download Microsoft fonts or use `brew install --cask font-calibri` |
| Output file not found | Check `outputs/` — filenames are datestamped. Run `ls outputs/*.pptx` |
| Analysis takes > 30 min | Likely a large Databricks query. Add explicit `LIMIT` in your data request first |
| Regulatory flag too generic | Run `/regulatory-check` with more specific context: include the exact metric and member count |

---

## Tips for better prompts

**Be specific about the output format:**
> "Produce a board paper format report with KPI strip at the top, three key findings, and a recommendations table."

**State the audience:**
> "This is for the Investment Committee — they want attribution detail, not member-level analysis."

**Specify the comparison baseline:**
> "Compare our participation rate against the APRA industry fund median, not the whole-of-market figure."

**Name the time period explicitly:**
> "Use FY2025 Q3 data — the file has multiple quarters."

**Ask for sensitivity analysis on projections:**
> "Show three scenarios: base case (7.5% return), downside (5%), and upside (9%)."

**Chain analyses:**
> "Now take those findings and produce a 5-minute executive briefing, then a slide deck with the top 4 insights."

---

## Getting help

- **Questions about the system:** Ask Bharath (Analytics & Insights)
- **Bug reports / feature requests:** Raise in the team backlog
- **Data access issues (Databricks):** Data Engineering team
- **Regulatory interpretation:** Compliance team — the system flags, humans decide
