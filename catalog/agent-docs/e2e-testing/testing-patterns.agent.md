# testing-patterns.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/testing-patterns.md.

## Test Organization

- One spec file per feature or page: `EntityAccessTable.spec.ts`, `EntityViewPage.spec.ts`, `EntityOperations.spec.ts`, `EntityFiltering.spec.ts`, `RelationManagement.spec.ts`, `ErrorHandling.spec.ts`.
- Structure: `test.describe('Feature or Page Name')` with `test('Action and expected outcome')`.
- Test names state the action and the expected outcome.

## Setup Patterns

- `prepareTest(page, entityName, options?)` creates one entity through the access list: `gotoWithWait`, `navigateToAccess`, `createOnAccesList`, `fillPrimitiveField`, `fillPrimitiveCheckBox`, `submitOnAccesListCreate`.
- Test data names use `TEST_DATA_PREFIX + faker.string.alpha(10)` so records can be filtered by prefix.
- `prepareHierarchy` builds parent, child and grandchild through the view dialogs.
- Hierarchy steps: create parent, filter to find it with `openAddAndApplyFilters`, open with `triggerAndWaitWithRegex(..., /.*~get$/)`, create child via the Create button (`/.*template$/`), confirm with Ok (`/.*validate$/`), save with Update.
- Wait for backend calls with `apiHelper.triggerAndWaitWithRegex`; `waitForTimeout(200)` is used between steps.

## CRUD Testing Patterns

- Full lifecycle: create, read via filter and `tableHelper.getRows`, update via `navigateToAnAccessListElement` and `updateAccessViewPage`, delete with the Delete button and `Yes`, verify zero rows.
- Required-field check: submit empty form, expect `This field is required`.
- Button labels include Nerd Font glyph prefixes (for example `󰆓 Create`, `󰗨 Delete`); match them exactly.

## Filtering Test Patterns

- Filter rows with `openAddAndApplyFilters(page, apiHelper, [{attributeName, startOption, option, value, type}])`.
- Clear filters between checks with `openClearAndApplyFilters(page, apiHelper, n)`.
- String options: `Like`, `Equal`, `Not equal` (uses `operationNth` and `valueNth`), `Matches` (regex, e.g. `prefix + '#A+$'`).
- Numeric options: `Greater than` with `type: 'numeric'`.
- `Is empty` uses `type: 'boolean'` with an empty value.

## Operation Testing Patterns

- Operations without input: click the operation button or open the action group (`Actions`) and click the item; check the resulting state field.
- Operations with input form: open with `triggerAndWaitWithRegex(..., /.*template$/)`, fill fields, submit with `/.*get$/`.
- Mapped input (selector): Submit stays disabled until a row is picked from the table (`gridcell`).
- Operations with output: confirm with `Yes`, then assert the output dialog fields.

## Error Handling Patterns

- Inline validation: fill invalid value, submit, expect the field error text.
- Operation faults: the error dialog shows the message, then `errorCode: ...` and `message: ...` list items; close with `Close`; the operation button must be enabled again.
- Multiple error details: each field error appears as `field: message` in the list; the code is `MULTIPLE_ERRORS`.

## Relation Testing Patterns

- Single relation: `checkEmptySingleRelationElement`, `fillSingleRelationElement`, `checkSingleRelationElementHasValue`, `navigateToSingleRelation`, `backNavigation`, `unsetSingleRelationElement(page, page, name, true)`.
- Collection relation: `createCollectionRelationElement(page, page, [{type, name, value}])`, `selectRowsOnTable`, `bulkRemoveOnTable`, then save with `updateAccessViewPage`.

## Sorting Test Pattern

- Assert row order with `assertRows(tableHelper, page, [[{cellName, textOperation: 'Contain', value}], ...])`.
- Column sort: click the `.MuiDataGrid-columnHeaderTitle` header through `apiHelper.triggerAndWait`. First click sorts ascending, second descending.

## Conditional UI Testing

- Check that a button is disabled before its precondition and enabled after a related row is created.
- After the action runs, the button is disabled again.

## Dialog Flow Testing

- Open the wizard with `triggerAndWaitWithRegex(..., /.*template$/)`.
- Fill fields scoped to `page.getByRole('dialog')`, move with `Next`, submit the last step with `/.*get$/`.
- Verify the completion text.
