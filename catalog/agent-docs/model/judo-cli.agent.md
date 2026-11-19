# judo-cli.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/judo-cli.md.

## Identity
- Artifact `judo-cli.jar`, at `target/judo-cli.jar` (downloaded by `./judo.sh build`; Maven `hu.blackbelt.judo.runtime:judo-model-cli:${judo-model-cli-version}`).
- Invoke: `java -jar target/judo-cli.jar -m model/<app>.model <command>`. No `judo_cli` alias in non-interactive shells.
- Source ESM `model/<app>.model`; interface GraphQL over ESM (and derived models when loaded).

## Why a CLI is mandatory
- ESM is one XMI file, tens of thousands of elements: too big to read safely.
- Elements cross-reference by `xmi:id`; hand edits silently dangle refs.
- Metamodel validation only at build time; CLI validates each mutation up front.
- CLI runs the transform pipeline ESM → PSM → ASM → RDBMS → Liquibase.

## Capability surface
- Query/introspection: entity types, TOs, relations, operations, UI defs; `__type`, `__schema`.
- Mutation: create/update/delete ESM elements; invalid mutations fail fast.
- Transformation: ESM → PSM → ASM → RDBMS → Liquibase (+ esm2ui); output `application/model/target/cli-generated/`. See `transformation-pipeline.md`.
- State: load/save/discard; in-memory edits tracked in hidden `.<file-name>.dirty` (e.g. `.<app>.model.dirty`).
- Tracing: element from ESM origin through derived models to runtime artifact and back.

## Mandatory rules
- Platform invariants, not preferences.
1. Never read the `.model` XML directly; use CLI queries.
2. Never edit the `.model` XML directly; use CLI mutations.
3. Always paginate: `limit`, `offset`, `totalCount`. Otherwise results silently truncated.
4. One writer per model file. Never two agents/terminals/CLI+Designer on same file; last `save` overwrites.
5. Parallel work: one git worktree (or copy) per task, all from same commit. Merge in target worktree: `merge <theirs.model> --base <base.model>` per copy; base = `git show <start-commit>:model/<app>.model > /tmp/base.model`. Without `--base`, add-add conflicts appear.
   - `merge --dry-run` first: lists conflicts with keys and fix commands (`--take <key>`, `--prefer mine|theirs`, or `delete`/`update`).
   - After merges: `validate --strict`, `save`, `status` (expect `state clean`, `unsaved changes none`), then commit.
   - `merge` never runs git. `<theirs.model>` must be the other copy's SAVED file. `--aird` also merges Designer `.aird` files.
6. Never `save` blindly: run `transform --load` and verify derived models query correctly first.
7. `transform` does NOT replace client build. It regenerates PSM, ASM, Measure, Expression, Script, Operation, RDBMS, Keycloak, Liquibase and runs esm2ui (writes `<app>-ui.model`; `--skip esm2ui` omits). No React output: after UI-affecting ESM changes run `./judo.sh build -f`.
8. `save` writes disk, does NOT commit. `git restore`/`git checkout` on the model later destroys uncommitted saves. Commit after each save or back up first.

## Command reference
- Invocation: `java -jar target/judo-cli.jar -m model/<app>.model <command> [options]`.
- Addressing: FQN (`<parentFqn>::<name>`; member `<ownerFqn>.<member>`), `id:<xmi:id>`, or unique short name. Ambiguous short name rejected, FQNs listed. Start-up ~0.4 s (per-model daemon holds model in memory).
- `query esm <Type> [--select ...] [--where k.op=v]`: simple read on esm/psm/asm/rdbms/ui. `--where`/`-w` dot-operators (`-w "name.contains=WorkReport"`); filters ANDed.
- `graphql '<query>'`: read/mutation. Filter argument is `where` (not `filter`). `--schema` exports schema; `--introspect` runs introspection.
- `create -t <Type> --ns <parent> [-n name] [--set k=v] [--index n | --before fqn | --after fqn]`: cascades like Designer (self-mapping of EntityType, view/form/table pages of TO, reverse member of two-way relation). `--schema [field]` describes fields; changes nothing.
- `update <fqn> --set/--unset/--add/--remove/--clear`: `--add feature` places a widget into container. `-f/--fqn` deprecated.
- `delete <fqn> [--cascade]`.
- `move <fqn> --index n | --before/--after fqn`: reorder (`moveUp`/`moveDown` gone).
- `relocate <fqn> --to <parent>`: keeps `xmi:id` and inbound refs.
- `fill <toFqn> [--pages view,form,table]`: create/populate TO view/form/table from members.
- `split <container> --layout VERTICAL|HORIZONTAL`.
- `merge <theirs.model> --base <base.model>`: three-way merge. Conflict kinds: `change-change`, `delete-change`, `change-delete`, `add-add`, `validation`; resolve `--take <key>`, `--prefer mine|theirs`, or printed fix commands.
- `validate [--strict]`: ESM EVL, esm2ui/UI EVL, transform dry run, in-memory. `--strict` deprecated: errors always exit non-zero.
- `transform [--load] [--skip steps] [--validate]`.
- `status [--json]`: clean/dirty, unsaved changes and intent.
- `save` / `discard [--force] [--derived]`: `save` never runs git.
- `mermaid model` / `mermaid from`: see Mermaid section.
- `server status` / `server stop [-f]`.
- Common flags: `--dry-run` (create, report, undo), `--json`, `--brief` (FQN only), `--no-check` (skip per-edit checks; run `validate` after), `--ns <fqn>`.
- Values: `--set a,b` sets list; `""` empty string; `null` rejected; `-s`/`--vars` verbatim (newlines, quotes, backslashes kept).
- Exit codes: 0 ok, 1 error, 2 rejected; `merge` also 4 for open conflicts.
- Prefer `query esm --select --where`, `status --json`, `mermaid` over parsing `graphql` JSON in scripts (scripts crash on `null`).

