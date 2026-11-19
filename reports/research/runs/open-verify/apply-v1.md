Working directory: /Users/bmiller/Projects/judo-blueprint. Follow the prompt below with <WORK>=target/open-verify and <BATCH>=v1. Items: the batch's `items`, each a proposal traced in the judo-ng code (worktrees updated to the latest develop): `text` is the proposed wording, `replaces` the sentence it corrects (empty for an addition), `evidence` the code. Re-open the evidence lines before writing, and correct the wording to what the code says. Ids look like <work>::<id>; copy them unchanged into the ledger.

# Apply findings to one batch (wave 1 and wave 2)

Work in the judo-blueprint repository root. Your batch: `<WORK>/batches/<BATCH>.json` (`files` = the only files you may edit). Items: wave 1 = its `items`; wave 2 = `<WORK>/wave2/<BATCH>.json` (kinds `research` with proposed text, `triage` with a correct fact, `handoff` from another batch).

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

Append to `<WORK>/ledger/<BATCH>.jsonl`:
`{"id":..,"status":..,"file":..,"heading":..,"evidence":"<repo>/<path>:<line> | cli:<cmd> | operator:<id>","change":"<one line>"}` (wave 2 adds `"wave":2`; handoffs add `"proposed"`).
`findings-ledger reconcile` fails the pass for any item without a line.

No git writes, no `check-all`. Final answer: counts per status and files changed, 3 lines.
