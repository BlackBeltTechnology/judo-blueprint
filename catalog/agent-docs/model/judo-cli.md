---
title: JUDO Model CLI
description: The JUDO Model CLI: mandatory rules, command reference, merge of parallel model copies, mermaid diagrams, session state and known pitfalls.
aliases: [model cli, judo cli commands, change model without editing xml, merge model copies, mermaid model diagram, model daemon session, discard unsaved model edits]
keywords: [judo-cli.jar, query, graphql, create, update, merge, validate, transform, save, discard, mermaid, trace.forward, judo-model-cli-version, dry-run, --base]
tags: [domain:model, layer:model, status:platform]
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

3. **Always paginate query results.** Use `limit`, `offset`, and `totalCount` together. `query` and `graphql` apply `limit` only when it is given, so without it every match is returned and nothing is truncated by the CLI. Helper scripts that pass a fixed `--limit` (for example `--limit 800`) do truncate silently, so check `totalCount` against the number of items returned.

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
| `validate [--strict]` | ESM EVL, esm2ui/UI EVL and a transform dry run, all on the in-memory model. `--strict` is deprecated (since `1.1.0.20261119_155735_a64aa981_develop` it prints a deprecation warning): validation errors always exit non-zero. See [Validation engine](#validation-engine). |
| `transform [--load] [--skip steps] [--validate]` | Run the transformation pipeline on the in-memory model, see [transformation-pipeline.md](transformation-pipeline.md). |
| `status [--json]` | State (`clean`/`dirty`), unsaved changes and their intent. |
| `save` / `discard [--force] [--derived]` | Persist or drop the unsaved edits. `save` never runs git; it writes a temp file and atomically moves it over the model file. |
| `mermaid model` / `mermaid from` | Draw the model as Mermaid class diagrams, see below. |
| `server status` / `server stop [-f]` | Manage the per-model daemon. |

`merge` matches elements by `xmi:id` and reports conflicts of kind `change-change`, `delete-change`, `change-delete`, `add-add` and `validation`, each with a key; resolve with `--take <key>`, `--prefer mine|theirs` or the printed fix commands. `--aird` also three-way merges the Designer `.aird` files.

Common mutation flags: `--dry-run` (create, report, undo), `--json`, `--brief` (only the FQN), `--no-check` (skip per-edit checks during bulk edits; run `validate` at the end), `--ns <fqn>` (parent namespace). `--set a,b` sets a list, `""` sets an empty string, `null` is rejected; `-s`/`--vars` values are kept verbatim (newlines, quotes and backslashes reach the model unchanged). Exit codes are 0 (ok), 1 (error) and 2 (rejected); `merge` also uses 4 for open conflicts.

Read the model with `query esm ... --select --where`, `status --json` and `mermaid` rather than parsing the JSON of `graphql` output in scripts: the most frequent CLI failure is a script that crashes on a `null` in the graphql result.

### Validation engine

Since CLI `1.1.0.20261119_155735_a64aa981_develop`, `validate` and `transform` run the ESM to UI step through the build's `Esm2UiWork`, with the engine chosen by the `judo.transformation.mode` system property (`ZETA` or `ETL`; Zeta when unset, as in the ESM Maven workflow), so the UI check gives the Maven build's verdict. To validate with ETL, start the daemon with `-Djudo.transformation.mode=ETL`. Older versions ran their own UI check and could pass a model that the Maven UI validation rejects.

### Mermaid diagrams of the model

`mermaid model [--scope <fqn>] [--depth n] [--split aggregate|package|none] [--kinds entity,enum,transfer,actor,operation] [--members types|names|none] [--md]` draws the **in-memory** model, including unsaved edits, as Mermaid `classDiagram`s. `mermaid from <file|->` converts saved `query`/`graphql` JSON into a diagram without a running daemon; `query esm <Type> --mermaid` and `graphql '<q>' --mermaid` draw a query result. Arrows: composition `*--`, aggregation `o--`, association `-->`, generalization `<|--`, mappings `..>` labelled `maps`; multiplicities are shown. Only class diagrams are produced. A diagram that exceeds the renderer limits produces a warning: narrow it with `--scope`, `--split aggregate` or `--members none`. This replaces a hand-written script such as the project's `diagram_generator.py`.

### Tracing an element through the pipeline

The GraphQL `trace` queries (`trace.forward`, `trace.backward`) follow an element through the transformation chain (ESM → PSM → ASM → RDBMS, and ESM → UI) by parsing the composite `xmi:id` strings described in [xmi-id-traceability.md](xmi-id-traceability.md); the result is a chain of hops with `modelType` and `xmiId`.

### Session, daemon and unsaved edits

The CLI runs one daemon per model. Its session lives under `~/.judo/sessions/<hash>/` (`session.json`, `daemon.log`). Unsaved edits are held in memory and mirrored about every 500 ms into the hidden overlay `.<file-name>.dirty` next to the model (plus `.base`/`.intent` sidecars); an external change of the model file reloads the model and discards them. ESM is loaded at daemon start, PSM/ASM/RDBMS/UI are loaded on the first query. `server status` and `server stop -f` manage the daemon. If `status` stays dirty after `save`/`discard`, run `discard --force`; as a last resort stop the server and delete the overlay file by hand.

### Version and jar pitfalls

- `--version` prints the CLI version (for example `judo-model-cli 1.1.0.20261119_155735_a64aa981_develop`); the pinned version is the Maven property `judo-model-cli-version` (and `judo-meta-esm-version`) in the root `pom.xml`.
- The jar is only downloaded when it is **missing**. After bumping the version properties, delete the old jar and run `./mvnw -f application/model/pom.xml -N validate`, otherwise the stale CLI keeps running.
- The pinned jar may be newer than a local checkout of the CLI source; read its documentation at the pinned commit (`git show <sha>:docs/commands/<cmd>.md`).
- Mutations stay in memory until an explicit `save`.
- A new project may not have `target/judo-cli.jar` yet, and it can be missing after `./judo.sh generate` or `build` (those run `mvnd clean`). Restore it with `./judo.sh generate-root` or `mvn -DgenerateRoot validate` in the project root (the root `pom.xml` downloads it in the `download-cli-for-generate-root` profile). Check that the file exists before a CLI call; a missing jar shows as `Unable to access jarfile`.

### Known limitations and gotchas

#### Creating, filling and changing elements

- **Reference-derived UI elements have no `name` in their `CreateInput`.** `DataField`, `DataColumn`, `DataFilter`, `ReferenceField`/`TabularReferenceField`, `OperationForm` and the `Inherited*` references take their name and FQN from the binding (`dataFeature`, `relationFeature`, `operation`); passing `name` fails with `contains a field not in <Kind>CreateInput: name`. Place them with `update <container> --add feature ...` (or `create -t ... --set dataFeature=...`); a "no name field" error can really be an ambiguous FQN. `RowOperation` has no create type; if the CLI cannot express a UI change, edit that one XMI element by hand and verify with `validate` (see [model-development.md](model-development.md)).
- **Do not hand-add members to a mapped transfer object.** `create -t TransferObjectType -s mapping=<entity>` already creates the mapped members and the view/form/table pages; since CLI `1.1.0.20261119_155735_a64aa981_develop`, creating a member with a name already used in the container is refused (`name '<n>' is already used in <container>`; also for rename and relocate); older versions create it and report `Named element ... is not unique in its container` and a mapped member without binding as `Mapped data member ... must have binding`.
- **`create -t MenuItemAccess` is refused** (`MenuItemAccess is created automatically`). `create -t Access --ns <actor> --set target=<transferObject>` creates the `Access` and a `MenuItemAccess` named `Menu`, labelled with the target type name; rename or reuse it instead of creating a second one. `delete` of an `Access` that a menu item references needs `--cascade`, which also removes the menu item. A new `Access` has `createable`, `updateable` and `deleteable` all `false`: set them explicitly (`--set createable=true`).
- **`fill` and columns.** `fill` adds a `DataColumn` and `DataField` for every member of the transfer object; run `fill <toFqn> --dry-run` first and delete unwanted columns afterwards. `fill` (or adding `DataColumn`s) clears the validation error `Columns are not defined for the viewable table of <TO>` (`ExposedTransferObjectTableHasColumns`). `DataColumn` and `DataFilter` do not exist before `fill` or an explicit `--add feature`, so `query esm DataColumn` returns nothing until then.
- **Access with list cardinality needs a table column.** `create -t Access --ns <Actor> --set target=<TO>` also creates `<TO>::<TO>_Table`. Until that table has a column, validation reports `Columns are not defined for the viewable table of <TO>` and the ESM model is invalid (`error esm Invalid model`, transform skipped). Add one: `create -t DataColumn --ns <TO>::<TO>_Table --set dataFeature=<TO>.<attribute>`, or run `fill <TO>`.
- **A type change must reach the mapped members.** Changing the `dataType` of an entity member leaves the mapped member of each transfer object on the old type; `validate` warns `Data type of data member ... must match the data type of its binding`. Update the mapped members too.
- **Gate `save` on `validate`.** `validate` exits non-zero when it reports a validation error (`--strict` is deprecated and not needed for the exit code); chain `validate && save` (not `;`), otherwise an invalid model is written to disk. Trust the exit code, not the summary line: in `1.1.0.20261119_155735_a64aa981_develop` the line `Validation complete: 0 errors` can follow printed UI errors (exit 1).
- **Duplicate FQNs.** Since CLI `1.1.0.20261119_155735_a64aa981_develop`, every write command refuses an FQN that matches several elements (an older model with duplicate names) and lists each element's `id:`; select one with `id:<xmi:id>`. Older versions act on the first element with that FQN; there, give the elements distinct names first.

#### Types, parameters, relation kinds and scripts

- **`MimeType`** has no `name` in its `CreateInput` either (the name derives from type and subType); `create -t MimeType -n ...` fails with `contains a field name ... not defined for input object type 'MimeTypeCreateInput'`. Working form: `create -t MimeType --ns <ns> -s type=application -s subType=json` (creates `application/json`). `BinaryType.mimeTypes` takes a comma-separated list (`-s mimeTypes=application/json,application/xml`) once each `MimeType` exists; a MIME type that does not exist yet fails with `'<type>' is not an allowed value`, so create the MIME types first.
- **Operation parameters** are declared with `containment` + `target`, not type/direction.
- **`managed` on an anonymous actor is refused.** `create -t ActorType ... -s anonymous=true -s managed=false` fails with `managed: does not apply to this ActorType (applies when not anonymous)`; leave `managed` out. The stored value then stays at its default (`true`), which has no effect for an anonymous actor without a principal (see [Anonymous vs Authenticated Behaviour](esm_metamodel/accesspoint.md)).
- **`relationKind` per layer.** On an entity relation `create -t OneWayRelationMember ... -s relationKind=AGGREGATION` is refused (`valid ASSOCIATION · COMPOSITION`). On a transient relation of an unmapped transfer object `AGGREGATION` is accepted (and is the required kind); `ASSOCIATION` is still created there and only `validate` reports `must be aggregation if transient`, so run `validate` before `save`.
- **A failed script leaves its earlier edits in memory** (and in the overlay), so running it again duplicates elements: `discard --force` before retrying. `discard` reverts **all** unsaved edits, not only the last one. Recipe: `save` before the script, run it, and on failure `discard --force`, fix the script and rerun; the saved file is the restore point (it also survives a daemon restart).
#### Validation, history and action placement

- **EVL checks that need a build.** Some checks (for example that a `MAPPED` member's `required` matches its binding) are only reliably exercised by the full build; after a build, re-run `validate` and check that the generated artifacts (ASM/SDK timestamps) contain the change before ticking a task as verified.
- **Rename keeps identity.** `update <fqn> --set name=...` on a data member keeps its `xmi:id`, so the incremental Liquibase diff produces a `renameColumn` and the column data survives instead of a drop and create. `discard --force` any exploratory rename.
- **`git checkout -- model/<app>.model` reverts every structural change**, not only UI changes (see rule 8).
- **Merge output** may print `[WARN] Zeta transformation not yet implemented, falling back to ETL`; it is harmless.
- **Signed identifiers cannot be minted with the CLI**; the runtime only mints them while serving a REST response, see [Bound operations](../backend/README.md).
- **`move` reports a changed element, not always the moved one.** Since CLI `1.1.0.20261119_155735_a64aa981_develop` the result names the moved element: `moved <fqn> index <from> -> <to>` (`--json`: `fromIndex`). In older versions the one-line result `changed <fqn> (in components)` names an element whose position changed, which can be the sibling that shifted. `move <fqn> --json` prints `reordered <fqn> in <list>` for the moved element, and `status` lists each unsaved move as `move <fqn> index=n` or `after=<fqn>`. Check the final order with a query (for example `graphql` on the container's `components`); `discard --force` drops a wrong reorder, together with all other unsaved edits.
- **`postCallAccessNavigation` cannot be cleared.** It is an attribute of the `OperationForm` (ui element) only. `update <operationForm> --unset postCallAccessNavigation` is refused (`cannot be cleared on OperationForm <name>`), `--clear` fails (`not a list`) and `--set postCallAccessNavigation=` is not an allowed value. Set it only when the target is final; to remove it, delete the `OperationForm` and place it again with `update <container> --add feature --feature <operation>`. The allowed values are the accesses whose target type matches the operation's output; `--set` lists them on error.
- **Place actions with `update <container> --add feature`.** The container must exist and be given by its exact FQN; `Container not found: <fqn>` means that FQN does not exist yet (create the `ActionGroup` first with `create -t ActionGroup --ns <viewFqn> -n <group>`). The operation must be a member of the container's transfer object: for a relation table (`<view>::<relation>`) it is an operation of the relation's target transfer object, otherwise the error is `'<op>' is not a feature of <TO> placeable here`, followed by the placeable features.
  - Table actions: `update <viewFqn>::<relation> --add feature --feature <operation> --as rowAction|tableAction|bulkAction`. This creates a `TableOperation` with a nested `OperationForm`.
  - A direct placement in an `ActionGroup`: `update <viewFqn>::<group> --add feature --feature <operation>` creates the `OperationForm` inside the group.
  - On a view, `--as action` is not a role (`valid field`).

## Querying and UI FQNs

`query <model> <Type>` builds GraphQL with `--select`, `--where`, `--limit`, `--offset`. Operators: `eq`, `contains`, `startsWith`, `endsWith`, `regex`, their case-insensitive forms (`icontains`, `istartsWith`, `iendsWith`, `iregex`), and `gt`, `gte`, `lt`, `lte`. Collection fields are pluralised and nested reference filters are AND-combined. `graphql` takes `--variables` and `-o`; `--schema` writes the SDL to `.judo-schema.graphql`.

`--select` takes scalar fields only (`name`, `fqn`, `createable`, `_type`); `--select "target{name}"` and `target.name` are rejected with `not a field of <Type>`, and a reference field selected by itself fails with `SubselectionRequired`. To read a reference field, use `graphql`, for example `graphql '{esm{accesses{items{name target{name}}}}}'`. `-w "fqn.eq=<fqn>"` filters by FQN; for a looser match use `name.contains`.

The GraphQL schema maps `Integer` and `Long` attributes to GraphQL `Int`; `Long` is narrowed to 32-bit, not `String`.

`ui` has no `MenuItem`, `MenuItemAccess`, `Access`, `ActorType` or `TableOperation` type: `query ui MenuItemAccess` fails with `ui type 'MenuItemAccess' does not exist`. These are `esm` types; use `query esm MenuItemAccess`, `query esm Access`, `query esm TableOperation`. The error lists the valid type names. A field the CLI reports as `not a field` lists the valid fields of that type: for example `textWidget` belongs to `DataField`, not to `StringType`.

For model type `ui`, FQNs are non-uniform: an Application is its simple name, a Theme is `<App>::Theme`, a Frame is `<containerFQN>::Frame`, a MimeType is `type/subType`, other named elements use `::` hierarchy, unnamed elements fall back to the XMI URI fragment.

GraphQL string filters accept only `eq`, `contains`, `startsWith`, `endsWith`, `regex` and their case-insensitive forms (`icontains`, `istartsWith`, `iendsWith`, `iregex`). There is no `in` operator on `StringFilter`. To match several values, query the type with a limit and filter the returned items in code.

The `ESM_DataFeature` interface in graphql does not define `memberType` or `getterExpression`. The concrete `ESM_DataMember` type (the `datamembers` list) has both, so read them from there: `graphql '{esm{datamembers(limit:3000){items{fqn memberType getterExpression}}}}'`, then match on `fqn`.

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
