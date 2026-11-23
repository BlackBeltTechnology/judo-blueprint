# JUDO model CLI: issues for the CLI developers

CLI version: `1.1.0.20261109_213146_746dc745_develop`. judo-ng base: latest `develop` (worktrees in `target/judo-ng-read/wt/`).
Sources: build-test gaps (R…), verified findings (WR…), today's scratch reproductions on `tests/fixtures/Sandbox.model`.
`session L<n>` = `reports/research/webshop-run/2026-11-11T14-06-20-342Z_01a1caee-58b6-724e-ae62-d32987dbcd2d.jsonl.gz`.
The catalog (`catalog/agent-docs/model/judo-cli.md`, "Known limitations and gotchas") documents the user-side workarounds; this file lists what should be fixed in the CLI.

## Summary

| # | Issue | Kind | Source |
|---|---|---|---|
| 1 | `create` accepts an `ASSOCIATION` transient relation that `validate` then rejects | inconsistent validation | today, scratch |
| 2 | `managed` refused on an anonymous actor, but stored as `true` | wrong default | R19-12 (b), scratch |
| 3 | Mapped TO creation silently adds every member; adding one again fails only at `validate` | silent side effect, late error | R7-14, R8-4, R19-12 (a), R19 (session L10240, L10256) |
| 4 | Duplicate elements are not refused at `create` | missing check | R7-14, R11-10 (**Fixed** in `a64aa981`) |
| 5 | `update` on a duplicate FQN acts on the first element, with no way to select another | missing selector | catalog (**Fixed** in `a64aa981`) |
| 6 | `--unset postCallAccessNavigation` does not clear it | broken command | catalog |
| 7 | `move` reports a different element than the moved one | misleading output | catalog (**Fixed** in `a64aa981`) |
| 8 | Data type change does not reach the mapped TO members | missing propagation | catalog |
| 9 | Access with list cardinality creates a table that fails validation until `fill` | invalid intermediate state | R0 #11 |
| 10 | `MenuItemAccess` refused; the auto item is labelled with the TO name | poor default | R18-8, R18 (session L9509–L9510) |
| 11 | `name` errors on reference-derived elements and `MimeType` are misleading | error message | R17-2, R17 (session L8803), catalog |
| 12 | A binary type with two MIME types cannot be created | missing feature | R17-2, R17 (session L9250) (Not a defect: works once the MIME types exist) |
| 13 | `validate` passes, the Maven UI validation of the same model fails | validator mismatch | R18-6, R19-1, R18 (session L9557–L9583), R19 (session L10381–L10390) (**Fixed** in `a64aa981`, confirmed on the failing model) |
| 14 | UI validation failure prints `{}: {}` | broken log format | R18-7 |
| 15 | `Zeta transformation not yet implemented, falling back to ETL` on every merge | noise | catalog |
| 16 | `--strict` is accepted silently although it has no effect | stale option | catalog, scratch (**Fixed** in `a64aa981`) |
| 17 | `update` with a three-level element FQN fails; the two-level form reports `changed` but the stored value does not follow | wrong element, silent success | R18 (session L9797–L9806) |
| 18 | The allowed-value error lists MIME types as object identities | unreadable error | R17 (session L8787–L8800) |
| 19 | `validate --strict` fails on an orphan operation form after `fill` | stale state after `fill` | R17 (session L8758–L8782) |
| 20 | `query --select` reference-field error does not name the fix | error message | R16 (session L6135, L6520), R18 (session L9889–L9890, L10222) |
| 21 | `validate` summary says `0 errors` after printing UI errors | contradicts exit code | CLI `a64aa981`, R18-6 model |
| 22 | `operationType=INITIALIZER` is stored without `initializer=true` | CLI skips the Designer's translation | R20 C1, R20 F6 |

## 1. `create` accepts an `ASSOCIATION` transient relation that `validate` rejects

