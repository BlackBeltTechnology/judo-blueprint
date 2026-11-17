# ui-authoring-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/ui-authoring-guide.md.

## TL;DR — Invariants every authoring step must respect
- Mapped TO with UI carries exactly `<form>`, `<table>`, `<view>` (containment; NO `xsi:type`).
- `xsi:type` required iff the containing EReference is abstract (see §3).
- Every data-showing leaf binds to a `structure::`/`operation::` element (`dataFeature`, `relationFeature`, `operation`, `access`, `target`, `hiddenBy`, `enabledBy`, `requiredBy`).
- Grid = 12 columns: sibling `col` sum in a horizontal row ≤ 12; `row > 0`.
- `hiddenBy`/`enabledBy`/`requiredBy`/`confirmationCondition` → boolean `DataMember` on the OWNER TO only.
- Sibling `name`s unique within a container.
- Canonical names: `<Entity>_Form`, `<Entity>_Table`, `<Entity>_View_Edit`. Never bare `View`/`Form`/`Table` (FQN collisions). Name before wiring.
- Every `Access` meant for UI needs a `MenuItemAccess` in `<menuItems>` (direct or in `MenuItemGroup`). Access alone = API-only.

## 1. Mental model — three layers
- Data (`structure::`): EntityType → mapped TO (projection) → DataMember / RelationMember / Operation.
- UI (`ui::`): Form/Table/View hold DataField, DataColumn, DataFilter, TabularReferenceField, OperationForm.
- Access (`accesspoint::`): ActorType → Access (`target` TO) and MenuItemAccess (`access`).
- Authoring order: EntityType → mapped TO attributes/relations/operations → Table → View → Form → Access → MenuItemAccess.

## 2. The three scaffolds per `TransferObjectType`
- `<form>` (TransferObjectForm): create/operation-input dialog. Mapped TO with `createable=true`, or unmapped TO used as operation input.
- `<table>` (TransferObjectTable): list. Mapped TO reachable via Access with `upper=-1`.
- `<view>` (TransferObjectView): detail/edit. Mapped TO reachable via Access.
- Unmapped operation-input TOs usually hold only `<form>`.

## 3. The `xsi:type` rule — concrete vs. abstract containment
- Required on child iff parent EReference is abstract; missing → "Class 'Column' is not found or is abstract". Most common XMI mistake.
- Concrete (NO xsi:type): TO→form/table/view; Table/TRF→rowOperations/tableOperations (TableOperation); TableOperation→operationForm (OperationForm); TabBar→tabs (Group); Stepper→steps (Group); ActorType→accesses (Access), claims (Claim); Entity/TO→attributes (DataMember).
- Abstract (xsi:type REQUIRED): Container→components (`ui:Component`: DataField, Group, TabBar, Stepper, TabularReferenceField, OperationForm, ActionGroup, ActionButton, TextField, Divider, Placeholder, Icon); Table/TRF→columns (DataColumn; RelationColumn if enabled); →filters (DataFilter); ActorType/MenuItemGroup→menuItems (MenuItemAccess/Operation/Group); ActionGroup→actions (OperationForm; ActionGroup rare); Entity/TO→relations (OneWay/TwoWayRelationMember).
- Root must declare `xmlns:ui="http://blackbelt.hu/judo/meta/esm/ui"`.

## 4. Containment tree — what goes where
- View: components → Group, TabBar, TabularReferenceField, DataField/OperationForm/ActionGroup/TextField/Divider/Placeholder/Icon.
- Form: components → Group, DataField/ActionButton/Divider/Placeholder.
- Group: components → Group, widgets, TRF. TabBar tabs → Group (one panel). Each tab can hold components/TRF/TabBar.
- Table: columns → DataColumn; filters → DataFilter; rowOperations / tableOperations → TableOperation; TableOperation.operationForm → OperationForm.
- Decision cheat sheet:
  - one attribute edit → DataField.
  - visual grouping → Group (`frame`, `layout=HORIZONTAL|VERTICAL`).
  - tabs → TabBar (`<tabs>` Groups). Wizard → Stepper (`<steps>` Groups).
  - to-many relation → TRF `relationFeature`.
  - to-one pick/navigate → TRF `representationComponent=button|tag`, `autocompleteRows=N`.
  - one bound operation → OperationForm `operation="<name>"`.
  - grouped operations → ActionGroup `featuredActions=N` with `<actions xsi:type="ui:OperationForm">`.
  - row action → `<rowOperations operation="<xmi-id>">` + nested `<operationForm>`.
  - bulk toolbar → `<tableOperations operation=… isBulk="true">` + `<operationForm>`.
  - static text/separator/spacer → TextField / Divider / Placeholder.

