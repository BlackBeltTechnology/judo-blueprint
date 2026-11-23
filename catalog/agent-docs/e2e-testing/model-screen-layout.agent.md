# model-screen-layout.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/model-screen-layout.md.

## Overview
- Generator emits UI model (`*-ui.json`): navigation, pages (Form, Table, View/Edit), page containers, actions.
- Generator also emits `VisualElementIds.ts`: constants mapping model element IDs to rendered components. Use them with `getByTestId()`.

## Navigation via Actor Accesses
- Sidebar menu shows Actor accesses only, not entity links. Each Actor access = menu item; nested accesses need hierarchical navigation in tests.
- `hiddenBy`, `enabledBy`, `requiredBy` boolean attributes hide/enable menu items and tabs; backend interceptors can drive them.
- Dynamic access tests: cover permitted and restricted scenarios.

## ID Format Structure
- Pattern: `{Actor}/(esm/_{UniqueModelId})/ElementType`. Example: `God/(esm/_<id>)/TransferObjectFormPageContainer`.
- Parts: Actor (role context), UniqueModelId (EMF/XMI id), ElementType (UI component type).

## Multi-Actor Applications
- Each actor has its own VisualElementIds namespace with actor prefix.
- Actor types: Anonymous (no auth), With Realm (realm isolation), Same Realm (shares realm), Other Realm (separate realm).

## Page Container Types
- Dashboards: `EmptyDashboardPageContainer` (no widgets), `DashboardPageContainer` (configurable widgets). Landing page per actor.
- Form (`TransferObjectFormPageContainer`): create entity. Export names `_Form`.
- Table (`TransferObjectTablePageContainer`): list in data grid; inner `TransferObjectTableTable`; column ids `TableColumn/(discriminator/...)`, filter ids `TableColumnFilter/...`. Export `_Table`.
- View/Edit (`TransferObjectViewPageContainer`): view and edit; embedded relations appear as tables inside. Export `_View_Edit` or `_View`.
- Page `pageActions` is a `TransferObjectFormButtonGroup` with `back`, `create` etc.

## Field Element Types
- Primitive suffixes: String → `StringTypeTextInput`; multiline → `StringTypeTextArea`; read-only → `StringTypeFormatted`; Boolean → `BooleanTypeCheckbox`; Numeric and Double → `NumericTypeVisualInput`; Date → `DateTypeInput`; Timestamp → `TimestampTypeDateTimeInput`; Time → `TimeTypeTypeTimeInput`; Binary → `BinaryTypeInput`; Email → `StringTypeTextInput` (with validation).
- Enumeration: `EnumerationTypeToggleButtonbar`, `EnumerationTypeCombo`, `EnumerationTypeRadio`.
- Layout: `DividerVisualElement` (optional label), `TextFieldVisualElement` (static text), `PlaceholderVisualElement`, `TabBarVisualElement`.
- Tree shape: flex containers stay as branch nodes; tables put columns under `columns` (e.g. `dataTable.columns.nameColumn`), same for filters, `toolbarActions`, `rowActions`.
- Tab elements have boolean `tabElement` (via `setTabElement(true)`) and `tab` property; not tagged with `tab` category.
- Only dialog suffix emitted: `-dialog-title` (on filter leaves). `-action-confirm`, `-action-cancel`, `-dialog-close-wrapper` are NOT generated.
- Tab Bar: group fields into tabs; each tab item keeps its own element type (field, link, embedded table).

### Relation Types
- Single link: `TabularReferenceFieldRelationDefinedLink`.
- Multiple table (1:N): `TabularReferenceFieldRelationDefinedTable`.
- Button: `TabularReferenceFieldButton` (opens relation in new page).
- Tag/chip: `TabularReferenceFieldRelationDefinedTable` rendered as chips.
- Categories: Composition (create/delete/view/edit; cascade delete), Aggregation (add/remove/view), Association (set/unset/view), Derived (filter/refresh/view only), Transient (runtime only).
- Recursive relations to same type form trees; derived relations have limited actions.

