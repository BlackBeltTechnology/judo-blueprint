---
title: ESM to UI Mapping: Tables & Navigation
description: ESM to UI Mapping: Tables & Navigation: ESM to UI model mapping reference for the generated React frontend.
aliases: [table columns mapping, table filters, row operations, menu items mapping, navigation menu model, relation column table, esm annotations frontend]
keywords: [ui:DataColumn, ui:DataFilter, ui:TableOperation, ui:RelationColumn, ui:MenuItemAccess, ui:MenuItemOperation, ui:MenuItemGroup, filterOperationType, confirmationType, generateActionsHook, generateVisualPropertiesHook, TabularReferenceField]
tags: [domain:frontend, layer:frontend, status:platform]
---

# ESM to UI Mapping: Tables & Navigation

**[◄ Widgets](./widgets.md)** | **[Overview](./README.md)**

This document covers table elements, navigation, transformation tracing, and advanced topics.

---

## Table-Specific Elements

These elements are used exclusively within `TransferObjectTable` or `TabularReferenceField`.

### DataColumn (ui:DataColumn)

**Supertypes:** `Column` → `VisualElement` → `NamedElement`

A column within a table displaying a single attribute for each row.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:DataColumn` | `name` *(generated, read-only)* | Column name | Column identifier — runtime value derived from `dataFeature.member.name` by a `getName()` EOperation override; XMI `name="…"` is stored but ignored on read and FQN computation |
| `ui:DataColumn` | `label` | Header text | Column header (i18n) |
| `ui:DataColumn` | `iconName` | Column icon | Header icon |
| `ui:DataColumn` | `dataFeature` | Bound attribute | Data binding |
| `ui:DataColumn` | `width` | Column width | Fixed pixel width |
| `ui:DataColumn` | `flex` | Flex value | Responsive width |
| `ui:DataColumn` | `sortable` | Allow sorting | Sort icon visibility |
| `ui:DataColumn` | `defaultSort` | Initial sort | `ASC`/`DESC`/`NONE` |
| `ui:DataColumn` | `filterable` | Allow filtering | Filter in column menu |
| `ui:DataColumn` | `hidden` | Hidden state | Column not displayed |
| `ui:DataColumn` | `align` | Text alignment | `LEFT`/`CENTER`/`RIGHT` |
| `ui:DataColumn` | `isPinnable` | Allow pinning | Pin column to left/right |
| `ui:DataColumn` | `formatValue` | Apply formatting | Format numeric values: with `true` the generated column uses `new Intl.NumberFormat(<locale>).format(value)` (locale grouping and decimal separators, default fraction digits); with `false` the raw value is shown. The attribute `scale` and currencies are not applied, so `89.9` stays `89.9`. For fixed decimals or a currency use a derived string attribute or a `customImplementation` column |
| `ui:DataColumn` | `customImplementation` | Custom column | Extension point for custom rendering |

**Default Sort Values:**

| Value | Frontend Effect |
|-------|-----------------|
| `ASC` | Ascending sort on initial load |
| `DESC` | Descending sort on initial load |
| `NONE` | No initial sort (default) |

**Example:**
```xml
<columns xsi:type="ui:DataColumn"
  xmi:id="_GHI789"
  name="nameColumn"
  label="Name"
  dataFeature="_nameAttribute"
  width="200"
  sortable="true"
  defaultSort="ASC"
  isPinnable="true"/>
```

### DataFilter (ui:DataFilter)

**Supertypes:** `VisualElement` → `NamedElement`

Filter control for a table, allowing users to search or narrow down results.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:DataFilter` | `name` *(generated, read-only)* | Filter name | Filter identifier — runtime value derived from `dataFeature.member.name + "Filter"` by a `getName()` EOperation override |
| `ui:DataFilter` | `label` | Filter label | Filter label (i18n) |
| `ui:DataFilter` | `iconName` | Filter icon | Input icon |
| `ui:DataFilter` | `dataFeature` | Bound attribute | Filter target |
| `ui:DataFilter` | `filterOperationType` | Filter mode | Comparison type |
| `ui:DataFilter` | `placeholder` | Input hint | Placeholder text |
| `ui:DataFilter` | `defaultValue` | Initial value | Pre-filled filter |
| `ui:DataFilter` | `hidden` | Hidden state | Filter not displayed |
| `ui:DataFilter` | `col` | Grid column | Filter width in grid |

