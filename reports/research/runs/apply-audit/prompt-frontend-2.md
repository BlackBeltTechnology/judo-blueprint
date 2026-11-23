# Apply findings to one batch (wave 1 and wave 2)

Work in the judo-blueprint repository root. Your batch: `target/apply-audit/batches/frontend-2.json` (`files` = the only files you may edit). Items: wave 1 = its `items`; wave 2 = `target/apply-audit/wave2/frontend-2.json` (kinds `research` with proposed text, `triage` with a correct fact, `handoff` from another batch).

## Per item: quick check, then apply

1. Find the target section (`kb_search` / `kb_get`; fall back to rg/read only if kb fails).
2. Quick-check the claim, at most ~3 lookups:
   - judo-ng source, read-only: `target/judo-ng-read/wt/<group>__<repo>/` (`ls` it); open the cited lines.
   - CLI: `java -jar target/judo-cli.jar <cmd> --help`, or try it on a /tmp copy of `tests/fixtures/Sandbox.model`. Never touch a repo model.
   - Developer decisions (knowledge-check K/R ids) need no code check unless code clearly contradicts them.
3. Status: `applied` | `already-correct` | `unverified` (not confirmed quickly: do NOT write) | `rejected` (code contradicts) | `not-platform` (project/domain-specific, tooling or framework-internal) | `handoff` (file owned by another batch: give file and exact `proposed` text).
4. Write only confirmed platform facts:
   - Correct a wrong sentence **in place**, smallest edit. Add missing facts as short bullets or a `###` sub-section in the best-fitting section.
   - **Never delete or shorten correct content; never rename, reorder or remove a heading; never touch `AGENTS.md`.** `content-guard` fails the gate on lost headings and pure deletions.
   - Frontmatter: append to `keywords`/`aliases` only.
   - No project or client names, no business domain words, no session/round/test references; neutral `<app>`, `<Actor>`, `<Entity>`, `<model>`.
   - If you add a `##`, add the same `##` with 1-3 bullets to the file's `<name>.agent.md` companion.

## Ledger (mandatory, exactly one line per item)

Append to `target/apply-audit/ledger/frontend-2.jsonl`:
`{"id":..,"status":..,"file":..,"heading":..,"evidence":"<repo>/<path>:<line> | cli:<cmd> | operator:<id>","change":"<one line>"}` (wave 2 adds `"wave":2`; handoffs add `"proposed"`).
`findings-ledger reconcile` fails the pass for any item without a line.

No git writes, no `check-all`. Final answer: counts per status and files changed, 3 lines.

Each item text carries the proposed fact and its judo-ng evidence from an audit of findings that triage had wrongly marked not platform; still re-check the code before writing. Update the `.agent.md` companion line for every fact you add to an agent-doc.
