# JUDO Blueprint

A pattern catalog of reusable best practices and model blueprints extracted from 26 real-world [JUDO](https://github.com/BlackBeltTechnology) projects. Collected automatically by AI agents that clone, analyze, and score project source code.

## What's Inside

```
best-practices/
  model/      — 71 patterns (entity design, naming, cardinalities, state machines, …)
  backend/    — 74 patterns (custom operations, interceptors, integrations, …)
  frontend/   — 77 patterns (theme overrides, layout, custom components, …)

model-blueprints/ — Reusable model fragments with detection queries + creation mutations

agent-docs/   — Reference documentation for JUDO development domains
PROJECTS.md   — Registry of all analyzed projects (source of truth)
```

## Quick Start

### Prerequisites

- [Claude Code](https://claude.com/claude-code) CLI
- Git SSH access to the project repositories listed in `PROJECTS.md`

### Collect Best Practices

```bash
/collect-best-practices              # Analyze all domains (model, backend, frontend)
/collect-best-practices model        # Only model-layer patterns
/collect-best-practices backend      # Only backend-layer patterns
/collect-best-practices frontend     # Only frontend-layer patterns
```

The command will:

1. Read `PROJECTS.md` for the project list and git URLs
2. Compare remote HEAD SHAs against previously analyzed versions
3. Clone changed/new projects to `/tmp/judo-projects/` (shallow, one at a time)
4. Dispatch 3 parallel analyzer agents per project (model, backend, frontend)
5. Update `best-practices/PROGRESS.md` with results and SHAs
6. Score all patterns and generate a summary report
7. Clean up cloned repos

### Add a New Project

Append a row to `PROJECTS.md`. The next `/collect-best-practices` run detects it as "NEW" automatically.

### Re-analyze a Project

Delete or modify its row in `best-practices/PROGRESS.md`. It will show as "CHANGED" on the next run.

### Start Fresh

Delete `best-practices/PROGRESS.md` — all projects are treated as NEW.

### Collect Model Blueprints

```bash
/collect-model-blueprints              # Analyze all projects for reusable model fragments
```

The command will:

1. Read `PROJECTS.md` for the project list and git URLs
2. Compare remote HEAD SHAs against `model-blueprints/PROGRESS.md`
3. Clone changed/new projects to `/tmp/judo-projects/` (shallow, one at a time)
4. Dispatch a model blueprint analyzer agent per project
5. Update `model-blueprints/PROGRESS.md` with results and SHAs
6. Generate a summary report
7. Clean up cloned repos

**Best practices vs model blueprints:**
- **Best practices** = "how to do things well" (conventions, guidelines, scored by frequency)
- **Model blueprints** = "reusable structural fragments" (concrete entity/attribute shapes with GraphQL creation mutations)

Each blueprint includes a **detection query** (find the fragment in a model) and **creation mutations** (recreate it in a new project with template placeholders).

### Add a Single Best Practice

```bash
/add-best-practice "Toggle boolean operation pattern" https://github.com/org/project/blob/main/custom/ToggleActiveCustomImpl.java
/add-best-practice "Singleton entity for global settings" https://github.com/org/project
```

Auto-detects the domain (model/backend/frontend) from the URL, confirms with you, then launches the appropriate analyzer agent for that one pattern.

### Add a Single Model Blueprint

```bash
/add-model-blueprint "Audit log entity with timestamp and action type enum" https://github.com/org/project
/add-model-blueprint "Address entity with street, city, postal code fields" https://github.com/org/project/blob/main/model/Project.model
```

Clones the project, uses CLI queries to survey the model structure, then generates detection queries and creation mutations for the described fragment. The agent discovers the exact attribute names, relation kinds, and cardinalities from the model before writing mutations.

## How It Works

### Agents

Four domain-specific agents analyze each project directly from source:

| Agent | Looks For | Used By |
|-------|-----------|---------|
| **Model Analyzer** | Entity design, cardinality conventions, naming patterns, generalization, UI model organization | `/collect-best-practices`, `/add-best-practice` |
| **Backend Analyzer** | Custom operation implementations, `.generator-ignore` overrides, interceptor chains, DI wiring, external integrations | `/collect-best-practices`, `/add-best-practice` |
| **Frontend Analyzer** | Theme overrides (`palette.ts`, `density.ts`), layout customizations, `custom/` folder patterns, public asset overrides | `/collect-best-practices`, `/add-best-practice` |
| **Model Blueprint Analyzer** | Reusable structural fragments (entity clusters, enum patterns, relation shapes) with CLI-driven detection queries and creation mutations | `/collect-model-blueprints`, `/add-model-blueprint` |

Key signals the agents look for:
- **`**/custom/`** folders — hand-written code reveals what developers actually customize
- **`**/.generator-ignore`** files — shows which generated files are commonly overridden
- **Model structure** — entity relationships, naming conventions via CLI introspection

### Scoring

Both best practices and model blueprints use the same scoring system, normalized to **0–100**. The final score is a weighted combination of three independent components:

```
score = 60% × project_weight + 20% × usage + 20% × recency
```

Each component is independently normalized to 0–100 before combining:

| Component | Weight | What it measures | Normalized how |
|-----------|--------|------------------|----------------|
| **Project weight** | **60%** | Average `Weight` from `PROJECTS.md` across the pattern's projects | `-10` → 0, `0` → 50, `+10` → 100 |
| **Usage** | 20% | How many projects use this pattern (minus alternative penalty for best-practices) | Min-max across all items |
| **Recency** | 20% | Average age rank of the pattern's projects (newer = higher) | Min-max across all items |

Project weight is the **dominant factor** — it determines the score range, while usage and recency fine-tune within that range.

Run scoring standalone:

```bash
# Best practices
python3 .claude/scripts/score-best-practices.py --top 30     # Top 30 patterns
python3 .claude/scripts/score-best-practices.py --summary     # Full summary
python3 .claude/scripts/score-best-practices.py --update      # Recalculate & write scores to files

# Model blueprints
python3 .claude/scripts/score-model-blueprints.py --top 20   # Top 20 blueprints
python3 .claude/scripts/score-model-blueprints.py --summary   # Full summary
python3 .claude/scripts/score-model-blueprints.py --update    # Recalculate & write scores to files
```

### Project Weights

The `Weight [-10;+10]` column in `PROJECTS.md` lets you flag projects as important or unimportant. Weights control **60% of the final score**, so they always have more impact than how many projects use a pattern or how recent those projects are.

| Weight | Score contribution (60% component) | Typical effect |
|--------|-------------------------------------|----------------|
| `-10` | 0 / 100 | Patterns from this project score near bottom |
| `-5` | 25 / 100 | Significant penalty |
| `0` | 50 / 100 | Neutral (default) — usage and recency decide the rest |
| `+5` | 75 / 100 | Significant boost |
| `+10` | 100 / 100 | Patterns from this project score near top |

When a pattern appears in multiple projects, the **average weight** across its projects is used. To set a weight, edit the last column of the project's row in `PROJECTS.md`:

```markdown
| 1   | **mlszksz-platform** | git@... | 2026-01-07 | 2026-02-24 | 104 | 5 |
```

Then re-run the scoring scripts with `--update` to apply.

## Commands & Scripts Reference

### Commands

| Command | Description |
|---------|-------------|
| `/collect-best-practices [domain]` | Batch-analyze all projects for best practices (model, backend, frontend) |
| `/collect-model-blueprints` | Batch-analyze all projects for reusable model structural fragments |
| `/add-best-practice <desc> <url>` | Add a single best practice from a specific GitHub project |
| `/add-model-blueprint <desc> <url>` | Add a single model blueprint from a specific GitHub project |

### Scripts

| Script | Description |
|--------|-------------|
| `query-catalog.py` | **Unified catalog query** — list all items (names + scores) or get full content by ID |
| `score-best-practices.py` | Score best practices (0–100, usage + recency − alternatives × weight) |
| `score-model-blueprints.py` | Score model blueprints (0–100, usage + recency × weight) |
| `rank-model-blueprints.py` | Rank model blueprints by usage count across projects |
| `check-project-versions.sh` | Compare remote HEAD SHAs against last-analyzed versions in PROGRESS.md |

All scripts live in `.claude/scripts/` and accept `--help` for full usage.

### Querying the Catalog

The `query-catalog.py` script provides a lightweight way to browse and selectively read catalog entries. Agents use this to avoid loading all 298 files — they list names first, then fetch only what's relevant.

```bash
# List everything (compact: id + title + score)
python3 .claude/scripts/query-catalog.py list

# Filter by type
python3 .claude/scripts/query-catalog.py list --type blueprint       # Only model blueprints
python3 .claude/scripts/query-catalog.py list --type best-practice   # Only best practices

# Filter by domain
python3 .claude/scripts/query-catalog.py list --domain model         # Model best-practices
python3 .claude/scripts/query-catalog.py list --domain backend       # Backend best-practices
python3 .claude/scripts/query-catalog.py list --domain frontend      # Frontend best-practices

# Filter by category
python3 .claude/scripts/query-catalog.py list --category entity

# Get full content of specific items (by ID)
python3 .claude/scripts/query-catalog.py get audit-log-entity
python3 .claude/scripts/query-catalog.py get collection-lower-bound-zero enum-state-machine
```

Agents follow a **list-then-get** workflow: run `list` to see all names and scores, survey the project, then `get` only the IDs that match patterns found in the project. This keeps context usage minimal while still allowing agents to update existing entries directly.

## Design Decisions

- **Clone on demand** — repos are `git clone --depth 1` to `/tmp` and deleted after analysis. No stale local copies, no manual syncing.
- **No intermediate research step** — agents read source directly and write to `best-practices/`. Fewer agents, no stale research files.
- **Sequential project processing** — one project at a time prevents context overflow. Each project's 3 domain agents run in parallel.
- **Idempotent** — re-running updates existing best practices (counts, timestamps) rather than duplicating them.
