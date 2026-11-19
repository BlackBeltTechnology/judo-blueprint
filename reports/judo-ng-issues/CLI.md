# JUDO model CLI: issues for the CLI developers

CLI version: `1.1.0.20261109_213146_746dc745_develop`. judo-ng base: latest `develop` (worktrees in `target/judo-ng-read/wt/`).
Sources: build-test gaps (R…), verified findings (WR…), today's scratch reproductions on `tests/fixtures/Sandbox.model`.
The catalog (`catalog/agent-docs/model/judo-cli.md`, "Known limitations and gotchas") documents the user-side workarounds; this file lists what should be fixed in the CLI.

## Summary

| # | Issue | Kind | Source |
|---|---|---|---|
| 1 | `create` accepts an `ASSOCIATION` transient relation that `validate` then rejects | inconsistent validation | today, scratch |
| 2 | `managed` refused on an anonymous actor, but stored as `true` | wrong default | R19-12 (b), scratch |
| 3 | Mapped TO creation silently adds every member; adding one again fails only at `validate` | silent side effect, late error | R7-14, R8-4, R19-12 (a) |
| 4 | Duplicate elements are not refused at `create` | missing check | R7-14, R11-10 |
| 5 | A failed script keeps its earlier edits; recovery is `save` before the script + `discard --force` (no new code needed) | missing hint | R11-10 |
| 6 | `update` on a duplicate FQN acts on the first element, with no way to select another | missing selector | catalog |
| 7 | `--unset postCallAccessNavigation` does not clear it | broken command | catalog |
| 8 | `move` reports a different element than the moved one | misleading output | catalog |
| 9 | Data type change does not reach the mapped TO members | missing propagation | catalog |
| 10 | Access with list cardinality creates a table that fails validation until `fill` | invalid intermediate state | R0 #11 |
| 11 | `MenuItemAccess` refused; the auto item is labelled with the TO name | poor default | R18-8 |
| 12 | `name` errors on reference-derived elements and `MimeType` are misleading | error message | R17-2, catalog |
| 13 | A binary type with two MIME types cannot be created | missing feature | R17-2 |
| 14 | `validate` passes, the Maven UI validation of the same model fails | validator mismatch | R18-6, R19-1 |
| 15 | UI validation failure prints `{}: {}` | broken log format | R18-7 |
| 16 | `Zeta transformation not yet implemented, falling back to ETL` on every merge | noise | catalog |
| 17 | `--strict` is accepted silently although it has no effect | stale option | catalog, scratch |

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

## 4. Duplicate elements are not refused at `create`

- **Behaviour:** two members with the same name in one container are created; `create` only prints `warn Named element code is not unique in its container` (reproduced: `create -t DataMember --ns Sandbox::EA -n code -s dataType=Sandbox::String` twice). Rerunning a script duplicates every element (see 5).
- **Expected:** `create` refuses a name that is already taken in the container.

## 5. A failed script keeps its earlier edits