- **Behaviour:** `create -t OneWayRelationMember --ns <Pkg>::<UnmappedTO> -n r -s memberType=TRANSIENT -s relationKind=ASSOCIATION` succeeds; only `validate` reports `must be aggregation if transient`. On an entity relation the same `relationKind=AGGREGATION` is refused at `create` (`valid ASSOCIATION · COMPOSITION`).
- **Expected:** `create` applies the same rule as `validate` (refuse, or default to `AGGREGATION`), as it already does for entity relations.
- **Reproduction:** scratch copy of `tests/fixtures/Sandbox.model`, commands above.
- **Workaround:** run `validate` before `save`.

## 2. `managed` refused on an anonymous actor, but stored as `true`

- **Behaviour:** `create -t ActorType --ns Sandbox -n G1 -s kind=HUMAN -s anonymous=true -s managed=false` → `managed: does not apply to this ActorType (applies when not anonymous)`. Without the flag the actor is stored with `"managed": true`.
- **Expected:** the stored value matches the rule (`false`, or unset) for an anonymous actor.
- **Workaround:** omit `managed`; it has no effect for an anonymous actor without a principal.

## 3. Mapped TO creation silently adds every member

- **Behaviour:** `create -t TransferObjectType -s mapping=<Entity>` creates a mapped member for every entity attribute and relation, including derived ones, plus the view, form and table (157 elements in one case). Creating one of these members again succeeds and fails later in esm and ui validation as `not unique`.
- **Expected:** the result line says what was created (it prints `(+N contained)` only); a second member with the same name is refused at `create`.
- **Workaround:** create the mapped TO, then delete the unwanted members.
- **Evidence (R19):** `create -t TransferObjectType` with a mapping to an entity reported `+157 contained`, then `+105 contained` in a second build; hand-added members then failed at `validate` with `NamedElementIsUniqueInItsContainer` and `Binding … is mapped by other mapped data members` (session L10240, L10256).

## 4. Duplicate elements are not refused at `create`

- **Behaviour:** two members with the same name in one container are created; `create` only prints `warn Named element code is not unique in its container` (reproduced: `create -t DataMember --ns Sandbox::EA -n code -s dataType=Sandbox::String` twice). Rerunning a failed script duplicates its earlier elements unless the model was saved before and discarded after the failure.
- **Expected:** `create` refuses a name that is already taken in the container.

## 5. `update` on a duplicate FQN

- **Behaviour:** `update` acts on the first element with a given FQN; there is no index or id suffix to select another.
- **Expected:** refuse an ambiguous FQN, or accept an `xmi:id` / index selector.

## 6. `postCallAccessNavigation` cannot be cleared

- **Behaviour:** `update <operationForm> --unset postCallAccessNavigation` leaves the value in place.
- **Expected:** `--unset` clears the reference.

## 7. `move` reports a different element

- **Behaviour:** the result `changed <fqn> (in components)` names an element whose position changed, which is not always the moved element.
- **Expected:** the result names the moved element and its new position.

## 8. Data type change does not reach the mapped members

- **Behaviour:** changing `dataType` of an entity attribute leaves the mapped member of each transfer object on the old type.
- **Expected:** the change propagates to mapped members, or `update` lists the members that now disagree.

## 9. Access with list cardinality creates an invalid table

- **Behaviour:** `create -t Access --ns <Actor> --set target=<TO>` also creates `<TO>::<TO>_Table` without columns; validation fails with `ExposedTransferObjectTableHasColumns` until `fill <TO> --pages view,form,table` runs.
- **Expected:** the cascade creates at least one column, or prints that `fill` is required.

## 10. `MenuItemAccess` refused, auto label is the TO name

- **Behaviour:** `create -t MenuItemAccess` → `MenuItemAccess is created automatically`; the auto-created menu item is labelled with the TO name (for example `PrivacyInfo`).
- **Expected:** `create -t Access` accepts a menu label, or the label defaults to the access name.
- **Evidence:** `runtime__judo-model-cli/.../commands/QueryCommand.java:350-354` (WR18-8, query part).
- **Evidence (R18):** `create -t MenuItemAccess` → `MenuItemAccess is created automatically`; the CLI suggests `create -t Access` (session L9509–L9510; catalog `judo-cli.md:124`).

## 11. Misleading `name` errors

