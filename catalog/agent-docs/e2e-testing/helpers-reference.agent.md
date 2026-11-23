# helpers-reference.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/helpers-reference.md.

## Overview
- Generated helpers live in `playwright/helpers/`: `ApiHelper.ts`, `TableHelper.ts`, `utils.ts`, `visualElementIds/VisualElementIds.ts`.
- Use the helpers instead of hand-written waits and selectors.

## ApiHelper
- `new ApiHelper()` builds the base API regex from `APP_URL`.
- `gotoWithWait(page, url?)`: navigate, wait for network idle.
- `triggerAndWait(page, locator)`: click, wait for any matching API response.
- `triggerAndWaitWithRegex(page, locator, regex)`: click, wait for the response matching the regex.
- `triggerAndWaitWithAction(page, promise, regex)`: run the promise (e.g. `fill`), wait for the matching response.
- Pattern suffixes: `/.*~list$/` table data, `/.*~get$/` single entity, `/.*template$/` create form, `/.*~validate$/` form submit, `/.*range$/` relation or autocomplete, `/.*create$/`, `/.*update$/`, `/.*delete$/`.

## TableHelper
- `new TableHelper()` works on MUI DataGrid tables.
- `getRow(page|locator, nth)`: 0-indexed, 0 is the header row, so data starts at 1.
- `getRows(page|locator)`: data rows only, selected by `aria-selected="false"`.
- `getCell(locator, cellName)`: cell by column data-field name (model attribute name, camelCase).
- `getCellInput(locator, cellName)`: input inside a cell, for inline edit.
- `getSortButton(page|locator, cellName)`: sort button of a column.

## Utils Module
- `TEST_DATA_PREFIX = 'X_TEST_'`: prefix all test data for cleanup.
- Types: `FilterType` (`text`, `numeric`, `boolean`, `enum`), `AddFilterSpec` (`operationNth`, `valueNth` for repeated fields), `CellAssertData` (`Contain`, `Have`, `BooleanValue`), `BackNavigationOptions` (`checkNetwork` default true, `regexExp` default `/.*get$/`).
- `formatNumber`: US-locale comma separators, e.g. `1234567` → `"1,234,567"`.
- Navigation: `navigateToAccess` (menu button, optional regex), `navigateToAnAccessListElement`, `navigateToCollectionRelationButton`, `navigateToSingleRelation`, `backNavigation`.
- Forms: `fillPrimitiveField` (optional filter flag and backCheck), `clearPrimitiveField`, `checkPrimitiveFieldHasValue`, `fillPrimitiveCheckBox`, `checkCheckboxPrimitiveCheckBoxHasValue`, `fillEnumCombobox`, `checkEnumCombobox`, `checkEnumComboboxOptions`.
- CRUD: `createOnAccesList` and `submitOnAccesListCreate` (create); `updateAccessViewPage` (update). Defaults use the `template` and `get` patterns.
- Filters: `openFilter(page, clear?, number?, nth?)`, low-level `addFilter`, `applyFilters(page, apiHelper, count)`, `openAddAndApplyFilters(page, apiHelper, filters)`, `openClearAndApplyFilters`, `clearFilters`.
- Assertions: `assertRows`, `assertRowContent(tableHelper, page, rowNum, data)`, `assertCellContent`.
- Single relation: `fillSingleRelationElement`, `checkSingleRelationElementHasValue`, `checkEmptySingleRelationElement`, `unsetSingleRelationElement`, `deleteSingleRelationElement`, `createSingleRelationElement`, `attachOnSingelRelationElement` (sic, the exported name), `openSingleRelationSelector`.
- Collection relation: `createCollectionRelationElement`, `openCollectionRelationElementCreate`, `submitCollectioRelationElementCreate` (sic), `acceptChangesOnDialogElement`.
- Table selection: `selectRowsOnTable`, `selecAllRowsOnTable` (sic), `bulkRemoveOnTable`, `bulkDeleteOnTable`.
- Operations: `callOperationWithInput(page, locator, name, groupName?)` opens the input form, `submitOperationCall(page, locator?, submitButton?, regExp?)` submits.
- `proccessRelationElement(page, locator, element)`: processes one relation field by its type.

## VisualElementIds
- Generated constants: `_id` (model element id), `_label`, and nested `id` / `label` per field, relation, column and page action.
- Use the `id` with `getByTestId`, or the `label` with `getByLabel`.
- Benefits: traceable to model elements, updates when the model changes, unambiguous selection.
