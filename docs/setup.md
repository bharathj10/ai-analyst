# How-To: Set Up an AI Analyst Project with Claude Code on Mac

**Author:** Bharath
**Created:** April 2026
**Last updated:** April 2026
**Purpose:** Step-by-step record of how to set up a Claude Code project (`ai-analyst`) so it can be repeated for future projects without re-figuring it out.

---

## What I'm building

A Claude Code workspace where:
- An **orchestrator agent** breaks down analytical questions into steps
- **Specialist subagents** handle each step (data fetching, analysis, charting, narrative)
- **Skills** provide reusable building blocks (data profiling, SQL, chart styles, narrative voice)
- Everything is version-controlled in **GitHub** so I can roll back changes and reuse across projects

---

## Prerequisites checklist

Before starting, I needed:

- [x] A Mac (any recent version)
- [x] A GitHub account (already had one)
- [x] An Anthropic Claude account (Pro or higher recommended for Claude Code)
- [x] About 30-45 minutes for first-time setup
- [x] Terminal access (Spotlight → "Terminal")

---

## Step 1: Install Homebrew (Mac package manager)

Homebrew is the standard way to install developer tools on Mac. Without it, you can't easily install Node.js, GitHub CLI, etc.

**Check if you have it:**
```bash
brew --version
```

If you get `zsh: command not found: brew`, install it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

What to expect during install:
- Asks for your Mac password (won't show characters as you type — that's normal)
- Asks you to press Return to continue
- May install Xcode Command Line Tools (one-time, takes a few minutes)
- Total time: 5–15 minutes

**Critical post-install step:** Homebrew prints two commands at the end. They look like:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

The exact path differs based on your Mac:
- **Apple Silicon (M1/M2/M3/M4):** `/opt/homebrew/`
- **Intel Macs:** `/usr/local/`

Run those two commands exactly as shown in your terminal output. Without this, `brew` won't work in future terminal sessions.

**Verify:**
```bash
brew --version
```

Should print `Homebrew 4.x.x`.

---

## Step 2: Install Node.js, GitHub CLI, and Claude Code

```bash
brew install node
brew install gh
npm install -g @anthropic-ai/claude-code
```

**Verify each one:**
```bash
node --version       # Should be v18 or higher
gh --version         # GitHub CLI version
claude --version     # Claude Code version
```

---

## Step 3: Authenticate Claude Code and GitHub

### Claude Code

```bash
claude
```

Opens a browser window — log in with your Anthropic account. Once it confirms, exit Claude Code with `/exit` or `Ctrl+D` (we come back to it later).

### GitHub CLI

```bash
gh auth login
```

Pick these options when prompted:
- **GitHub.com**
- **HTTPS**
- **Yes, authenticate Git**
- **Login with a web browser**

It shows a one-time code, opens your browser, you paste the code in. Done.

### Set Git identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

Use the same email as your GitHub account so commits link to your profile.

### Optional: pick a friendlier git editor

By default Git uses `vim` for commit messages, which is unintuitive. To use `nano` instead (or VS Code if installed):

```bash
git config --global core.editor "nano"
# or
git config --global core.editor "code --wait"
```

---

## Step 4: Get the project files into place

Create a Projects folder in your home directory and move the starter template there:

```bash
mkdir -p ~/Projects
mv ~/Downloads/ai-analyst ~/Projects/
cd ~/Projects/ai-analyst
```

The `cd` puts you inside the project. Every command from this point assumes you're in `~/Projects/ai-analyst`.

**Verify the structure:**
```bash
ls -la
```

Should show: `.claude`, `CLAUDE.md`, `README.md`, `data`, `outputs`, `scripts`, `requirements.txt`, `.gitignore`.

---

## Step 5: Set up the Python environment

A virtual environment isolates this project's Python packages from your system Python — important because different projects often need different versions.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

After `source`, your terminal prompt shows `(.venv)` at the start — that confirms the environment is active.

**Verify:**
```bash
python -c "import pandas; print(pandas.__version__)"
```

Should print something like `2.2.x`.

