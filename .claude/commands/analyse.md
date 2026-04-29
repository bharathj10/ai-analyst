---
description: Run a full analysis on a dataset — profile, analyse, visualise, write up
argument-hint: <dataset path> <question>
---

You're being asked to run a full analysis. The user has provided:

**Dataset:** `$1`
**Question:** $2

Use the `analyst-orchestrator` subagent. Pass it both the dataset path and the question. The orchestrator will plan the work and delegate to the data-fetcher, analyst, visualiser, and narrative-writer.

When the orchestrator returns, summarise what was produced and where the deliverables are saved.
