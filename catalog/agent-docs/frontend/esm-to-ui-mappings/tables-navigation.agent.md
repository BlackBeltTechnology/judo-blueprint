# tables-navigation.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md.

## Table-Specific Elements
- Used only inside `TransferObjectTable` or `TabularReferenceField`.

### DataColumn (ui:DataColumn)
- `name` is generated/read-only (from `dataFeature.member.name`); XMI `name` ignored.
- Attributes: `label` (i18n header), `iconName`, `dataFeature` (binding), `width` (px), `flex`, `sortable`, `defaultSort` (`ASC`/`DESC`/`NONE`, default NONE), `filterable`, `hidden`, `align` (`LEFT`/`CENTER`/`RIGHT`), `isPinnable`, `formatValue`, `customImplementation`.
- `formatValue=true`: `new Intl.NumberFormat(<locale>).format(value)` (grouping/decimal, default fraction digits). `scale` and currencies NOT applied (`89.9` stays `89.9`). Fixed decimals/currency: derived string attribute or `customImplementation` column.

### DataFilter (ui:DataFilter)
- `name` generated: `dataFeature.member.name + "Filter"`.
- Attributes: `label`, `iconName`, `dataFeature`, `filterOperationType`, `placeholder`, `defaultValue`, `hidden`, `col` (grid column).
- `filterOperationType`: `EQUALS`, `NOT_EQUALS`, `LESS_THAN`, `LESS_OR_EQUAL`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LIKE` (contains), `NOT_LIKE`, `RANGE` (from/to), `ENUMERATION` (dropdown), `BOOLEAN` (checkbox/toggle).

### TableOperation (ui:TableOperation)
- Attributes: `name`, `label`, `iconName`, `operation`, `isBulk` (multi-select), `variant` (contained/outlined/text), `hiddenBy`, `enabledBy`, `operationForm` (nested form for params), `confirmationType` (`NONE`/`CONDITIONAL`/`MANDATORY`), `confirmationMessage`, `confirmationCondition` (Boolean DataFeature).
- Placement: `rowOperations` (row action menu, single row) or `tableOperations` (toolbar, can be bulk).
- Row action button label comes from the button element nested in the operation's form, not the TableOperation `label`. CLI: `java -jar target/judo-cli.jar -m <model> update '<ns>::<Entity>_Table::<op>TableOperation::<op>' -s "label=<Text>"`.

### RelationColumn (ui:RelationColumn)
- `name` generated from `relationFeature`; GraphQL identity is `dataFeatureOfRelationFeature`.
- Attributes: `label`, `iconName`, `relationFeature`, `width`, `flex`, `sortable`, `hidden`, `align`, `attributePath` (attribute shown from related entity), `customImplementation`.
- Avoid on top-level `TransferObjectTable` (backing an Access/MenuItemAccess list): codegen bug (dangling refs like `ViewGalaxyStored`), unreliable sort/filter/row-action wiring.
  - Use `TabularReferenceField` in view/form for related collections.
  - Use plain `DataColumn` on a mapped string attribute or DERIVED attribute flattening the relation (e.g. `self.owner.fullName`) for display.
  - Reserve RelationColumn for embedded relation tables in detail screens.
- See ui-authoring-guide Pitfalls.

### Row Click and Default Labels
- Open-page row action → `onRowClick` (page opens; not rendered as button). Other `rowOperations` → buttons in action column.
- Missing `label` → default from TO name: `<Entity>Info Table` (table page), `<Entity>Info View / Edit` (view page). Set `label` on table, view, menu item (or i18n keys). CLI: `java -jar target/judo-cli.jar -m <model> update '<ns>::<Entity>Info_Table' -s "label=<Text>"`.

## Navigation Elements

### MenuItem (ui:MenuItem) — abstract
- Attributes: `name` (route id), `label`, `iconName`, `hidden`, `order`. Concrete: MenuItemAccess, MenuItemOperation, MenuItemGroup.

### MenuItemAccess
- Adds `access` (target access; link to table/view). Example `access="_customersAccess"`.

### MenuItemOperation
- Adds `targetOperation` (static operation binding).

### MenuItemGroup
- Submenu container: `items` (child MenuItems), `collapsed` (initial state), `orientation` (`HORIZONTAL`/`VERTICAL`).

## Transformation Tracing
- UI element IDs embed ESM xmi:id: `Actor/(esm/<xmi:id>)/AttributeType`.
- Example: ESM `DataMember` `code` (xmi:id `_ZeK4…`) → UI attribute `Actor/(esm/_ZeK4…)/AttributeType` with `isRequired` → TextField with required validation.
- Model files: `model/<app>.model` (ESM), `application/frontend-react/model/<app>-ui.model` (UI).

## ESM Annotations
- Defined at model root (`annotations` with `name`, `className="hu.blackbelt.judo.meta.esm.accesspoint.Access"`).
- Project annotations: `dashboard` (dashboard entry point), `profile` (user profile entry). Defined but NOT applied to any element currently.
- Applied elements reference via `annotations` attribute. Transform to UI `availableAnnotations` (`name`) and element `annotations`.
- Frontend: `<ComponentProxy annotations={['dashboard']} />`. Helper: `getAnnotationNamesForElement(element)`.

## Hook Generation
- `generateActionsHook="true"` → scaffold `src/custom/hooks/{pages,dialogs,containers}/register<Name>ActionsHook.ts.default` (see action-hooks.md#container-actions).
- `generateVisualPropertiesHook="true"` → `is<Field>Hidden`, `is<Field>Disabled`, `is<Field>Readonly`, `is<Field>Required` handlers in container hook type.
- Widget `onBlur="true"` → `on{Field}BlurAction` handler.

## Supertype Inheritance and Behaviour

### Inheritance Hierarchy
- NamedElement → VisualElement → {FormElement (Component → Widget → DataField, ReferenceField (TabularReferenceField also Tabular), Divider, Placeholder, Icon, Container (Group, TabBar, Stepper, TransferObjectForm, OperationForm); Page (TransferObjectView, TransferObjectTable also Tabular)); ActionButton; Column (DataColumn, RelationColumn); DataFilter; PerformableAction → TableOperation; ActionGroup; MenuItem (MenuItemAccess, MenuItemOperation, MenuItemGroup)}.
- Tabular (mixin): TransferObjectTable, TabularReferenceField.

### Inherited Attributes
- NamedElement: `name`. VisualElement: `label`, `iconName`, `customImplementation`. Component: `col`, `row`, `hiddenBy`, `enabledBy`, `requiredBy`. Widget: `onBlur`. Container: `components`. Page: `actionGroup`, `additionalMaskFeatures`, `generateVisualPropertiesHook`, `generateActionsHook`. Tabular: `columns`, `filters`, `rowOperations`, `tableOperations`, `countRows`, `checkboxSelection`, `isInlineEditable`. ReferenceField: `relationFeature`. PerformableAction: `operation`, `confirmationType`, `confirmationMessage`, `confirmationCondition`.

### Behaviour Implications
- Components: 12-column grid (`col`, `row`). Widgets: `onBlur` triggers update actions. Containers: nested children. Pages: page actions/toolbar. Tabular: columns/filters, sorting. PerformableAction: confirmation dialogs.

### Type-Specific DataField Behaviour
- StringType: `textWidget`, `textMultiLine`, `textMask`, `isTypeAheadField`.
- EnumerationType: `enumWidget` (RADIO/COMBO/TOGGLE_BUTTONBAR).
- NumericType: `formatValue`, `minValueBy`, `maxValueBy`.
- BooleanType: `booleanWidget` (CHECKBOX/COMBO), `valueLabelPlacement`.
- Date/Timestamp/Time: `minValueBy`, `maxValueBy`.
- Full rules: model/esm_metamodel/ui-behaviour.md.

## Related Documentation
- ../../model/esm_metamodel/ui-behaviour.md (conditional rules), ../../model/esm_metamodel/ui.md (UI element definitions), ../../model/ui-authoring-guide.md (authoring playbook), `judo-model-cli` skill for model queries/tracing.