### Mermaid diagrams
- `mermaid model [--scope <fqn>] [--depth n] [--split aggregate|package|none] [--kinds entity,enum,transfer,actor,operation] [--members types|names|none] [--md]`: draws IN-MEMORY model incl. unsaved edits as `classDiagram`s.
- `mermaid from <file|->`: saved `query`/`graphql` JSON → diagram, no daemon. `query esm <Type> --mermaid` and `graphql '<q>' --mermaid` draw a query result.
- Arrows: composition `*--`, aggregation `o--`, association `-->`, generalization `<|--`, mappings `..>` labelled `maps`; multiplicities shown. Class diagrams only.
- Over renderer limits → warning: narrow with `--scope`, `--split aggregate`, or `--members none`. Replaces hand scripts like `diagram_generator.py`.

### Tracing
- GraphQL `trace.forward` / `trace.backward` follow element ESM → PSM → ASM → RDBMS and ESM → UI by parsing composite `xmi:id` (see `xmi-id-traceability.md`). Result: hops with `modelType`, `xmiId`.

### Session, daemon, unsaved edits
- One daemon per model; session in `~/.judo/sessions/<hash>/` (`session.json`, `daemon.log`).
- Unsaved edits in memory, mirrored ~every 500 ms to hidden overlay `.<file-name>.dirty` (plus `.base`/`.intent` sidecars). External change to model file reloads and discards them.
- ESM loaded at daemon start; PSM/ASM/RDBMS/UI on first query.
- `status` stuck dirty after save/discard → `discard --force`; last resort: stop server and delete overlay by hand.

### Version and jar pitfalls
- `--version` shows stale `1.0.0` (baked manifest). Real versions: Maven properties `judo-model-cli-version` and `judo-meta-esm-version` in root `pom.xml`.
- Jar downloaded only when MISSING. After bumping versions: delete old jar, run `./mvnw -f application/model/pom.xml -N validate`.
- Pinned jar may be newer than local CLI source; read docs at pinned commit: `git show <sha>:docs/commands/<cmd>.md`.
- Mutations stay in memory until `save`.
- `target/judo-cli.jar` can be missing after `./judo.sh generate` or `build` (they run `mvnd clean`). Restore: `./judo.sh generate-root` or `mvn -DgenerateRoot validate` (root `pom.xml`, profile `download-cli-for-generate-root`). Missing jar shows `Unable to access jarfile`.

### Known limitations and gotchas

#### Creating, filling, changing
- Anonymous `ActorType`: `-s managed=...` refused (`applies when not anonymous`); omit it (stored default `true`, no effect).
- `relationKind=AGGREGATION`: refused on entity relations (valid `ASSOCIATION`, `COMPOSITION`); accepted and required on transient relations of unmapped TOs (`ASSOCIATION` there only fails `validate`).
- Reference-derived UI elements (`DataField`, `DataColumn`, `DataFilter`, `ReferenceField`/`TabularReferenceField`, `OperationForm`, `Inherited*`) have NO `name` in CreateInput; name/FQN come from binding (`dataFeature`, `relationFeature`, `operation`). Passing `name` → `contains a field not in <Kind>CreateInput: name`. Place with `update <container> --add feature ...` or `create -t ... --set dataFeature=...`. "No name field" can mean ambiguous FQN.
- `RowOperation`: no create type; if CLI can't express it, edit that one XMI element by hand and verify with `validate` (`model-development.md`).
- Don't hand-add members to mapped TO: `create -t TransferObjectType -s mapping=<entity>` creates mapped members and view/form/table pages. Duplicate → `Named element ... is not unique in its container`; unbound mapped member → `Mapped data member ... must have binding`.
- `create -t MenuItemAccess` refused. `create -t Access --ns <actor> --set target=<TO>` creates Access + `MenuItemAccess` named `Menu`; rename/reuse. Deleting an Access referenced by a menu item needs `--cascade`. New Access has `createable`/`updateable`/`deleteable` all `false`: set explicitly.
- `fill <toFqn>` adds DataColumn + DataField per member; run `fill <toFqn> --dry-run` first; delete unwanted after. `fill`/adding DataColumns clears `Columns are not defined for the viewable table of <TO>` (`ExposedTransferObjectTableHasColumns`). DataColumn/DataFilter don't exist before `fill` or `--add feature`; `query esm DataColumn` empty until then.
- Access with list cardinality needs table column: `create -t Access ... target=<TO>` also creates `<TO>::<TO>_Table`. Without a column → validation error, ESM invalid (`error esm Invalid model`, transform skipped). Fix: `create -t DataColumn --ns <TO>::<TO>_Table --set dataFeature=<TO>.<attribute>` or `fill <TO>`.
- Type change must reach mapped members: change `dataType` of entity member → mapped member of each TO keeps old type; `validate` warns `Data type of data member ... must match the data type of its binding`.
- Gate save: `validate && save` (not `;`) — otherwise invalid model written.
- Duplicate FQNs: `update` acts on first element; no suffix to select; rename first.
- `MimeType` CreateInput has no `name` (derives from type/subType); `create -t MimeType -n ...` fails.
- Operation parameters: `containment` + `target`, not type/direction.
- Failed script leaves earlier edits in memory/overlay; rerun duplicates elements → `discard --force` first. `discard` reverts ALL unsaved edits.

