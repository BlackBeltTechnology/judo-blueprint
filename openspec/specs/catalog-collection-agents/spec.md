# catalog-collection-agents Specification

## Purpose
Provides reusable pi skills, each with scripts it calls, to consume, diagram, author, distill and maintain the catalog. They replace all Claude Code commands, agents and scripts, and are installable by any JUDO project at the catalog's release tag.

## Requirements

### Requirement: Repository is a pi package
The repository SHALL be a pi package whose manifest exports exactly the reusable skills: `judo-blueprint`, `judo-model-mermaid`, `judo-blueprint-author`, `judo-session-distill`. The internal skill `judo-catalog-maintain` SHALL be project-local and SHALL NOT be exported.

#### Scenario: Install in a consumer
- **WHEN** a JUDO project runs `pi install git:github.com/BlackBeltTechnology/judo-blueprint@<tag>`
- **THEN** pi lists the four exported skills, and not `judo-catalog-maintain`

### Requirement: Skills plus sweep subagents
Catalog workflows SHALL be delivered as pi skills. The sweep's judgement steps SHALL be subagents defined in `.pi/agents/judo-sweep-*.md` and dispatched from the operator's session. The repository SHALL contain no slash-command files, no prompt templates, no flows and no other agent definitions. Deterministic steps SHALL be skill scripts, which the subagents and the session call rather than reimplement.

#### Scenario: Clean tree
- **WHEN** CI lists `.claude/`, `.pi/prompts/`, `.pi/agents/` and `.pi/flows/`
- **THEN** only `.pi/agents/judo-sweep-*.md` exist, and there is no `.pi/flows/` and no `.claude/`

### Requirement: Use the CLI, link its docs
The skills SHALL use only the pinned JUDO CLI jar. For command documentation they SHALL link to the CLI's `--help`/`--schema` output and the CLI repository's `judo-cli` docs, and SHALL NOT copy them into this repository.

#### Scenario: No copied CLI docs
- **WHEN** CI searches this repository for a copy of the CLI command reference
- **THEN** none is found, and skill references link to the CLI skill instead

### Requirement: Fragments built only through the CLI
Fragments SHALL be created and changed only through CLI commands and `save`, never by editing the model file by hand.

#### Scenario: Fragment written by the CLI
- **WHEN** an author changes a fragment
- **THEN** the change comes from CLI commands followed by `save`, and the PR shows the `save` change summary

### Requirement: One job per skill
Each skill's `SKILL.md` description SHALL name one job and when to use it. Skills compose by calling each other's scripts through documented relative paths, never by copying them.

#### Scenario: Author renders through the Mermaid skill
- **WHEN** `judo-blueprint-author` finishes an entry with a fragment
- **THEN** it calls the `judo-model-mermaid` render script, and no second render implementation exists in the repository

### Requirement: Scripts usable standalone and by CI
Every bundled script SHALL:
- run from any working directory;
- print usage on `--help`;
- produce machine-readable output with `--json`;
- exit non-zero on failure.

CI SHALL call these same scripts for gates, Sandbox checks and versioning.

#### Scenario: CI uses skill scripts
- **WHEN** the gates job runs
- **THEN** it invokes `judo-catalog-maintain/scripts/check-all`, which calls the exported skills' scripts

#### Scenario: Help
- **WHEN** any bundled script runs with `--help`
- **THEN** it prints usage and exits 0

### Requirement: Diagram a project's own model
`judo-model-mermaid` SHALL also render Mermaid for a scope of the caller's own JUDO model, not only for fragments.

#### Scenario: Consumer diagram
- **WHEN** a rackinspect session asks for a diagram of `rackinspect::entities::Fault` with depth 1
- **THEN** the skill renders it with the CLI and leaves the project model unmodified

### Requirement: Model overview before analysis
For each source project, the sweep SHALL first print the whole source model with the JUDO CLI in read-only mode: one Mermaid diagram per aggregate without members, one with typed members, one access view of transfer objects and actors, and element counts. The overview SHALL be read before any drill-down. It SHALL be written only to a gitignored work folder. The PR and `PROJECTS.md` SHALL carry only the counts and a candidate list in neutral names, with the entry each candidate maps to or `new`.

#### Scenario: Overview first
- **WHEN** the sweep starts on `rackinspect@<sha>`
- **THEN** it writes `shape.md`, `domain.md`, `access.md`, `counts.txt` and `custom.md` under `target/sweep/rackinspect/<sha>/` before reading any backend, frontend or spec file

#### Scenario: Overview never committed
- **WHEN** the sweep PR is opened
- **THEN** no overview file is tracked, and the redaction check passes on the PR body and the `PROJECTS.md` diff