**Filter Operation Types:**

| Type | Frontend Effect |
|------|-----------------|
| `EQUALS` | Exact match filter |
| `NOT_EQUALS` | Not equal filter |
| `LESS_THAN` | Less than comparison |
| `LESS_OR_EQUAL` | Less than or equal |
| `GREATER_THAN` | Greater than comparison |
| `GREATER_OR_EQUAL` | Greater than or equal |
| `LIKE` | Contains/partial match |
| `NOT_LIKE` | Does not contain |
| `RANGE` | From/to range filter |
| `ENUMERATION` | Dropdown selection |
| `BOOLEAN` | Checkbox/toggle |

**Example:**
```xml
<filters xsi:type="ui:DataFilter"
  xmi:id="_JKL012"
  name="statusFilter"
  label="Status"
  dataFeature="_statusAttribute"
  filterOperationType="ENUMERATION"
  col="4"/>
```

Known defects in the generated filter UI and helpers:

- Operator labels in the filter dialog use the keys `judo.modal.filter.<operator>` with default `Operation`; add the operator keys to i18n, or every untranslated operator shows `Operation`.
- A boolean filter stores `!!event.target.value`. A checkbox's value is `on` even when unchecked, so unchecking does not switch the filter off. Verify boolean filters after unchecking.
- The single-value filter component uses `enumValues` in its `useCallback` body but not in its dependency list, so changed enumeration values are not picked up. It also pushes into `filters?.filter(...)`, which is `undefined` when `filters` is `undefined`, so it throws when the filter has a value; initialise the filter array in a custom hook.
- In-memory filtering (`applyInMemoryFilters`) passes the original `data` to every filter instead of the accumulated result, so only the last filter applies. Verify each filter result in the generated table.
- The enumeration operator lookups (`getOperationEnumValue`, `getOperation`) cast to `keyof typeof _BooleanOperation`. Both operation enums define the same four keys, so this is a type-level mistake with no runtime effect today.
- The default operation lookup passes the enum value `equal` and then reads the enum by key, so it resolves to `undefined`.

### TableOperation (ui:TableOperation)

**Supertypes:** `PerformableAction` → `VisualElement` → `NamedElement`

An action that can be performed on table rows (row-level operations) or as bulk operations.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:TableOperation` | `name` | Operation name | Action identifier |
| `ui:TableOperation` | `label` | Button text | Action label (i18n) |
| `ui:TableOperation` | `iconName` | Icon | Action icon |
| `ui:TableOperation` | `operation` | Target operation | Operation binding |
| `ui:TableOperation` | `isBulk` | Bulk scope | Enable for multi-select |
| `ui:TableOperation` | `variant` | Button style | contained/outlined/text |
| `ui:TableOperation` | `hiddenBy` | Hidden condition | DataFeature controlling visibility |
| `ui:TableOperation` | `enabledBy` | Enabled condition | DataFeature controlling enabled state |
| `ui:TableOperation` | `operationForm` | Nested form | Form configuration for parameters |
| `ui:TableOperation` | `confirmationType` | Confirmation | `NONE`/`CONDITIONAL`/`MANDATORY` |
| `ui:TableOperation` | `confirmationMessage` | Confirmation text | Message in confirmation dialog |
| `ui:TableOperation` | `confirmationCondition` | Confirmation condition | Boolean DataFeature |

**Label of a row action.** The row action button shows the label of the button element nested in the operation's form element, not the label of the `TableOperation` itself. With the CLI the element is named `<ns>::<Entity>_Table::<op>TableOperation::<op>`:

```bash
java -jar target/judo-cli.jar -m <model> update '<ns>::<Entity>_Table::<op>TableOperation::<op>' -s "label=<Text>"
```

**Context:** TableOperations are placed in either `rowOperations` or `tableOperations` container:
- `rowOperations` - Appears in row action menu, operates on single row
- `tableOperations` - Appears in table toolbar, can be bulk operations

**Example:**
```xml
<rowOperations xsi:type="ui:TableOperation"
  xmi:id="_MNO345"
  name="deleteAction"
  label="Delete"
  iconName="delete"
  operation="deleteOperation"
  confirmationType="MANDATORY"
  confirmationMessage="Delete this record?"/>

