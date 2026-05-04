# AI Analyst

A Claude Code workspace that turns a CSV — or a Databricks table — into a finished analytical deliverable: charts, an interactive HTML report, a slide deck, and a written board paper. It is purpose-built for Australian superannuation and financial-services analytics.

**What it replaces:** the 1–3 day cycle of extracting data, writing Python, building charts, formatting slides, and writing up findings. Most analyses complete in under 30 minutes.

**What it does not replace:** your judgement. Review every output before it goes to stakeholders.

---

## What you get from a single prompt

```
/analyse data/members.csv "what's driving low salary sacrifice participation among 25–34 year-olds?"
```

The system profiles the data, runs statistical analysis, builds charts, writes the narrative, and produces:

| File | What it is |
|---|---|
| `outputs/YYYY-MM-DD_topic_interactive.html` | Standalone interactive report — **email this one** |
| `outputs/YYYY-MM-DD_topic_deck.pptx` | Slide deck for board meetings |
| `outputs/YYYY-MM-DD_topic_report.docx` | Word document for formal reports |
| `outputs/YYYY-MM-DD_topic.md` | Written findings (internal record) |
| `outputs/charts/` | All charts as PNGs |

The `.html` file is self-contained — no server, no login, works offline in any browser.

---

## Setup (one-time, ~30 minutes)

### What you need before you start

