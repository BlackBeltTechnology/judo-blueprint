---
name: "collect-model-blueprints"
description: "Clone projects on-demand, analyze ESM models, and collect reusable structural fragments (model + backend + frontend) into model-blueprints/"
user-invocable: true
allowed-tools:
  - Task(judo-model-blueprint-analyzer, judo-backend-blueprint-analyzer, judo-frontend-blueprint-analyzer)
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

Orchestrate the collection of reusable structural fragments (blueprints) from JUDO project source code into the `model-blueprints/` catalog. Blueprints come in two flavors:

1. **Model blueprints** — structural fragments discovered from the ESM model (entity clusters, enums, TOs), with optional backend/frontend implementation. Directory contains: `BLUEPRINT.md`, `model.md`, and optionally `backend.md`/`frontend.md`.
2. **Implementation-only blueprints** — patterns discovered from custom backend/frontend code that have no model counterpart (e.g., external service integrations, cross-cutting hook patterns, custom component systems). Directory contains: `BLUEPRINT.md` with `impl_only: true`, plus `backend.md` and/or `frontend.md` (no `model.md`).

Projects are **cloned fresh from Git on-demand** to `/tmp/judo-projects/`, analyzed by three specialized agents (model first, then backend + frontend in parallel — with backend/frontend also performing **discovery scans** for implementation-only patterns), then cleaned up.

## Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: Parse registry and check versions**
   - `subject`: "Parse registry and check versions"
   - `description`: "Read PROJECTS.md for project list with git URLs, run version check against model-blueprints/PROGRESS.md"
   - `activeForm`: "Checking project versions"

2. **Task: Process projects (model + backend + frontend)**
   - `subject`: "Process selected projects"
   - `description`: "For each selected project: clone to /tmp, dispatch model blueprint analyzer first, validate mutations, then dispatch backend + frontend analyzers in parallel, update PROGRESS.md, cleanup"
   - `activeForm`: "Processing projects"

3. **Task: Validate all blueprint mutations**
   - `subject`: "Validate all blueprint mutations"
   - `description`: "Run test-blueprint-mutations.sh to validate all mutation syntax"
   - `activeForm`: "Validating mutations"

4. **Task: Generate summary report**
   - `subject`: "Generate summary report"
   - `description`: "Display final summary: total blueprints, backend/frontend coverage, cross-project stats"
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

Read `model-blueprints/PROGRESS.md` if it exists. This file tracks which projects have been processed per domain, their last-analyzed SHA, and allows version comparison.

**Format of `model-blueprints/PROGRESS.md`:**

```markdown
# Model Blueprint Collection Progress

> Last run: 2026-03-05 | Status: complete

| # | Project | Model | Backend | Frontend | Last SHA | Status |
|---|---------|-------|---------|----------|----------|--------|
| 1 | mlszksz-platform | done | pending | pending | abc1234 | pending |
| 2 | trivia | done | done | done | def5678 | done |
```

The `Model`, `Backend`, `Frontend` columns can be: `done`, `skipped` (no relevant source), or `pending`.
The `Last SHA` column stores the 7-char short SHA of HEAD at the time of last analysis.
The `Status` column is `done` when ALL domain columns are done/skipped, otherwise `pending`.

#### Sync PROGRESS.md with PROJECTS.md

Compare PROJECTS.md against PROGRESS.md. If any project in PROJECTS.md is missing from PROGRESS.md, add it as a new row with all domains set to `pending`, Last SHA to `-`, and Status to `pending`. This ensures new projects added to PROJECTS.md are automatically picked up.

### Step 2: Version Check + User Selection

Run the version check script with the custom progress file path:

```bash
bash $CLAUDE_PROJECT_DIR/.claude/scripts/check-project-versions.sh $CLAUDE_PROJECT_DIR/PROJECTS.md $CLAUDE_PROJECT_DIR/model-blueprints/PROGRESS.md
```

Display the comparison table to the user. Projects will show as:
- **unchanged** — remote SHA matches last-analyzed SHA
- **CHANGED** — remote SHA differs from last-analyzed SHA
- **NEW** — not in PROGRESS.md at all

Also check for projects where `Model: done` but `Backend: pending` or `Frontend: pending` — these can resume from the backend/frontend stage without re-running the model agent.

Ask the user: **"Process all changed + new projects? Or select specific projects? (Projects with pending backend/frontend will also be included for those stages.)"**

Default behavior: process all CHANGED + all NEW + all with pending backend/frontend.

### Step 3: Process Selected Projects One at a Time

For each selected project, in order:

#### 3a. Clone (full shallow clone)

Clone the **entire** repository (not sparse — backend/frontend code is needed):

```bash
git clone --depth 1 <git-url> /tmp/judo-projects/<name>/
```

If clone fails (private repo, network issue), log the error, mark as `skipped` in PROGRESS.md, and continue to next project.

#### 3b. Find Model File

```bash
ls /tmp/judo-projects/<name>/model/*.model 2>/dev/null | grep -v '\-esm\.model$'
```

