---
title: JUDO Model CLI
description: The JUDO Model CLI: mandatory rules, command reference, merge of parallel model copies, mermaid diagrams, session state and known pitfalls.
---

# JUDO Model CLI

The `judo-cli.jar` is the JUDO platform's command-line interface to the model. Every read of and change to the ESM **must** go through this tool — never by editing the model files directly.

## Identity

| | |
|---|---|
| **Artifact** | `judo-cli.jar` |
| **Location** | `target/judo-cli.jar` (downloaded by `./judo.sh build`; Maven coordinate `hu.blackbelt.judo.runtime:judo-model-cli:${judo-model-cli-version}`) |
| **Invocation** | `java -jar target/judo-cli.jar -m model/<app>.model <command>` (a `judo_cli` shell alias is not available in non-interactive shells) |
| **Source ESM** | `model/<app>.model` |
| **Interface** | GraphQL over the ESM (and over the derived models, when loaded) |

## Why a CLI is mandatory

The ESM is stored as a single XMI file (`model/<app>.model`). Three properties of that file make it unsafe to read or edit by hand:

- **Size.** A typical project's ESM contains tens of thousands of XMI elements. Reading the file is expensive in token budget and dangerous in attention — patterns spread across thousands of lines are easily missed.
- **Internal cross-references.** Elements reference each other by `xmi:id`. A single hand edit in one part of the file can silently dangle a reference somewhere else, with no immediate error.
- **Schema validation.** The metamodel imposes containment rules, type constraints, and structural invariants. The build will reject mutations that violate them — but only at build time, long after the bad edit was made.

For all three reasons, the CLI exists. It exposes the ESM as a GraphQL graph, validates every mutation against the metamodel before applying it, and runs the platform's transformation pipeline that lifts ESM into PSM, ASM, RDBMS and the other derived models.

## Capability surface

The tool groups its capabilities into a small set of concerns:

| Concern | What it does |
|---|---|
| **Querying & introspection** | Read elements (entity types, transfer objects, relations, operations, UI definitions). Walk relationships. Use schema introspection (`__type`, `__schema`) to discover available fields and types. |
| **Mutation** | Create, update, and delete ESM elements. Metamodel rules are enforced — invalid mutations fail fast, before they reach the build. |
| **Transformation** | Run the platform pipeline ESM → PSM → ASM → RDBMS → Liquibase (plus esm2ui), producing derived models in `application/model/target/cli-generated/`. See [transformation-pipeline.md](transformation-pipeline.md). |
| **State management** | Load, save, and discard model state. Track in-memory edits via the hidden `.<file-name>.dirty` side-item file (for example `.<app>.model.dirty`). |
| **Tracing** | Follow an element from its ESM origin through every derived model down to the runtime artifact (and back). |

## Mandatory rules

These rules are **platform invariants**, not preferences. Violating them produces incorrect or destructive results.

1. **Never read the `.model` XML file directly.** Always go through CLI queries. The XML is too large to safely read in attention, and any analysis that bypasses the GraphQL view is unverified.

2. **Never edit the `.model` XML file directly.** Even tiny hand edits can break `xmi:id` references in distant parts of the file. Always go through CLI mutations.

3. **Always paginate query results.** Use `limit`, `offset`, and `totalCount` together. Without explicit pagination, large result sets are silently truncated and the assistant operates on a partial view of the model.

4. **One writer per model file.** A model file is changed by exactly one CLI session at a time. Never point two agents, two terminals or a CLI and the Designer at the same `.model` file: each holds its own in-memory copy and the last `save` silently overwrites the other's edits.

