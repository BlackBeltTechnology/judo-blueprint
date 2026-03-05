---
name: "collect-blueprints"
description: "Clone projects on-demand, analyze source directly, and collect reusable patterns into blueprint catalogs"
argument-hint: "[model|backend|frontend|all]"
user-invocable: true
allowed-tools:
  - Task(judo-model-analyzer, judo-backend-analyzer, judo-frontend-analyzer)
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
---

Orchestrate the collection and scoring of reusable patterns from JUDO project source code into the `blueprint/` catalog. Projects are **cloned fresh from Git on-demand** to `/tmp/judo-projects/`, analyzed by 3 domain-specific agents, then cleaned up. No local `projects/` or `research/` directories needed.

## Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: Parse registry and check versions**
   - `subject`: "Parse registry and check versions"
   - `description`: "Read PROJECTS.md for project list with git URLs, run version check against blueprint/PROGRESS.md"
   - `activeForm`: "Checking project versions"

2. **Task: Process projects**
   - `subject`: "Process selected projects"
   - `description`: "For each selected project: clone to /tmp, dispatch analyzer agents, update PROGRESS.md, cleanup"
   - `activeForm`: "Processing projects"

3. **Task: Score all blueprints**
   - `subject`: "Score all blueprints"
   - `description`: "Run the scoring script to calculate weighted scores for all collected blueprints"
   - `activeForm`: "Scoring blueprints"

4. **Task: Generate summary report**
   - `subject`: "Generate summary report"
   - `description`: "Display final summary of collected blueprints: total counts by domain, top patterns, and alternatives"
   - `activeForm`: "Generating summary report"

---

## Usage

**Syntax:**
```
/collect-blueprints [domain]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `model` | Collect only model-layer blueprints |
| `backend` | Collect only backend-layer blueprints |
| `frontend` | Collect only frontend-layer blueprints |
| `all` (default) | Collect all three domains |

**Examples:**
```
/collect-blueprints              # Collect all domains
/collect-blueprints model        # Only model patterns
/collect-blueprints backend      # Only backend patterns
/collect-blueprints frontend     # Only frontend patterns
```

---

## Orchestrator Instructions

When this command is invoked, follow these steps:

### Step 1: Parse Arguments and Read Registry

Create the output directories if they don't exist:

```bash
mkdir -p blueprint/model blueprint/backend blueprint/frontend
```

Parse the argument to determine which domains to process:
- No argument or `all` → process all three domains
- `model` → only model domain
- `backend` → only backend domain
- `frontend` → only frontend domain

#### Read Project Registry

Read `PROJECTS.md` to get the full project list with git URLs. Parse the markdown table to extract:
- Project name (strip `**` bold markers)
- Git URL
- Project index (row number)

This is the **only source of truth** for which projects to process. No hardcoded lists.

#### Load Progress Tracker

Read `blueprint/PROGRESS.md` if it exists. This file tracks which projects have been processed, their last-analyzed SHA, and allows version comparison.

**Format of `blueprint/PROGRESS.md`:**

```markdown
# Blueprint Collection Progress

> Last run: 2026-03-04 | Status: complete