#### Scenario: Every candidate accounted for
- **WHEN** the overview yields 14 candidates
- **THEN** the PR body lists all 14, each with its target entry or `new`

#### Scenario: Source model unchanged
- **WHEN** the overview has been printed
- **THEN** the CLI reports the source model as clean

### Requirement: Custom code inventory before analysis
The sweep SHALL write a custom-code inventory (custom frontend, interceptors, custom backend operation code) to the same gitignored work folder, found by JUDO conventions. Each item SHALL be mapped to its target model element or listed as unmapped. Candidates SHALL combine a model shape with the custom code it relies on. Sweeps SHALL update only blueprints and best practices.

#### Scenario: Inventory coverage
- **WHEN** the inventory is written for a JUDO project
- **THEN** it covers frontend hook and custom-implementation registrations, custom components, generator overrides, `OperationCallInterceptor` implementations and abstractions on them, and custom operation code

#### Scenario: Generated code is never counted as custom
- **WHEN** a fresh clone is inventoried
- **THEN** only tracked files are considered, generated-and-tracked files (schema migrations, committed `.default` files) are listed separately, and a file keeping the generator header but differing from its `.default` counts as custom

#### Scenario: Fast mode needs no build
- **WHEN** `custom-overview` runs without `--generate`
- **THEN** it finishes without running Maven, Node or the generator

#### Scenario: Interceptor mapped to its operation
- **WHEN** a project has an `OperationCallInterceptor` that acts on a ticket position range operation
- **THEN** the inventory lists it under that operation and under the interceptor mechanism

#### Scenario: Frontend hook mapped to its page
- **WHEN** `application-customizer.tsx` registers a container actions hook for a generated form
- **THEN** the inventory lists it under the transfer object or page that the form renders

#### Scenario: Recurring customization becomes a best-practice candidate
- **WHEN** the same customization mechanism is used the same way on several unrelated elements
- **THEN** the sweep lists it as a frontend or backend best-practice candidate

### Requirement: Sweep per project with subagents
A project sweep SHALL:
- create a detached, read-only source worktree and a blueprint branch worktree;
- run the overview scripts;
- dispatch the model, backend, frontend and schema explorer subagents in parallel, each searching the catalog with the kb CLI;
- merge candidates with a script and cross-validate them with a subagent;
- author only in the blueprint worktree;
- gate with at most three fix rounds;
- push and open the PR only after operator confirmation.

#### Scenario: Read-only explorers
- **WHEN** the explorer subagents run
- **THEN** none of them has write or edit tools, and the source worktree is unchanged afterwards

#### Scenario: Catalog search per lane
- **WHEN** an explorer finds a candidate
- **THEN** its lane file names the catalog entry matched by kb search, or `new`, with evidence paths

#### Scenario: Operator checkpoint
- **WHEN** cross-validation has written `decisions.json`
- **THEN** no author subagent is dispatched until the operator approves the decisions

#### Scenario: Re-run one lane
- **WHEN** the operator asks to re-run only the frontend lane
- **THEN** only `lanes/frontend.json` is rewritten, and the merge is redone from all four lane files

#### Scenario: Gate rounds bounded
- **WHEN** the gates fail three times
- **THEN** the sweep stops with the gate report and nothing is pushed

### Requirement: Cross-project overlap report
`sweep-overlap` SHALL report entries touched by more than one project sweep, and `new` candidates that match across projects. It SHALL NOT merge anything.

#### Scenario: Overlap reported
- **WHEN** the rackinspect and mlszksz-platform sweeps both add evidence to `audit-log-entity`
- **THEN** the report lists that entry with both sweep branches

### Requirement: Project registry and sweep
`PROJECTS.md` SHALL list each source project with its URL, kind, weight, branch and last swept SHA. The sweep SHALL:
- analyse each distinct remote repository once, at a pinned SHA of its branch, ignoring local worktrees;
- resume from the first incomplete project;
- record evidence for every entry it writes;
- update the swept SHA only after the batch merges.

#### Scenario: Unreachable recorded SHA
- **WHEN** a recorded SHA no longer exists on the remote
- **THEN** the sweep runs a full re-sweep and reports why

#### Scenario: Resume
- **WHEN** a sweep fails on `mlszksz-platform` after `rackinspect` completed
- **THEN** a re-run skips `rackinspect`

### Requirement: Output conforms before review
Every entry a skill writes SHALL pass entry lint, redaction and the Sandbox check before it is offered for review.

#### Scenario: Entry without fragment
- **WHEN** an authored model-shaped entry lacks a passing fragment
- **THEN** it is not offered for merge
