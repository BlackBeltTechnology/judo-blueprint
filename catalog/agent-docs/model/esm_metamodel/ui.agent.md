# ui.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/esm_metamodel/ui.md.

## Quick Reference: All UI Elements
- Containers: TransferObjectView, TransferObjectTable, TransferObjectForm, Group, TabBar, Stepper.
- Widgets: DataField, TabularReferenceField, OperationForm, TextField, ActionButton, Divider, Placeholder, Icon, ActionGroup.
- Table elements: DataColumn, DataFilter, TableOperation (also RelationColumn, see Table-Specific Elements).
- Navigation: MenuItemAccess, MenuItemOperation, MenuItemGroup.
- Abstract: VisualElement, Container, Component, Widget, FormElement, Tabular, SwitchView, ReferenceField, Column, Filter, MenuItem.

## Supertype Quick Reference
- Use the table to decide which behaviour rules from ui-behaviour apply.
- View/Form: Container → FormElement → VisualElement. Table: Tabular → VisualElement.
- Group: Container + Component. TabBar/Stepper: SwitchView → Component.
- Widgets (DataField, TextField, ActionButton, Divider, Placeholder, Icon): Widget → Component.
- OperationForm/ActionGroup: Widget + PerformableAction. TabularReferenceField: Tabular + ReferenceField (+ Widget + PerformableAction).
- DataColumn/RelationColumn: Column. DataFilter: Filter. TableOperation: VisualElement. MenuItem*: MenuItem.

## UI Containers
### TransferObjectView
- Detail screen to view/edit one object. `titleFrom` (`LABEL`/`ATTRIBUTE`), `titleAttribute` (used when ATTRIBUTE).
- `dialogSize` (`UNDEFINED`/`XS`/`SM`/`MD`/`LG`/`XL`); `openInDialog`; `autoCloseOnSave`.
- `layout` (`HORIZONTAL`/`VERTICAL`/`DEFAULT`); `frame`; `horizontal`/`vertical` alignment.
- `components` (children); `additionalMaskFeatures`; `generateActionsHook`, `generateVisualPropertiesHook`.
### TransferObjectTable
- List/grid/cards. `columns` (DataColumn), `filters`, `rowOperations`, `tableOperations` (toolbar).
- `rowsPerPage` (default 10), `selectorRowsPerPage`, `selectorDialogSize`.
- `checkboxSelection` (`AUTO`/`ENABLED`/`DISABLED`); `masterDetail`.
- `representationComponent` (`TableRepresentation`: `table`, `tag`, `card`).
- `countRows`, `isInlineEditable`, `actionColumnWidth`, `crudOperationsDisplayed` (default 1), `transferOperationsDisplayed` (default 0), `additionalMaskFeatures`, hook flags.
### TransferObjectForm
- Input parameters of an operation, often in dialogs. `label` = dialog title; `dialogSize`; `layout`; `frame`; alignment; `components`; `autoOpenAfterCreate`; hook flags.
### Group
- Visual grouping: `layout`, `frame`, `col` (1-12), `label`, `components`, `hidden` (default hidden).
### TabBar
- `orientation` (HORIZONTAL/VERTICAL), `tabs` (Group[] = tab panels).
- Tab panel (child Group): `label`, `iconName`, `components`.
### Stepper
- `orientation`, `linear` (no step skipping), `steps` (Group[]).
- Step panel (child Group): `label`, `optional` (skippable), `components`.

