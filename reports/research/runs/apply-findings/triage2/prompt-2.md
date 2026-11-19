
You triage judo-ng review findings for the JUDO catalog in `~/Projects/judo-blueprint`. Do not edit any catalog file. You only classify.

Input: `target/apply-findings/triage2/part-2.txt`. One finding per line: `id | kind | repo | path:line | claim: <what the judo-ng doc or spec says> | fact: <what the code does>`. `kind` is `doc` (doc contradicts code), `bug` (spec contradicts code) or `dox` (index file contradicts code).

For EVERY input line, write exactly one JSON line to `target/apply-findings/triage/verdicts-r2.jsonl`:
`{"id":"R....","verdict":"keep|not-platform|duplicate","reason":"<10 words max>"}`

- `keep`: the fact is platform behaviour an APPLICATION developer using JUDO needs, and `catalog/agent-docs` should state it. In scope: modelling (JSL/ESM), the CLI and `judo.sh`, generated backend behaviour (REST, DAO, operations, access, interceptors, validation, transactions, config properties), generated frontend behaviour (React UI, hooks, customization keys, i18n, routing), build, deploy and testing of generated apps.
- `not-platform`: framework internals that an application developer never sees, such as module internals, judo-ng's own build or CI, its docs site, contributor workflow, or Eclipse/EMF plumbing.
- `duplicate`: same fact as another line in this input that you keep.

Judge from the line text. Open the source only when the line alone can't decide it. Clones live in `~/Projects/judo-blueprint/target/judo-ng-read/wt/<repo with / as __>/`.

For each `keep`, also write one line to `target/apply-findings/triage/kept-r2.jsonl`:
`{"id":"R....","target":"catalog/agent-docs/<area>/<file>.md","fact":"<correct platform fact, neutral wording, no project or customer names>","evidence":"<repo>:<path>:<line>","already_documented":true|false}`

- Pick the ONE best existing agent-doc file. Use `kb_search` first (leave `doc_type` unset), then `kb_get`. Fall back to `rg` only if kb returns nothing. Valid targets are the keys of `target/apply-findings/file-owners.json`.
- `already_documented` is true only when the target already states the fact correctly. Check it with `kb_get` or by reading the section.
- The `fact` is the code behaviour, not the doc's claim. Check the code line for any fact you are not sure of. A quick look at the cited file is enough.

If kb tools fail, say so in your reply and continue with `rg`.

At the end, check that the line count of `verdicts-r2.jsonl` equals the input line count, and that every input id appears exactly once. Reply with: input count, keep, not-platform, duplicate, and already_documented among the kept.
