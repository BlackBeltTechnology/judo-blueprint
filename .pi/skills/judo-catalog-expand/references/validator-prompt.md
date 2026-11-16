# Claim validator task

Input: a JSONL batch of claims mined from a build session (fields: id, type, round, functions, what, why, kind, workaround, catalog_paths, gaps_ref, evidence, proposed, proposed_target, confidence). Miners made mistakes; your job is to VALIDATE every claim, not to trust it.

Sources (read-only):
- Session dump helper: `.pi/skills/judo-catalog-expand/scripts/session-dump <SESSION.jsonl> START END` prints session JSONL lines START..END. `session:L<n>` evidence may be a session line OR a line in the chunk text file (`<WORK>/chunks/cNN_L<a>-<b>.txt`, chunk id = prefix of the claim id). Check whichever matches.
- Application repo <APP_DIR>: GAPS.md, TRACE.md, git log/show, source files.
- Catalog: kb_search + kb_get FIRST (never the `kb` CLI), then grep catalog/ if needed.
- judo-ng read-only clones under target/judo-ng-read/wt for platform-bug claims (check briefly; do not spend long).
- Existing records: openspec/changes/archive/2026-11-16-restructure-blueprints-for-kb/judo-doc-problems.md and judo-knowledge-check-developer-corrections.md (already-known issues).

For EACH claim decide:
- `verdict`: confirmed | partly | refuted | unverifiable
- `catalog_status`: missing | wrong | covered | partly-covered | n/a  (what the catalog says TODAY; cite the path/section you checked. If the builder said "not documented" but the catalog covers it, that is refuted + the real issue is "builder did not find it": note retrieval problem)
- `disposition`: add-catalog | modify-catalog | platform-ticket | tool-fix | one-off | no-action
- `target`: exact catalog file to add/modify (existing path, or proposed new path), tool name, or judo-ng module
- `note`: one or two plain sentences: what you checked and found; for add/modify, the one-line content that should go in.
- `dup_of`: id of an earlier claim in your batch with the same root problem, or null (merge duplicates: keep the first, list the others' ids in `merged`).
Keep all original fields; add the new ones.

Write <WORK>/validated/<BATCH>.jsonl (one object per input claim, same order). Edit nothing else. No state-changing git. Plain language, no em dashes.
Final answer: three lines only (counts per type and kind; the 3 most important items; anything not done). Detail goes in your output file.
