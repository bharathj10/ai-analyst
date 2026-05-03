# AI Analyst

A Claude Code workspace that orchestrates specialist subagents to answer analytical questions end-to-end — from raw data to executive-ready insight.

This project is tailored for Australian superannuation and financial-services analytics. It is designed to turn raw member, fund, or benchmark data into executive-ready analysis, charts, reports, and presentations.

## What's in here

```
ai-analyst/
├── .claude/
│   ├── agents/             # Subagent definitions
│   │   ├── analyst-orchestrator.md   # The brain — plans and delegates
│   │   ├── data-fetcher.md           # Loads and profiles data
│   │   ├── analyst.md                # Runs statistical analysis
│   │   ├── visualiser.md             # Builds charts
│   │   └── narrative-writer.md       # Writes the report
│   ├── skills/             # Reusable capability packs
│   │   ├── data-profiling/
│   │   ├── sql-query-builder/
│   │   ├── chart-builder/
│   │   └── insight-narrative/
│   └── commands/           # Slash commands
│       ├── analyse.md      # /analyse <path> <question>
│       └── profile.md      # /profile <path>
├── data/                   # Input datasets (gitignored; do not commit PII)
├── outputs/                # Generated reports and charts (gitignored)
├── projects/               # Optional multi-project workspace
├── scripts/                # Generated analysis scripts
├── AGENTS.md               # Codex project instructions
├── CLAUDE.md               # Project context loaded every session
└── requirements.txt
```

## Getting started

1. **Install Claude Code** (one-time):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Clone and enter the project**:
   ```bash
   git clone https://github.com/bharathj10/ai-analyst.git
   cd ai-analyst
   ```

3. **Set up Python environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Optional: configure Databricks credentials**:
   ```bash
   cp .env.example .env
   # Fill in DATABRICKS_HOST, DATABRICKS_HTTP_PATH, and DATABRICKS_TOKEN
   ```

5. **Launch Claude Code**:
   ```bash
   claude
   ```

6. **Try it**:
   - Drop a CSV or parquet file in `data/`
   - Run `/profile data/your_file.csv` to get a quick health-check
   - Run `/analyse data/your_file.csv "what's driving X"` for full orchestration

## Where to put data

Use one of these two patterns.

**Single project or quick analysis**

Put data in the root `data/` folder:

```text
data/member_snapshot.csv
```

Prompt with the exact data path:

```text
/profile data/member_snapshot.csv
/analyse data/member_snapshot.csv "Analyse salary sacrifice participation by age band. Save outputs under outputs/ with the prefix 2026-05-03_salary_sacrifice."
```

**Multiple separate projects in this repo**

Put each project's data in that project's folder:

```text
projects/gender-gap/data/member_snapshot.csv
projects/member-exits/data/exits_snapshot.csv
projects/salary-sacrifice/data/contributions_snapshot.csv
```

Prompt with the active project folder and the exact data path:

```text
Use projects/gender-gap as the active project folder.
Profile projects/gender-gap/data/member_snapshot.csv.
Analyse the gender gap in balances and contributions for the trustee audience.
Save cleaned data, charts, and reports under projects/gender-gap/outputs.
```

Do not rely on the agent guessing where the data is. Always name the file path and output folder in the prompt.

## Running multiple analyses

If you need three different analyses, run them as separate, clearly named questions. This keeps the plan, scripts, charts, and reports easier to review and rerun.

Example:

```text
/analyse data/member_snapshot.csv "Analyse salary sacrifice participation by age band"
/analyse data/member_snapshot.csv "Analyse the gender gap in balances and contributions"
/analyse data/member_snapshot.csv "Analyse drivers of member exits by tenure and age"
```

For each analysis:

- Start with `/profile` when using a new dataset
- State the dataset, question, time period, and target audience
- Ask for a distinct output name, such as `2026-05-03_salary_sacrifice`
- Keep outputs in `outputs/` and charts in `outputs/charts/`
- Compare results only after all three analyses have their own sourced findings

