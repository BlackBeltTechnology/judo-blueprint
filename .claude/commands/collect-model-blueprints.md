---
name: "collect-model-blueprints"
description: "Clone projects on-demand, analyze ESM models, and collect reusable structural fragments into model-blueprints/"
user-invocable: true
allowed-tools:
  - Task(judo-model-blueprint-analyzer)
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

Orchestrate the collection of reusable model structural fragments (blueprints) from JUDO project source code into the `model-blueprints/` catalog. Projects are **cloned fresh from Git on-demand** to `/tmp/judo-projects/`, analyzed by the model blueprint analyzer agent, then cleaned up.

## Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: Parse registry and check versions**
   - `subject`: "Parse registry and check versions"
   - `description`: "Read PROJECTS.md for project list with git URLs, run version check against model-blueprints/PROGRESS.md"
   - `activeForm`: "Checking project versions"

2. **Task: Process projects**
   - `subject`: "Process selected projects"
   - `description`: "For each selected project: clone to /tmp, dispatch blueprint analyzer agent, update PROGRESS.md, cleanup"
   - `activeForm`: "Processing projects"

3. **Task: Generate summary report**
   - `subject`: "Generate summary report"
   - `description`: "Display final summary of collected model blueprints: total counts, fragment types, and cross-project coverage"
   - `activeForm`: "Generating summary report"

---

## Usage

**Syntax:**
```
/collect-model-blueprints
```

**Examples:**
```
/collect-model-blueprints              # Analyze all projects for model blueprints
```

---

## Orchestrator Instructions

When this command is invoked, follow these steps:

### Step 1: Parse Arguments and Read Registry

Create the output directory if it doesn't exist:

```bash
mkdir -p model-blueprints
```

#### Read Project Registry

Read `PROJECTS.md` to get the full project list with git URLs. Parse the markdown table to extract:
- Project name (strip `**` bold markers)
- Git URL
- Project index (row number)

This is the **only source of truth** for which projects to process. No hardcoded lists.

#### Load Progress Tracker

Read `model-blueprints/PROGRESS.md` if it exists. This file tracks which projects have been processed, their last-analyzed SHA, and allows version comparison.

**Format of `model-blueprints/PROGRESS.md`:**

```markdown
# Model Blueprint Collection Progress

> Last run: 2026-03-05 | Status: complete

| # | Project | Model Blueprints | Last SHA | Status |
|---|---------|-----------------|----------|--------|
| 1 | mlszksz-platform | done | abc1234 | done |
| 2 | trivia | done | def5678 | done |
```

The `Model Blueprints` column can be: `done`, `skipped` (no model file), or `pending`.
The `Last SHA` column stores the 7-char short SHA of HEAD at the time of last analysis.
The `Status` column is `done` when the blueprint column is done/skipped, otherwise `pending`.

### Step 2: Version Check + User Selection

Run the version check script with the custom progress file path:

