# Double-check one applied batch

Repo: /Users/bmiller/Projects/judo-blueprint. Batch `<batch>`: items in `target/apply-findings/batches/<batch>.json`, applier ledger in `target/apply-findings/ledger/<batch>.jsonl`, edits visible with `git diff -- <batch files>`.
Note: diff lines that only add `aliases:`/`keywords:`/`tags:` frontmatter, or remove `fragment:`/`diagram:` frontmatter and `mermaid:generated` markers, are a separate change. Ignore them.

For EVERY `applied` item:
1. Open the evidence (judo-ng `target/judo-ng-read/wt/<repo>/<path>:<line>`, `java -jar target/judo-cli.jar ... --help`, or the operator item). Does it support the exact text written? Quick check, at most ~2 lookups.
2. Check the written text: platform fact only; no project, client or business-domain words; no session/round/test references; neutral `<app>`/`<Entity>` placeholders.
3. Check the diff: no correct content deleted or shortened, no heading renamed, reordered or removed, no `AGENTS.md` or generated block touched.

Fix problems directly, only in the batch's files: reword wrong text to what the evidence says, remove an unsupported addition, restore deleted correct text from `git show HEAD:<file>`.
Also apply the `handoff` items whose target file is in this batch, if the evidence confirms them.
Spot-check 5 `unverified`/`rejected` items: if one is clearly confirmable in one lookup, apply it.

Write one JSON line per checked item to `target/apply-findings/check/<batch>.jsonl`:
`{"id":..,"verdict":"ok|fixed|removed|restored|applied-now","note":".."}`.
Use `kb_search` / `kb_get` to locate topics. No git writes. Reply with counts per verdict and any remaining concern.
