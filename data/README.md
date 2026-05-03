# Data folder

Drop input datasets here when you are running a single default project or a quick one-off analysis.

Contents are gitignored — do not commit data with PII.

Suggested structure:
- `raw/` — untouched source files
- `processed/` — cleaned datasets produced by the data-fetcher agent

For multiple separate projects in this repo, use project-specific folders instead:

```text
projects/<project-name>/data/
```

Example prompt:

```text
/profile data/member_snapshot.csv
/analyse data/member_snapshot.csv "Analyse salary sacrifice participation by age band. Save outputs under outputs/."
```
