# Projects

Use this folder when several separate analytical projects share the same AI Analyst repo setup.

If you only have one project or a quick one-off analysis, use the root `data/` and `outputs/` folders instead. Use `projects/` when you need multiple separate workstreams in the same repo.

Recommended project structure:

```text
projects/<project-name>/
├── data/       # Raw and processed project data; gitignored
├── outputs/    # Reports, charts, decks, and HTML artefacts; gitignored
├── scripts/    # Reusable project-specific scripts
└── README.md   # Project brief, owner, data source, assumptions, outputs
```

Each project README should state:

- Business question
- Audience and owner
- Data source and time range
- Key assumptions
- Required outputs
- Any privacy, regulatory, or access constraints

Keep project findings separate until each analysis has sourced outputs. Create a cross-project synthesis only when explicitly needed.

Prompt pattern:

```text
Use projects/<project-name> as the active project folder.
Profile projects/<project-name>/data/<dataset>.csv.
Analyse <question> for <audience>.
Save cleaned data, charts, and reports under projects/<project-name>/outputs.
```