- **Behaviour:** when a command in a script fails, the commands before it stay applied in memory and in the `.dirty` overlay; rerunning the fixed script duplicates them.
- **Not a missing feature:** `save` before the script makes the saved file the restore point; `discard --force` reverts to it (all unsaved edits, so save first). This survives a daemon restart, which in-memory undo would not.
- **Evidence:** every edit runs as one step on an EMF command stack (`EsmTransaction.run` → `session.execute`); `--dry-run` already undoes its step (`runtime__judo-model-cli/src/main/java/hu/blackbelt/judo/cli/mutation/EsmTransaction.java:85-86`); `save` and `discard` clear the stack with `tx.flush()` (`.../commands/SaveCommand.java:89`, `.../commands/DiscardCommand.java:96`; `discard` reloads the model).
- **Expected (small):** when a command fails partway through a script, the error ends with the hint `fix: discard --force` (and the recipe is documented in the CLI's model-mutations docs). An `undo N` / checkpoint (session.undo() N times, then rewrite the overlay) is optional: it gives a restore point without saving an unfinished model, and is cheaper than reloading a large model.
- **Workaround:** `save` → run the script → on failure `discard --force`, fix, rerun.

## 6. `update` on a duplicate FQN

- **Behaviour:** `update` acts on the first element with a given FQN; there is no index or id suffix to select another.
- **Expected:** refuse an ambiguous FQN, or accept an `xmi:id` / index selector.

## 7. `postCallAccessNavigation` cannot be cleared

- **Behaviour:** `update <operationForm> --unset postCallAccessNavigation` leaves the value in place.
- **Expected:** `--unset` clears the reference.

## 8. `move` reports a different element

- **Behaviour:** the result `changed <fqn> (in components)` names an element whose position changed, which is not always the moved element.
- **Expected:** the result names the moved element and its new position.

## 9. Data type change does not reach the mapped members

- **Behaviour:** changing `dataType` of an entity attribute leaves the mapped member of each transfer object on the old type.
- **Expected:** the change propagates to mapped members, or `update` lists the members that now disagree.

## 10. Access with list cardinality creates an invalid table

- **Behaviour:** `create -t Access --ns <Actor> --set target=<TO>` also creates `<TO>::<TO>_Table` without columns; validation fails with `ExposedTransferObjectTableHasColumns` until `fill <TO> --pages view,form,table` runs.
- **Expected:** the cascade creates at least one column, or prints that `fill` is required.

## 11. `MenuItemAccess` refused, auto label is the TO name

- **Behaviour:** `create -t MenuItemAccess` → `MenuItemAccess is created automatically`; the auto-created menu item is labelled with the TO name (for example `PrivacyInfo`).
- **Expected:** `create -t Access` accepts a menu label, or the label defaults to the access name.
- **Evidence:** `runtime__judo-model-cli/.../commands/QueryCommand.java:350-354` (WR18-8, query part).

## 12. Misleading `name` errors

- **Behaviour:** `DataField`, `DataColumn`, `DataFilter`, `ReferenceField`, `TabularReferenceField`, `OperationForm`, `Inherited*` and `MimeType` have no `name` in their `CreateInput`; passing `-n` gives `contains a field not in <Kind>CreateInput: name`. The same message also appears for an ambiguous FQN.
- **Expected:** the message says how the name is derived (binding, or `type`/`subType` for `MimeType`) and which field to set; an ambiguous FQN gets its own message.
- **Evidence:** WR17-2: `create -t MimeType --ns Sandbox -n x --dry-run` rejected; `-s type=application -s subType=json` created `application/json`.

## 13. Binary type with two MIME types

- **Behaviour:** `create -t BinaryType -s mimeTypes=application/json,application/xml --dry-run` is rejected.
- **Expected:** a list value for a multi-valued reference, or a documented `--add` form.

## 14. `validate` passes, Maven UI validation fails

- **Behaviour:** after `fill` placed an INSTANCE operation with a file output on a derived singleton access, `validate` printed `passed ui` and the Maven build failed in the frontend-react model step (`Verify UI model is presented`).
- **Evidence:** the CLI runs the same `ui.evl` (`runtime__judo-model-cli/.../commands/ValidateCommand.java:114-118, 161-166`, `.../mutation/UiCheck.java:87-110`); the failing rules come from the esm2ui transformation of a derived access (`runtime__judo-tatami-client/judo-tatami-esm2ui-etl/src/main/epsilon/transformations/ui/modules/accesspoint/accessView.etl:31-32`). The difference is in the transformation input or options between the CLI dry run and the Maven workflow (`judo-tatami-client-workflow/.../WorkflowHelper.java:124-130`).
- **Expected:** `validate` reproduces the build verdict.
- **Workaround:** delete the operation forms that `fill` placed on the derived access view.

## 15. UI validation failure prints `{}: {}`

- **Behaviour:** a UI validation failure is logged as `{}: {}` without the rule or element.
- **Evidence:** `runtime__judo-tatami-client/judo-tatami-ui-validation/.../StringBuilderLogger.java:449-453` formats SLF4J-style `{}` placeholders with `String.format`; `models__judo-meta-ui/.../validation/UiJavaValidator.java:125`. Reproduced with `judo-cli -m <model> validate` on a scratch model (WR18-7).
- **Expected:** the rule name and element are printed.

## 16. Zeta warning on every merge

- **Behaviour:** merge prints `[WARN] Zeta transformation not yet implemented, falling back to ETL`.
- **Expected:** no warning for the default path, or a flag to choose the mode.

## 17. `--strict` is accepted silently

- **Behaviour:** `validate` already exits non-zero on a validation error; `validate --strict` is accepted without a deprecation message, and `--help` does not list it.
- **Expected:** a deprecation warning, or an `unknown option` error.