```bash
bash $CLAUDE_PROJECT_DIR/.claude/scripts/check-project-versions.sh $CLAUDE_PROJECT_DIR/PROJECTS.md $CLAUDE_PROJECT_DIR/model-blueprints/PROGRESS.md
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

#### 3a. Sparse Clone (model/ directory only)

Only fetch the `model/` directory — do NOT clone the entire repository:

```bash
git clone --depth 1 --filter=blob:none --sparse <git-url> /tmp/judo-projects/<name>/
git -C /tmp/judo-projects/<name>/ sparse-checkout set model/
```

If clone fails (private repo, network issue), log the error, mark as `skipped` in PROGRESS.md, and continue to next project.

#### 3b. Find Model File

```bash
ls /tmp/judo-projects/<name>/model/*.model 2>/dev/null | grep -v '\-esm\.model$'
```

Get the model file path. **CRITICAL**: Only use files matching `model/*.model` — **NEVER** use `*-esm.model` files (those are compiled/generated artifacts, not source models). If no valid `.model` file exists after excluding `-esm.model`, mark as `skipped` in PROGRESS.md and continue to next project.

#### 3c. Dispatch Blueprint Analyzer Agent

Launch one agent using the Task tool with `run_in_background: false` (wait for completion):

- `subagent_type`: `judo-model-blueprint-analyzer`
- `description`: "Blueprint analysis: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>** (index N of TOTAL). Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path>`. Read existing model blueprints from model-blueprints/ first, then survey the entire model using the CLI queries in order. Identify recurring structural fragments (entity clusters, common attribute sets, enum patterns, generalization hierarchies). Write/update blueprints in model-blueprints/. Include detection queries and creation mutations with template placeholders. Report what you found."

#### 3d. Update Progress

1. Get the current remote HEAD SHA:
   ```bash
   git -C /tmp/judo-projects/<name>/ rev-parse --short=7 HEAD
   ```
2. **Update `model-blueprints/PROGRESS.md`**: Mark the Model Blueprints column as `done` for this project. Store the HEAD SHA. Set Status to `done`.
3. Log progress: "Project N/M (<PROJECT>) complete."

#### 3e. Cleanup

```bash
rm -rf /tmp/judo-projects/<name>/
```

#### 3f. Advance to Next Project

**IMPORTANT**: Do NOT launch the agent for the next project until the current project's agent has completed. This keeps context manageable.

### Step 4: Generate Summary Report

After all projects are processed:

1. Count total blueprint files:
   ```bash
   ls model-blueprints/*.md 2>/dev/null | grep -v PROGRESS | grep -v INDEX | wc -l
   ```

2. Read all blueprint files and compile a summary:
   - Total blueprints collected
   - Blueprints by category (entity clusters, attribute sets, enum patterns, etc.)
   - Most common fragments (highest usage_count)
   - Cross-project coverage (which fragments appear in most projects)

3. Present the results to the user including:
   - Total fragments cataloged
   - Top fragments by usage count
   - Projects processed
   - Suggestion to run `/collect-model-blueprints` again after adding new projects to PROJECTS.md

---

## Key Design Decisions

### Why Separate from Best Practices?

- **Best practices** = "how to do things well" (conventions, guidelines, scoring)
- **Model blueprints** = "reusable structural fragments that recur across projects" (concrete entity/attribute shapes with creation mutations)
- Different output format (blueprints include detection queries + creation mutations)
- No scoring (blueprints are structural, not ranked by quality)

### Why Single Agent (not 3)?

Model blueprints are model-only by definition. There's no backend or frontend component — they're purely about ESM structural fragments.

### Why No Scoring Step?

Blueprints track `usage_count` (how many projects have this fragment) but don't need weighted scoring. A fragment appearing in 15/26 projects is inherently more reusable than one in 2/26 — the count alone is sufficient.

### Clone on Demand

Same pattern as `/collect-best-practices`:
- **Saves disk space** — repos use sparse checkout (`model/` only) and are deleted after analysis
- **Always fresh** — version checking catches remote changes
- **Extensible** — add a row to `PROJECTS.md` and it just works

### Extensibility

- **Add a project**: Append one row to `PROJECTS.md` → `/collect-model-blueprints` detects as "NEW"
- **Re-analyze a project**: Delete its row from `model-blueprints/PROGRESS.md` or change its SHA → shows as "CHANGED"
- **Start fresh**: Delete `model-blueprints/PROGRESS.md` → all projects treated as NEW
- **No hardcoded lists** in any agent or command

---

## Notes

- **Progress is tracked in `model-blueprints/PROGRESS.md`** — interrupted runs can resume
- Only one agent per project (model-only), projects are processed sequentially
- Running this command again is idempotent: existing blueprints get updated counts/timestamps, not duplicated
- The version check script accepts a custom PROGRESS.md path as second argument
- Agents use `maxTurns: 50` to prevent runaway context usage per project
- Cloned repos go to `/tmp/judo-projects/` and are cleaned up after each project
