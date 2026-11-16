# kb golden queries

`kb-golden.json` holds 62 developer-style questions, each with the catalog path that should answer it: 33 agent-docs, 16 blueprints, 13 practices. Queries are written as a developer would ask them, not copied from entry aliases.

`check-all` builds a fresh index of `catalog/` only (what consumers index), runs `kb eval`, and fails below the floor in `threshold.json`.

## Baseline (2026-11-10, catalog-only index)

| Set | n | P@1 | P@5 | MRR |
|---|---|---|---|---|
| golden (tuned against) | 62 | 0.726 | 0.919 | 0.789 |
| holdout (never tuned) | 15 | 0.467 | 0.800 | 0.570 |

The golden misses were fixed through doc `description` fields and entry aliases, not by editing queries (one golden target was wrong: `generalization-guide.md` is about doc placeholders, so that query now expects `advanced-modeling-patterns.md`). The holdout set was written afterwards to measure whether those fixes generalise; trust it more.

**Biggest remaining lever:** directory `AGENTS.md` index rows take top-5 slots. Searching with `--doc-type doc` (kb_search `doc_type: "doc"`) gives golden P@5 0.968 and holdout 0.867. The consumer skill tells agents to use it for content questions.
