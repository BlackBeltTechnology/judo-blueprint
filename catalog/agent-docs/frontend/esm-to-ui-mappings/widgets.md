---
title: ESM to UI Mapping: Widget Components
description: ESM to UI Mapping: Widget Components: ESM to UI model mapping reference for the generated React frontend.
aliases: [widget attributes, data field widget type, table reference field options, operation form dialog, confirmation dialog settings, action group overflow, stepper wizard, text field widget]
keywords: [ui:DataField, ui:TabularReferenceField, ui:OperationForm, representationComponent, enumWidget, textWidget, booleanWidget, confirmationType, featuredActions, relationFeature, rowsPerPage, autocompleteRows]
tags: [domain:frontend, layer:frontend, status:platform]
---

# ESM to UI Mapping: Widget Components

**[◄ Overview](./README.md)** | **[Tables & Navigation ►](./tables-navigation.md)**

This document covers widget components that display and edit data within containers.

---

## Widget Components

### Form Autofocus

In a form container the first input whose attribute is not read-only receives focus after `autoFocusRefDelay` (200 ms). The selection checks only the attribute's read-only flag, not visibility, so a hidden input that comes first can receive focus.

### DataField (ui:DataField)

**Supertypes:** `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:DataField` | `name` *(generated, read-only)* | Field name | Input name — runtime value derived from `dataFeature.member.name` by a `getName()` EOperation override; XMI `name="…"` is stored but ignored on read and FQN computation |
| `ui:DataField` | `label` | Label text | Input label (i18n) |
| `ui:DataField` | `iconName` | Icon | Input adornment |
| `ui:DataField` | `col` | Grid column (1-12) | Grid md prop (default: 12) |
| `ui:DataField` | `row` | Row span | Textarea rows (default: 1). Only `rows` is emitted; `minRows` is not. |
| `ui:DataField` | `stretch` | Stretch behavior | `NONE`/`HORIZONTAL`/`VERTICAL`/`BOTH` |
| `ui:DataField` | `fit` | Fit mode | `LOOSE`/`TIGHT` |
| `ui:DataField` | `dataFeature` (ref) | Bound attribute | Data binding |
| `ui:DataField` | `onBlur` | Blur trigger | `on{Field}BlurAction` hook |
| `ui:DataField` | `tooltipText` | Tooltip | Help icon with tooltip |
| `ui:DataField` | `hiddenBy` (ref) | Dynamic visibility | DataFeature controlling hidden state |
| `ui:DataField` | `enabledBy` (ref) | Dynamic enabled | DataFeature controlling enabled state |
| `ui:DataField` | `requiredBy` (ref) | Dynamic required | DataFeature controlling required state |
| `ui:DataField` | `minValueBy` (ref) | Minimum value | DataFeature for min validation |
| `ui:DataField` | `maxValueBy` (ref) | Maximum value | DataFeature for max validation |

#### Widget Type Attributes

Type-specific attributes:

| Attribute | Applies To | Values | Frontend Effect |
|-----------|------------|--------|-----------------|
| `enumWidget` | EnumerationType | `COMBO`/`RADIO`/`TOGGLE_BUTTONBAR` | Enum input type. `COMBO` renders an MUI Autocomplete, not a Select with MenuItem options. |
| `textWidget` | StringType | `TEXT`/`INPUT` | `TEXT`=read-only, `INPUT`=editable. `TEXT` renders the value as plain text (`ui:Formatted`): no label, no input, no tooltip, optionally an icon. `INPUT` renders a labelled input (`ui:TextInput` or `ui:TextArea`). To keep the label on a read-only value, use `INPUT` on a read-only (derived) member. |
| `textMultiLine` | StringType | Boolean | Enable textarea |
| `textMask` | StringType | Pattern string | Input mask (only when `textWidget=INPUT` and `textMultiLine=false`). The generated input does not apply it: only `maxLength` is emitted. |
| `textCountCharacters` | StringType | Boolean | Show character counter. Rendered only when `countCharacters` is set and the bound attribute has `maxLength`. |
| `isTypeAheadField` | StringType | Boolean | Autocomplete from previous values |
| `booleanWidget` | BooleanType | `CHECKBOX`/`COMBO`/`SWITCH` | Boolean input type. ESM models (esm2ui): unset or `CHECKBOX` gives a checkbox, `COMBO` the trinary-logic combo, `SWITCH` a `ui:Switch`. The React template has widget fragments only for checkbox and trinary-logic combo, so do not rely on `SWITCH` (*verify* how it renders). JSL models (jsl2ui): a boolean view field always becomes the trinary-logic combo; the checkbox rule is commented out. |
| `valueLabelPlacement` | BooleanType | `DEFAULT`/`TOP`/`START`/`BOTTOM`/`END` | Checkbox label placement (only when `booleanWidget=CHECKBOX`) |
| `formatValue` | NumericType | Boolean | Apply number formatting (default: true) |

