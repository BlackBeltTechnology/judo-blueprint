Double-check the wave-2 items of these batches: deployment-a deployment-b testing. For each batch, follow the prompt below with <WORK>=target/apply-findings and <BATCH>=that batch. Check only ledger lines with "wave":2 whose id has no line yet in check/<BATCH>.jsonl; earlier items are already checked. Use kb_search/kb_get first; if kb fails, say so and fall back to rg.

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

Also: handoff R1065 (prune `[Y/n]`) targets `deployment/build-process.md`, which your batch deployment-a owns. Verify it against judo.sh and apply it if the source confirms it.