Get the model file path. **CRITICAL**: Only use files matching `model/*.model` — **NEVER** use `*-esm.model` files (those are compiled/generated artifacts, not source models). If no valid `.model` file exists after excluding `-esm.model`, mark `Model` as `skipped` in PROGRESS.md — but **do NOT skip the project entirely**. The project may still have custom backend/frontend implementations worth discovering. Proceed to Stage 2 (3e) with no model file and no blueprint IDs from model analysis.

#### 3c. Stage 1: Model Blueprint Analysis (sequential)

**Check PROGRESS.md**: If this project's `Model` column is already `done`, skip to Stage 2 (3e).

Launch the model blueprint analyzer agent using the Task tool with `run_in_background: false` (wait for completion):

- `subagent_type`: `judo-model-blueprint-analyzer`
- `description`: "Blueprint analysis: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>** (index N of TOTAL). Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path>`. Read existing model blueprints from model-blueprints/ first, then survey the entire model using the CLI queries in order. Identify recurring structural fragments (entity clusters, common attribute sets, enum patterns, generalization hierarchies). Write/update blueprints in model-blueprints/. Include detection queries and creation mutations with template placeholders. Report what you found, including the list of blueprint IDs you created or updated."

**From the agent's output, collect the list of blueprint IDs that were created or updated.** This list is passed to the backend/frontend agents.

#### 3d. Stage 1.5: Validate Model Mutations

After the model agent completes, validate **only the blueprints that were created or updated** (from the list collected in 3c):

```bash
# For each blueprint ID from the agent's output:
$CLAUDE_PROJECT_DIR/tests/test-blueprint-mutations.sh --blueprint <blueprint-id>
```

Run one validation per modified blueprint. Do NOT run the full test suite here — only test the ones that changed.

- If all pass: proceed to Stage 2
- If any fail: report the failures to the user. These should be fixed before backend/frontend analysis.

Update PROGRESS.md: mark `Model: done` for this project.

#### 3e. Stage 2: Backend + Frontend Analysis (parallel)

**Check PROGRESS.md**: Skip `Backend` or `Frontend` if already `done` or `skipped`.

**Determine which blueprint IDs to analyze** using `query-catalog.py`:

```bash
python3 $CLAUDE_PROJECT_DIR/query-catalog.py list --project <PROJECT> --type blueprint
```

This returns all blueprints whose `projects:` frontmatter includes this project — works both when Stage 1 just ran (the model agent updates frontmatter) and when resuming (Model already `done`). Extract the blueprint IDs from the output table. If no blueprint IDs are found (e.g., the project has no model file), pass an empty list — the agents will still run **discovery mode** to find implementation-only patterns.

Launch **both** agents in parallel using `run_in_background: true`:

**Backend agent:**
- `subagent_type`: `judo-backend-blueprint-analyzer`
- `description`: "Backend blueprints: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>**. Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path or 'none'>`. Blueprint IDs to analyze: `<comma-separated-ids or 'none'>`.

**IMPORTANT: Run Phase 0 (Discovery Scan) FIRST.** Before processing blueprint IDs, scan the project's backend code for implementation-only patterns — custom implementations that don't correspond to any model-level blueprint. Check custom/**/*.java, separate Maven modules (keycloak-client/, integration/, etc.), interceptors, and service layers. Create new impl-only blueprints (with `impl_only: true`) for patterns not already in the catalog.

**Then run Phase 1 (Match Mode).** For each blueprint ID, read its BLUEPRINT.md and model.md to understand the structural pattern, then search the project's backend code (custom/**/*.java, interceptors, DI wiring) for related implementations. Write backend.md for each blueprint where you find implementation. Also add a `## Backend Implementation` reference section to BLUEPRINT.md if you create a backend.md.

Report what you found, including both impl-only blueprints created AND backend.md files written for existing blueprints."

**Frontend agent:**
- `subagent_type`: `judo-frontend-blueprint-analyzer`
- `description`: "Frontend blueprints: <PROJECT>"
- `prompt`: "Analyze project **<PROJECT>**. Project path: `/tmp/judo-projects/<PROJECT>/`. Model file: `<model-path or 'none'>`. Blueprint IDs to analyze: `<comma-separated-ids or 'none'>`.

