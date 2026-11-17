# Research open findings and propose text (no edits)

Work in the judo-blueprint repository root. Your list: `<WORK>/research/<NAME>.json`: items a quick check could not settle (`first_pass` says why), often missing topics.

Per item, up to ~8 lookups:
1. Find the answer in judo-ng source (`target/judo-ng-read/wt/<group>__<repo>/`, digests in `target/judo-ng-read/digest/`) or by running the CLI on a /tmp copy of `tests/fixtures/Sandbox.model`. `kb_search` / `kb_get` show what the catalog already says.
2. Developer decisions (K/R ids) need no code check: propose the note and the docs that need it.
3. Write the doc text: platform fact only, neutral placeholders, no project/domain/session words, short.
4. If the source does not settle it, status `open` with what you found. Never guess.

Do NOT edit repo files. One line per item to `<WORK>/research/<NAME>.out.jsonl`:
`{"id":..,"status":"proposed|already-correct|open|not-platform","file":"catalog/...md","heading":"<existing heading>","text":"<markdown to insert or corrected sentence>","replace":"<old sentence, corrections only>","evidence":"<repo>/<path>:<line>[, ...]"}`.
Final answer: counts per status, 3 lines.