##### Widget attributes per data type

**Type-Specific Behaviour (from ui-behaviour.md):**

| Data Type | Available Attributes | Conditional Rules |
|-----------|---------------------|-------------------|
| `StringType` | `textWidget`, `textMultiLine`, `textMask`, `isTypeAheadField`, `textCountCharacters` | `textMask` enabled only when `textMultiLine=false` AND `textWidget=INPUT` |
| `EnumerationType` | `enumWidget` | - |
| `NumericType` | `formatValue`, `minValueBy`, `maxValueBy` | `minValueBy`/`maxValueBy` disabled when in TableOperation |
| `DateType` | `minValueBy`, `maxValueBy` | `minValueBy`/`maxValueBy` disabled when in TableOperation |
| `TimestampType` | `minValueBy`, `maxValueBy` | `minValueBy`/`maxValueBy` disabled when in TableOperation |
| `TimeType` | `minValueBy`, `maxValueBy` | `minValueBy`/`maxValueBy` disabled when in TableOperation |
| `BooleanType` | `booleanWidget`, `valueLabelPlacement` | `valueLabelPlacement` enabled only when `booleanWidget=CHECKBOX` |
| `BinaryType` | - | File upload widget. `maxFileSize` is not enforced client-side, and binary uploads are not base64-encoded in the generated input. |
| `MeasuredType` | - | Inherits NumericType behavior |

**Read-only fields of other types:** `textWidget=TEXT` is the only switch and applies to string fields. A date, number or enumeration field is rendered read-only when its bound member is read-only (a derived member); `enabledBy` only disables the input, so a date field keeps its picker icon. To show such a value as plain text, bind a derived string member (for example a formatted value) instead of the mapped member.

**Inherited from `Widget`:** `onBlur`, `requiredBy`, `minValueBy`, `maxValueBy`
**Inherited from `Component`:** `col`, `row`, `stretch`, `fit`, `hiddenBy`, `enabledBy`

**Generated input notes:**
- Numeric inputs use only the attribute `scale` (as `decimalScale`); `precision` has no effect.
- No `PasswordInput` element type exists; password fields are not produced by a separate template.
- Text areas set `rows` only; `minRows` is not emitted.
- Time inputs always show hours, minutes and seconds; `baseUnit` is not read.

**Example:**
```xml
<components xsi:type="ui:DataField"
  xmi:id="_T-UiwLLKEfCE0JrRXgRyVA"
  name="fullAddress"
  label="FullAddress"
  iconName="format-size"
  col="12"
  row="1"
  onBlur="false"
  dataFeature="_60recLLBEfCC_efogf7jJg"
  enumWidget="COMBO"
  textMultiLine="false"
  textWidget="INPUT"
  formatValue="true"/>
```

- **Boolean combo:** the trinary-logic combo has three entries, `Yes` (true), `No` (false) and `Unknown` (null or undefined). The generated widget therefore shows "unknown" for an empty value.
- **Hide a row action per row:** set `hiddenBy` on the row button to a boolean attribute of the row's transfer object. The generated table hides the button when `!!row.<attribute>` is true. There is no other per-row hook.
- **Count only:** a table with `showTotalCount` sends the header `X-Judo-CountRecords: true` on its list call and reads the total from the `X-Judo-Count` response header. A count-only call is a list call with that header and `_mask: '{}'`; read the header from the response, ignore the body.
- **Route parameters:** a page route is the page name split at `::`, each part capitalized and joined with `/`, plus `/:signedIdentifier` when the page is a view on a relation (or a refreshable output view), unless it opens in a dialog or is a single-access page. The identifier in the URL is the signed identifier (`__signedIdentifier`) of the row.

### TabularReferenceField (ui:TabularReferenceField)

**Supertypes:** `Tabular` + `ReferenceField` → (`VisualElement`, `Widget` + `PerformableAction`)