- A Mac (any recent model)
- An [Anthropic account](https://claude.ai) — Pro plan or higher recommended
- Terminal access: press `Cmd + Space`, type `Terminal`, press Enter

---

### Step 1 — Install Homebrew (Mac package manager)

**Check if you already have it:**
```bash
brew --version
```

If you see `zsh: command not found: brew`, install it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

When the installer finishes, it prints two commands at the bottom of your screen. They look like:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```
**Run those two commands exactly as shown** — without this step, `brew` will stop working when you close the terminal.

Verify: `brew --version` should print `Homebrew 4.x.x`.

---

### Step 2 — Install Node.js, GitHub CLI, and Claude Code

```bash
brew install node
brew install gh
npm install -g @anthropic-ai/claude-code
```

Verify each one:
```bash
node --version     # should show v18 or higher
gh --version       # GitHub CLI version
claude --version   # Claude Code version
```

---

### Step 3 — Authenticate

**Claude Code:**
```bash
claude
```
A browser window opens — log in with your Anthropic account. Once confirmed, exit with `/exit` or `Ctrl+D`.

**GitHub CLI:**
```bash
gh auth login
```
Choose: GitHub.com → HTTPS → Yes, authenticate Git → Login with web browser. Follow the prompts.

**Set your git identity** (use the same email as your GitHub account):
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

### Step 4 — Clone the repo and set up Python

```bash
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/YOUR-USERNAME/ai-analyst.git
cd ai-analyst

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After `source .venv/bin/activate`, your terminal prompt shows `(.venv)` — that confirms Python is ready.

Verify:
```bash
python -c "import pandas; print(pandas.__version__)"
# Should print 2.2.x or similar
```

> **Every time you come back to this project:** run `source .venv/bin/activate` before starting work. If you get `ModuleNotFoundError`, this is why.

---

### Step 5 — Test it

```bash
claude
```

In the Claude Code prompt, type:
```
list the agents available in this project
```

Claude should describe the analyst-orchestrator, data-fetcher, analyst, visualiser, narrative-writer, and other agents. Setup is working.

---

## Your first analysis

Drop a CSV into `data/`, then:

```
/profile data/your_file.csv
```

This runs a data health check — shape, column types, missing values, duplicates. Takes under 2 minutes.

Then run the full analysis:
```
/analyse data/your_file.csv "what's driving X?"
```

Outputs land in `outputs/` with today's date prefix.

---

## Slash commands

| Command | What it does |
|---|---|
| `/analyse <file> <question>` | Full pipeline: profile → analyse → charts → report → deck |
| `/profile <file>` | Data health check — shape, nulls, duplicates, distributions |
| `/adequacy <file>` | Retirement adequacy assessment — projections, ASFA gaps, Age Pension dependency |
| `/research <topic>` | Cited research brief from APRA, ASIC, ATO, industry sources |
| `/benchmark <metric>` | Gap vs APRA industry medians, peer group, and dollar impact |
| `/regulatory-check <finding>` | Flags trustee, APRA, ASIC obligations triggered by a finding |
| `/format <findings-json>` | Packages completed findings into HTML, PPTX, Word, or Markdown |

---

## Examples you can copy

**Profile a new dataset:**
```
/profile data/member_snapshot.csv
```

**Full analysis — salary sacrifice:**
```
/analyse data/member_snapshot.csv "Analyse salary sacrifice participation by age band and gender. What share of members are below the APRA industry median? What is the dollar impact of the gap?"
```

**Retirement adequacy assessment:**
```
/adequacy data/member_snapshot.csv
```
Or with more specifics:
```
Use projects/retirement-adequacy as the active project folder.
Analyse the retirement adequacy of our member base using projects/retirement-adequacy/data/members.csv.
Project to age 67. Show base case (7.5% net return), downside (5.5%), and upside (9.5%) scenarios.
Audience is the trustee board.
Save all outputs under projects/retirement-adequacy/outputs/.
```

**Research a regulatory topic:**
```
/research "APRA SPS 515 member outcomes assessment — what are the annual obligations?"
```

**Benchmark a metric:**
```
/benchmark "our fund's salary sacrifice participation rate of 23% for 35–44 year-olds"
```

**Check for regulatory obligations:**
```
/regulatory-check "28% of members aged 55–64 are not on track for a comfortable retirement under the ASFA standard"
```

**Model a what-if scenario:**
```
Model the impact of increasing salary sacrifice by 2% of salary for all members
aged 30–44 who are not currently participating. Project the change in retirement
balance at age 67 and the reduction in Age Pension dependency.
Show base (7.5%), downside (5.5%), and upside (9.5%) return scenarios.
```

**Combine finished analyses into one board pack:**
```
Combine the three completed analyses into one board-ready executive summary with shared caveats and a prioritised action plan.
```

**Query Databricks directly** (once configured — see [Databricks setup](#databricks-connection-setup)):
```
Analyse member contribution patterns for FY2025 from the Unity Catalog table
main_catalog.super_analytics.member_contributions.
Focus on salary sacrifice by age band and compare to the APRA industry benchmark.
```

---

## Where to put your data

### One project or a quick analysis

Put data in the root `data/` folder:
```
data/member_snapshot.csv
```
Outputs go to `outputs/`.

### Multiple separate projects in the same repo

Create a project folder for each workstream:
```
projects/gender-gap/data/member_snapshot.csv
projects/member-exits/data/exits_snapshot.csv
projects/salary-sacrifice/data/contributions_snapshot.csv
```

In your prompt, always name the active project folder:
```
Use projects/gender-gap as the active project folder.
Profile projects/gender-gap/data/member_snapshot.csv.
Analyse the gender gap in balances and contributions for a trustee audience.
Save all outputs under projects/gender-gap/outputs/.
```

See `projects/README.md` for the recommended project folder structure.

> **Data never goes into git.** `data/`, `outputs/`, and all `projects/*/data/` and `projects/*/outputs/` paths are gitignored. Raw member data stays on local disk only.

---

## Resuming a session

```bash
cd ~/Projects/ai-analyst
source .venv/bin/activate
claude                  # new session
claude --continue       # resume the last session
```

Exit anytime with `/exit` or `Ctrl+D`. Cancel a running response with `Ctrl+C`.

---

## Databricks connection setup

The system connects to a Databricks SQL warehouse via the SQL connector. One-time setup:

```bash
pip install databricks-sql-connector python-dotenv
cp .env.example .env
```

Edit `.env` with your workspace details (never commit this file):
```
DATABRICKS_HOST=https://adb-xxxx.xx.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxxxxxxxxx
DATABRICKS_TOKEN=dapixxxxxxxxxxxxxxxx
```

**Where to find each value:**
- `DATABRICKS_HOST` — your workspace URL from the browser address bar
- `DATABRICKS_HTTP_PATH` — SQL Warehouses → your warehouse → Connection Details tab → HTTP Path
- `DATABRICKS_TOKEN` — Settings → Developer → Access Tokens → Generate New Token

Test the connection:
```bash
python scripts/databricks_connector.py --test
# Should print: Connection OK | Workspace: ...
```

Once connected, reference tables directly in prompts using three-part names (`catalog.schema.table`):
```
/profile main_catalog.super_analytics.member_snapshot_2025q4
```

---

## Output formats

| Format | Best for |
|---|---|
| **Interactive HTML** (`.html`) | Sharing with executives — self-contained, works offline, has interactive charts and filters |
| **PowerPoint** (`.pptx`) | Board meetings, anything you project |
| **Word** (`.docx`) | Formal reports, documents that get annotated or redlined |
| **Markdown** (`.md`) | Internal record, source document, GitHub |
| **Findings JSON** (`_findings.json`) | Machine-readable results for chaining further analyses |

---

## Tips for better prompts

**State the audience** — the system adjusts tone and depth:
> "This is for the Investment Committee — they want attribution detail, not member-level analysis."

**Name the time period:**
> "Use FY2025 Q3 data — the file covers multiple quarters."

**Specify the comparison baseline:**
> "Compare against the APRA industry fund median, not the whole-of-market figure."

**Ask for scenarios on projections:**
> "Show three scenarios: base case 7.5%, downside 5.5%, upside 9.5%."

**Chain further steps:**
> "Now take those findings and produce a 5-minute executive briefing, then a slide deck with the top 4 insights."

**Before sharing outputs externally**, check:
- [ ] Spot-check 3+ key figures against the source data
- [ ] Confirm n > 30 for any segment cited in findings
- [ ] APRA benchmark data cited with its vintage (year + publication name)
- [ ] Any regulatory flags reviewed by the compliance team
- [ ] No member identifiers, names, or sensitive details in outputs

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: brew` | Install Homebrew — Step 1 above |
| `command not found: claude` | `npm install -g @anthropic-ai/claude-code` |
| `ModuleNotFoundError: pandas` | Python env not active — run `source .venv/bin/activate` |
| `command not found: gh` | `brew install gh` |
| Stuck in vim during a git commit | Press `Esc`, type `:q!`, press Enter. Then run `git config --global core.editor nano` |
| Git asking for name / email | Run the `git config --global` commands in Step 3 |
| Databricks `connection refused` | Check the warehouse is running in the Databricks UI; verify `.env` values |
| `PermissionError` on a Databricks table | Request Unity Catalog SELECT permission from your DBA |
| Output file not found | Files are datestamped — run `ls outputs/` to list what was generated |
| Analysis takes longer than 30 min | Likely a large Databricks query. Ask for a sample first: "use LIMIT 100000" |
| Deck font looks wrong | Calibri must be installed. On Mac: `brew install --cask font-calibri` |
| Regulatory flag too generic | Run `/regulatory-check` with more specific context — include the exact metric and member count |

---

## Repo structure

```
ai-analyst/
├── .claude/
│   ├── agents/             # Subagent definitions (orchestrator, analyst, visualiser, etc.)
│   ├── skills/             # Reusable capability packs (domain knowledge, SQL, charting)
│   └── commands/           # Slash commands (/analyse, /profile, /adequacy, etc.)
├── data/                   # Your input datasets — gitignored, never committed
├── outputs/                # Generated reports and charts — gitignored
├── projects/               # Optional multi-project workspace — gitignored per project
├── scripts/                # Output-building scripts (build_html.py, build_deck.py, etc.)
├── docs/                   # Extended setup guide and team guide
├── CLAUDE.md               # Project context and instructions loaded every session
└── requirements.txt        # Python dependencies
```

---

## Extending the system

**New slash command** — create `.claude/commands/your-command.md`:
```markdown
---
description: One-line description
argument-hint: <arg1> [optional-arg2]
---
What to do with $1 and $2...
```

**New agent** — create `.claude/agents/your-agent.md`:
```markdown
---
name: your-agent
description: When to invoke this agent (the orchestrator reads this to decide when to call it)
tools: Read, Write, Bash, Glob
---
# Role and instructions...
```

**New skill** — create `.claude/skills/your-skill/SKILL.md`. Skills are reference documents loaded into an agent's context on demand — useful for domain knowledge, coding patterns, or style guides.

**Reuse this template for a new project:**
```bash
cd ~/Projects
mkdir new-project && cd new-project
cp -r ../ai-analyst/.claude .
cp ../ai-analyst/.gitignore .
cp ../ai-analyst/requirements.txt .
# Edit CLAUDE.md to reflect the new domain
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
git init && git add . && git commit -m "Initial scaffold from ai-analyst template"
gh repo create new-project --private --source=. --push
```

---

## Further reading

- `docs/setup.md` — detailed first-time setup walkthrough with screenshots and gotchas
- `docs/TEAM_GUIDE.md` — full team reference: all workflows, Databricks setup, governance checklist, agent descriptions
- `projects/README.md` — how to structure multi-project work in this repo

---

## License

MIT
