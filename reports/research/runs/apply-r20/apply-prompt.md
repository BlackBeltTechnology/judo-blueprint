# Apply the verified R20 findings

Work in `/Users/bmiller/Projects/judo-blueprint`. Verdicts with evidence and proposed text: `target/apply-r20/verdicts-*.jsonl` (20 items). Apply every target except `kb` and `none`.

## Before writing each item

Re-open its evidence (judo-ng `target/judo-ng-read/wt/...` file:line, or rerun the CLI command with `java -jar target/judo-cli.jar` on a copy in `target/apply-r20/scratch-apply/`). Write only what the evidence shows. When a proposal says *Verify* and another item's evidence settles it, use that evidence and drop *Verify*.

## Merge rules

- **R20-C1 + R20-F6:** one new CLI.md issue (next free number after the last `## N.`), not two. It covers: `create`/`update -s operationType=INITIALIZER` stores `initializer=false`; on an unmapped transfer object `validate` exits 1; on an entity it validates but generates `accept(<Entity> _this)` and is no initializer; working form `operationType=STATIC` + `initializer=true` (generates `void run()` on an entity as well). The same facts, consistent, in `judo-cli.md` (gotchas), `esm_metamodel/operation.md` (INITIALIZER Special Handling) and `best-practices/model/initializer-operation.md` (R20-4).
- **R20-F3 + R20-8:** one sub-heading in `build-process.md`, one addition to FRAMEWORK.md #2. The trigger is one actor with two accesses to the same transfer object whose view has a tabular reference field; the build and `validate` still pass.
- **R20-2 + R20-F1:** `schema-evolution.md` names where the `epsilon-runtime` feature goes (a karaf-features `extra-bundles` fragment override); FRAMEWORK.md #7 gets the corrected workaround (its "Workaround: none" is outdated).
- **R20-C4:** add the exit-0-on-GraphQL-error note to CLI.md #20 only if the rerun shows exit 0.
- **R20-F5:** write only what the code shows (`generate` deletes stale files listed in `.generated-files`); no framework issue.

## Writing rules

- agent-docs and best practices are add-or-correct only: never rename, reorder or remove headings, never shorten correct text. A `replaces` sentence is corrected in place.
- Platform facts only: no webshop or project names, no session words; placeholders `<Model>`, `<Actor>`, `<Entity>`, `<app>`.
- Labels are sub-headings, never a bold-only line. Match the target file's style.
- In CLI.md and FRAMEWORK.md follow the existing issue format and also update their Summary table if they have one.
- If a changed agent-doc has a `.agent.md` companion, add the new facts to the matching section of the companion too.

## Ledger

One line per target to `target/apply-r20/ledger.jsonl`: `{"id":..,"file":..,"heading":..,"status":"applied|merged-into:<id>|skipped","note":".."}`.

No git writes, no `check-all`. Final answer: counts per status, 3 lines.