**Important:** Every time you come back to this project, run `source .venv/bin/activate` before starting work. Otherwise Python won't find the packages.

---

## Step 6: Initialise Git and push to GitHub

Inside the project folder:

```bash
git init
git add .
git commit -m "Initial scaffold: AI analyst with orchestrator and specialist agents"
```

If Git asks you to set your name/email and dumps you into vim, escape with `Esc` then `:q!` then `Enter`. Run the `git config` commands from Step 3, then redo the commit.

### If you got stuck in vim

Vim has two modes:
- **Normal mode** (default) — keys are commands, not text
- **Insert mode** — keys type text. Press `i` to enter, `Esc` to leave

To exit:
- **Save and exit:** `Esc`, then `:wq`, then `Enter`
- **Exit without saving:** `Esc`, then `:q!`, then `Enter`

### Create the GitHub repo and push

```bash
gh repo create ai-analyst --private --source=. --push
```

What this does:
- Creates a new private repo on your GitHub account named `ai-analyst`
- Connects your local folder to it
- Pushes all your code

Verify by visiting `https://github.com/<your-username>/ai-analyst`.

---

## Step 7: Test the project in Claude Code

```bash
claude
```

This launches Claude Code from inside the project folder. It auto-loads `CLAUDE.md`, your agents, skills, and slash commands.

### Quick sanity check

In the Claude Code prompt, type:
```
list the agents available in this project
```

Claude should mention: `analyst-orchestrator`, `data-fetcher`, `analyst`, `visualiser`, `narrative-writer`.

### Test with sample data

1. Drop a CSV file into `data/` (use `super_members_2026Q1.csv` from the synthetic dataset I generated)
2. Profile it:
   ```
   /profile data/super_members_2026Q1.csv
   ```
3. Run a full analysis:
   ```
   /analyse data/super_members_2026Q1.csv "what's driving differences in salary sacrifice behaviour across age bands?"
   ```

The orchestrator plans the work, delegates to each specialist, and writes a report into `outputs/`.

### Exit Claude Code

- Type `/exit` or press `Ctrl+D`
- Mid-response: `Ctrl+C` once cancels, twice exits

### Resume later

```bash
cd ~/Projects/ai-analyst
source .venv/bin/activate
claude
# or to continue last session:
claude --continue
```

---

## Common issues I hit

| Problem | Fix |
|---|---|
| `command not found: brew` | Install Homebrew (Step 1) |
| `command not found: claude` | `npm install -g @anthropic-ai/claude-code` |
| Stuck in vim | `Esc` → `:q!` → `Enter` |
| Git asking for name/email | Run `git config --global` commands |
| Python `ModuleNotFoundError` | Forgot to activate venv: `source .venv/bin/activate` |
| `gh: command not found` | `brew install gh` |

---

## Where to save this guide

I keep this in **two places** for redundancy:

1. **In the project repo itself** at `docs/setup-guide.md` — version-controlled with the project, updated alongside any setup changes
2. **In a personal knowledge folder** — separately, so it's findable across all my projects

For the personal knowledge folder, I suggest:

```
~/Documents/HowTo/
├── 01-mac-claude-code-setup.md          (this file)
├── 02-create-new-claude-project.md      (next guide)
├── 03-customise-agents-and-skills.md
├── 04-claude-code-daily-workflow.md
└── ...
```

Numbering keeps them in a sensible reading order.

---

## Reuse pattern for future projects

When I want to start a new Claude Code project (e.g., for Food Tie content tools):

```bash
cd ~/Projects
mkdir foodtie-content && cd foodtie-content

# Copy reusable Claude Code config
cp -r ../ai-analyst/.claude .
cp ../ai-analyst/.gitignore .
cp ../ai-analyst/requirements.txt .

# Edit CLAUDE.md to reflect the new project context
# Tweak or remove agents that don't apply
# Add new skills/agents specific to this project

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Git + GitHub
git init
git add .
git commit -m "Initial scaffold from ai-analyst template"
gh repo create foodtie-content --private --source=. --push
```

Skills like `chart-builder` and `insight-narrative` are reusable as-is. Agents are usually project-specific.