| # | Project | Model | Backend | Frontend | Last SHA | Status |
|---|---------|-------|---------|----------|----------|--------|
| 1 | mlszksz-platform | done | done | skipped | abc1234 | done |
| 2 | trivia | done | done | done | def5678 | done |
```

Each domain column can be: `done`, `skipped` (no relevant source), or `pending`.
The `Last SHA` column stores the 7-char short SHA of HEAD at the time of last analysis.
The `Status` column is `done` when all requested domain columns are done/skipped, otherwise `pending`.

### Step 2: Version Check + User Selection

Run the version check script to compare remote HEAD SHAs against last-analyzed SHAs:

```bash
bash $CLAUDE_PROJECT_DIR/.claude/scripts/check-project-versions.sh
```

Display the comparison table to the user. Projects will show as:
- **unchanged** — remote SHA matches last-analyzed SHA
- **CHANGED** — remote SHA differs from last-analyzed SHA
- **NEW** — not in PROGRESS.md at all

Ask the user: **"Process all changed + new projects? Or select specific projects?"**

Default behavior: process all CHANGED + all NEW projects.

If the user wants specific projects, let them pick from the list.

### Step 3: Process Selected Projects One at a Time

For each selected project, in order:

#### 3a. Clone

```bash
git clone --depth 1 <git-url> /tmp/judo-projects/<name>/
```

If clone fails (private repo, network issue), log the error, mark as `skipped` in PROGRESS.md, and continue to next project.

#### 3b. Find Model File

```bash
ls /tmp/judo-projects/<name>/model/*.model 2>/dev/null
```

Get the model file path. If no `.model` file exists, the project may only have backend/frontend — agents will handle gracefully.

#### 3c. Dispatch Analyzer Agents in Parallel

Launch up to 3 agents simultaneously (one per selected domain) using the Task tool with `run_in_background: true`:

**Model agent** (if domain includes model):
- `subagent_type`: `judo-model-analyzer`
- `description`: "Model analysis: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>** (index N of TOTAL). Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path>`. Read existing blueprints from blueprint/model/ first, then analyze the model source directly. Cross-reference patterns with .generator-ignore files. Update or create blueprints in blueprint/model/. Keep examples concise (3-5 lines). Report what you found."

**Backend agent** (if domain includes backend):
- `subagent_type`: `judo-backend-analyzer`
- `description`: "Backend analysis: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>** (index N of TOTAL). Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path>`. Read existing blueprints from blueprint/backend/ first, then scan custom/ folders for Java implementations, .generator-ignore files, and interceptors. Cross-reference with model via CLI. Update or create blueprints in blueprint/backend/. Keep examples concise (3-5 lines). Report what you found."

**Frontend agent** (if domain includes frontend):
- `subagent_type`: `judo-frontend-analyzer`
- `description`: "Frontend analysis: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>** (index N of TOTAL). Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path>`. Read existing blueprints from blueprint/frontend/ first, then scan custom/ folders, .generator-ignore files, theme/, layout/, public/ directories. Cross-reference with UI model via CLI. Update or create blueprints in blueprint/frontend/. Keep examples concise (3-5 lines). Report what you found."

#### 3d. Wait and Update Progress

1. Wait for ALL agents for this project to complete (use TaskOutput with `block: true`)
2. Get the current remote HEAD SHA:
   ```bash
   git -C /tmp/judo-projects/<name>/ rev-parse --short=7 HEAD
   ```
3. **Update `blueprint/PROGRESS.md`**: Mark each domain column as `done` for this project. Mark domains that had no relevant source as `skipped`. Store the HEAD SHA in `Last SHA` column. Set Status to `done`.
4. Log progress: "Project N/M (<PROJECT>) complete. Patterns: model=X, backend=Y, frontend=Z"

#### 3e. Cleanup

```bash
rm -rf /tmp/judo-projects/<name>/
```

#### 3f. Advance to Next Project

**IMPORTANT**: Do NOT launch agents for the next project until the current project's agents have all completed. This keeps context manageable.

### Step 4: Generate Domain Indexes

After all projects are processed, generate INDEX.md files for each domain.

For each active domain, read all blueprint files and create an index:

```bash
# Count blueprints per domain
ls blueprint/model/*.md 2>/dev/null | grep -v INDEX | wc -l
ls blueprint/backend/*.md 2>/dev/null | grep -v INDEX | wc -l
ls blueprint/frontend/*.md 2>/dev/null | grep -v INDEX | wc -l
```

Generate each INDEX.md by reading all blueprint files in that domain and creating a sorted table.

### Step 5: Score all blueprints

Run the scoring script to calculate weighted scores:

```bash
python3 $CLAUDE_PROJECT_DIR/.claude/scripts/score-blueprints.py --update
```

Then display the top patterns:

```bash
python3 $CLAUDE_PROJECT_DIR/.claude/scripts/score-blueprints.py --top 30
```

### Step 6: Generate summary report

Run the summary view:

```bash
python3 $CLAUDE_PROJECT_DIR/.claude/scripts/score-blueprints.py --summary
```

Present the results to the user including:
- Total patterns collected per domain
- Top 10 highest-scored patterns overall
- Any alternative solution groups found
- Suggestion to run `/collect-blueprints` again after adding new projects to PROJECTS.md

---

## Key Design Decisions

### Why Clone on Demand?

Instead of keeping 26 repos permanently in `projects/`:
- **Saves disk space** — repos are cloned `--depth 1` and deleted after analysis
- **Always fresh** — no stale local copies; version checking catches remote changes
- **Extensible** — add a row to `PROJECTS.md` and it just works
- **No manual syncing** — no need to `git pull` 26 repos

### Why No Intermediate Research Step?

The old workflow was: researchers write to `research/` → collectors read `research/`.
The new flow is: analyzers read source directly → write to `blueprint/`.
- **Fewer agents** — 3 instead of 6
- **No stale research** — always analyzing current source
- **Less disk usage** — no 313 research files to maintain

### Why One Project at a Time?

Each analyzer agent needs to:
1. Read ALL existing blueprints (growing as we process more projects)
2. Analyze the project source with CLI queries
3. Write updated blueprints

Processing all projects in one agent causes **context overflow**. Sequential processing keeps each agent invocation manageable.

### What Patterns to Find (CRITICAL)

The agents search for **BEST PRACTICES** in JUDO development:

1. **Custom folders** (`**/custom/`) — hand-written code reveals what developers actually customize
2. **Generator-ignore files** (`**/.generator-ignore`) — shows what files are commonly overridden
3. **Model structure** — entity design, cardinality, naming conventions via CLI
4. **Theme/Layout overrides** — standard frontend customization layers
5. **Interceptor chains** — backend cross-cutting concern patterns

### Pattern Categories by Domain

- **Model**: Collection lower bounds always 0, naming conventions, common cardinalities, generalization patterns, UI model organization
- **Backend**: Toggle operations, custom implementation patterns, interceptor chains, DI wiring, external integrations
- **Frontend**: Theme overrides (palette.ts, density.ts), layout customizations (Header, Drawer, Logo), custom/ folder patterns (application-customizer.tsx, landing pages), public asset overrides

### Extensibility

- **Add a project**: Append one row to `PROJECTS.md` → `/collect-blueprints` detects as "NEW" (no SHA in PROGRESS.md)
- **Re-analyze a project**: Delete its row from `PROGRESS.md` or change its SHA → shows as "CHANGED"
- **Start fresh**: Delete `blueprint/PROGRESS.md` → all projects treated as NEW
- **No hardcoded lists** in any agent or command

### Scoring Formula

```
score = (usage_count * 10) + (recency_bonus) - (alternative_penalty)

recency_bonus = sum(project_weight for each project)
  where project_weight = project_index / total_projects * 10

alternative_penalty = alternative_count * 2
```

---

## Notes

- **Progress is tracked in `blueprint/PROGRESS.md`** — interrupted runs can resume
- Each project's 3 agents run in parallel; projects are processed sequentially
- Running this command again is idempotent: existing blueprints get updated counts/timestamps, not duplicated
- The scoring script at `.claude/scripts/score-blueprints.py` can also be run standalone
- The version check script at `.claude/scripts/check-project-versions.sh` can also be run standalone
- Agents use `maxTurns: 50` to prevent runaway context usage per project
- Cloned repos go to `/tmp/judo-projects/` and are cleaned up after each project
