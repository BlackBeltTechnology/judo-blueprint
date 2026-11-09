# Review decisions

Generated 2026-11-06 16:07 from `review-state.json`.

## Missing knowledge (`openspec/changes/restructure-blueprints-for-kb/knowledge-gaps-report.md`)

### 1. Summary
- **accept** · 324 validated gaps in 72 topics.
- **accept** · The biggest holes are platform runtime behaviour that developers had to dig for:
- **accept** · The model languages have no reference.
- **accept** · Model changes break the frontend in ways nobody documented.
- **accept** · Configuration that every production app needs is absent:
- **accept** · Testing knowledge is thin.
- **accept** · Domain knowledge:
- **accept** · agent-docs
- **accept** · best-practices
- **accept** · model-blueprints
- **accept** · cli
- **accept** · High:
- **accept** · Medium:
- **accept** · Low:

### Scope decisions needed
Topic decision: **accept**
- **accept** · JSL (textual model language);
- **accept** · Spring Boot runtime;
- **accept** · Flutter frontend.

### How to read an item
Topic decision: **accept**
- **accept** · the priority and its evidence;
- **accept** · where the knowledge should go;
- **accept** · what the catalog has today, when there is a partial mention;
- **accept** · the facts to add.

### Method
Topic decision: **accept**
- **accept** · Mining.
- **accept** · Validation.
- **accept** · Grouping.

### Limits
Topic decision: **accept**
- **accept** · Session counts come from the miners and may overcount.
- **accept** · The session corpus is two developers on one project.
- **accept** · The fact text is the miner's wording; only the sampled claims were checked against source line by line.
- **accept** · Confirm each topic against source when you write the entry, as the catalog's own validation rule requires.

