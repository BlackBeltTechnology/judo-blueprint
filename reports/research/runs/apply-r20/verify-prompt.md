# Verify R20 webshop findings against code

Work in `/Users/bmiller/Projects/judo-blueprint`. Your items: the ids listed in your task, full text in `target/apply-r20/inventory.json`. They come from a build agent (webshop round R20); treat every sentence as a claim to check, not as fact.

## Validate against code, always

For EVERY item, settle it from code or a reproduction. A doc or the item text is never evidence.
- **judo-ng source:** `target/judo-ng-read/wt/<area>__<repo>/` (full tree; `ls target/judo-ng-read/wt`). The pinned CLI source is `wt/runtime__judo-model-cli` (at `a64aa98`). Cite `wt/<repo>/<path>:<line>` with the short SHA (`git -C <wt> log -1 --format=%h`). If a repo has a newer `origin/develop`, check whether it changes the answer.
- **CLI reproduction:** `java -jar target/judo-cli.jar ...` (version `1.1.0.20261119_155735_a64aa981_develop`) on a COPY of a model in `target/apply-r20/scratch-<your group>/` (copy `~/Projects/webshop-test/model/webshop.model` or `tests/fixtures/Sandbox.model`). Record the exact command, exit code and the relevant output lines.
- **Generated or runtime behaviour:** read the generator template or runtime code that produces it; the webshop project at `~/Projects/webshop-test` (read only) shows generated output and logs.
- **Catalog check:** `kb_search` / `kb_get` (format json, then the exact headingPath) for what the catalog already says. Whenever something is unclear or fails, use kb_search and kb_get first.

## Verdict per item (no "open" parking)

- `confirmed`: the code shows the claim as written.
- `partly`: some of it is right; say exactly which part is wrong.
- `wrong`: the code contradicts it.
- `already-documented`: the catalog already states it correctly (give file + heading).
- `cannot-verify`: only after a real trace; name the concrete blocker (missing repo, needs a running stack) and what you tried.

## Proposal per item

Where should the corrected fact go?
- `catalog/agent-docs/<file>.md` + heading: platform facts and user-side workarounds. Exact text to ADD (or the exact sentence to correct and its replacement). Add-or-correct only: never remove headings or correct text. Neutral wording: no webshop/project names, no session words, placeholders like `<app>`, `<Entity>`. Labels as sub-headings, never a bold-only line. Follow the target file's style.
- `reports/judo-ng-issues/CLI.md`: a CLI defect for the CLI developers, in that file's issue format (title, Reproduction, Behaviour, Expected, Workaround, evidence).
- `reports/judo-ng-issues/FRAMEWORK.md`: a generator/runtime/judo.sh defect, same style.
- `kb`: a defect of the kb tool (evidence from `/Users/bmiller/Projects/Pi-Packages/pi-agent-dashboard/packages/kb*/src`).
- `none`: with the reason.
An item can need two targets (a defect report plus the workaround in agent-docs).

## Output

One JSON line per item to `target/apply-r20/verdicts-<your group>.jsonl`:
`{"id":..,"verdict":..,"evidence":["wt/...:line@sha" or "cmd -> exit N: output"],"correct":"<the verified statement>","targets":[{"file":..,"heading":..,"replaces":"<exact current sentence or empty>","text":"<exact text>"}],"note":".."}`

No edits outside `target/apply-r20/`, no git writes, never edit judo-ng or the webshop. Final answer: counts per verdict, 3 lines.
