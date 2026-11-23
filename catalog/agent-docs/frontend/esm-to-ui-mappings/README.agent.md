# README.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/esm-to-ui-mappings/README.md.

## Quick Reference: All UI Elements

- Containers: `TransferObjectView` (detail/edit page), `TransferObjectTable` (list/grid), `TransferObjectForm` (operation input dialog), `Group` (div), `TabBar` (MUI Tabs), `Stepper` (MUI Stepper).
- Widgets: `DataField` (TextField, DatePicker, Checkbox…), `TabularReferenceField` (to-many: table, tags, cards, button), `OperationForm` (action button), `TextField` (static, Typography), `ActionButton` (submit/cancel), `Divider`, `Placeholder`, `Icon`, `ActionGroup` (button group with overflow).
- Table elements: `DataColumn` (MUI DataGrid column), `DataFilter`, `TableOperation`.
- Navigation: `MenuItem` (abstract), `MenuItemAccess` (route to data access), `MenuItemOperation` (static operation), `MenuItemGroup` (collapsible submenu).
- Supertypes decide inherited attributes and behaviour rules; see `../../model/esm_metamodel/ui-behaviour.md`.

## ESM UI Elements

- UI definitions are model elements under the entity type (`ui:` namespace), not annotations: `<form>`, `<table>`, `<view>` children of `structure:EntityType`.

## Entity to UI Mapping

### Entity Structure

- `EntityType.name` → TypeScript interface. `createable` / `updateable` / `deleteable` → action availability (create, edit, delete buttons).

### Attributes (DataMember)

- `name` → field binding. `required="true"` → required indicator. `dataType` → input component.
- `memberType="DERIVED"` → read-only. `memberType="STORED"` → editable.
- `defaultExpression` → pre-populated value. `getterExpression` → computed field.

### Relations (TwoWayRelationMember / OneWayRelationMember)

- `lower="0"` optional, `lower="1"` required indicator. `upper="1"` single (link), `upper="-1"` collection (table).
- `createable` / `updateable` / `deleteable` → `isCreatable` / `isUpdatable` / `isDeletable`.
- `relationKind`: COMPOSITION / AGGREGATION / ASSOCIATION. `target` = related type; `partner` = inverse binding.

### CRUD Flags and UI Element Visibility

- C (`createable`) → Create button in table header. R → always available. U (`updateable`) → fields editable, Attach/Detach buttons. D (`deleteable`) → Delete button on rows.
- Configurations: all false = view only (Filter, Refresh, View button). C only adds Create. U only: edit + Attach/Detach for associations. D only: Delete on rows. All true: full CRUD.
- Association attach/detach uses update flag: Attach links existing entities; Detach unlinks without deleting. COMPOSITION delete removes the entity.

### Parent Flags Affect Child Operations

- Applies when navigating from a grid row, tag, or single relation link to a child.
- Parent `updateable=false`: view-only on the child, regardless of the child's own flags (no edit, no Attach/Detach, no Update).
- Parent `deleteable=false`: no delete on the child.
- Navigation sources: grid row click or view button; tag click; single relation link.

### Runtime Override via JSON Data

- JSON attributes `__updateable` and `__deleteable` override per record (e.g. `"__updateable": false`, `"__deleteable": false`).
- Precedence:
  1. Model flag `false` → disabled, not overridable.
  2. Model flag `true` and `__updateable`/`__deleteable` `false` → disabled for that record.
  3. Model flag `true` and key absent or `true` → enabled.

## Data Types

| ESM type | Attribute | UI model | Component |
|---|---|---|---|
| `StringType` | `maxLength` | StringType | TextField; multiline if `maxLength > 255` |
| `NumericType` | `precision`, `scale` | NumericType | NumericInput |
| `BooleanType` | - | BooleanType | Checkbox |
| `DateType` | - | DateType | DatePicker |
| `TimestampType` | - | TimestampType | DateTimePicker |
| `TimeType` | - | TimeType | TimePicker |
| `BinaryType` | `mimeTypes` | BinaryType | BinaryInput (file) |
| `EnumerationType` | `members` | EnumerationType | Autocomplete/Radio |

- `BinaryInput` is an upload control: shows file name, not a preview. Image preview needs a custom visual element; see `../../../best-practices/frontend/binary-blob-url-hook.md`.

### Enumeration Members

- `members` → option list; member `name` → option value; labels are i18n generated.

## UI Definition Elements

### Form Definition (ui:form)

- `name` → component name; `label` → title; `layout` → VERTICAL/HORIZONTAL; `generateActionsHook`, `generateVisualPropertiesHook` → hook generation.

### View Definition (ui:view)

- `name` → view component; `label` → title; `titleFrom` → LABEL or ATTRIBUTE; `frame` → border/container.

### Table Definition (ui:table)

- `name`, `label`; `rowsPerPage` → `tablePageLimit` (pagination); `checkboxSelection` → ENABLED/DISABLED; `crudOperationsDisplayed` → CRUD button count; `transferOperationsDisplayed`; hook flags.
- Example: `checkboxSelection="ENABLED" rowsPerPage="10" crudOperationsDisplayed="1" transferOperationsDisplayed="0"`.

## UI Container Elements

### TransferObjectView

- Supertypes: Container → FormElement → VisualElement → NamedElement. Single-object detail/edit.
- `titleFrom`: `LABEL` | `ATTRIBUTE`; `titleAttribute` is effective only when `titleFrom=ATTRIBUTE`.
- `openInDialog` opens as dialog; `dialogSize` (`UNDEFINED`/`XS`/`SM`/`MD`/`LG`/`XL`) is effective only when `openInDialog=true`.
- `autoCloseOnSave`: close dialog after save.
- `layout`: `HORIZONTAL`/`VERTICAL`/`DEFAULT`. `horizontal`: `LEFT`/`RIGHT`/`CENTER`/`SPACE_BETWEEN`/`SPACE_AROUND`. `vertical`: `TOP`/`BOTTOM`/`CENTER`/`SPACE_BETWEEN`/`SPACE_AROUND`.
- `frame`: border/card. `components`: fields, groups, tabs. `additionalMaskFeatures`: extra REST query fields. Hook flags.

### TransferObjectTable

- Supertypes: Tabular → VisualElement → NamedElement. List/grid.
- `columns` (DataColumn), `filters` (DataFilter), `rowOperations` (action column), `tableOperations` (toolbar).
- `rowsPerPage` default 10; `selectorRowsPerPage`, `selectorDialogSize` for selector dialogs.
- `checkboxSelection`: `AUTO`/`ENABLED`/`DISABLED`. `countRows`, `isInlineEditable`, `masterDetail`.
- `representationComponent`: `table` | `card`. `actionColumnWidth`. `additionalMaskFeatures`.
- `crudOperationsDisplayed` default 1; `transferOperationsDisplayed` default 0. Hook flags.
- Inherited from Tabular: `columns`, `filters`, `rowOperations`, `tableOperations`, `countRows`, `checkboxSelection`, `isInlineEditable`, `additionalMaskFeatures`.

### TransferObjectForm

- Supertypes: Container → FormElement → VisualElement → NamedElement. Operation input, usually a dialog.
- `name`, `label`, `dialogSize` (same values), `layout`, `horizontal`, `vertical` (same values as View), `frame`, `components`.
- `autoOpenAfterCreate`: open the created element after the operation. Hook flags.
- Inherited from Container: `layout`, `horizontal`, `vertical`, `frame`, `components`, `performableActions`.
