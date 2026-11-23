# widgets.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md.

## Widget Components
- Maps ESM `ui:*` elements to React frontend effects. Every widget table: ESM attribute → UI model → frontend effect.
- Inherited: `Widget` gives `onBlur`, `requiredBy`, `minValueBy`, `maxValueBy`; `Component` gives `col`, `row`, `stretch`, `fit`, `hiddenBy`, `enabledBy`.

### DataField (ui:DataField)
- `name` is generated/read-only (runtime name from `dataFeature.member.name` via `getName()` override).
- Layout: `col` (1-12, grid md, default 12), `row` (textarea rows, default 1), `stretch` (`NONE`/`HORIZONTAL`/`VERTICAL`/`BOTH`), `fit` (`LOOSE`/`TIGHT`).
- Binding: `dataFeature` (bound attribute); `onBlur` → `on{Field}BlurAction` hook; `tooltipText` (help icon); `hiddenBy`/`enabledBy`/`requiredBy` (DataFeature refs); `minValueBy`/`maxValueBy` for validation.
- Widget attributes: `enumWidget` (`COMBO`/`RADIO`/`TOGGLE_BUTTONBAR`); `textWidget` (`TEXT` = read-only plain text, no label/input/tooltip; `INPUT` = labelled input); `textMultiLine` (textarea); `textMask` (only when `textWidget=INPUT` and `textMultiLine=false`); `textCountCharacters`; `isTypeAheadField` (strings only); `booleanWidget` (`CHECKBOX`/`COMBO`); `valueLabelPlacement` (only when CHECKBOX; `DEFAULT`/`TOP`/`START`/`BOTTOM`/`END`); `formatValue` (numeric, default true).
- Per type: `minValueBy`/`maxValueBy` disabled inside TableOperation (numeric, date, timestamp, time). Binary = file upload. MeasuredType inherits numeric behaviour.
- Boolean combo is trinary: `Yes` (true), `No` (false), `Unknown` (null/undefined) shown for empty.
- Read-only: `textWidget=TEXT` is the only switch and only for strings. Date/number/enum fields are read-only when the bound member is read-only (derived); `enabledBy` only disables the input (picker icon stays). For plain text, bind a derived string member.
- Hide per-row action: `hiddenBy` on the row button → hidden when `!!row.<attribute>`; no other per-row hook.
- Count only: `showTotalCount` sends `X-Judo-CountRecords: true` on list call, reads `X-Judo-Count` header; count call uses `_mask: '{}'`.
- Route parameters: page route = page name split at `::`, parts capitalised and joined with `/`; adds `/:signedIdentifier` for relation views or refreshable output views (not dialogs or single-access pages). Id = row `__signedIdentifier`.

### TabularReferenceField (ui:TabularReferenceField)
- To-one or to-many relation widget; supertypes Tabular + ReferenceField.
- `representationComponent`: `table`/`tag`/`card`/`button`. `buttonStyle` (`text`/`contained`/`outlined`) only for button.
- `relationFeature` (bound relation); `smallTable` (carried as `isSmallTable`; React generator ignores it).
- `checkboxSelection`: `AUTO`/`ENABLED`/`DISABLED`. `countRows`, `isInlineEditable`.
- Paging: `rowsPerPage` (default 10, many only); `selectorRowsPerPage` (default 10); `autocompleteRows` (default 10, single only).
- `selectorDialogSize`: `UNDEFINED`/`XS`/`SM`/`MD`/`LG`/`XL`. `actionColumnWidth`.
- Content: `columns` (DataColumn), `filters` (DataFilter), `rowOperations` (action column), `tableOperations` (toolbar), `additionalMaskFeatures` (extra REST query fields).
- Button counts: `crudOperationsDisplayed` (default 1), `transferOperationsDisplayed` (default 0).
- Conditional: many → `rowsPerPage`, `isInlineEditable`, `smallTable`; single → `autocompleteRows`; AGGREGATION/COMPOSITION → `smallTable`; `button` → `buttonStyle`.
- Single relation autocomplete limited by `autocompleteRows`; `isTypeAheadField` does NOT apply to relations.
- `representationComponent` has no dropdown value beyond the four listed.

### OperationForm (ui:OperationForm)
- Container widget bound to one operation; usually a button opening an optional dialog for parameters.
- `operation` binding; `name` generated (from `operation.name`, fallback stored name) via `getName()` override.
- `label`, `iconName`, `variant` (`contained`/`outlined`/`text`), `disabled`/`hidden` (static), `col`, `row`.
- `dialogSize`: `XS`/`S`/`M`/`L`/`XL`/`UNDEFINED`.
- Confirmation: `confirmationType` = `NONE` (no dialog) / `CONDITIONAL` (dialog if `confirmationCondition` boolean is true) / `MANDATORY` (always). `confirmationMessage` text.
- `postCallAccessNavigation` (navigate to Access after success); `autoOpenAfterCreate` (open created element).
- `generateVisualPropertiesHook` and `generateActionsHook`: extension point flags.
- `components`: nested DataField, ActionButton, Group, TabularReferenceField.

### TextField (ui:TextField)
- Unbound static text: `name`, `text`, `col`, `variant` (typography).

### ActionButton (ui:ActionButton)
- `action`: `SUBMIT` (submit/save operation) or `CANCEL` (close dialog or navigate back without saving). `label`, `iconName`, `variant`.

### Layout Components
- `ui:Group`: `name`, `layout` (HORIZONTAL/VERTICAL), `frame` (border), `col`, `label` (section header).
- `ui:TabBar`: `orientation` (HORIZONTAL/VERTICAL), `tabs` (group list) → MUI Tabs; tab panel content = `components`.

### Stepper (ui:Stepper)
- Wizard container of child groups. `orientation`, `steps` (group list), `linear` (force sequential). Step panel: `label` (header), `components` (content).

### Divider (ui:Divider)
- Visual separator with `name`, `col`, `row`.

### Placeholder (ui:Placeholder)
- Reserved space. `name`, `col`, `row`, `customImplementation` flag. Generator has no widget for it: renders nothing unless a custom component is plugged in.

### Icon (ui:Icon)
- Standalone icon: `name`, `iconName` (material icon), `col`, `row`.

### ActionGroup (ui:ActionGroup)
- Groups actions with overflow: `label` (i18n header), `featuredActions` (first N shown as buttons), `actions` (PerformableAction list). Remaining actions go into a popup menu.
- FAB: a page counts as having a FAB group when any nested ButtonGroup is FAB; place FAB groups directly under the page container.