## UI Components & Widgets
- Bound controls; almost always bound to structure or operation feature.
### DataField
- Generated `name`: `getName()` override returns `dataFeature.member.name`; stored XMI `name` ignored on read; read-only in GraphQL create input and dropped on update.
- `dataFeature` (DataMember), `label`, `iconName`, `col`, `row` (textarea rows), `stretch` (`NONE`/`HORIZONTAL`/`VERTICAL`/`BOTH`), `fit` (`LOOSE`/`TIGHT`).
- `hiddenBy`, `enabledBy`, `requiredBy`, `minValueBy`, `maxValueBy` (DataFeature refs); `onBlur` (generates `on{Field}BlurAction`); `tooltipText`.
- Widget attributes: `enumWidget` (`COMBO`/`RADIO`/`TOGGLE_BUTTONBAR`); `textWidget` (`TEXT`/`INPUT`); `textMultiLine`; `textMask`; `textCountCharacters`; `booleanWidget` (`CHECKBOX`/`COMBO`); `formatValue`; `isTypeAheadField`; `valueLabelPlacement` (`TOP`/`START`/`BOTTOM`/`END`/`DEFAULT`).
### TabularReferenceField
- To-many (or to-one) relation widget; relation binding, representation (table/tag/card/button), selector and paging attributes (see widgets companion for frontend behaviour).
- Contains `columns`, `filters`, `rowOperations`, `tableOperations`, `checkboxSelection`, `selectorDialogSize`, `additionalMaskFeatures`.
### OperationForm
- Generated `name`: `getName()` returns `operation.name` (fallback stored `name`); identity is the `operation` reference; dropped on update in GraphQL.
- `operation` binding (by name); `confirmationType` (`NONE`/`CONDITIONAL`/`MANDATORY`); `components` nested.
### TextField
- Static, unbound text; `variant`. Not bound to data.
### ActionButton
- `action`: `SUBMIT` (save), `CANCEL` (close/back, no save), `VIRTUAL` (default: only runs its own PerformableAction); `variant` (`contained`/`outlined`/`text`).
### Divider
- Horizontal separator; optional centred label.
### Placeholder
- Reserves layout space; no visible content.
### Icon
- Standalone icon; no text or interaction.
### ActionGroup
- Groups operation buttons (`actions`: OperationForm[]); overflow menu behaviour.

## Table-Specific Elements
### DataColumn
- Shows one attribute per row. Bound to DataMember (`dataFeature`). `sort` (`NONE`/`ASC`/`DESC`).
- Generated `name` from `dataFeature.member.name` (same rule as DataField).
- Derived attributes are sortable/filterable like stored ones.
- XMI gotcha: `<columns>` typed as abstract `Column`; each child needs `xsi:type="ui:DataColumn"` (or `ui:RelationColumn`) and root must declare `xmlns:ui="http://blackbelt.hu/judo/meta/esm/ui"`; else "Class 'Column' is not found or is abstract". Same for other abstract containments.
- TS2393 "Duplicate function implementation" = relation named like a generator factory method (see generator reserved names).
### RelationColumn
- Shows a scalar on a related TO. Required: `relationFeature` (OneWay/TwoWay RelationMember on row TO) AND `dataFeatureOfRelationFeature` (DataMember on the target). Setting only `relationFeature` passes CLI but fails the build-time ESM validator.
- Optional: `name`, `label`, `width` (CSS), `visible` (default true), `sort`.
- Do NOT place on a top-level TransferObjectTable (backing an Access/menu): generated row types break (`ViewXStored` missing). Alternatives: put a TabularReferenceField (button for to-one, table for to-many) in the view; or add a DERIVED DataMember (e.g. `partnerName <- partner.name`) and use a plain DataColumn.
- Reserve for tables embedded in a detail screen.
### DataFilter
- Filter control: `dataFeature`, `label`, `defaultOperation`, `col` (default 12), `row`, `fit`, `stretch`.
- `range` (from/to, default false); `multiValue` (default false); `alwaysShown` (toolbar, default false); `filterReference`; `iconName`.
- FilterOperationType: `EQUAL`, `NOT_EQUAL`, `IS_EMPTY`, `IS_NOT_EMPTY`, `LESS`, `LESS_OR_EQUAL`, `GREATER`, `GREATER_OR_EQUAL`, `LIKE` (pattern/contains).
### TableOperation
- Row or table level action, bound to `operation` (Operation); `operationForm` contained config; `iconName`.
- Placed in `rowOperations` (row) or `tableOperations` (toolbar).

## Navigation Elements
- MenuItem is abstract; concrete: MenuItemAccess, MenuItemOperation, MenuItemGroup.
### MenuItemAccess
- Navigates to an access point (`accesspoint:Access`) → table/view screen.
### MenuItemOperation
- Triggers a static operation from the menu (may open input form via `operationForm`).
### MenuItemGroup
- Sub-menu container; `menuItems` (MenuItemAccess / MenuItemOperation / nested MenuItemGroup).