A complex widget for managing relationships (to-one or to-many).

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:TabularReferenceField` | `name` | Table name | Component name |
| `ui:TabularReferenceField` | `label` | Header | Table title (i18n) |
| `ui:TabularReferenceField` | `iconName` | Icon | Header icon |
| `ui:TabularReferenceField` | `col` | Grid column (1-12) | Layout width |
| `ui:TabularReferenceField` | `relationFeature` (ref) | Bound relation | Data binding to RelationMember |
| `ui:TabularReferenceField` | `representationComponent` | Display type | `table`/`tag`/`card`/`button` |
| `ui:TabularReferenceField` | `buttonStyle` | Button style | `text`/`contained`/`outlined` (when `representationComponent=button`) |
| `ui:TabularReferenceField` | `smallTable` | Compact mode | Dense table without pagination. Carried to the ui model as `isSmallTable`; the React generator does not read it. Pagination depends on the table being eager: a table over an aggregation or composition relation (or inside a Form) is eager (all rows in memory, no paging), any other table is lazy and paged |
| `ui:TabularReferenceField` | `checkboxSelection` | Selection mode | `AUTO`/`ENABLED`/`DISABLED` |
| `ui:TabularReferenceField` | `countRows` | Show row count | Display total row count |
| `ui:TabularReferenceField` | `isInlineEditable` | Inline editing | Enable inline row editing |
| `ui:TabularReferenceField` | `rowsPerPage` | Page size | Pagination limit (default: 10) |
| `ui:TabularReferenceField` | `selectorRowsPerPage` | Selector page size | Pagination for selector dialogs (default: 10) |
| `ui:TabularReferenceField` | `selectorDialogSize` | Selector dialog size | `UNDEFINED`/`XS`/`SM`/`MD`/`LG`/`XL` |
| `ui:TabularReferenceField` | `autocompleteRows` | Autocomplete limit | Search result limit for single relations (default: 10) |
| `ui:TabularReferenceField` | `actionColumnWidth` | Action column width | Fixed width for action column |
| `ui:TabularReferenceField` | `columns` | Column definitions | DataColumn list |
| `ui:TabularReferenceField` | `filters` | Filter controls | DataFilter list |
| `ui:TabularReferenceField` | `rowOperations` | Row actions | TableOperation list (in action column) |
| `ui:TabularReferenceField` | `tableOperations` | Table actions | TableOperation list (in toolbar) |
| `ui:TabularReferenceField` | `additionalMaskFeatures` | Extra query fields | Additional attributes for REST queries |
| `ui:TabularReferenceField` | `crudOperationsDisplayed` | CRUD button count | Number of CRUD buttons (default: 1) |
| `ui:TabularReferenceField` | `transferOperationsDisplayed` | Transfer button count | Number of transfer buttons (default: 0) |
| `ui:TabularReferenceField` | `onBlur` | Blur trigger | `on{Field}BlurAction` hook |
| `ui:TabularReferenceField` | `hiddenBy` (ref) | Dynamic visibility | DataFeature controlling hidden state |
| `ui:TabularReferenceField` | `enabledBy` (ref) | Dynamic enabled | DataFeature controlling enabled state |

#### Conditional Behaviour


| Condition | Enabled Attributes |
|-----------|-------------------|
| `relationFeature.upper == -1` (many) | `rowsPerPage`, `isInlineEditable`, `smallTable` |
| `relationFeature.upper == 1` (single) | `autocompleteRows` |
| `relationKind in (AGGREGATION, COMPOSITION)` | `smallTable` |
| `representationComponent == 'button'` | `buttonStyle` |

`representationComponent` has no dropdown value (only `table`, `tag`, `card`, `button`). For a to-one relation, the relation selector's autocomplete search is limited by `autocompleteRows`; `isTypeAheadField` applies only to string attributes, not to relations.

**Inherited from `Tabular`:** `columns`, `filters`, `rowOperations`, `tableOperations`, `countRows`, `checkboxSelection`, `isInlineEditable`, `additionalMaskFeatures`
**Inherited from `ReferenceField`:** `relationFeature`
**Inherited from `Widget`:** `onBlur`
**Inherited from `Component`:** `col`, `hiddenBy`, `enabledBy`

**Example:**
```xml
<components xsi:type="ui:TabularReferenceField"
  xmi:id="_UINekLLKEfCE0JrRXgRyVA"
  name="nationalInduvidualElectoralDistrict"
  label="NationalInduvidualElectoralDistrict"
  iconName="table_rows"
  checkboxSelection="ENABLED"
  col="12"
  relationFeature="_80D8QLLBEfCC_efogf7jJg"
  representationComponent="table"
  rowsPerPage="10"
  selectorRowsPerPage="10"
  autocompleteRows="10"/>