5. **Parallel model work happens in separate worktrees, joined with `merge`.** Give every parallel task its own git worktree (or its own copy of the model file), all started from the same commit. Each task edits and saves only its own copy. Then, in the target worktree, run `merge <theirs.model> --base <base.model>` once per copy, where `<base.model>` is the file all copies started from (for example `git show <start-commit>:model/<app>.model > /tmp/base.model`). Without `--base`, elements both copies added are reported as add-add conflicts.
   - Use `merge --dry-run` first. It lists every conflict with a key and the fix commands (`--take <key>`, `--prefer mine|theirs`, or a follow-up `delete` / `update`).
   - After the merges: `validate --strict`, `save`, `status` (expect `state clean`, `unsaved changes none`), then commit.
   - `merge` never runs git. Committing and removing the worktrees stays with the caller. `<theirs.model>` must be the other copy's **saved** file; the merge is one unsaved editing step (`status` shows it, `save` writes it, `discard --force` drops it).
   - `--aird` also merges the Designer diagram files of the copies.

6. **Never `save` blindly.** Always run the transformation pipeline (`transform --load`) and verify the derived models query correctly **before** persisting an ESM mutation. A `save` without prior validation can leave the model in a state that the next build will reject.

7. **`transform` does not replace the client-side build.** It regenerates PSM, ASM, Measure, Expression, Script, Operation, RDBMS, Keycloak and Liquibase and also runs esm2ui (writing `<app>-ui.model`; `--skip esm2ui` omits it), all from the in-memory model. It does not generate the React frontend: after any UI-affecting ESM mutation (forms, tables, views, menu items, actor scaffolding), the client-side build (`./judo.sh build -f`) must run. See [transformation-pipeline.md](transformation-pipeline.md).

8. **`save` writes to disk; it does not commit.** A CLI `save` overwrites the on-disk `.model` file but does not make a git commit. Running `git restore` or `git checkout` on the model file at any later point silently destroys every uncommitted save. Either commit immediately after each `save`, or copy the model file to a backup before any git operation that could touch it.

## Command reference

Invoke every command as `java -jar target/judo-cli.jar -m model/<app>.model <command> [options]`. Elements are addressed by FQN (`<parentFqn>::<name>`, for a member `<ownerFqn>.<member>`), by `id:<xmi:id>` or by a unique short name; an ambiguous short name is rejected with the matching FQNs listed. Start-up is about 0.4 s because a per-model daemon holds the model in memory.

| Command | What it does |
|---|---|
| `query esm <Type> [--select ...] [--where k.op=v]` | Simple read syntax on esm/psm/asm/rdbms/ui. `--where`/`-w` uses dot-operators (`-w "name.contains=WorkReport"`); several filters are ANDed. |
| `graphql '<query>'` | GraphQL read/mutation surface. Filtering uses the argument `where` (not `filter`). `--schema` exports the schema, `--introspect` runs introspection. |
| `create -t <Type> --ns <parent> [-n name] [--set k=v] [--index n \| --before fqn \| --after fqn]` | Create any ESM element the way the Designer does (cascades such as the self-mapping of an `EntityType`, the view/form/table pages of a transfer object, the reverse member of a two-way relation). `--schema [field]` describes fields and valid values and changes nothing. |
| `update <fqn> --set/--unset/--add/--remove/--clear` | Change features; `--add feature` places a widget into a container. (`-f/--fqn` is deprecated.) |
| `delete <fqn> [--cascade]` | Delete an element. |
| `move <fqn> --index n \| --before/--after fqn` | Reorder inside the parent (`moveUp`/`moveDown` no longer exist). |
| `relocate <fqn> --to <parent>` | Change the parent while keeping the `xmi:id` and the inbound references. |
| `fill <toFqn> [--pages view,form,table]` | Create and populate a transfer object's view/form/table from its members. |
| `split <container> --layout VERTICAL\|HORIZONTAL` | Split a container into two groups (Designer "Split"). |
| `merge <theirs.model> --base <base.model>` | Three-way merge of a model copy, see "Merging parallel model copies" below. |
| `validate [--strict]` | ESM EVL, esm2ui/UI EVL and a transform dry run, all on the in-memory model. |
| `transform [--load] [--skip steps] [--validate]` | Run the transformation pipeline on the in-memory model, see [transformation-pipeline.md](transformation-pipeline.md). |
| `status [--json]` | State (`clean`/`dirty`), unsaved changes and their intent. |
| `save` / `discard [--force] [--derived]` | Persist or drop the unsaved edits. `save` never runs git. |
| `mermaid model` / `mermaid from` | Draw the model as Mermaid class diagrams, see below. |
| `server status` / `server stop [-f]` | Manage the per-model daemon. |

