# writing-tests.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/writing-tests.md.

## Test File Structure

- Tests live in `playwright/tests/`; one file per feature or page.
- Imports: `test, expect, Page` from `@playwright/test`; `TableHelper`, `ApiHelper` from `../helpers/...`; `utils` helpers; `faker` from `@faker-js/faker`.
- `test.describe` holds `new TableHelper()` and `new ApiHelper()`; optional shared `prepareTest(page, data)` setup.
- Arrange/Act/Assert; prefix test data with `TEST_DATA_PREFIX`.

## Navigation Patterns

- Dashboard: `apiHelper.gotoWithWait(page)`; custom path `gotoWithWait(page, '/custom-path')` (waits for network idle).
- Menu: `navigateToAccess(page, '󰵲 Galaxies')`; custom regex `navigateToAccess(page, name, /.*~list$/)`.
- Row to view: `apiHelper.triggerAndWaitWithRegex(page, page.getByText(name), /.*~get$/)`.
- Back: `backNavigation(page)` (network wait default); `backNavigation(page, '󰁍 Back', { checkNetwork: false })`.

## Form Interactions

- Text: `fillPrimitiveField(page, "Name *", value)`. Optional 3rd arg `true` when a modeled filter is present (uses nth selector). Fourth/fifth args `false, false` skip back-check (faster, less safe). Verify with `checkPrimitiveFieldHasValue(page, name, value)`.
- Text fields commit after a short debounce. If `fill()` does not register (Update/Create stays disabled, or missing required attribute), use `field.fill('')`, `field.pressSequentially(text, { delay: 20 })`, then `field.blur()`.
- Checkbox: `fillPrimitiveCheckBox(page, name, true|false)`; verify `checkCheckboxPrimitiveCheckBoxHasValue`.
- Enum: `fillEnumCombobox(page, page, name, option)`; verify `checkEnumCombobox(page, name, option)`.
- Binary: read-only text field shows file name, next to icon button titled `Upload file` wrapping a hidden file input. Upload via file chooser or `setInputFiles`; assert the file name in the text field.
- Dates: format `MM/DD/YYYY HH:MM:SS`, e.g. `fillPrimitiveField(page, "Discovered", '11/05/2024 12:12:12')`.

## CRUD Operations

- Create: `navigateToAccess` → `createOnAccesList(page)` → `fillPrimitiveField` → `submitOnAccesListCreate(page)` (waits for list refresh).
- Update: change fields → `updateAccessViewPage(page)`.
- Delete: click `button '󰗨 Delete'`, then `button 'Yes'`.

## Table Interactions

- `tableHelper.getRow(page, n)`: row 0 is header; first data row is 1. `getRows(page)` excludes header. Count with `toHaveCount`.
- `tableHelper.getCell(row, "dataField")`: cell by column `data-field`. Assert with `toContainText` or `toHaveText`.
- `assertRows(tableHelper, page, [[{cellName, textOperation, value}], ...])` for multiple rows; `assertRowContent(tableHelper, page, rowIndex, [...])` for one row's cells.
- `textOperation` values seen: `Contain`, `Have`, `BooleanValue`.
- Boolean cells: icon class `mdi mdi-check-circle JUDO-mdi-icon true` on `> div span`. Values: `'true'`, `'false'`, `'undefined'`.
- Select rows: `selectRowsOnTable(page, page, [names])`; all: `selecAllRowsOnTable(page)` (sic spelling in helper).
- Sort: click `.MuiDataGrid-columnHeaderTitle` with `hasText` via `apiHelper.triggerAndWait`.

## Filtering

- `openAddAndApplyFilters(page, apiHelper, [{ attributeName, startOption, option, value, type }])`; types `text`, `enum`.
- Text options: `Like` (contains), `Equal`, `Not equal`, `Matches` (regex), `Less than`, `Greater than`, `Less or equal`, `Greater or equal`.
- Numeric options: `Equal`, `Not equal`, less/greater variants, `Is empty`, `Is not empty`.
- Boolean: `Is empty`, `Is not empty`. Enum: `Equal` (dropdown).
- Same field twice: add `operationNth: 1` (second operation dropdown) and `valueNth: 1` (second value input).
- Clear: `openClearAndApplyFilters(page, apiHelper, currentFilterCount)` clears and applies empty set; `clearFilters(page)` clears only.

## Relation Handling

### Single Relation (Autocomplete)

- Select: `fillSingleRelationElement(page, page, "Owner", "John Doe")` (triggers range API).
- Verify: `checkSingleRelationElementHasValue(page, name, value)`; empty: `checkEmptySingleRelationElement(page, name)`.
- Unset: `unsetSingleRelationElement(page, page, name, true)` (3rd arg `true` = update after). Delete related: `deleteSingleRelationElement(page, page, name, true)`. Open related view: `navigateToSingleRelation(page, page, name)`.
- Picker popups render OUTSIDE the dialog: open the picker inside the dialog, but locate and click the option from `page`.
- Create related: `createSingleRelationElement(page, page, name, [{type: 'string'|'numeric'|'boolean', name, value}], true)`.
- Attach from selector: `attachOnSingelRelationElement(page, page, relation, filterAttr, filterValue, updateAfter, onSettedElement)`; `onSettedElement` true if already has value.

### Collection Relations

- Open relation table (button opens separate page): `navigateToCollectionRelationButton(page, page, "Stars")`.
- Create inline: `createCollectionRelationElement(page, page, [{type, name, value}])`.
- Bulk unlink: select rows then `bulkRemoveOnTable(page)`. Bulk delete: `selecAllRowsOnTable(page)` then `bulkDeleteOnTable(page)`.

## Operations (Actions)

- Simple op: click `button '󰖕 Create Life'`, or via `button '󰖚 Actions 󰅀'` then `menuitem`.
- With input: `callOperationWithInput(page, page, '󰅂 createEntity', '󰖚 Actions')`; fill fields; `submitOperationCall(page, page, '󰅂 Submit', /.*get$/)`.
- Mapped input (selector): click op button, select grid cells (`gridcell` name), then submit with `triggerAndWaitWithRegex` on `button '󱓞 Submit'`.
- Output: trigger, confirm `Yes`, assert output textbox value.
- Errors: assert `dialog` text (`An error occurred`) and `listitem` (e.g. `errorCode: Validation failed`); close with `button 'Close'`.

## Dialog Handling

- Confirmation: click action, then `button 'Yes'` or `button 'No'`.
- Form dialog: `const dialog = page.getByRole('dialog')`; fill fields in it; `acceptChangesOnDialogElement(page, dialog)`.
- Draft-mode dialogs label submit from translation key `judo.dialogs.draft.submit` (default `Ok`); an app translation may change it (e.g. `Submit`). Look up by the app's label.
- Dialog close icon: `data-testid` `<container XMIID>-dialog-close-wrapper`; not in generated `VisualElementIds.ts`.

## Waiting for API Responses

- `apiHelper.triggerAndWaitWithRegex(page, locator, regex)`.
- Common patterns: `/.*~list$/` (list data), `/.*~get$/` (single entity), `/.*template$/` (form template), `/.*~validate$/` (validation), `/.*range$/` (relation range query).

## Test Data Management

- Always prefix: `TEST_DATA_PREFIX + faker.string.alpha(10)` (e.g. `X_TEST_AbCdEfGhIj`).
- Generators: `faker.string.alpha`, `faker.internet.email`, `faker.number.int({min, max})`, `faker.number.float({min, max, precision})`, `faker.date.past().toISOString()`.
- Display numbers: `formatNumber(id)` gives thousands separators (`1,234,567`); compare with `toHaveValue`.