## 5. Data-binding cheat sheet
- DataField/DataColumn/DataFilter `dataFeature` → DataMember (xmi:id).
- TRF `relationFeature` → One/TwoWayRelationMember (xmi:id).
- TableOperation `operation` → Operation (xmi:id).
- OperationForm `operation` → Operation by NAME STRING (exception; matched to owner TO operations; mistyped id = silent no-op).
- MenuItemAccess `access` → Access on same Actor (xmi:id). MenuItemOperation `targetOperation` → Operation (xmi:id).
- Access `target` → TO (xmi:id).
- Widgets `hiddenBy`/`enabledBy`/`requiredBy`; OperationForm `confirmationCondition` → boolean DataMember on owner TO.
- DataField numeric/date/time `minValueBy`/`maxValueBy` → same-type DataMember on owner TO.

## 6. Layout model
- Attributes: `col` 1..12 (validator ≤12), `row` (1; textarea larger), `layout` (HORIZONTAL/VERTICAL/DEFAULT), `horizontal`/`vertical` (LEFT/CENTER/TOP…), `frame` (bool), `stretch` (NONE/HORIZONTAL/VERTICAL/BOTH), `fit` (LOOSE/TIGHT).
- HORIZONTAL Group: col values sum to 12. VERTICAL (or default): each child on own row; `col` = its width.

## 7. Widget selection for `DataField` by bound attribute type
- StringType: `textWidget` (TEXT|INPUT), `textMultiLine`, `textMask` (needs textMultiLine=false AND textWidget=INPUT), `isTypeAheadField`, `textCountCharacters`.
- EnumerationType: `enumWidget` (COMBO|RADIO|TOGGLE_BUTTONBAR).
- BooleanType: `booleanWidget` (CHECKBOX|COMBO); `valueLabelPlacement` only with CHECKBOX.
- NumericType: `formatValue`, optional `minValueBy`/`maxValueBy` (disabled inside TableOperation).
- Date/Time/Timestamp: optional `minValueBy`/`maxValueBy`.
- BinaryType: file upload, no widget attrs. MeasuredType: no widget attrs.

## 8. `TabularReferenceField` rules by relation shape
- to-many (`upper=-1`): `rowsPerPage`, `isInlineEditable`, `smallTable`, `checkboxSelection`, `countRows`. Representation: table, button (ASSOCIATION only), tag, card (AGGREGATION: table, tag, card).
- to-one (`upper=1`): `autocompleteRows`, `buttonStyle`. Representation: table, plus button for ASSOCIATION.
- COMPOSITION: CRUD buttons {create, delete}; smallTable valid.
- AGGREGATION: CRUD buttons {add, remove} (selector dialog).
- ASSOCIATION: add/remove via selector.
- `crudOperationsDisplayed`, `transferOperationsDisplayed` control buttons before overflow menu.
- Observed allowed values: (upper 1, AGGREGATION) table; (1, ASSOCIATION) table,button; (-1, ASSOCIATION) table,button,tag,card; (-1, AGGREGATION) table,tag,card. Change `relationKind` first, then `representationComponent`; read allowed list from error.

## 9. `hiddenBy` / `enabledBy` / `requiredBy`
- All reference a boolean DataMember on the same owner TO.
- hiddenBy (widgets, MenuItem*, Group, ActionGroup): true → hidden. enabledBy (widgets, MenuItem*): true → enabled. requiredBy (DataField): true → required.
- On MenuItem*, hiddenBy references a boolean on the Actor's principal TO (usually DERIVED permission flag) — dynamic menu pattern (advanced-modeling-patterns.md §2).
- Hide a generated action: add TRANSIENT/DERIVED boolean to owner TO; set hiddenBy on OperationForm/ActionButton/ActionGroup (`update <viewFqn>::<action> --set hiddenBy=<TO>.<bool>`). TableOperation has no hiddenBy → set on its nested OperationForm.

## 10. Operations wiring
- Surfaces: OperationForm inline in View/Form/Group; OperationForm in ActionGroup (overflow); TableOperation.operationForm in rowOperations (single row) or tableOperations (toolbar; `isBulk=true` multi-select); MenuItemOperation on ActorType (global).
- `confirmationType` on OperationForm: `NONE`; `CONDITIONAL` (uses `confirmationCondition`); `MANDATORY` (always; `confirmationMessage`).
- `confirmationCondition`: without it always asks; with boolean DataMember on owner TO, asks only when true for that row/owner. Message from `confirmationMessage`, i18n key `<button key>.confirmation`.
- Operation output page (mapped transfer): Back (always), Refresh (output mapped to entity), Update (output declares `update`; page type `OPERATION_OUTPUT_UPDATE`; action `<operation>::Update`), Delete (declares `delete`). Unmapped output: Back only.
- CLI: `create -t ActionGroup --ns <viewFqn> -n <group>` (`--ns` required; TO refused). `update <viewFqn> --add feature --feature <operation>` then `relocate <viewFqn>::<operation> --to <viewFqn>::<group>`.
- Field order follows container `components` order. Reorder with `move <fqn> --index n` (or `--before`/`--after`), not delete/re-add.