`merge` matches elements by `xmi:id` and reports conflicts of kind `change-change`, `delete-change`, `change-delete`, `add-add` and `validation`, each with a key; resolve with `--take <key>`, `--prefer mine|theirs` or the printed fix commands. `--aird` also three-way merges the Designer `.aird` files.

Common mutation flags: `--dry-run` (create, report, undo), `--json`, `--brief` (only the FQN), `--no-check` (skip per-edit checks during bulk edits; run `validate` at the end), `--ns <fqn>` (parent namespace). `--set a,b` sets a list, `""` sets an empty string, `null` is rejected; `-s`/`--vars` values are kept verbatim (newlines, quotes and backslashes reach the model unchanged). Exit codes are 0 (ok), 1 (error) and 2 (rejected); `merge` also uses 4 for open conflicts.

Read the model with `query esm ... --select --where`, `status --json` and `mermaid` rather than parsing the JSON of `graphql` output in scripts: the most frequent CLI failure is a script that crashes on a `null` in the graphql result.

### Mermaid diagrams of the model

`mermaid model [--scope <fqn>] [--depth n] [--split aggregate|package|none] [--kinds entity,enum,transfer,actor,operation] [--members types|names|none] [--md]` draws the **in-memory** model, including unsaved edits, as Mermaid `classDiagram`s. `mermaid from <file|->` converts saved `query`/`graphql` JSON into a diagram without a running daemon; `query esm <Type> --mermaid` and `graphql '<q>' --mermaid` draw a query result. Arrows: composition `*--`, aggregation `o--`, association `-->`, generalization `<|--`, mappings `..>` labelled `maps`; multiplicities are shown. Only class diagrams are produced. A diagram that exceeds the renderer limits produces a warning: narrow it with `--scope`, `--split aggregate` or `--members none`. This replaces a hand-written script such as the project's `diagram_generator.py`.

### Tracing an element through the pipeline

The GraphQL `trace` queries (`trace.forward`, `trace.backward`) follow an element through the transformation chain (ESM → PSM → ASM → RDBMS, and ESM → UI) by parsing the composite `xmi:id` strings described in [xmi-id-traceability.md](xmi-id-traceability.md); the result is a chain of hops with `modelType` and `xmiId`.

### Session, daemon and unsaved edits

The CLI runs one daemon per model. Its session lives under `~/.judo/sessions/<hash>/` (`session.json`, `daemon.log`). Unsaved edits are held in memory and mirrored about every 500 ms into the hidden overlay `.<file-name>.dirty` next to the model (plus `.base`/`.intent` sidecars); an external change of the model file reloads the model and discards them. ESM is loaded at daemon start, PSM/ASM/RDBMS/UI are loaded on the first query. `server status` and `server stop -f` manage the daemon. If `status` stays dirty after `save`/`discard`, run `discard --force`; as a last resort stop the server and delete the overlay file by hand.

### Version and jar pitfalls

- `--version` reports a stale `1.0.0` from a baked manifest; read the real version from the Maven properties `judo-model-cli-version` and `judo-meta-esm-version` in the root `pom.xml`.
- The jar is only downloaded when it is **missing**. After bumping the version properties, delete the old jar and run `./mvnw -f application/model/pom.xml -N validate`, otherwise the stale CLI keeps running.
- The pinned jar may be newer than a local checkout of the CLI source; read its documentation at the pinned commit (`git show <sha>:docs/commands/<cmd>.md`).
- Mutations stay in memory until an explicit `save`.