```

### OperationForm (ui:OperationForm)

**Supertypes:** `Container` → `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

Widget that triggers an action, bound to a specific operation. Typically renders as a button with optional dialog for input parameters. Contains nested form elements (DataFields, ActionButtons) when the operation has parameters.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:OperationForm` | `name` *(generated, read-only)* | Form name | Component name — runtime value derived from `operation.name` (fallback to stored `name` when blank) by a `getName()` EOperation override |
| `ui:OperationForm` | `label` | Form/button text | Button label (i18n) |
| `ui:OperationForm` | `iconName` | Icon | Button icon |
| `ui:OperationForm` | `operation` | Target operation | Operation binding |
| `ui:OperationForm` | `col` | Grid column | Layout width |
| `ui:OperationForm` | `row` | Row span | Layout height |
| `ui:OperationForm` | `disabled` | Disabled state | Static disabled |
| `ui:OperationForm` | `hidden` | Hidden state | Static hidden |
| `ui:OperationForm` | `variant` | Button style | contained/outlined/text |
| `ui:OperationForm` | `dialogSize` | Dialog dimensions | `XS`/`S`/`M`/`L`/`XL`/`UNDEFINED` |
| `ui:OperationForm` | `confirmationType` | Confirmation behavior | `NONE`/`CONDITIONAL`/`MANDATORY` |
| `ui:OperationForm` | `confirmationMessage` | Message in dialog | Confirmation dialog text |
| `ui:OperationForm` | `confirmationCondition` | Boolean DataFeature | Condition for CONDITIONAL type |
| `ui:OperationForm` | `postCallAccessNavigation` | Access navigation | Navigate to Access after success |
| `ui:OperationForm` | `autoOpenAfterCreate` | Auto-open created | Opens created element automatically |
| `ui:OperationForm` | `generateVisualPropertiesHook` | Enable visual hook | Extension point for visual properties |
| `ui:OperationForm` | `generateActionsHook` | Enable actions hook | Extension point for custom actions |
| `ui:OperationForm` | `components` | Form widgets | DataFields, ActionButtons, Groups |

**Confirmation Types:**

| Type | Frontend Effect |
|------|-----------------|
| `NONE` | Operation executes without confirmation |
| `CONDITIONAL` | Confirmation dialog shown based on boolean attribute value |
| `MANDATORY` | Confirmation dialog always shown before execution |

**Nested Form Elements:**
- `DataField` - Input fields bound to operation parameters
- `ActionButton` - Submit/Cancel buttons
- `Group` - Layout container for organizing form fields
- `TabularReferenceField` - Relation selector within form

**Example:**
```xml
<components xsi:type="ui:OperationForm"
  xmi:id="_ABC123"
  name="approveForm"
  label="Approve"
  iconName="check"
  operation="approveOperation"
  dialogSize="M"
  confirmationType="MANDATORY"
  confirmationMessage="Are you sure you want to approve?"
  col="3">
  <components xsi:type="ui:DataField" name="comment" dataFeature="comment" col="12"/>
  <components xsi:type="ui:ActionButton" name="submit" action="SUBMIT" label="Confirm"/>
  <components xsi:type="ui:ActionButton" name="cancel" action="CANCEL" label="Cancel"/>
</components>
```

### TextField (ui:TextField)

Simple unbound text display widget for static text or labels.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:TextField` | `name` | Element name | Component name |
| `ui:TextField` | `text` | Display text | Static text content |
| `ui:TextField` | `col` | Grid column | Layout width |
| `ui:TextField` | `variant` | Text style | Typography variant |

**Example:**
```xml
<components xsi:type="ui:TextField"
  xmi:id="_DEF456"
  name="infoText"
  text="Please fill in all required fields"
  col="12"/>
```

### ActionButton (ui:ActionButton)

Button for standard form actions like Submit or Cancel.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:ActionButton` | `name` | Button name | Component name |
| `ui:ActionButton` | `action` | Action type | SUBMIT / CANCEL |
| `ui:ActionButton` | `label` | Button text | Button label (i18n) |
| `ui:ActionButton` | `iconName` | Icon | Button icon |
| `ui:ActionButton` | `variant` | Button style | contained/outlined/text |

**Action Types:**

| Action | Frontend Effect |
|--------|-----------------|
| `SUBMIT` | Triggers form submission/save operation |
| `CANCEL` | Closes dialog/navigates back without saving |

### Layout Components

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:Group` | `name` | Group name | Container div |
| `ui:Group` | `layout` | Direction | HORIZONTAL/VERTICAL |
| `ui:Group` | `frame` | Border | Container styling |
| `ui:Group` | `col` | Grid column | Layout width |
| `ui:Group` | `label` | Group title | Section header |
| `ui:TabBar` | `name` | Tab container | MUI Tabs |
| `ui:TabBar` | `orientation` | Tab direction | HORIZONTAL/VERTICAL |
| `ui:TabBar` | `tabs` | Tab panels | Group list |
| Tab panel | `components` | Tab content | Tab panel content |