### judo-model-cli usage the catalog must teach or link
- **accept** · CLI GraphQL query language and schema inspection (`P13-06`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · CLI Mermaid diagram generation from models (`P13-07`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · CLI server session and unsaved-changes persistence (`P13-08`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · JUDO Model CLI command set and syntax (`P13-01`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · JUDO Model CLI query/mutation syntax gotchas (where vs filter, -w dot-operator, containment+target, dirty-state) (`S12-02`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Model-change workflow: manual ESM XML edits, EVL validation only on build, judo-cli discard reverts ALL in-memory changes (`S03-05`)
  - Note: Accept: keep 'EVL validation runs on build' in catalog; drop the outdated manual-XML-edit framing; discard-reverts-all goes upstream to judo-cli skill.
- **accept** · Never hand-parse .model XMI files; query the model through judo-model-cli (`S17-06`)
  - Note: Accept: best practice for agent-docs/model — query the model through the CLI, never hand-parse .model XMI.
- **accept** · judo-model-cli / ESM version pins, jar redeploy, and reading upstream docs at the pinned commit (`S22-02`)
  - Note: Accept: CLI/ESM version pins in root pom; read upstream docs at pinned commit (matches proposal pin/download rule).
- **accept** · judo_cli cannot create reference-derived UI elements or disambiguate duplicate FQNs (`S11-02`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · judo_cli invocation pitfalls (non-interactive alias, stale jar, wrong model in skill) (`S01-08`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · judo_cli location, invocation and stale --version reporting (`S11-03`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · judo-cli UI mutation gotchas: TabularReferenceFieldCreateInput has no name field (`S13-05`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Derived-model generation and reload via CLI transform/discard (`P13-03`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Adding a UI field/form member via judo-model-cli mutation (`S10-01`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Reference-derived UI elements have no writable name on CreateInput (`S11-01`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Renaming a JUDO model attribute via judo-cli preserves xmiId and yields an incremental renameColumn (not delete+create) (`S25-01`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Model CLI cannot add a column to a card table (switch to table, edit, switch back) (`S22-03`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Three-way ESM model merge and conflict resolution (`P13-02`)
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Tatami Maven workflow plugin configuration (default-model-workflow goal and parameters) (`P22-04`)
  - Note: Accept: Tatami default-model-workflow plugin config — misfiled under CLI, put in agent-docs/deployment.
- **defer** · Eclipse m2e launcher configurations and IDE run workflow (`P28-07`)
  - Note: IDE (Eclipse) tooling, not CLI; revisit later.
- **reject** · JSL editor / IDE tooling (VS Code extension and TextMate bundle) (`P34-03`)
  - Note: JSL is out of scope (scope decision).
- **accept** · Model validation gate (validateModels and ESM/UI validation rules) (`P23-04`)
  - Note: Accept: validateModels gate is Maven build config — agent-docs/model, not CLI skill.

### 6. Excluded candidates
Topic decision: **accept**
- **accept** · 6. Excluded candidates

### Already covered (findability, not missing)
Topic decision: **accept**
- **accept** · P33-06
- **accept** · P12-09
- **accept** · S01-03
- **accept** · S26-02
- **accept** · S05-04
- **accept** · S13-07
- **accept** · P24-06
- **accept** · P31-05
- **accept** · P14-01
- **accept** · P16-06
- **accept** · P01-05
- **accept** · P14-06
- **accept** · P05-07
- **accept** · P21-03
- **accept** · S02-01
- **accept** · S09-05

### Not needed by application developers
- **accept** · Not needed by application developers

### Not verifiable
- **accept** · P24-01 Link columns/actions on a row table are never generated:

## Catalog updates (`openspec/changes/restructure-blueprints-for-kb/catalog-update-report.md`)

### 1. Summary
- **accept** · agent-docs have confirmed wrong API facts, and they spread.
- **accept** · Model blueprints still carry the old generation format.
- **accept** · Best practices and blueprints present project code as platform API.
- **accept** · Real developers struggle with UI and model decisions and with reading the model, more than with CLI syntax.
  - Note: Clear CLI usage update: read the model with query/status --json/mermaid via the pinned CLI; footguns go upstream to judo-cli skill.
- **accept** · The CLI has changed under the docs.
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · Validated reading works, and its results show where the catalog needs a validation step.

### 2. Evidence base
- **accept** · judo-ng full read
- **accept** · Validator results
- **accept** · agent-docs pass 1
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Catalog cross-check
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Developer sessions
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · New CLI
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · doc conflict
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · suspected bug
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · DOX disagreement
  - Note: Process record (how the exploration ran / what it found): accepted as documented.

### 3. agent-docs: what to update
- **accept** · (a) Pass-1 findings:
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · (b) Full-read findings:
  - Note: Process record (how the exploration ran / what it found): accepted as documented.

### 3.3 Model (MO-001…008)
- **accept** · model/judo-cli.md:
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.

### 3.6 Coverage gap
- **accept** · Pass 1 checked 38 of 70 docs.
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Proposal:
  - Note: Process record (how the exploration ran / what it found): accepted as documented.

### 6. What real development sessions add
- **accept** · Model reads dominate
  - Note: Clear CLI usage update: read the model with query/status --json/mermaid via the pinned CLI; footguns go upstream to judo-cli skill.
- **accept** · Parsing GraphQL JSON breaks
  - Note: Clear CLI usage update: read the model with query/status --json/mermaid via the pinned CLI; footguns go upstream to judo-cli skill. Scripts must check exit code before parsing --json (finding 0028).
- **accept** · CLI resolution failures
  - Note: Clear CLI invocation update: one resolution order ($JUDO_CLI_JAR, then target/), reuse task 2.3 script contract.
- **accept** · Most-read docs
  - Note: Process record (how the exploration ran / what it found): accepted as documented.

### 7. Models: what generated the catalog, and what to use now
- **accept** · Original catalog
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Developer sessions
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · agent-docs pass 1
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · judo-ng full read
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Rejected
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · A cheap reader plus a validation of every flagged item is enough.
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Single-reader "suspected bugs" are the least reliable output (133 of 186 wrong verdicts) and need validation before any 
  - Note: Process record (how the exploration ran / what it found): accepted as documented.
- **accept** · Known false positives belong in the reader prompt up front:
  - Note: Process record (how the exploration ran / what it found): accepted as documented.

### 8. Effect on the open tasks of `restructure-blueprints-for-kb`
- **accept** · 1.1 Pin the CLI
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.
- **accept** · 1.2–1.5
  - Note: Next-step / task-plan item: accepted.
- **accept** · 2.1–2.9
  - Note: Next-step / task-plan item: accepted.
- **accept** · 3.1–3.2 Import
  - Note: Next-step / task-plan item: accepted.
- **accept** · 3.3 kb-ify
  - Note: Next-step / task-plan item: accepted.
- **accept** · 3.4 judo-ng explorer pass
  - Note: Next-step / task-plan item: accepted.
- **accept** · 3.5 Operator review
  - Note: Next-step / task-plan item: accepted.
- **accept** · 4.1 entry-lint
  - Note: Next-step / task-plan item: accepted.
- **accept** · 4.4 Pass A
  - Note: Next-step / task-plan item: accepted.
- **accept** · 5.1–5.5 Fragments
  - Note: Next-step / task-plan item: accepted.
- **accept** · 6.1–6.3 Pass B
  - Note: Next-step / task-plan item: accepted.
- **accept** · 7.1–7.4 Sweep
  - Note: Clear CLI usage update: read the model with query/status --json/mermaid via the pinned CLI; footguns go upstream to judo-cli skill. Use query esm --select --where for sweep inspection.
- **accept** · 8.1–8.3 Distillation
  - Note: Clear CLI usage update: read the model with query/status --json/mermaid via the pinned CLI; footguns go upstream to judo-cli skill.
- **accept** · 9.1 kb eval
  - Note: Next-step / task-plan item: accepted.
- **accept** · 9.4 Consumer switch
  - Note: Clear CLI syntax/usage update: owned by the CLI judo-cli skill (pinned 9f6a4bd); catalog links, no copied syntax.

### Proposed new tasks
Topic decision: **accept**
- **accept** · 3.4b Generate review.md v2 from the full read:
- **accept** · 3.6 Propagation sweep:
  - Note: Next-step / task-plan item: accepted.
- **accept** · 4.1b entry-lint vocabulary check, using the judo-ng identifier vocabulary built at the pinned SHAs and stored outside th
  - Note: Next-step / task-plan item: accepted.

### 9. Recommended order
Topic decision: **accept**
- **accept** · 9. Recommended order

### 10. Open questions for the operator
Topic decision: **accept**
- **accept** · Which template state is the agent-docs import base:
  - Note: Import base = feature/JNG-6349_AddZetaValidatiob@6273a87 (not 5bddd8b^). Resolve the 58 conflicts found there during import. Follow-up: proposal.md, design.md (line 153) and tasks.md 3.2 still name 5bddd8b^ and must be updated.
- **accept** · Should validated platform bugs (section 3.1) appear in agent-docs as "known issues", or go only to judo-ng issue trackin
  - Note: Both: short known-issue note in agent-docs that links the judo-ng issue.
- **accept** · Is the mercury-3 reader + validator setup acceptable for the sweep (task 7), or should validation stay on Opus?
  - Note: Yes for mercury-3 reader+validator, but suspected-bug verdicts stay validated on Opus (133/186 wrong verdicts came from them).

