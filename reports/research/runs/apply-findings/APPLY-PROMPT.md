# Apply findings to the JUDO catalog: one batch

Repo: /Users/bmiller/Projects/judo-blueprint. You own ONE batch: `target/apply-findings/batches/<batch>.json`.
It has `files` (the only files you may edit) and `items` (findings to apply).

## Per item: quick check, then apply

1. Read the item. Open the target section of the doc (use `kb_search` / `kb_get` to find where a topic lives; if a kb call fails, fall back to rg/read).
2. Quick-check the claim against the source of truth. At most ~3 lookups per item; do not research beyond that.
   - judo-ng source (read-only): `target/judo-ng-read/wt/<repo>/` (103 repos named `<group>__<repo>`, e.g. `wt/template__judo-esm-fullstack-project-template`; `ls target/judo-ng-read/wt`). Grep the identifier, open the cited lines.
   - CLI behaviour: `java -jar target/judo-cli.jar --help` / `<command> --help`; for a behaviour test copy `tests/fixtures/Sandbox.model` to a /tmp scratch dir first. Never touch repo models.
   - A generated project for reference only: `~/Projects/webshop-test` (take only platform facts from it, never its domain).
   - Developer statements (items from `knowledge-check` with K/R ids) are operator decisions: apply them unless judo-ng code clearly contradicts.
3. Decide: `applied` (confirmed and written), `already-correct` (doc already says it), `unverified` (could not confirm quickly; do NOT write), `rejected` (code contradicts the finding), `not-platform` (project/domain-specific, tool or framework-internal; nothing for app developers), `handoff` (right file belongs to another batch: give file + exact proposed text).
4. Apply only confirmed platform facts:
   - Correct a wrong sentence in place with the smallest edit. Add missing facts as short bullets or a short sub-section in the best-fitting existing section.
   - NEVER delete or shorten correct content, NEVER rename, reorder or remove headings, NEVER touch generated blocks or `AGENTS.md`. Frontmatter: you may only append to `keywords`/`aliases`.
   - No "previously this said" notes; no session, round or test references (no "R6", "webshop", "build test").
   - NO domain-specific content: no project or client names, no business domain (products, orders, galaxies, inspections...). Use neutral placeholders: `<app>`, `<Actor>`, `<Entity>`, `<model>`.
   - Platform claims you cannot confirm are not written. Where a doc already states something unconfirmable, leave it.
   - Keep the doc's style: plain, present tense, concrete commands and paths.

## Ledger (mandatory, one line per item)

Append JSON lines to `target/apply-findings/ledger/<batch>.jsonl`:
`{"id":..,"status":..,"file":..,"heading":..,"evidence":"<repo>/<path>:<line> or cli:<command> or operator:<id>","change":"<one line: what was written or why not>"}`
Every item gets exactly one line. Handoffs carry `"proposed":"<exact text>"`.

## Rules

- Edit only files listed in your batch `files`. No git writes (no add/commit/stash/checkout).
- judo-ng clones are read-only.
- Work through all items; be quick. When done, reply: counts per status and the files you changed.