<tableOperations xsi:type="ui:TableOperation"
  xmi:id="_BLK456"
  name="bulkExport"
  label="Export Selected"
  iconName="download"
  operation="exportOperation"
  isBulk="true"/>
```

### RelationColumn (ui:RelationColumn)

**Supertypes:** `Column` → `VisualElement` → `NamedElement`

A column within a table displaying a relation (link to related entity).

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:RelationColumn` | `name` *(generated, read-only)* | Column name | Column identifier — runtime value derived from `relationFeature` by a `getName()` EOperation override; identity for the GraphQL surface is `dataFeatureOfRelationFeature` |
| `ui:RelationColumn` | `label` | Header text | Column header (i18n) |
| `ui:RelationColumn` | `iconName` | Column icon | Header icon |
| `ui:RelationColumn` | `relationFeature` | Bound relation | Relation binding |
| `ui:RelationColumn` | `width` | Column width | Fixed pixel width |
| `ui:RelationColumn` | `flex` | Flex value | Responsive width |
| `ui:RelationColumn` | `sortable` | Allow sorting | Sort icon visibility |
| `ui:RelationColumn` | `hidden` | Hidden state | Column not displayed |
| `ui:RelationColumn` | `align` | Text alignment | `LEFT`/`CENTER`/`RIGHT` |
| `ui:RelationColumn` | `attributePath` | Display path | Attribute to show from related entity |
| `ui:RelationColumn` | `customImplementation` | Custom column | Extension point |

**Example:**
```xml
<columns xsi:type="ui:RelationColumn"
  xmi:id="_REL123"
  name="customerColumn"
  label="Customer"
  relationFeature="_customerRelation"
  attributePath="name"
  width="200"/>
```

**When not to use `RelationColumn`.** Avoid `RelationColumn` on **top-level** `TransferObjectTable`s — the tables that back an `Access` / `MenuItemAccess` and render as a primary list screen. At this level `RelationColumn` triggers a **frontend codegen bug**: the generated list screen references a non-existent sibling (observed symptom: dangling `View<RelatedType>Stored`-style refs, e.g. `ViewGalaxyStored`), and sorting / filtering / row-action wiring on relation-typed columns is unreliable. Instead:

1. **Prefer `TabularReferenceField`** in the owning `<view>` or `<form>` when the user needs to navigate or manage the related collection — this is the canonical widget for relation display inside a detail screen.
2. **Prefer a plain `DataColumn`** bound to a mapped `DataMember` (either a bound string attribute or a `DERIVED` attribute whose `getterExpression` flattens the related value, e.g. `self.owner.fullName`) when you only need to *display* a label from the related entity in the list.