## Action Types
- Page actions: Back `*BackButton`, Create `*CreateButton`, Update `*UpdateButton`, Delete `*DeleteButton`, Cancel `*CancelButton`, Refresh `*RefreshButton`.
- Table actions: Filter `*FilterButton`, Refresh, Export `*ExportButton`, Create, Add `*AddSelectorButton`, Set `*SetSelectorButton`, Clear `*ClearButton`, BulkRemove `*BulkRemoveButton`, BulkDelete `*BulkDeleteButton`, InlineCreate `TabularReferenceTableInlineCreateButton`.
- Row actions: `*RowViewButton`, `*RowRemoveButton`, `*RowDeleteButton`.
- Custom operations: `OperationFormVisualElement` (operation button), `ActionButtonVisualElement` (Ok/Cancel), `OperationFormCallButton` (submit of operation form).
- Operation with input shows a form first; operation without input runs immediately.
- Row-level operations appear in a per-row dropdown; the same operation can be reused on multiple relation tables with different discriminators.
- Embedded table actions use `TabularReferenceTable*` prefix: Filter, Refresh, Export, Create, `AddSelectorOpenButton`, Clear, BulkRemove, BulkDelete, RowView, RowRemove, RowDelete.

## Static/Menu Operations
- Operations not bound to an entity appear as menu buttons on dashboard or navigation.
- Input/output combinations: None/None (fire-and-forget); None/Mapped TO (returns data); Unmapped TO/Mapped TO (form input); Mapped TO/Mapped TO (selector input); Entity/Entity.

## Operations with Selector Input
- Operation requiring an existing entity opens a table selector modal (selector button pattern).

## Operations with Confirmation Dialog
- Some operations show a confirmation dialog before execution; test conditional dialogs.

## Inline Edit Tables
- Tables can create/edit rows inline (inline create button).
- Inline inputs: String → text; Date → date picker; Double/Numeric → number; Email → email; Enumeration → dropdown; Boolean → checkbox.

## Embedded Table Row Operations
- Row operations on embedded tables in view/edit pages for context-specific actions on related entities.

## Tag/Chip Components
- Same base ID as tables, rendered as chips for compact many-to-many display.
- Tag: horizontal chip list, click to remove, autocomplete add, clear-all bulk. Table: grid, row selection, add modal, toolbar bulk. Tags suit simple references; tables suit many fields per item.

## Selected Target Pattern
- Single relation (1:1, N:1): "Set" selector opens a table to choose the target.

## Single Relation Link Actions
- Link (`TabularReferenceFieldRelationDefinedLink`) has a dropdown menu and direct actions for CRUD on the single relation.

## Association Table Pattern
- Inline association tables add existing entities to a relation without creating new ones.

## Using VisualElementIds in Tests
- Import specific page constants (e.g. `EntityName_Form`, `_Table`, `_View_Edit`) from `VisualElementIds`.
- Select with `page.getByTestId(CONST._id)` or `CONST.field.id`.
- Frontend renders these IDs as `data-testid`.
- Test form validation and table interactions through constants.

## Naming Conventions
- Export names: `{FeatureGroup}{TransferObjectName}{TransferObjectName}_{PageType}`.
- Page types: `_Form` (create), `_Table` (list), `_View_Edit` / `_View`.
- Special case: `GodDashboard` for dashboards.

## Relation Discriminators
- Table columns and filters in embedded tables carry a discriminator (`discriminator/Actor/(esm/_tableId)/...`) so same-named fields in different tables stay unique.

## Best Practices
- Import only needed page constants.
- Prefer `getByTestId()` with constants over text selectors.
- Check element existence before interacting with optional elements.
- Combine with `TableHelper` for MUI DataGrid.
- Use `ApiHelper` to wait for API calls after button clicks.

## See Also
- Writing tests, Helpers reference (TableHelper, ApiHelper), Testing patterns.