- **Behaviour:** `DataField`, `DataColumn`, `DataFilter`, `ReferenceField`, `TabularReferenceField`, `OperationForm`, `Inherited*` and `MimeType` have no `name` in their `CreateInput`; passing `-n` gives `contains a field not in <Kind>CreateInput: name`. The same message also appears for an ambiguous FQN.
- **Expected:** the message says how the name is derived (binding, or `type`/`subType` for `MimeType`) and which field to set; an ambiguous FQN gets its own message.
- **Evidence:** WR17-2: `create -t MimeType --ns Sandbox -n x --dry-run` rejected; `-s type=application -s subType=json` created `application/json`.
- **Evidence (R17):** `create -t MimeType --ns <Pkg> -n json` → `name not defined for MimeTypeCreateInput` (session L8803).

## 12. Binary type with two MIME types

- **Behaviour:** `create -t BinaryType -s mimeTypes=application/json,application/xml --dry-run` is rejected.
- **Expected:** a list value for a multi-valued reference, or a documented `--add` form.
- **Evidence (R17):** the refusal for a MIME type that does not exist yet names the value (`mimeTypes: application/json is not an allowed value`) but not the `MimeType` element that must be created first (session L9250). Once both MIME types exist, `update --add` adds the second one (see #18).

## 13. `validate` passes, Maven UI validation fails

- **Behaviour:** after `fill` placed an INSTANCE operation with a file output on a derived singleton access, `validate` printed `passed ui` and the Maven build failed in the frontend-react model step (`Verify UI model is presented`).
- **Evidence:** the CLI runs the same `ui.evl` (`runtime__judo-model-cli/.../commands/ValidateCommand.java:114-118, 161-166`, `.../mutation/UiCheck.java:87-110`); the failing rules come from the esm2ui transformation of a derived access (`runtime__judo-tatami-client/judo-tatami-esm2ui-etl/src/main/epsilon/transformations/ui/modules/accesspoint/accessView.etl:31-32`). The difference is in the transformation input or options between the CLI dry run and the Maven workflow (`judo-tatami-client-workflow/.../WorkflowHelper.java:124-130`).
- **Expected:** `validate` reproduces the build verdict.
- **Workaround:** delete the operation forms that `fill` placed on the derived access view.
- **Evidence (R18, R19):** R18: after a file operation was added, `validate --strict` passed and the build failed at `Verify UI model is presented` (session L9557–L9583). R19: after an operation's output was changed, `validate` passed and the build failed with `ActionContainerSameWithActionDefinition`; `fill` on the new transfer object fixed it (session L10381–L10390).

## 14. UI validation failure prints `{}: {}`

- **Behaviour:** a UI validation failure is logged as `{}: {}` without the rule or element.
- **Evidence:** `runtime__judo-tatami-client/judo-tatami-ui-validation/.../StringBuilderLogger.java:449-453` formats SLF4J-style `{}` placeholders with `String.format`; `models__judo-meta-ui/.../validation/UiJavaValidator.java:125`. Reproduced with `judo-cli -m <model> validate` on a scratch model (WR18-7).
- **Expected:** the rule name and element are printed.

## 15. Zeta warning on every merge

- **Behaviour:** merge prints `[WARN] Zeta transformation not yet implemented, falling back to ETL`.
- **Expected:** no warning for the default path, or a flag to choose the mode.

## 16. `--strict` is accepted silently

- **Behaviour:** `validate` already exits non-zero on a validation error; `validate --strict` is accepted without a deprecation message, and `--help` does not list it.
- **Expected:** a deprecation warning, or an `unknown option` error.

## 17. `update` with a three-level element FQN fails; the stored value does not follow

- **Behaviour:** `update <table element> -s representationComponent=card` with the three-level element FQN fails with `element not found`. The two-level FQN is accepted and prints `changed`, but a following `query` still shows the old value `TABLE`. The success line does not print the stored value.
- **Expected:** the success line prints the stored value; the element FQN form is documented in the help.
- **Reproduction:** not reproduced in this pass; session evidence only.
- **Workaround:** read the value back with `query` after every `update`; use the two-level FQN.
- **Source:** R18; session L9797–L9806.

## 18. The allowed-value error lists MIME types as object identities

- **Behaviour:** `update <BinaryType> --add mimeTypes=<fqn>` for a MIME type that does not exist prints `[WARN] … not an allowed value`, then the valid list as `MimeTypeImpl@3973722f` instead of MIME type FQNs.
- **Expected:** the list prints the FQN of each candidate (for example `text/csv`).
- **Cause (not traced):** the list comes from `EsmUtils.getCandidateLabels` in the ESM model (`models__judo-meta-esm/.../EsmFieldEditor.java:329-332`); the label falls back to an object's default `toString`.
- **Not reproduced:** the claim that `--add` keeps only the first MIME type. After both MIME types exist, `--add` adds the second reference (session L8787–L8800).
- **Workaround:** create the MIME types first (`create -t MimeType -s type=… -s subType=…`), then `update --add`.
- **Source:** R17; session L8787–L8800.

## 19. `validate --strict` fails on an orphan operation form after `fill`

- **Behaviour:** after `fill` of a type that has an operation on a table, `validate --strict` reports `NamedElementHaveToBeInApplication` for an orphan `FormCall` (`<op>::FormCall`). Deleting the operation form does not clear it. Deleting the table operation does, and re-adding it with `update <Table> --add feature --feature <op> --as tableAction` passes.
- **Expected:** `fill`, or deleting the form, removes the call it created.
- **Reproduction:** not reproduced in this pass; session evidence only.
- **Workaround:** delete the table operation, then re-add it with `--as tableAction`.
- **Source:** R17; session L8758, L8766, L8779, L8782.

## 20. `query --select` error for reference fields does not name the fix

- **Behaviour:** `query esm <Type> --select name,dataType` fails with `Subselection required for type ESM_Primitive` (the same error for `ESM_Class` and `ESM_TransferObjectType`). A nested selection such as `principal{fqn}` fails with `not a field of ActorType`. The same field works inside `judo graphql`.
- **Expected:** the message says that reference fields cannot be selected with `--select` and names `judo graphql` with a nested selection.
- **Note:** the scalar-only rule itself is documented (`judo-cli.md:156`); only the message is in scope. `--where fqn~=…` is not an operator (`fqn.contains` works); that was a builder mistake.
- **Workaround:** use `judo graphql` for reference fields.
- **Also:** `query esm Access -s name,target` prints `"data": null` plus the GraphQL `SubselectionRequired` error and exits 0 (rerun with CLI `1.1.0.20261119_155735_a64aa981_develop` on a Sandbox copy); a script cannot detect the failure by the exit code.
- **Source:** R16 (session L6135, L6297, L6520, L6670); R18 (session L9889–L9890, L10222, L10269).

## 21. `validate` summary ignores UI errors

- **Behaviour:** with CLI `1.1.0.20261119_155735_a64aa981_develop` on the re-created R18-6 model, `validate` prints four UI errors, omits `passed ui`, exits 1, and still ends with `Validation complete: 0 errors, 2 warnings`.
- **Expected:** the summary counts the UI (and transform) errors, so it agrees with the exit code.
- **Evidence:** `reports/research/runs/cli-verify/fix13.md` (lines 28-36).

## 22. `operationType=INITIALIZER` is stored without `initializer=true`

- **Reproduction:** scratch copy of `tests/fixtures/Sandbox.model`; `create -t TransferObjectType -n Jobs --ns Sandbox`; `create -t Operation -n seed --ns Sandbox::Jobs -s operationType=INITIALIZER`. The same create on an entity (`--ns <pkg>::<Entity>`), followed by `transform --skip=asm,rdbms`, shows the PSM result.
- **Behaviour:** exit 0, and `update <fqn> --schema` shows `operationType = INITIALIZER`, `initializer = false`.
  - On an unmapped transfer object `create` prints `warn Operation: Jobs.seed must be static in unmapped transfer object type`, and `validate` (also `--strict`) exits 1 (`error esm Invalid model`).
  - On an entity there is no warning and `validate` passes, but ESM to PSM treats the operation as an instance operation (`BoundTransferOperation`, guards use `operationType != STATIC`, `OperationRules.java:3163-3185`), so the generated interface is `accept(<Entity> _this)` and the operation is no initializer (`initializer = false`).
- **Expected:** the selection maps to `STATIC` plus `initializer = true`, as in the Designer (`esm.odesign:14821,14837-14857`), or `INITIALIZER` is not offered (`EsmCandidates.java:224-239` lists it as a plain enum value; the CLI has no mapping, no `INITIALIZER` hit in its `src/main`), or `validate` rejects the literal on an entity too.
- **Workaround:** `update <fqn> -s operationType=STATIC -s initializer=true` (an unmapped transfer object also needs `customImplementation=true` or a body). With STATIC + `initializer=true` the PSM holds an `UnboundOperation` with `initializer="true"`, and the generated interface is `void run()` on an entity as well as on an unmapped transfer object (`judo-psm-generator-sdk-core-api/.../OperationHelper.java:105,196,237-240`).
- **Source:** R20 C1, R20 F6 (the item's "entity-hosted initializers get `accept(_this)`" came from this literal, not from the host kind); judo-meta-esm 87578dd. Triage: ESM candidate list, not CLI code.

## Verification of `1.1.0.20261119_155735_a64aa981_develop`

Pinned in `pom.xml` on 2026-11-19; scratch copy of `tests/fixtures/Sandbox.model`.

| # | Check | Result |
|---|---|---|
| 4 | `create -t DataMember --ns Sandbox::EA -n code ...` twice; `update Sandbox::EA.code2 --set name=code` | refused: `name 'code' is already used in Sandbox::EA`, `fix choose another name` |
| 5 | saved model with two members `code` (name edited in the XMI), `update Sandbox::EA.code --set required=false` | refused, exit 2: `'Sandbox::EA.code' is ambiguous: 2 elements`, lists both `id:`; `update id:<xmi:id> ...` addresses one |
| 7 | `move Sandbox::EA.code2 --index 0` | `moved Sandbox::EA.code2 index 1 -> 0`; `--json` has `fromIndex` |
| 16 | `validate --strict` | `warn --strict is deprecated: validation errors always give a non-zero exit` |
| 12 | create both MIME types, then `create -t BinaryType -n Bin2 -s mimeTypes=application/json,application/xml` | stored; the earlier failure came from MIME types that did not exist |
| 13 | R18-6 model re-created in a worktree (`fill` on the derived singleton access): old CLI, new CLI, Maven frontend-react model step | old: `passed ui`, exit 0; new: the same four UI errors as Maven, exit 1; Maven: `BUILD FAILURE`. Record: `reports/research/runs/cli-verify/fix13.md` |
| 1, 2 | rechecked | unchanged (known ESM issues, see triage) |

The catalog (`catalog/agent-docs/model/judo-cli.md`) documents the new behaviour with the version, and keeps the old behaviour for older pinned CLIs.

## Triage by the CLI maintainers

Checked against `judo-model-cli` (branch `feature/JNG-6380_cli_guidance`) and the judo-ng sources in `target/judo-ng-read/wt/`. Rule: judo-meta-esm is legacy code and stays untouched, and the CLI gets no workarounds for ESM behaviour. Items caused by ESM or judo-tatami are known issues with a user-side workaround. The CLI fixes only what its own code gets wrong.

### CLI issues (fixed in judo-model-cli, OpenSpec change `fix-cli-field-report-issues`)

| # | What the CLI gets wrong | Fix |
|---|---|---|
| 4 | `create -n` and rename write the given name over the unique name ESM chose, so the CLI itself creates duplicates. Script reruns make it worse. | Refuse inside the edit step with ESM's existing `EsmUtils.isUniqueName` (`EsmUtils.java:3092`); nothing is written. No ESM change. |
| 5 | `GenericModelSchema.resolveAll` returns the first element for an exact FQN, and checks for duplicates only for short names. `id:<xmi:id>` is already accepted everywhere. | Write commands refuse an FQN that matches several elements and list each `id:`. |
| 7 | `move` prints the EMF Compare summary of the step. A reorder can be read as other siblings moving. | The move result carries the old index as a field, and `move` prints `moved <fqn> index a -> b`. |
| 13 | Root cause: the CLI pinned judo-tatami-client `1.1.0.20260511`, whose esm2ui is ETL only (no transformation mode). The build uses the current tatami-client, where `Esm2UiWork` defaults to Zeta (`TransformationMode.java:93`). So `validate` ran a different esm2ui than the build. | Pin moved to `1.1.0.20261109_211802_9d130d8d_develop`, and esm2ui runs the build's own `Esm2UiWork`, so `judo.transformation.mode` picks the engine as in the build. Epsilon runtime added explicitly (the new tatami-client no longer brings it). Still to confirm: rerun the failing model's build and `validate`. |
| 16 | `--strict` is declared deprecated in `ValidateCommand` but prints nothing. | One `warn --strict is deprecated` line. |

Recovery from a failed script stays save before the script, then `discard --force` after a failure. It is documented in the CLI user guide, with no new command.

Item 11 (misleading `-n` error) comes from the CLI's own input layer, but it is cosmetic and not in this change.

Item 12 does not reproduce on the current CLI: `create -t BinaryType -s mimeTypes=application/json,application/xml` stores both MIME types once they exist (`create -t MimeType -s type=application -s subType=json`). The candidate list prints MIME types as `MimeTypeImpl@…`, and a MimeType's FQN prints as `<Model>/mimeTypes`. Both come from judo-meta-esm (`EsmCandidates.getCandidateLabels`, `EsmFqnResolverImpl`); they are known issues.

### Known issues, caused by ESM or judo-tatami (no CLI change)

| # | Cause | Workaround |
|---|---|---|
| 1 | ESM's allowed values for `relationKind` (EsmFieldRules/EsmCandidates) have no rule for transient relations. The rule exists only in EVL (`oneWayRelationMember.evl`, `AggregationIfTransient`). ESM already defaults a new transient relation to AGGREGATION. | Leave `relationKind` unset, or run `validate` before `save`. |
| 2 | `managed` is a required EBoolean with default `true` (`esm.ecore`); EsmFieldRules marks it as applying only to actors that are not anonymous. The Designer stores the same `managed="true"` on an anonymous actor (see `DebateTest.model`, actor `Actor`). | None needed; the value has no effect on an anonymous actor. |
| 3 | ESM's mapped-TO creator adds a member for every entity feature, plus a view, form and table. Adding one of them again is a duplicate (CLI item 4 refuses that). | Create the mapped TO, then delete the members you don't want. |
| 6 | Correction: `--unset postCallAccessNavigation` does not silently keep the value. It fails with `error … 'postCallAccessNavigation' cannot be cleared on OperationForm …`, exit 2, even when the field is empty. Cause: `EsmCandidates.java:271-273` registers the field with candidates but without `.unsettable()`, and `EsmFieldEditor.java:274-276` refuses to clear such a field. The field is optional (`esm.ecore:738`), and the Designer's candidate list starts with `null` (`EsmUtils.getSelectableOutputNavigationAccesses`, `EsmUtils.java:5778`), so clearing is a valid Designer action. ESM fix if ever needed: add `.unsettable()` to that registration. | Delete and recreate the operation form (not verified). |
| 8 | ESM does not pass a member's `dataType` change on to the mapped TO members. | Update the mapped members too. |
| 9 | ESM's access creator builds the TO table without columns. | Run `fill <TO> --pages view,form,table` after `create -t Access`. |
| 10 | ESM creates the `MenuItemAccess` and labels it with the TO's name. | Set the menu item's `label` afterwards. |
| 14 | judo-tatami-client `StringBuilderLogger` fills SLF4J `{}` placeholders with `String.format`. | None. |
| 15 | Zeta esm2psm, asm2script and script2operation are not implemented. tatami's own Work classes (e.g. `Esm2PsmWork`, judo-tatami-esm2psm line 150) log the fallback to ETL. The CLI's `transform` runs the build's own `EsmDefaultWorkflow`, so the build logs the same lines. The CLI does not filter them. | Ignore it. |