#### Validation, history, action placement
- Some EVL checks (e.g. MAPPED member `required` vs binding) reliably run only in full build. After build re-run `validate`; check ASM/SDK timestamps contain change before marking verified.
- Rename keeps identity: `update <fqn> --set name=...` on data member keeps `xmi:id` → incremental Liquibase emits `renameColumn` (data survives). `discard --force` exploratory renames.
- `git checkout -- model/<app>.model` reverts ALL structural changes (rule 8).
- Merge may print `[WARN] Zeta transformation not yet implemented, falling back to ETL`; harmless.
- Signed identifiers cannot be minted with CLI; runtime mints only while serving REST (`../backend/README.md`).
- `move`: one-line `changed <fqn> (in components)` may name the sibling that shifted. `move <fqn> --json` prints `reordered <fqn> in <list>`; `status` shows `move <fqn> index=n` / `after=<fqn>`. Verify via `graphql` on container `components`; `discard --force` drops wrong reorder (and all other unsaved edits).
- `postCallAccessNavigation`: attribute of `OperationForm` only. `--unset` refused (`cannot be cleared on OperationForm <name>`); `--clear` fails (`not a list`); `--set postCallAccessNavigation=` not allowed. Set only when final. To remove: delete OperationForm, re-place via `update <container> --add feature --feature <operation>`. Allowed values = accesses whose target type matches the operation output; `--set` lists them on error.
- Place actions with `update <container> --add feature`. Container must exist, by exact FQN (`Container not found: <fqn>`): create ActionGroup first with `create -t ActionGroup --ns <viewFqn> -n <group>`. Operation must be member of container's TO (`'<op>' is not a feature of <TO> placeable here` lists placeable features). For relation table `<view>::<relation>`: operation of the relation's target TO.
  - Table actions: `update <viewFqn>::<relation> --add feature --feature <operation> --as rowAction|tableAction|bulkAction` → `TableOperation` with nested `OperationForm`.
  - ActionGroup direct: `update <viewFqn>::<group> --add feature --feature <operation>` → `OperationForm` inside group.
  - On a view `--as action` is not valid.

## Querying and UI FQNs
- `query <model> <Type>`: `--select`, `--where`, `--limit`, `--offset`. Operators: `eq`, `contains`, `startsWith`, `endsWith`, `regex`; case-insensitive `icontains`, `istartsWith`, `iendsWith`, `iregex`; `gt`, `gte`, `lt`, `lte`. Collections pluralised; nested reference filters AND-combined.
- `graphql` takes `--variables`, `-o`; `--schema` writes SDL to `.judo-schema.graphql`.
- `--select` scalars only (`name`, `fqn`, `createable`, `_type`). `--select "target{name}"` / `target.name` → `not a field of <Type>`; reference selected alone → `SubselectionRequired`. Read reference via `graphql '{esm{accesses{items{name target{name}}}}}'`.
- `-w "fqn.eq=<fqn>"` exact FQN; `name.contains` for loose.
- `ui` has no `MenuItem`, `MenuItemAccess`, `Access`, `ActorType`, `TableOperation`: those are `esm` types (`query ui MenuItemAccess` → `ui type 'MenuItemAccess' does not exist`). Error lists valid types. `not a field` lists valid fields (e.g. `textWidget` belongs to `DataField`, not `StringType`).
- UI FQNs: Application = simple name; Theme = `<App>::Theme`; Frame = `<containerFQN>::Frame`; MimeType = `type/subType`; other named = `::` hierarchy; unnamed = XMI URI fragment.

## Reach for the CLI when…
- Knowing what's in the model; adding/modifying/removing any element; verifying a change transformed correctly; tracing a runtime artifact (REST endpoint, DB table, UI form) to ESM origin.

## Do not reach for the CLI for…
- Java source code; React custom hooks, overrides, theme files (use file system); building (`./judo.sh build`).
- CLI authority = the model only.

## See also
- `transformation-pipeline.md` (transform output, server vs client regeneration); `model-development.md` (workflow, naming, JQL); `ui-authoring-guide.md`; `xmi-id-traceability.md`.
