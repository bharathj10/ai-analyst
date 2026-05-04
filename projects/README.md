# Projects

Use this folder when you have more than one separate analytical workstream in the same repo. Each project gets its own data, scripts, and outputs — kept isolated so findings don't mix.

If you only have one question or a quick one-off, use the root `data/` and `outputs/` folders instead.

---

## When to use projects/

Use `projects/<name>/` when:
- You have multiple unrelated analyses (e.g. gender gap study + member exit study + fee analysis)
- Different analyses have different assumptions, time ranges, or audiences
- You want to keep scripts and outputs cleanly separated and rerunnable

Use root `data/` and `outputs/` when:
- You have one dataset and one question
- You're doing a quick exploratory profile

---

## Folder structure for each project

```
projects/<project-name>/
├── data/           # Input datasets — gitignored, never committed
├── outputs/        # Reports, charts, decks, HTML artefacts — gitignored
│   └── charts/     # PNG charts
├── scripts/        # Analysis scripts generated during the project — gitignored
└── README.md       # Project brief (see template below) — gitignored
```

> Everything under `projects/*/` is gitignored. Project-specific work stays on your local machine — it never goes into the shared repo.

---

## Starting a new project

### 1 — Create the folder structure

```bash
mkdir -p projects/my-project/{data,outputs/charts,scripts}
```

### 2 — Add a README for the project

Create `projects/my-project/README.md` using this template:

```markdown
# Project name

**Business question:** What are we trying to answer?
**Audience:** Who will read the outputs (e.g. trustee board, investment committee)?
**Owner:** Who is responsible for this analysis?
**Data source:** What dataset(s) are being used?
**Time range:** What period does the data cover?
**Key assumptions:** Return rate, retirement age, benchmarks used, etc.
**Required outputs:** HTML report, PPTX deck, Word document?
**Privacy / regulatory constraints:** Any PII handling notes or regulatory flags?
```

### 3 — Drop your data in

```
projects/my-project/data/your_file.csv
```

### 4 — Prompt Claude

Always name the active project folder at the start:

```
Use projects/my-project as the active project folder.
Profile projects/my-project/data/your_file.csv.
Analyse [your question] for [your audience].
Save all outputs under projects/my-project/outputs/.
```

---

## Example prompts

**Profile the data first:**
```
Use projects/gender-gap as the active project folder.
Profile projects/gender-gap/data/member_snapshot.csv.
```

**Full analysis:**
```
Use projects/gender-gap as the active project folder.
Analyse the gender gap in projected retirement balances using projects/gender-gap/data/member_snapshot.csv.
Project to age 67. Show base case (7.5% net return), downside (5.5%), and upside (9.5%).
Audience is the trustee board.
Save all charts and reports under projects/gender-gap/outputs/.
```

**Multiple questions, same dataset:**
```
Use projects/salary-sacrifice as the active project folder.
Using projects/salary-sacrifice/data/members.csv, answer these three questions:
1. What is our salary sacrifice participation rate by age band and gender?
2. How does it compare to the APRA industry median?
3. What is the lifetime dollar impact of the gap for a median-aged member?
Save separate findings files for each question, then combine into one board report.
```

---

## Running multiple projects in parallel

Run each project separately and keep findings isolated until each has its own sourced outputs. Only combine across projects when you deliberately want a cross-project synthesis.

```
# Analyse salary sacrifice
Use projects/salary-sacrifice as the active project folder.
/analyse projects/salary-sacrifice/data/members.csv "salary sacrifice participation by age band"

# Separately, analyse gender gap
Use projects/gender-gap as the active project folder.
/analyse projects/gender-gap/data/members.csv "gender gap in projected retirement balances"

# After both are done, combine
Combine the findings from projects/salary-sacrifice/outputs and projects/gender-gap/outputs
into one executive summary for the June trustee board meeting.
```
