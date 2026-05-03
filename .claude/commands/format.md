---
description: Convert analysis findings into a consultant-quality PPTX deck, Word report, and Markdown brief — all three output formats in one step
argument-hint: <findings JSON path or analysis topic>
---

Use the `output-formatter` agent to package this analysis into polished deliverables.

**Input:** $ARGUMENTS

The output-formatter will:
1. Read the findings JSON and any associated charts (same date prefix in `outputs/`)
2. Read the markdown report if one exists
3. Build a `DeckConfig` and `ReportConfig` from the findings
4. Run `scripts/build_deck.py` to produce a consultant-quality PPTX
5. Run `scripts/build_report.py` to produce a Word report with premium formatting
6. Save a concise Markdown brief alongside

**Design standards applied automatically:**
- Every slide title is an action sentence stating the finding (not the topic)
- Cover includes a bottom-line sentence — the single thing an exec reads first
- Hero-number slide for the most important statistic
- Action cards with specific metrics for recommendations
- Running headers/footers with classification marking on Word doc
- Australian English, AUD formatting, DD/MM/YYYY dates throughout

**Output files:**
- `outputs/YYYY-MM-DD_<topic>_deck.pptx`
- `outputs/YYYY-MM-DD_<topic>_report.docx`
- `outputs/YYYY-MM-DD_<topic>_brief.md`

When done, report the three output paths and confirm the slide count.
