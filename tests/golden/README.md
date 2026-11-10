# kb golden queries

`kb-golden.json` holds 62 developer-style questions, each with the catalog path that should answer it: 33 agent-docs, 16 blueprints, 13 practices. Queries are written as a developer would ask them, not copied from entry aliases.

`check-all` builds a fresh index of `catalog/` only (what consumers index), runs `kb eval`, and fails below the floor in `threshold.json`.

## Baseline (2026-11-10, catalog-only index)

| P@1 | P@5 | Recall@10 | MRR |
|---|---|---|---|
| 0.629 | 0.839 | 0.871 | 0.695 |

Indexing the whole repo drops P@5 to 0.758, because openspec sweep files compete. Consumers index `catalog/` only, so the gate measures that.

## Known misses (top 5)

Most misses are agent-docs rules outranked by a practice entry or a directory `AGENTS.md` on the same topic:

- interceptor scope → `backend/interceptors.md` (got a practice)
- business error 422 / ValidationException 400 → `backend/error-handling-guide.md` (got `error-code-enum`)
- `@JudoTest` transaction modes → `backend/custom-operations.md` (got integration-testing docs, arguably fine)
- actor access getter has no `self` → `backend/architectural-patterns.md`
- view model panel → `model/advanced-modeling-patterns.md` (got the practice, which links it)
- abstract entity polymorphic create → `model/generalization-guide.md`
- `hiddenBy`/`enabledBy` → `model/ui-authoring-guide.md` (got the practice)
- interceptor testing → `integration-testing/interceptor-testing.md` (got the `AGENTS.md` index)
- notification read/unread → `model-blueprints/notification-entity`

Improve these through the docs (headings, aliases), not by editing the queries.
