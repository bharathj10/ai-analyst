# AI Analyst

A Claude Code workspace that orchestrates specialist subagents to answer analytical questions end-to-end — from raw data to executive-ready insight.

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
├── data/                   # Input datasets (gitignored)
├── outputs/                # Reports, charts (gitignored except samples)
├── scripts/                # Generated analysis scripts
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
   git clone <your-repo-url>
   cd ai-analyst
   ```

3. **Set up Python environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Launch Claude Code**:
   ```bash
   claude
   ```

5. **Try it**:
   - Drop a CSV or parquet file in `data/`
   - Run `/profile data/your_file.csv` to get a quick health-check
   - Run `/analyse data/your_file.csv "what's driving X"` for full orchestration

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
