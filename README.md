# JUDO Blueprint

A pattern catalog of reusable best practices extracted from 26 real-world [JUDO](https://github.com/BlackBeltTechnology) projects. Blueprints are collected automatically by AI agents that clone, analyze, and score project source code.

## What's Inside

```
blueprint/
  model/      — 71 patterns (entity design, naming, cardinalities, state machines, …)
  backend/    — 74 patterns (custom operations, interceptors, integrations, …)
  frontend/   — 77 patterns (theme overrides, layout, custom components, …)

agent-docs/   — Reference documentation for JUDO development domains
PROJECTS.md   — Registry of all analyzed projects (source of truth)
```

## Quick Start

### Prerequisites

- [Claude Code](https://claude.com/claude-code) CLI
- Git SSH access to the project repositories listed in `PROJECTS.md`

### Collect Blueprints

```bash
/collect-blueprints              # Analyze all domains (model, backend, frontend)
/collect-blueprints model        # Only model-layer patterns
/collect-blueprints backend      # Only backend-layer patterns
/collect-blueprints frontend     # Only frontend-layer patterns
```

The command will:

1. Read `PROJECTS.md` for the project list and git URLs
2. Compare remote HEAD SHAs against previously analyzed versions
3. Clone changed/new projects to `/tmp/judo-projects/` (shallow, one at a time)
4. Dispatch 3 parallel analyzer agents per project (model, backend, frontend)
5. Update `blueprint/PROGRESS.md` with results and SHAs
6. Score all patterns and generate a summary report
7. Clean up cloned repos

### Add a New Project

Append a row to `PROJECTS.md`. The next `/collect-blueprints` run detects it as "NEW" automatically.

### Re-analyze a Project

Delete or modify its row in `blueprint/PROGRESS.md`. It will show as "CHANGED" on the next run.

### Start Fresh

Delete `blueprint/PROGRESS.md` — all projects are treated as NEW.

## How It Works

Three domain-specific agents analyze each project directly from source:

| Agent | Looks For |
|-------|-----------|
| **Model** | Entity design, cardinality conventions, naming patterns, generalization, UI model organization |
| **Backend** | Custom operation implementations, `.generator-ignore` overrides, interceptor chains, DI wiring, external integrations |
| **Frontend** | Theme overrides (`palette.ts`, `density.ts`), layout customizations, `custom/` folder patterns, public asset overrides |

Key signals the agents look for:
- **`**/custom/`** folders — hand-written code reveals what developers actually customize
- **`**/.generator-ignore`** files — shows which generated files are commonly overridden
- **Model structure** — entity relationships, naming conventions via CLI introspection

### Scoring

Each pattern gets a weighted score:

```
score = (usage_count × 10) + recency_bonus − alternative_penalty
```

- **Recency bonus** — newer projects contribute more weight
- **Alternative penalty** — patterns with many alternatives score lower (−2 per alternative)

Run scoring standalone:

```bash
python3 .claude/scripts/score-blueprints.py --top 30     # Top 30 patterns
python3 .claude/scripts/score-blueprints.py --summary     # Full summary
python3 .claude/scripts/score-blueprints.py --update       # Recalculate all scores
```

## Design Decisions

- **Clone on demand** — repos are `git clone --depth 1` to `/tmp` and deleted after analysis. No stale local copies, no manual syncing.
- **No intermediate research step** — agents read source directly and write to `blueprint/`. Fewer agents, no stale research files.
- **Sequential project processing** — one project at a time prevents context overflow. Each project's 3 domain agents run in parallel.
- **Idempotent** — re-running updates existing blueprints (counts, timestamps) rather than duplicating them.