Reserve `RelationColumn` for embedded relation tables inside detail screens where relation-navigation semantics are explicitly expected. See also [UI Authoring Guide — Pitfalls](../../model/ui-authoring-guide.md#14-pitfalls-and-validation-rules).

### Row Click and Default Labels

- **Row click.** When a table's row actions include an open-page action, the generated table passes it as `onRowClick`, so clicking a row opens that page (the view page for a mapped table); such an action is not rendered as a row button. Other row operations (`rowOperations`) appear as buttons in the action column.
- **Default labels.** An element without a `label` gets a default derived from the transfer object name, for example `<Entity>Info Table` for the table page and `<Entity>Info View / Edit` for the view page. Page titles, menu entries and the phone bottom bar show the label, so set `label` on the table, view and menu item (or provide i18n keys) to show user-facing text:

```bash
java -jar target/judo-cli.jar -m <model> update '<ns>::<Entity>Info_Table' -s "label=<Text>"
```

---

## Navigation Elements

These elements define the application's navigation structure.

### MenuItem (ui:MenuItem) - Abstract

**Supertypes:** `VisualElement` → `NamedElement`

Abstract base class for menu items. Use concrete subclasses `MenuItemAccess` or `MenuItemOperation`.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:MenuItem` | `name` | Menu item name | Route identifier |
| `ui:MenuItem` | `label` | Display text | Menu label (i18n) |
| `ui:MenuItem` | `iconName` | Icon | Menu icon |
| `ui:MenuItem` | `hidden` | Hidden state | Not displayed |
| `ui:MenuItem` | `order` | Sort order | Menu position |

### MenuItemAccess (ui:MenuItemAccess)

**Supertypes:** `MenuItem` → `VisualElement` → `NamedElement`

Menu item that navigates to an Access (data table/view).

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:MenuItemAccess` | `name` | Menu item name | Route identifier |
| `ui:MenuItemAccess` | `label` | Display text | Menu label (i18n) |
| `ui:MenuItemAccess` | `iconName` | Icon | Menu icon |
| `ui:MenuItemAccess` | `access` | Target access | Link to data table/view |
| `ui:MenuItemAccess` | `hidden` | Hidden state | Not displayed |
| `ui:MenuItemAccess` | `order` | Sort order | Menu position |

**Example:**
```xml
<menuItems xsi:type="ui:MenuItemAccess"
  xmi:id="_PQR678"
  name="customersMenu"
  label="Customers"
  iconName="people"
  access="_customersAccess"
  order="1"/>
```

### MenuItemOperation (ui:MenuItemOperation)

**Supertypes:** `MenuItem` → `VisualElement` → `NamedElement`

Menu item that triggers a static operation.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:MenuItemOperation` | `name` | Menu item name | Action identifier |
| `ui:MenuItemOperation` | `label` | Display text | Menu label (i18n) |
| `ui:MenuItemOperation` | `iconName` | Icon | Menu icon |
| `ui:MenuItemOperation` | `targetOperation` | Target operation | Static operation binding |
| `ui:MenuItemOperation` | `hidden` | Hidden state | Not displayed |
| `ui:MenuItemOperation` | `order` | Sort order | Menu position |

**Example:**
```xml
<menuItems xsi:type="ui:MenuItemOperation"
  xmi:id="_OPR678"
  name="syncMenu"
  label="Sync Data"
  iconName="sync"
  targetOperation="_syncOperation"
  order="5"/>
```

### MenuItemGroup (ui:MenuItemGroup)

**Supertypes:** `MenuItem` → `VisualElement` → `NamedElement`

A container for creating sub-menus within the main navigation.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:MenuItemGroup` | `name` | Group name | Submenu identifier |
| `ui:MenuItemGroup` | `label` | Display text | Submenu header (i18n) |
| `ui:MenuItemGroup` | `iconName` | Icon | Submenu icon |
| `ui:MenuItemGroup` | `items` | Child items | Nested MenuItem list |
| `ui:MenuItemGroup` | `hidden` | Hidden state | Not displayed |
| `ui:MenuItemGroup` | `order` | Sort order | Menu position |
| `ui:MenuItemGroup` | `collapsed` | Initial state | Collapsed by default |
| `ui:MenuItemGroup` | `orientation` | Menu direction | `HORIZONTAL`/`VERTICAL` |

**Example:**
```xml
<menuItems xsi:type="ui:MenuItemGroup"
  xmi:id="_STU901"
  name="settingsMenu"
  label="Settings"
  iconName="settings"
  order="10">
  <items xsi:type="ui:MenuItemAccess" name="usersMenu" label="Users" access="_usersAccess"/>
  <items xsi:type="ui:MenuItemAccess" name="rolesMenu" label="Roles" access="_rolesAccess"/>
</menuItems>
```

---

## Transformation Tracing

UI model elements contain ESM xmi:id references in their IDs:

```
UI Element ID: Actor/(esm/_ZeK4oLK0EfCC_efogf7jJg)/AttributeType
                     └── ESM xmi:id reference ──┘
```

### Tracing Example

**Goal:** Trace `code` attribute from ESM to frontend

1. **ESM Source** (`model/\<app>.model`):
```xml
<elements xsi:type="structure:EntityType" name="Activity">
  <attributes xsi:type="structure:DataMember"
    xmi:id="_ZeK4oLK0EfCC_efogf7jJg"
    name="code"
    required="true"/>
</elements>
```

2. **UI Model** (`application/frontend-react/model/\<app>-ui.model`):
```xml
<attributes xmi:id="Actor/(esm/_ZeK4oLK0EfCC_efogf7jJg)/AttributeType"
  name="code"
  isRequired="true"/>
```

3. **Generated Frontend** (TextField with required validation)

## ESM Annotations

ESM supports annotations that can be applied to Access elements. Annotations are defined at the model root level and referenced by elements.

### Annotation Definition (ESM)

Annotations are defined at the model root level in `model/\<app>.model`:

```xml
<annotations xmi:id="_08mnIGStEeuRaM6aPF_6_w"
  name="dashboard"
  className="hu.blackbelt.judo.meta.esm.accesspoint.Access"/>
<annotations xmi:id="_yVrvIGUkEeuRaM6aPF_6_w"
  name="profile"
  className="hu.blackbelt.judo.meta.esm.accesspoint.Access"/>
```

### Available Annotation Types in This Project

| Annotation Name | className | Purpose |
|----------------|-----------|---------|
| `dashboard` | `hu.blackbelt.judo.meta.esm.accesspoint.Access` | Marks access as dashboard entry point |
| `profile` | `hu.blackbelt.judo.meta.esm.accesspoint.Access` | Marks access as user profile entry |

**Note:** These annotations are defined in the model but are currently **not applied to any elements** in the \<app> project.

### How Annotations Would Be Used

When annotations are applied, elements reference them via `annotations` attribute:

```xml
<!-- Hypothetical usage - not present in current model -->
<accesses xmi:id="..."
  name="someAccess"
  annotations="_08mnIGStEeuRaM6aPF_6_w"
  .../>
```

### Transformation to UI Model

ESM annotations become `availableAnnotations` in the UI model:

```xml
<availableAnnotations xmi:id="Actor/(esm/_08mnIGStEeuRaM6aPF_6_w)/Annotation" name="dashboard"/>
<availableAnnotations xmi:id="Actor/(esm/_yVrvIGUkEeuRaM6aPF_6_w)/Annotation" name="profile"/>
```

When elements have annotations, they would appear as:
```xml
<relations xmi:id="..."
  annotations="Actor/(esm/_08mnIGStEeuRaM6aPF_6_w)/Annotation"
  .../>
```

### Frontend Usage

When annotations are applied to elements, they are passed to components:

```tsx
<ComponentProxy
  ...
  annotations={['dashboard']}  // Array of annotation names
>
```

Helper functions for working with annotations:
- `getAnnotationNamesForElement(element)` - Get all annotation names for an element

## Hook Generation

| ESM Attribute | Generated Hook | Purpose |
|---------------|----------------|---------|
| `generateActionsHook="true"` | scaffold `src/custom/hooks/{pages,dialogs,containers}/register<Name>ActionsHook.ts.default` | [Custom action implementations](../hooks/action-hooks.md#container-actions) |
| `generateVisualPropertiesHook="true"` | `is<Field>Hidden`, `is<Field>Disabled`, `is<Field>Readonly`, `is<Field>Required` handlers in the generated container hook type | [Hook scaffolds and container hook names](../hooks/action-hooks.md#container-actions) |
| Widget `onBlur="true"` | `on{Field}BlurAction` handler in the container hook type | Field blur event handler |

## Supertype Inheritance and Behaviour

Understanding the supertype hierarchy is essential for determining which attributes are available on each element and what behaviour is inherited.

### Inheritance Hierarchy

```
NamedElement
├── VisualElement
│   ├── FormElement
│   │   ├── Component
│   │   │   ├── Widget
│   │   │   │   ├── DataField
│   │   │   │   ├── ReferenceField
│   │   │   │   │   └── TabularReferenceField (also extends Tabular)
│   │   │   │   ├── Divider
│   │   │   │   ├── Placeholder
│   │   │   │   ├── Icon
│   │   │   │   └── Container
│   │   │   │       ├── Group
│   │   │   │       ├── TabBar
│   │   │   │       ├── Stepper
│   │   │   │       ├── TransferObjectForm
│   │   │   │       └── OperationForm
│   │   │   └── Page
│   │   │       ├── TransferObjectView
│   │   │       └── TransferObjectTable (also extends Tabular)
│   │   └── ActionButton
│   ├── Column
│   │   ├── DataColumn
│   │   └── RelationColumn
│   ├── DataFilter
│   ├── PerformableAction
│   │   └── TableOperation
│   ├── ActionGroup
│   └── MenuItem
│       ├── MenuItemAccess
│       ├── MenuItemOperation
│       └── MenuItemGroup
└── Tabular (mixin)
    ├── TransferObjectTable
    └── TabularReferenceField
```

### Inherited Attributes by Supertype

| Supertype | Inherited Attributes |
|-----------|---------------------|
| `NamedElement` | `name` |
| `VisualElement` | `label`, `iconName`, `customImplementation` |
| `FormElement` | (marker interface) |
| `Component` | `col`, `row`, `hiddenBy`, `enabledBy`, `requiredBy` |
| `Widget` | `onBlur` |
| `Container` | `components` (child widgets) |
| `Page` | `actionGroup`, `additionalMaskFeatures`, `generateVisualPropertiesHook`, `generateActionsHook` |
| `Tabular` | `columns`, `filters`, `rowOperations`, `tableOperations`, `countRows`, `checkboxSelection`, `isInlineEditable` |
| `ReferenceField` | `relationFeature` |
| `PerformableAction` | `operation`, `confirmationType`, `confirmationMessage`, `confirmationCondition` |

### Behaviour Implications

1. **Components** (`col`, `row`): Grid layout positioning with 12-column grid
2. **Widgets** (`onBlur`): Can trigger update actions on blur
3. **Containers** (`components`): Can contain nested UI elements
4. **Pages** (`actionGroup`): Have page-level actions and toolbar
5. **Tabular** (`columns`, `filters`): Support tabular data display with filtering and sorting
6. **PerformableAction** (`confirmationType`): Can show confirmation dialogs

### Type-Specific Behaviour

DataField behaviour varies based on the bound attribute's data type:
- **StringType**: `textWidget`, `textMultiLine`, `textMask`, `isTypeAheadField`
- **EnumerationType**: `enumWidget` (RADIO/COMBO/TOGGLE_BUTTONBAR)
- **NumericType**: `formatValue`, `minValueBy`, `maxValueBy`
- **BooleanType**: `booleanWidget` (CHECKBOX/COMBO), `valueLabelPlacement`
- **DateType/TimestampType/TimeType**: `minValueBy`, `maxValueBy`

See [UI Element Behaviour Rules](../../model/esm_metamodel/ui-behaviour.md) for complete conditional rules.

---

## Related Documentation

- [UI Element Behaviour Rules](../../model/esm_metamodel/ui-behaviour.md) - Conditional attribute rules and validation
- [ESM UI Package Reference](../../model/esm_metamodel/ui.md) - Complete UI element definitions
- [UI Authoring Guide](../../model/ui-authoring-guide.md) - Authoring playbook for ESM UI scaffolds
- Use `judo-model-cli` skill for model queries and tracing