If the three analyses need to be compared in one executive pack, run the three analyses first, then ask:

```text
Combine the three completed analyses into one board-ready summary, with shared caveats and a prioritised action plan.
```

## Running multiple projects in one repo

If you need three different projects using the same repository, keep the shared AI analyst setup in the repo root and create separate project folders under `projects/`. This works well when the projects share agents, skills, dependencies, and governance standards, but need separate datasets, scripts, outputs, and assumptions.

Use this pattern for related projects. For example:

- Salary sacrifice analysis
- Gender gap analysis
- Member exits analysis

Each project gets its own data and output folders. The root `data/` and `outputs/` folders can still be used for a single default project, but once you are running multiple projects, prefer `projects/<project-name>/...` paths to avoid mixing files.

Recommended structure:

```text
projects/
├── salary-sacrifice/
│   ├── data/
│   ├── outputs/
│   ├── scripts/
│   └── README.md
├── gender-gap/
│   ├── data/
│   ├── outputs/
│   ├── scripts/
│   └── README.md
└── member-exits/
    ├── data/
    ├── outputs/
    ├── scripts/
    └── README.md
```

For each project:

- Create a short `projects/<project-name>/README.md` with the business question, owner, data source, time range, assumptions, and expected outputs
- Put project-specific raw data in `projects/<project-name>/data/`
- Save project-specific artefacts in `projects/<project-name>/outputs/`
- Save reusable project scripts in `projects/<project-name>/scripts/`
- Include the project name in output filenames, for example `2026-05-03_gender_gap_board_summary.html`
- Do not mix outputs across projects unless you are deliberately creating a cross-project synthesis
- In prompts, always say `Use projects/<project-name> as the active project folder`

Example prompt:

```text
Use projects/gender-gap as the working project folder. Profile the dataset, analyse the gender gap in balances and contributions, and save all outputs under projects/gender-gap/outputs.
```

Use separate repositories instead when projects have different access controls, different data sensitivity, different package stacks, or different audiences. For example, a trustee board analytics project and a public marketing analytics project should not share one repo by default.

## Data and outputs

The repository intentionally does not include raw datasets, processed datasets, generated reports, or charts. Those folders are gitignored because superannuation member data can contain sensitive information.

- For one project, put input data in `data/`
- For multiple projects, put input data in `projects/<project-name>/data/`
- For one project, write cleaned datasets to `data/processed/`
- For multiple projects, write cleaned datasets under `projects/<project-name>/outputs/` or `projects/<project-name>/data/processed/`
- For one project, write reports, charts, decks, and other generated artefacts to `outputs/`
- For multiple projects, write reports, charts, decks, and other generated artefacts to `projects/<project-name>/outputs/`
- Keep any individual-level PII out of committed files

## How orchestration works

When you ask a multi-step question, the `analyst-orchestrator` agent:

1. Plans the work in `outputs/_plan.md`
2. Delegates fetching to `data-fetcher`
3. Delegates analysis to `analyst`
4. Delegates charts to `visualiser`
5. Delegates write-up to `narrative-writer`
6. Returns a finished report in `outputs/`

Each subagent runs in its own context window — your main conversation stays clean.

## Reusing this template

The `.claude/` folder is portable. To bootstrap a new project:

```bash
# Copy just the skills (most reusable)
cp -r ai-analyst/.claude/skills new-project/.claude/

# Or copy the entire scaffold
cp -r ai-analyst/.claude new-project/
# Then customise CLAUDE.md and agent definitions
```

## Adding new skills or agents

- **New skill**: create `.claude/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`)
- **New agent**: create `.claude/agents/<name>.md` with frontmatter (`name`, `description`, `tools`, optionally `skills`)
- **New command**: create `.claude/commands/<name>.md` with frontmatter (`description`, `argument-hint`)

The `description` field is what Claude uses to decide when to invoke — write it like a trigger condition.

## License

MIT
