Working directory: /Users/bmiller/Projects/judo-blueprint. Batches: bp5 bp6 bp7 bp8, with <WORK>=target/bp-check. These are blueprint and best-practice files, checked against judo-ng findings (prompt: .pi/skills/judo-catalog-expand/references/blueprint-check-prompt.md). Its rules for edits apply to you too: no deletions, no heading changes, no mermaid edits, and generic wording.

PART 1, double-check: follow the prompt below for each batch, for every ledger line with status applied.

PART 2, research the unverified items: for each ledger line with status unverified, settle it from the judo-ng code (target/judo-ng-read/wt) and the corrected agent-docs (kb_search then kb_get). Write one line per item to <WORK>/research/<BATCH>.out.jsonl: {"id":..,"status":"proposed|open|already-correct|not-platform","evidence":..}. If the result is proposed, apply the fix yourself in place, then append a ledger line {"id":..,"status":"applied","wave":2,"file":..,"evidence":..,"change":..} and a check line with verdict applied-now. Use open only when the code really cannot settle it, and say what is missing.

# Double-check one applied batch

Work in the judo-blueprint repository root. Batch `<BATCH>`: items in `<WORK>/batches/<BATCH>.json` and `<WORK>/wave2/<BATCH>.json`, applier ledger `<WORK>/ledger/<BATCH>.jsonl`, edits in `git diff -- <batch files>`. Frontmatter-only additions are a separate change: ignore them.

For EVERY `applied` item:
1. **Open the evidence yourself** (judo-ng file:line, `java -jar target/judo-cli.jar ... --help`, or the operator item). Do not trust the ledger or the item text: a spot check found wrong fallbacks and counts that appliers had copied from proposals. Does the evidence support the exact sentence written, including defaults, counts and fallbacks?
2. Check that the written text is a platform fact only, with no project/client/domain or session words and neutral placeholders.
3. Check that the diff deletes or shortens no correct content, leaves every heading in place, and does not touch `AGENTS.md`.
4. Read the whole section the item landed in: does the new text contradict a sentence next to it (old or new)? Fix the wrong one from the source.

Fix directly, only in the batch's files. Reword to what the evidence says, remove an unsupported addition, or restore deleted correct text from `git show HEAD:<file>`. Apply `handoff` items for your files if the evidence confirms them.

One line per checked item to `<WORK>/check/<BATCH>.jsonl`: `{"id":..,"verdict":"ok|fixed|removed|restored|applied-now","note":".."}`. `findings-ledger reconcile` fails for any applied item without a verdict.
No git writes. Final answer: counts per verdict and remaining concerns, 3 lines.
