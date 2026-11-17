# ui-behaviour.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/esm_metamodel/ui-behaviour.md.

## Common Behaviour Rules

- `Component` grid: `col` 1–12 (error text: minimum width ≤ 12); `row` > 0.
- VisualElement common attrs: `name`, `label` (i18n key), `iconName`, `customImplementation`.
- Widget-only binding attrs: `hiddenBy`, `enabledBy`, `requiredBy` (DataFeature).

## DataField Type-Specific Rules

- Applies by `dataFeature.dataType`.
- StringType: `textWidget` (TEXT/INPUT), `textMultiLine`, `textMask` (only when not multiline and INPUT), `isTypeAheadField`, `textCountCharacters`.
- EnumerationType: `enumWidget` = `RADIO`, `COMBO`, `TOGGLE_BUTTONBAR`.
- NumericType, DateType, TimestampType, TimeType: `minValueBy`/`maxValueBy` disabled inside a TableOperation; NumericType also has `formatValue`.
- BooleanType: `booleanWidget` = `CHECKBOX` or `COMBO`; `valueLabelPlacement` (`DEFAULT`, `START`, `END`, `TOP`, `BOTTOM`) only for CHECKBOX.
- MeasuredType and BinaryType: no extra attrs (Binary is the file upload widget).

## Container-Specific Rules

- TransferObjectView: `titleFrom` (`LABEL`/`ATTRIBUTE`); `titleAttribute` only for ATTRIBUTE; `openInDialog`; `dialogSize` only when dialog; `autoCloseOnSave`; hook flags.
- TransferObjectForm: `autoOpenAfterCreate`, `dialogSize`, hook flags.
- TransferObjectTable: `rowsPerPage`, `countRows`, `crudOperationsDisplayed`, `transferOperationsDisplayed`, `selectorRowsPerPage`, `selectorDialogSize`, `checkboxSelection` (`ENABLED`, `DISABLED`, `AUTO`), `isInlineEditable`, `representationComponent` (`table`, `card`).
- TabularReferenceField: `smallTable` only for many relations that are composition or aggregation; `rowsPerPage`, `isInlineEditable` only for many (`upper = -1`); `autocompleteRows` only for single (`upper = 1`); `buttonStyle` only when representation is `button`.
- TabularReferenceField representations: `table`, `card`, `tag`, `button`; single relations allow table/button/tag, many allow table/card/tag.
- Relation kinds: composition gets `{create, delete}`; aggregation gets `{add, remove}`.
- Group: `layout` (`HORIZONTAL`, `VERTICAL`), `frame`.

## Conditional Attribute Rules

- OperationForm confirmation: `confirmationType` (`NONE`, `CONDITIONAL`, `MANDATORY`); message enabled unless NONE; condition enabled only for CONDITIONAL.
- Confirmation candidates: boolean attributes of the owner TransferObjectType.
- `postCallAccessNavigation`: accesses whose type matches the operation output.
- TableOperation: `isBulk`; `confirmationCondition` disabled when `isBulk = true` (bulk ops cannot use row-level conditions).

## Validation Rules

- Grid: `col <= 12` and `row > 0` produce errors.
- TabularReferenceField relation rules: many enables `rowsPerPage`, `isInlineEditable`, `smallTable`; single enables `autocompleteRows`; AGGREGATION or COMPOSITION enables `smallTable`.
- Context: widget inside TableOperation disables `minValueBy`/`maxValueBy`.

## Default Values

- TransferObjectTable: `rowsPerPage` 10, `selectorRowsPerPage` 10, `crudOperationsDisplayed` 1, `transferOperationsDisplayed` 0, `checkboxSelection` `DISABLED`, `countRows` false, `isInlineEditable` false.
- TabularReferenceField: as table, plus `autocompleteRows` 10 and `smallTable` false.
- DataField: `col` 12, `row` 1, `onBlur` false, `formatValue` true, `textMultiLine` false, `isTypeAheadField` false, `textCountCharacters` false.
- OperationForm: `confirmationType` `NONE`; hook flags false.
- TransferObjectView: `titleFrom` `LABEL`, `openInDialog` false, `autoCloseOnSave` false, `dialogSize` `UNDEFINED`.
- TransferObjectForm: `dialogSize` `UNDEFINED`, `autoOpenAfterCreate` false.

## Attribute Help Text Reference

- Help text per element: DataField, OperationForm, TabularReferenceField, TransferObjectView, TransferObjectForm, TransferObjectTable, ActionButton, ActionGroup, PerformableAction, Common.
- ActionButton `action`: `SUBMIT` (invoke with form params), `CANCEL` (exit), `VIRTUAL` (default, no built-in behaviour).
- ActionGroup `featuredActions`: first n actions as buttons; rest go into a pop-up menu.
- PerformableAction `actionContainer`: card heading or page action section.
- Hook flags: generated frontend gets extension points (visual properties, actions) for custom code.

## Context Detection Rules

- Container checks: widget not in TableOperation; OperationForm parent is not TableOperation; container types are TransferObjectView, TransferObjectForm, Group; tabular types are TransferObjectTable, TabularReferenceField.
- Display mode is set by `representationComponent` (`table`, `card`, `button`).
- Relation kind: COMPOSITION means parent owns child lifecycle; AGGREGATION is shared reference without ownership.
- Candidate selection: operations come from the owner type; navigation accesses match operation output type; condition attrs are boolean members; numeric, date, timestamp and time members are filtered by `dataType`.
- Validation checks: `DataMember.dataType` not null; `RelationFeature.target` not null; `TableOperation.isBulk = true`.

## Related Documentation

- `./ui.md` (complete UI element definitions), `./structure.md` (entity and attribute definitions), `../../frontend/esm-to-ui-mappings/README.md` (ESM to React mapping).
