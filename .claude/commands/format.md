---
description: Convert analysis findings into polished output formats — Interactive HTML, PPTX deck, Word report, and/or Markdown brief
argument-hint: <findings JSON path or analysis topic>
---

You're being asked to package existing analysis findings into formatted deliverables.

**Input:** $ARGUMENTS

**Step 1 — Ask which formats are needed.**

Before doing any work, present this choice:

---
Which output formats do you need?

- **H** — Interactive HTML (standalone `.html` — best for emailing or sharing with execs)
- **P** — PowerPoint deck (`.pptx` — for board meetings and presentations)
- **W** — Word report (`.docx` — for formal or annotated documents)
- **M** — Markdown brief (`.md` — for internal records)

Reply with one or more letters (e.g. `HP` for HTML + PowerPoint, `HPW` for all formatted outputs).

---

Wait for the user's reply before proceeding.

**Step 2 — Delegate to `output-formatter`.**

Pass it:
- The findings path from `$ARGUMENTS`
- The confirmed format selection

The output-formatter will produce only the requested formats using the parametric build scripts.

**Design standards applied automatically:**
- Every slide/section title states the finding (not the topic)
- HTML includes interactive Plotly charts, KPI strip, and data quality summary
- Cover and HTML header include a bottom-line sentence — the one thing an exec reads first
- Action cards and recommendations carry specific metrics
- Australian English, AUD formatting, DD/MM/YYYY dates throughout

When done, report the paths of all files produced.