## 11. End-to-end wiring — making an entity visible to a role
- Per entity: (1) mapped TO exists; (2) form/table/view with canonical names; (3) one Access on actor with `target`=TO; collection `upper=-1`; singleton `upper=1` with `!any()`-terminated getterExpression; (4) getterExpression = permission/tenancy filter (advanced-modeling-patterns.md §2); (5) MenuItemAccess → Access inside MenuItemGroup on `<menuItems>`; (6) menu `hiddenBy` → DERIVED permission flag on principal TO.

## 12. Skeleton template of a composed View
- View → DataField (flat fields); Group `layout=HORIZONTAL` `col=12` with two DataField `col=6`; TabBar `col=12` with `<tabs name="…" layout="HORIZONTAL">`; within tab: ActionGroup `featuredActions=2` with `<actions xsi:type="ui:OperationForm">`; TRF `relationFeature`, `representationComponent="table"`, `rowsPerPage`, `crudOperationsDisplayed`; DataColumn children; DataFilter `defaultOperation`; `<rowOperations operation=…>` with `<operationForm>`.
- Form: same pattern, no TRF, no ActionGroup.

## 13. Per-entity authoring checklist
- Data side: EntityType with CRUD flags; mapped TO exposes attributes/relations; operations exist.
- Table: DataColumn per visible attribute; DataFilter per searchable; rowOperations; tableOperations; `rowsPerPage`, `checkboxSelection`, `countRows`, `crudOperationsDisplayed`.
- Form: DataField per input, Groups summing to 12; widget attrs per type (§7).
- View: flat fields top; Groups; TabBar for tabs; to-many as TRF; consider `titleFrom=ATTRIBUTE` + `titleAttribute`.
- All dataFeature/relationFeature/operation/hiddenBy/enabledBy/requiredBy/confirmationCondition resolve. col sums ≤12; row>0; sibling names unique.
- Actor: Access (target TO, upper, CRUD flags, getterExpression); MenuItemAccess in MenuItemGroup; `hiddenBy` on menu item → principal permission boolean; Claim on principal TO maps identifier (email/username).

## 14. Pitfalls and validation rules
- Missing `xsi:type` on abstract child → "Class 'Column' / 'Filter' / 'MenuItem' / 'Component' is not found or is abstract". Add correct type (§3).
- Missing `xmlns:ui` on root → same error.
- `xsi:type` on `<form>`/`<table>`/`<view>` → parse errors; remove.
- col sum > 12 → "The minimum width must be less or equal to 12." Redistribute.
- hiddenBy/enabledBy/requiredBy on non-boolean or cross-TO member → validator error.
- OperationForm.operation is a name string, not id; use operation `name`.
- Relation named with generator-reserved name (e.g. `template`) → `TS2393 Duplicate function implementation` at frontend build. Rename; see esm_metamodel/generator-reserved-names.md.
- Duplicate sibling name → validator error.
- TabBar/Stepper with `<components>` instead of `<tabs>`/`<steps>` → not rendered. Children are Groups with no xsi:type.
- `smallTable=true` on single relation TRF → warning/ignored; valid only when `relationFeature.upper=-1`.
- RelationColumn on top-level TransferObjectTable (backing Access/menu) → frontend codegen bug (dangling `View<X>Stored`, e.g. `ViewGalaxyStored`), fragile sort/filter. Fix: TRF inside view/form; or plain DataColumn on mapped scalar DataMember (bound or DERIVED flattening, e.g. `owner.fullName`). Reserve RelationColumn for embedded detail tables.
- Bare `View`/`Form`/`Table` sibling names → FQN collisions (`<package>::View`); non-deterministic output. Rename to `<TO>View`/`<TO>Form`/`<TO>Table` before adding children.
- `minValueBy`/`maxValueBy` inside TableOperation → ignored. Put on non-table DataField.

## 15. Auditing layout completeness across an actor
- Step 1: judo_cli GraphQL query over actortypes → accesses (name, accessType, lower, upper, CRUD flags, target TO table/view/form component counts) and menuItems totalCount.
- Step 2 tiers:
  - P0 dead click: target TO has no `table` → no AccessTablePage.
  - P1 broken create/edit: table cols ≥1 but form missing/0 components while createable or updateable.
  - P2 broken detail: table present, view missing/0 components.
  - P3 skeletal: table.columns totalCount == 1.
  - OK: table cols ≥3, view ≥3, form ≥3 (or absent for read-only).
  - Read-only access (all CRUD false) needs no form; not P1.
