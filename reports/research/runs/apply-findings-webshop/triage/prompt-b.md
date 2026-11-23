Working directory: /Users/bmiller/Projects/judo-blueprint. Do NOT edit any file except your output file.

Input: target/apply-findings-webshop/triage/part-b (JSON lines: id, text). Each is a gap that a build agent logged while building a real JUDO app (~/Projects/webshop-test, read-only evidence) with this catalog as its kb.

For EVERY input line, write one JSON line to target/apply-findings-webshop/research/b.out.jsonl:
{"id":..,"status":"proposed|already-correct|not-platform|kb-tool|open","file":"catalog/<path>.md","heading":"<## heading>","proposed":"<exact new or corrected text>","replaces":"<exact current sentence it corrects, or empty for an addition>","evidence":"<judo-ng repo/path:line | cli:<cmd> | app file:line>"}

- proposed: a platform fact the catalog is missing or states wrongly. Settle it from the judo-ng code (target/judo-ng-read/wt, read-only), the CLI (java -jar target/judo-cli.jar ... --help, scratch copies only) or the running app's code as evidence. Generic wording: no webshop, product, order or other domain names; use <app>, <Entity>, <Actor>. Pick the ONE best existing catalog file (agent-docs for platform behaviour; a blueprint or best practice only when the gap is about that entry).
- already-correct: the catalog already says it correctly (give file and heading).
- not-platform: app-specific, test-data or environment issue (for example flaky tests from shared data).
- kb-tool: a problem of the kb search tool itself, not of catalog content.
- open: the code cannot settle it quickly; say what is missing in evidence.
Quick checks, at most ~4 lookups per gap. kb_search first to find catalog sections; read short files whole. At the end, check one output line per input id. Reply with counts per status.
