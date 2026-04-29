# AI Analyst Project

## About this project

This is an AI-powered analytics workspace. It uses an orchestrator agent that delegates to specialist subagents (data, analysis, visualisation, narrative) to answer business questions end-to-end — from raw data to executive-ready insight.

## About the user

- Bharath, Lead Analytics & Insights at a superannuation firm (Australia)
- Also runs Food Tie (ecommerce — lunchware, expanding into kitchen products)
- Based in Melbourne
- Audience for outputs: typically executives or non-technical stakeholders

## Tech preferences

- **Language:** Python 3.11+ with `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
- **SQL dialects:** Default to ANSI SQL; flag dialect-specific syntax (Snowflake, BigQuery, Postgres)
- **Notebooks:** Prefer plain `.py` scripts in `scripts/` over `.ipynb` for version control friendliness
- **Package management:** `uv` if available, otherwise `pip` with `requirements.txt`
- **Locale:** Australian English in narrative (analyse, organisation, customise), AUD for currency, DD/MM/YYYY for dates

## Folder conventions

- `data/` — input datasets (raw CSVs, parquet, etc.). Never commit data with PII.
- `outputs/` — generated reports, charts, exported tables. Datestamp filenames: `2026-04-29_<description>.<ext>`
- `scripts/` — reusable Python scripts and analysis notebooks
- `.claude/agents/` — subagent definitions
- `.claude/skills/` — reusable skill packages
- `.claude/commands/` — slash commands for common workflows

## Workflow defaults

- Always start a new analysis by profiling the data (use the `data-profiling` skill)
- For any question requiring multi-step work, delegate to the `analyst-orchestrator` agent
- When writing narrative, lead with the answer, then the evidence (BLUF — bottom line up front)
- Charts should be self-explanatory: clear title, labelled axes, source note
- Cite specific numbers from the data, not vague descriptors ("revenue grew 12.4%" not "revenue grew strongly")

## Output style

- Executive summaries: max 5 bullet points, each ≤ 20 words
- Detailed analysis: prose with embedded charts, max 2 pages equivalent
- Always include: data source, time range covered, caveats/limitations

## Privacy & data handling

- Treat any column that could identify a person as sensitive (member IDs, emails, names)
- Never echo PII into prompts or commit to git
- For superannuation work specifically: aggregate to cohort level before analysis where possible