## Common Attributes
- Layout: `col` (1-12, all widgets), `row` (DataField), `layout` (Group, Form), `frame` (View, Group).
- Visibility: `hidden` (all elements), `disabled` (interactive elements).
- Style: `iconName` (widgets), `variant` (buttons), `dialogSize` (View, Form).
- Hook generation: `generateActionsHook` (`use{Container}Actions`), `generateVisualPropertiesHook` (`use{Container}VisualProps`) for View, Table, Form; `onBlur` (`on{Field}BlurAction`, DataField).

## Enumerations
- Layout: `HORIZONTAL`, `VERTICAL`, `DEFAULT` (parent direction).
- DialogSize: `UNDEFINED`, `XS`, `SM`, `MD`, `LG`, `XL`.
- CheckboxSelection: `AUTO`, `ENABLED` (show checkboxes), `DISABLED`.
- TitleFrom: `LABEL`, `ATTRIBUTE`.
- EnumWidget: `COMBO`, `RADIO`, `TOGGLE_BUTTONBAR`. TextWidget: `TEXT` (read-only), `INPUT`. BooleanWidget: `CHECKBOX`, `COMBO` (Yes/No).
- Action: `SUBMIT`, `CANCEL`, `VIRTUAL` (default).
- Justify: `DEFAULT`, `START`, `END`, `CENTER`, `SPACE_BETWEEN`, `SPACE_AROUND`. Align: `DEFAULT`, `STRETCH`, `START`, `END`, `CENTER`.
- Horizontal: `LEFT`, `RIGHT`, `CENTER`, `SPACE_BETWEEN`, `SPACE_AROUND`. Vertical: `TOP`, `BOTTOM`, `CENTER`, `SPACE_BETWEEN`, `SPACE_AROUND`.
- Stretch: `NONE`, `HORIZONTAL`, `VERTICAL`, `BOTH`. Fit: `LOOSE` (standard), `TIGHT` (reduced). Padding: `YES`, `NO`.
- Placement: `TOP`, `START`, `BOTTOM`, `END`, `DEFAULT`. TabOrientation and MenuOrientation: `HORIZONTAL`, `VERTICAL`.
- ConfirmationType: `NONE`, `CONDITIONAL`, `MANDATORY`. ColumnSort: `NONE`, `ASC`, `DESC`.
- FilterOperationType (see DataFilter). RepresentationComponent: `table`, `tag`, `card`, `button`.

## Element Hierarchy
- Inheritance: VisualElement → FormElement → Container (View, Form, Group) / Component → Widget (all widgets; ReferenceField → TabularReferenceField) / SwitchView (TabBar, Stepper). VisualElement → Tabular (TransferObjectTable, TabularReferenceField), Column (DataColumn), Filter (DataFilter), TableOperation, MenuItem.
- Containment: View → Group (nested groups, widgets, ActionGroup → OperationForm[], tab/step groups). Table → DataColumn[], DataFilter[], TableOperation[] (row and table). Form → Group, TabBar/Stepper. ActorType.menuItems → MenuItemAccess / MenuItemOperation (→ OperationForm) / MenuItemGroup (nested).

## Abstract Base Classes
- VisualElement: `name`, `label` (i18n), `iconName`, `customImplementation` (Boolean; marks any visual element as custom implementation; exposed as extension point instead of generated), `subTheme`.
- Container: `layout`, `components`, `horizontal`, `vertical`, `frame`, `performableActions`.
- Component: `col`, `row`, `stretch`, `fit`, `hiddenBy`, `enabledBy`.
- Widget: `onBlur`, `requiredBy`, `minValueBy`, `maxValueBy`.
- Filter / Column / Tabular / MenuItem: shared attributes described in their elements above (`actionContainer` reference on containers).

## Related Documentation
- UI Behaviour Rules (conditional attributes, validation, defaults).
- ESM Structure, Operation and Accesspoint packages.
- Frontend ESM-to-UI mapping.