### Stepper (ui:Stepper)

**Supertypes:** `Container` → `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

Container that organizes child groups into a sequential wizard-style flow.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:Stepper` | `name` | Stepper name | Component name |
| `ui:Stepper` | `orientation` | Direction | HORIZONTAL/VERTICAL |
| `ui:Stepper` | `steps` | Step panels | Group list |
| `ui:Stepper` | `linear` | Linear mode | Force sequential |
| Step panel | `label` | Step title | Step header |
| Step panel | `components` | Step content | Step panel content |

### Divider (ui:Divider)

**Supertypes:** `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

Visual separator element for dividing sections within a container.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:Divider` | `name` | Divider name | Component name |
| `ui:Divider` | `col` | Grid column | Layout width |
| `ui:Divider` | `row` | Row span | Layout height |

**Example:**
```xml
<components xsi:type="ui:Divider"
  xmi:id="_DIV123"
  name="sectionDivider"
  col="12"/>
```

### Placeholder (ui:Placeholder)

**Supertypes:** `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

Reserved space for custom implementations or future content.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:Placeholder` | `name` | Placeholder name | Component name |
| `ui:Placeholder` | `col` | Grid column | Layout width |
| `ui:Placeholder` | `row` | Row span | Layout height |
| `ui:Placeholder` | `customImplementation` | Custom flag | Marked for custom implementation; the generator has no widget for a placeholder, so it renders nothing. To plug in a custom component, set `customImplementation` on a `DataField` instead (see [hooks/ui-hooks.md → Field and View Display](../hooks/ui-hooks.md)) |

**Example:**
```xml
<components xsi:type="ui:Placeholder"
  xmi:id="_PH123"
  name="customSection"
  customImplementation="true"
  col="12"/>
```

### Icon (ui:Icon)

**Supertypes:** `Widget` → `Component` → `FormElement` → `VisualElement` → `NamedElement`

Standalone icon display widget.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:Icon` | `name` | Icon name | Component name |
| `ui:Icon` | `iconName` | Material icon | Icon display |
| `ui:Icon` | `col` | Grid column | Layout width |
| `ui:Icon` | `row` | Row span | Layout height |

**Example:**
```xml
<components xsi:type="ui:Icon"
  xmi:id="_ICO123"
  name="statusIcon"
  iconName="check_circle"
  col="1"/>
```

### ActionGroup (ui:ActionGroup)

**Supertypes:** `VisualElement` → `NamedElement`

Container for grouping related actions/buttons with automatic overflow handling.

| ESM Element | ESM Attribute | UI Model | Frontend Effect |
|-------------|---------------|----------|-----------------|
| `ui:ActionGroup` | `name` | Group name | Component name |
| `ui:ActionGroup` | `label` | Group label | Group header (i18n) |
| `ui:ActionGroup` | `featuredActions` | Featured count | First N actions as buttons |
| `ui:ActionGroup` | `actions` | Action list | PerformableAction list |

**Behaviour:** The first `featuredActions` actions are displayed as standalone buttons. Remaining actions are placed in a popup menu.

**FAB button groups:**
- A FAB group with one button and `featuredActions=0` renders nothing, because the speed dial needs more than one button.
- The speed-dial toggle shows the group icon or no icon; it never uses a `SpeedDialIcon` element.
- `hiddenBy` applies to featured FAB buttons, not to speed-dial items in the same group.
- Dialog FAB groups render after `DialogContent`, outside the dialog body.
- A page counts as having a FAB group when any nested `ButtonGroup` is a FAB, even if no top-level group is. Workaround: place FAB groups directly under the page container.

**Example:**
```xml
<actionGroup xsi:type="ui:ActionGroup"
  xmi:id="_AG123"
  name="pageActions"
  featuredActions="2">
  <actions xsi:type="ui:PerformableAction" name="edit" label="Edit"/>
  <actions xsi:type="ui:PerformableAction" name="delete" label="Delete"/>
  <actions xsi:type="ui:PerformableAction" name="export" label="Export"/>
</actionGroup>
```