### Known limitations and gotchas

- **Reference-derived UI elements have no `name` in their `CreateInput`.** `DataField`, `DataColumn`, `DataFilter`, `ReferenceField`/`TabularReferenceField`, `OperationForm` and the `Inherited*` references take their name and FQN from the binding (`dataFeature`, `relationFeature`, `operation`); passing `name` fails with `contains a field not in <Kind>CreateInput: name`. Place them with `update <container> --add feature ...` (or `create -t ... --set dataFeature=...`); a "no name field" error can really be an ambiguous FQN. `RowOperation` has no create type; if the CLI cannot express a UI change, edit that one XMI element by hand and verify with `validate` (see [model-development.md](model-development.md)).
- **Duplicate FQNs.** `update` acts on the first element with a given FQN and there is no suffix to select the other; give the elements distinct names first.
- **Operation parameters** are declared with `containment` + `target`, not type/direction.
- **A failed script leaves its earlier edits in memory** (and in the overlay), so running it again duplicates elements: `discard --force` before retrying. `discard` reverts **all** unsaved edits, not only the last one.
- **EVL checks that need a build.** Some checks (for example that a `MAPPED` member's `required` matches its binding) are only reliably exercised by the full build; after a build, re-run `validate` and check that the generated artifacts (ASM/SDK timestamps) contain the change before ticking a task as verified.
- **Rename keeps identity.** `update <fqn> --set name=...` on a data member keeps its `xmi:id`, so the incremental Liquibase diff produces a `renameColumn` and the column data survives instead of a drop and create. `discard --force` any exploratory rename.
- **`git checkout -- model/<app>.model` reverts every structural change**, not only UI changes (see rule 8).
- **Merge output** may print `[WARN] Zeta transformation not yet implemented, falling back to ETL`; it is harmless.
- **Signed identifiers cannot be minted with the CLI**; the runtime only mints them while serving a REST response, see [Bound operations](../backend/README.md).

## Querying and UI FQNs

`query <model> <Type>` builds GraphQL with `--select`, `--where`, `--limit`, `--offset`. Operators: `eq`, `contains`, `startsWith`, `endsWith`, `regex`, their case-insensitive forms (`icontains`, `istartsWith`, `iendsWith`, `iregex`), and `gt`, `gte`, `lt`, `lte`. Collection fields are pluralised and nested reference filters are AND-combined. `graphql` takes `--variables` and `-o`; `--schema` writes the SDL to `.judo-schema.graphql`.

For model type `ui`, FQNs are non-uniform: an Application is its simple name, a Theme is `<App>::Theme`, a Frame is `<containerFQN>::Frame`, a MimeType is `type/subType`, other named elements use `::` hierarchy, unnamed elements fall back to the XMI URI fragment.

## Reach for the CLI when…

- You need to know what is currently in the model (entities, attributes, relations, actors, UI definitions).
- You need to add, modify, or remove any model element.
- You need to verify that a model change actually transformed correctly.
- You need to trace where a runtime artifact (REST endpoint, database table, UI form) originates in the ESM.

## Do not reach for the CLI for…

- Reading or modifying the application's Java source code (use the file system).
- Reading or modifying the React frontend's custom hooks, overrides, or theme files (use the file system).
- Building the project (use `./judo.sh build`).

The CLI's authority is the model. Code, build, and runtime concerns live elsewhere.

## See also

- [Transformation Pipeline](transformation-pipeline.md) — what `transform` produces, and the boundary between server-side and client-side regeneration.
- [Model Development](model-development.md) — modeling workflow, naming conventions, JQL.
- [UI Authoring Guide](ui-authoring-guide.md) — what to put in the model when authoring UI.
- [XMI ID Traceability](xmi-id-traceability.md) — how the platform tracks an element through the pipeline.
