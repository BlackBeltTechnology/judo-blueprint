# Research open findings and propose doc text (no edits)

Repo: /Users/bmiller/Projects/judo-blueprint. Your list: `target/apply-findings/research/<name>.json`. Each item failed a quick check in the first pass (`first_pass` says why). Many are missing platform topics (B-ids): the docs say nothing, and app developers need the answer.

Per item, up to ~8 lookups:
1. Find the answer in judo-ng source (read-only): `target/judo-ng-read/wt/<group>__<repo>/` (`ls target/judo-ng-read/wt`), plus per-repo digests in `target/judo-ng-read/digest/`. CLI behaviour: `java -jar target/judo-cli.jar <cmd> --help`, or try it on a /tmp copy of `tests/fixtures/Sandbox.model`. Use `kb_search` / `kb_get` to see what the catalog already says.
2. Items with K/R ids (`knowledge-check`) are developer decisions: propose the text without a code check (e.g. "JCL is deprecated", "measures are not in use"), and pick the docs that need a one-line note.
3. Write the answer as doc text: platform fact only, neutral placeholders (`<app>`, `<Entity>`), no project, client or business-domain words, no session/round/test references, plain present tense, short (bullets or a short `###` sub-section).
4. If the source does not settle it, say so: status `open` with what you found. Never guess.

Do NOT edit any repo file. Append one JSON line per item to `target/apply-findings/research/<name>.out.jsonl`:
`{"id":..,"status":"proposed|already-correct|open|not-platform","file":"catalog/agent-docs/...md","heading":"<existing heading to add under>","text":"<exact markdown to insert or the corrected sentence>","replace":"<exact old sentence, only for corrections>","evidence":"<repo>/<path>:<line>[, ...]"}`.
Reply with counts per status.
