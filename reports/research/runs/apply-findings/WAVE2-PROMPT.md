# Wave 2: apply researched facts to one batch's files

Repo: /Users/bmiller/Projects/judo-blueprint. Your batch: `<batch>`. Files you may edit: `files` in `target/apply-findings/batches/<batch>.json`. Items: `target/apply-findings/wave2/<batch>.json`. Kinds:
- `research`: proposed doc text with evidence (`text`, optional `replace`, `heading`, `evidence`).
- `triage`: a judo-ng finding stating a correct platform fact (`text`) the doc should hold.
- `handoff`: text another batch proposed for your file.

Per item, quick (at most ~3 lookups):
1. Confirm the evidence supports the text (open `target/judo-ng-read/wt/<group>__<repo>/<path>:<line>`, or `java -jar target/judo-cli.jar <cmd> --help`). Developer decisions (K/R ids) need no code check.
2. Check what the doc already says (`kb_get` / read the section). If it already says it, record `already-correct`.
3. Apply: insert under the named existing heading, or replace the wrong sentence with the smallest edit. If several items cover one topic, merge them into one coherent passage.

Same rules as `target/apply-findings/APPLY-PROMPT.md` (read it): never delete or shorten correct content, never rename, reorder or remove headings (adding a `###` is fine; add `##` only if no section fits), no project, client or business-domain words, neutral `<app>`/`<Entity>`, no session/round/test references, platform facts only, no git writes, edit only your files.
If you add a `##` heading to a file that has a `<name>.agent.md` companion, add the same `##` with 1-3 terse bullets to the companion.

Ledger: append to `target/apply-findings/ledger/<batch>.jsonl` one line per item: `{"id":..,"wave":2,"status":"applied|already-correct|unverified|rejected|not-platform","file":..,"heading":..,"evidence":..,"change":".."}`.
Reply with counts per status and the files changed.
