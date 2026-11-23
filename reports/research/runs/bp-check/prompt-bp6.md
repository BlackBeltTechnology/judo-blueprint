
Work in the judo-blueprint repository root. Your batch is `target/bp-check/batches/bp6.json`. Its `files` are the only files you may edit, plus their `.agent.md` companions. Its `items` are finding-to-file pairs: `id` (`<finding>@<n>`), `target` (the blueprint or best-practice file), `section` (the matched section, or null for an identifier match), `confirmed` (true when the finding was already verified and applied to agent-docs), and `text` (claim, fact and source of the finding).

Work file by file. Read each target file once (`kb_get` per section, or read it), then judge all of its items:

- `not-relevant`: the file does not talk about what the finding is about. Most matches are this; decide fast.
- `already-correct`: the file talks about it and agrees with the correct fact.
- `applied`: the file states the wrong claim, contradicts the fact, or is missing a caveat the reader needs right there. Fix it **in place** with the smallest edit.
- `rejected`: the finding itself is wrong (the code contradicts it).
- `unverified`: you can't settle it with a quick check. Do not write.

Rules for `applied`:
1. The source of truth is the judo-ng code (`target/judo-ng-read/wt/<group>__<repo>/`, read-only) and the corrected agent-docs (`catalog/agent-docs`, via `kb_search` then `kb_get`). For `confirmed` items the agent-docs already hold the checked fact: link to it (`../../agent-docs/...`) and align with it. For unconfirmed items, open the cited code line first (at most ~3 lookups).
2. Never delete or shorten correct content. Never rename, reorder or remove a heading. Never touch `AGENTS.md` or a ```mermaid block (a diagram fix goes in the ledger `change` as a proposal). Frontmatter: append only.
3. Platform facts only. No project or client names, no business-domain words, no session or round references. Use neutral `<app>`, `<Entity>`, `<Actor>`.
4. If you change a statement summarised in the file's `.agent.md` companion, correct the companion line too.

Ledger, mandatory, exactly one line per item, appended to `target/bp-check/ledger/bp6.jsonl`:
`{"id":..,"status":..,"file":..,"heading":..,"evidence":"<repo>/<path>:<line> | agent-docs/<path>#<section>","change":"<one line>"}`.
`findings-ledger reconcile` fails the pass for any item without a line.

If you pass `section` to `kb_get`, copy `headingPath` from `kb_search` with `format: "json"`. If kb fails, say so and fall back to rg.

No git writes, no `check-all`. At the end, check that your ledger has one line per item. Final answer: counts per status and files changed, 3 lines.