- Step 3 menu: menuItems.totalCount == 0 with accesses > 0 → all API-only; add MenuItemAccess per access.
- Step 4 after `./judo.sh build -f`: UI model pagedefinitions `actors::<Actor>::<access>::AccessTablePage` (missing → P0), `AccessFormPage` (missing with create/update → P1), `AccessViewPage` (missing → P2); `navigationitems.totalCount == 0` with accesses → menu missing.
- Step 5: repair order P0 → P1 → P2 → P3 → menu.

## 16. Repairing layout debt at scale
- Workflow: audit → plan tiers → stage (one tier or TO group) → `judo_cli save` → checkpoint commit → `./judo.sh build -f` (delegate to judo-frontend-developer) → `judo_cli discard --derived --force` → verify pagedefinitions → rollback on failure (`git restore model/<app>.model` + `judo_cli discard --force`).
- Stage size: ~80 mutations / 4 TOs workable; 200+ / 15 TOs not.
- Pre-stage: rename ambiguous containers (`TransferObjectView::View` etc.) to `<TO>View`/`<TO>Table`/`<TO>Form` BEFORE children; ambiguous FQN makes create pick a parent non-deterministically.
- Save discipline: `judo_cli save` writes file, does NOT commit; `git restore` discards it. Commit after each save or copy to `.bak`. `judo_cli discard` reverts only since last save — not a rollback for saved stages.
- Final stage: MenuItemAccess creation (`judo_cli graphql "mutation { create(input: { menuItemAccess: { container: \"<package>::actors::<Actor>\", containment: \"menuItems\", name, label, iconName, access: \"<package>::actors::<Actor>.<name>\" }}) { success fqn }}"`). Until then React `menu-items.tsx` is `return [];`.

## 17. Reference-derived elements, custom components and capability rules
- Reference-derived (DataField, DataColumn, ReferenceField, `<Feature>Filter` DataFilter, OperationForm, Inherited* refs): name computed from binding (`dataFeature.member.name`, `…name + "Filter"`, `operation.name`). CLI CreateInput has no `name`; writable: `container`, `containment`, `label`, `documentation`, binding.
- Add DataField to existing view/form: `update <container> --add feature …`; bound to existing MAPPED or TRANSIENT member.
- Embedded table columns/filters may bind member or inherited reference; `EsmUtils.purifyAttribute` rebinds; equivalent.
- TRF `representationComponent="button"` still needs `<columns>` (else warning "Columns are not defined for viewable table").
- CONDITIONAL confirmation: `confirmationCondition` must be boolean attribute of operation's root type; else "Confirmation condition must be an attribute of the root type". EVL rule is authoritative, not selector list.
- Sorting/filtering in generated UI: only for mapped targets with ≥1 non-TRANSIENT attribute of supported type (orderable: string, numeric, date, timestamp, time, boolean; filterable adds enumeration). See model-validation-and-transformation.md.
- Relation table columns belong to relation target TO: `update <viewFqn>::<relation> --add feature --feature <member>`. On page element → "'<member>' is not a feature of <PageTO> placeable here". Also fires when already placed; `valid` list shows placeable only. `fill <TO>` places a column per member.
- `isEager` not an ESM attribute. Set by transformation `true` for AGGREGATION/COMPOSITION relation or when holding page is Form. Eager: rows in memory, no server paging/sort/filter. Other: lazy (server, paged). Embed table: to-many TRF `representationComponent=table` on view; use AGGREGATION/COMPOSITION for eager.
- Eager table rows saved with page: create opens draft (`isDraft`), adds to owner data; server call only on page Update (save). Tests must click page Update. Lazy (association) rows created immediately.
- Custom React component: annotation with prefix `use` (generator param `customComponentAnnotationPrefix`, default `use`), e.g. `useFancyText` on visual element → developer-implemented widget. See frontend/README.md.

## 18. Related documentation
- esm_metamodel/ui.md (attribute dictionary), esm_metamodel/ui-behaviour.md (conditional rules), esm_metamodel/ui-visual-styleguide.md (visual indicators), esm_metamodel/structure.md (DataMember/RelationMember), esm_metamodel/accesspoint.md (ActorType/Access/Claim), advanced-modeling-patterns.md (Dynamic Menu, Polymorphic Creation), esm_metamodel/generator-reserved-names.md, judo-cli.md (CLI mutations), ../frontend/README.md (customizing generated React).