**IMPORTANT: Run Phase 0 (Discovery Scan) FIRST.** Before processing blueprint IDs, scan the project's frontend code for implementation-only patterns — custom components, cross-cutting Pandino hooks, theme systems, and other custom implementations that don't correspond to any model-level blueprint. Check custom/**, application-customizer, .generator-ignore, src/theme/, src/layout/. Create new impl-only blueprints (with `impl_only: true`) for patterns not already in the catalog.

**Then run Phase 1 (Match Mode).** For each blueprint ID, read its BLUEPRINT.md and model.md to understand the structural pattern, then search the project's frontend code (custom/**, hooks, theme, layout) for related implementations. Write frontend.md for each blueprint where you find implementation. Also add a `## Frontend Implementation` reference section to BLUEPRINT.md if you create a frontend.md.

Report what you found, including both impl-only blueprints created AND frontend.md files written for existing blueprints."

Wait for both agents to complete.

Update PROGRESS.md: mark `Backend` and `Frontend` as `done` (or `skipped` if no backend/frontend code exists in the project).

#### 3f. Update Overall Status

1. Get the current remote HEAD SHA:
   ```bash
   git -C /tmp/judo-projects/<name>/ rev-parse --short=7 HEAD
   ```
2. Update `model-blueprints/PROGRESS.md`: store SHA, update `Status` to `done` if all three domains are done/skipped.
3. Log progress: "Project N/M (<PROJECT>) complete."

#### 3g. Cleanup

```bash
rm -rf /tmp/judo-projects/<name>/
```

#### 3h. Advance to Next Project

**IMPORTANT**: Do NOT start the next project until all agents for the current project have completed.

### Step 4: Validate Modified Blueprint Mutations

After all projects are processed, validate **only the blueprints that were created or updated** during this run. Maintain a cumulative list of all blueprint IDs touched across all projects, then test each one:

```bash
# For each blueprint ID that was created or updated during the run:
$CLAUDE_PROJECT_DIR/tests/test-blueprint-mutations.sh --blueprint <blueprint-id>
```

- If all pass: proceed to summary
- If any fail: report the failures to the user with specific errors.

### Step 5: Generate Summary Report

After validation:

1. Count files:
   ```bash
   echo "Directories:"; ls -d model-blueprints/*/ 2>/dev/null | wc -l
   echo "BLUEPRINT.md:"; find model-blueprints/ -name "BLUEPRINT.md" | wc -l
   echo "model.md:"; find model-blueprints/ -name "model.md" | wc -l
   echo "backend.md:"; find model-blueprints/ -name "backend.md" | wc -l
   echo "frontend.md:"; find model-blueprints/ -name "frontend.md" | wc -l
   echo "Impl-only:"; grep -rl "impl_only: true" model-blueprints/*/BLUEPRINT.md 2>/dev/null | wc -l
   ```

2. Present the results to the user:
   - Total blueprints cataloged
   - Model blueprints (with model.md)
   - **Implementation-only blueprints** (with `impl_only: true`, no model.md)
   - Blueprints with backend implementation
   - Blueprints with frontend implementation
   - Top fragments by usage count
   - Projects processed
   - Suggestion to re-run after adding new projects

---

## Key Design Decisions

### Three-Stage Pipeline: Model -> Validate -> Backend + Frontend (with Discovery)

The model blueprint must be written first because the backend/frontend agents **read** the BLUEPRINT.md and model.md to understand what entities/operations to search for. The model agent creates the structural definition, then the backend/frontend agents search for implementation patterns based on that definition.

**However**, the backend/frontend agents also run a **discovery scan** (Phase 0) before matching against known blueprints. This discovers implementation-only patterns — custom code that doesn't correspond to any model entity. These get their own blueprint directories with `impl_only: true` and no `model.md`. This means even projects without a `.model` file can contribute blueprints.

### Full Clone (not Sparse)

Unlike a model-only version which uses sparse checkout (`model/` only), this version needs the entire repository because:
- Backend agent needs `custom/**/*.java`, interceptors, Guice modules
- Frontend agent needs `custom/**/*`, `src/theme/`, `src/layout/`, `.generator-ignore`

### Resume Support

PROGRESS.md tracks three domain columns independently:
- If Model is `done` but Backend/Frontend are `pending`, the command skips the model agent and goes straight to backend/frontend
- This allows interrupted runs to resume without re-analyzing the model
- Projects where all three are `done` are skipped entirely

### PROGRESS.md Auto-Sync

New projects added to PROJECTS.md are automatically added to PROGRESS.md as `pending` rows when the command runs. No manual PROGRESS.md editing needed.

### Clone on Demand

Same pattern as `/collect-best-practices`:
- **Always fresh** — version checking catches remote changes
- **Extensible** — add a row to `PROJECTS.md` and it just works
- **Cleanup** — repos are deleted after each project

### Extensibility

- **Add a project**: Append one row to `PROJECTS.md` -> `/collect-model-blueprints` detects as "NEW"
- **Re-analyze a project**: Delete its row from PROGRESS.md or change its SHA -> shows as "CHANGED"
- **Re-run backend/frontend only**: Set Model to `done`, Backend/Frontend to `pending` -> only runs those stages
- **Start fresh**: Delete `model-blueprints/PROGRESS.md` -> all projects treated as NEW
- **No hardcoded lists** in any agent or command

---

## Notes

- **Progress is tracked in `model-blueprints/PROGRESS.md`** with per-domain columns — interrupted runs can resume
- Projects are processed sequentially (one at a time), but backend + frontend agents run in parallel within each project
- Running this command again is idempotent: existing blueprints get updated counts/timestamps/examples, not duplicated
- The version check script accepts a custom PROGRESS.md path as second argument
- All agents use `maxTurns: 50` to prevent runaway context usage per project
- Cloned repos go to `/tmp/judo-projects/` and are cleaned up after each project
