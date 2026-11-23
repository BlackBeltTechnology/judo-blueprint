# Validate and settle mined build-session items (one pass, no open status)

Working directory: /Users/bmiller/Projects/judo-blueprint. Edit NO catalog file; write only your output file and scratch files under /tmp/tools-02/.

Input: target/gap-analysis-r16/batches/tools-02.jsonl: items mined from a build session (webshop build test, rounds R16 to R19). Miners make mistakes: validate every item, do not trust it.

Sources (read-only):
- Session: `.pi/skills/judo-catalog-expand/scripts/session-chunks reports/research/webshop-run/2026-11-11T14-06-20-342Z_01a1caee-58b6-724e-ae62-d32987dbcd2d.jsonl --dump START END` prints session lines; chunk texts are in target/gap-analysis-r16/chunks/.
- App: ~/Projects/webshop-test (GAPS.md, git log/show, sources). Read-only.
- Catalog: kb_search + kb_get FIRST, then read short files whole or grep catalog/.
- Already processed: target/apply-findings-webshop/ledger/*.jsonl (ids WR16-*..WR19-*, the GAPS items) and reports/judo-ng-issues/{CLI,FRAMEWORK}.md, reports/kb-issues/KB.md. An item already settled there gets status "duplicate" with dup_of = that id or report section.
- judo-ng code: target/judo-ng-read/wt/<group>__<repo>/ on latest develop (metamodel, transformations, generators/templates incl. judo.sh.hbs, runtime, maven plugins). The framework is entirely there; trace it.
- CLI reproduction: copy tests/fixtures/Sandbox.model to /tmp/tools-02/ and run java -jar target/judo-cli.jar -m /tmp/tools-02/Sandbox.model ... Never touch a repo model or the app.

For EVERY input item write one JSON line to target/gap-analysis-r16/validated/tools-02.jsonl, keeping id, round, what, kind, plus:
- "status": "proposed" (catalog change needed) | "already-correct" (catalog covers it; cite path+heading) | "rejected" (claim wrong per code or session) | "not-platform" (builder mistake, test design, app-only, orchestrator process: say which) | "duplicate" (dup_of set) | "upstream" (CLI, framework or kb defect, no catalog change beyond what exists)
  There is NO open/unverifiable status. Keep tracing until settled.
- "file": catalog/<path>.md, "heading": exact heading, "replaces": exact current sentence to correct or "", "proposed": exact new text (generic wording: no project, client or domain names; use <app>, <Entity>, <Actor>; no CLI commands in best-practices or model-blueprints, only in agent-docs)
- "evidence": "<repo>/<path>:<line> | cli:<command → result> | session:L<n> | app:<path>"
- "upstream_kind": "cli" | "framework" | "kb" | null, and "upstream": one paragraph for those developers (behaviour, expected, evidence file:line), for every real tool or platform defect (also when status is proposed, since the catalog then documents the workaround).
- "dup_of": id or null. Merge same-root items inside your batch: the first carries the proposal, the others status "duplicate".
Agent-tool items about kb: check them against kb now (kb_search/kb_get with the same query); a kb defect gets status upstream/upstream_kind kb; a retrieval miss where the catalog lacks the fact is a catalog gap (proposed).
Plain language, no em dashes. Final answer: three lines (counts per status and upstream_kind; top 3 items; anything not done).
