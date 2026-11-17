---
title: E2E test troubleshooting
description: Common Playwright E2E failures and fixes.
aliases: [e2e test failing, playwright test timeout, element not found in playwright, e2e failures in CI, filter not applied in test, relation selector empty, backend suite green but no tests ran]
keywords: [getByRole, getByLabel, TableHelper, openAddAndApplyFilters, fillSingleRelationElement, triggerAndWaitWithRegex, playwright.config.ts, retries, APP_URL, storageState, operationNth, valueNth]
tags: [domain:testing, layer:test, status:platform]
---

# E2E Test Troubleshooting

## Common Issues and Solutions

### Test Execution Issues

#### Tests fail with "Target page, context or browser has been closed"

**Cause**: Page navigation or action completed before test could interact.

**Solution**: Add explicit waits for elements:
```typescript
// Wait for element before interacting
await page.getByRole('button', { name: 'Submit' }).waitFor({ state: 'visible' });
await page.getByRole('button', { name: 'Submit' }).click();

// Or use ApiHelper to wait for API
await apiHelper.triggerAndWaitWithRegex(
  page,
  page.getByRole('button', { name: 'Submit' }),
  /.*~validate$/
);
```

#### Tests timeout waiting for API responses

**Cause**: Wrong regex pattern or API not called.

**Solutions**:
1. Check the network tab to see actual API endpoints
2. Update regex pattern to match:
```typescript
// Debug: Log all network requests
page.on('response', response => {
  console.log(response.url());
});

// Common patterns
/.*~list$/      // List endpoints
/.*~get$/       // Get single entity
/.*template$/   // Form templates
/.*~validate$/  // Validation
/.*range$/      // Autocomplete/selector
```

3. Increase timeout in playwright.config.ts:
```typescript
projects: [
  {
    name: 'chromium',
    timeout: 4 * 60 * 1000, // 4 minutes
    use: {
      actionTimeout: 10000,
    },
    expect: {
      timeout: 5000
    }
  }
]
```

#### Element not found with getByRole/getByLabel

**Cause**: Element not rendered, wrong selector, or element inside shadow DOM.

**Solutions**:
1. Use Playwright Inspector to find correct selector:
```bash
npx playwright test --debug
```

2. Try alternative selectors:
```typescript
// By role
page.getByRole('button', { name: 'Submit' })

// By label
page.getByLabel('Name')

// By text
page.getByText('Submit')

// By test ID (if available)
page.getByTestId('submit-button')

// By CSS (last resort)
page.locator('.MuiButton-root')

// By data attribute
page.locator('[data-field="name"]')
```

3. Check if element is in dialog:
```typescript
// Wrong - looks in entire page
page.getByLabel('Name');

// Correct - scoped to dialog
page.getByRole('dialog').getByLabel('Name');
```

4. Watch for several elements with the same accessible name. Generated pages can contain, for example, a column menu button and the input of the same field, so `getByLabel('<Field>')` may match more than one element. Prefer the generated element ids: every generated visual element carries `data-testid` equal to its id (exported by the generated `VisualElementIds.ts`), and dropdown menu items use their id as `data-testid`. Otherwise narrow the lookup, for example `getByRole('textbox', { name })` or a scope inside `getByRole('dialog')`.

### Data Grid Issues

#### Table rows not found

**Cause**: TableHelper uses specific selectors for MUI DataGrid.

**Solution**: Ensure using correct row indexing:
```typescript
const tableHelper = new TableHelper();

// Row 0 is header, data starts at row 1
const firstDataRow = tableHelper.getRow(page, 1);
const secondDataRow = tableHelper.getRow(page, 2);

// For scoped tables (in dialogs)
const dialogTable = tableHelper.getRow(page.getByRole('dialog'), 1);
```

#### Cell content assertion fails

**Cause**: Cell name doesn't match data-field attribute.

**Solution**: Check actual data-field in browser DevTools:
```typescript
// Find correct cell name
// Open DevTools > Elements > Find the cell
// Look for: <div data-field="fieldName">

// Use exact data-field value
tableHelper.getCell(row, "name");        // correct
tableHelper.getCell(row, "Name");        // wrong - case sensitive
tableHelper.getCell(row, "entityName");  // wrong - use model attribute name
```

#### Boolean cell assertions fail

**Cause**: Wrong CSS class expected.

**Solution**: Use correct BooleanValue assertion:
```typescript
// Correct classes
await expect(cell.locator('> div span')).toHaveClass('mdi mdi-check-circle JUDO-mdi-icon true');
await expect(cell.locator('> div span')).toHaveClass('mdi mdi-close-circle JUDO-mdi-icon false');
await expect(cell.locator('> div span')).toHaveClass('mdi mdi-minus JUDO-mdi-icon undefined');

// Or use helper
await assertCellContent(tableHelper, page, 1, {
  cellName: 'active',
  textOperation: 'BooleanValue',
  value: 'true'  // or 'false' or 'undefined'
});
```

### Filter Issues

#### Filters not applied

**Cause**: Missing wait for API after applying filters.

**Solution**: Use openAddAndApplyFilters which includes wait:
```typescript
// Correct - waits for API
await openAddAndApplyFilters(page, apiHelper, [
  { attributeName: 'Name', startOption: 'Like', option: 'Like', value: 'Test', type: 'text' }
]);

// Manual approach with wait
await openFilter(page, true);
await addFilter(page, 'Name', 'Like', 'Like', 'Test', 'text');
await applyFilters(page, apiHelper, 1, true);  // true = doWait
```

#### Multiple filters on same field fail

**Cause**: Need to specify operationNth and valueNth for additional filters.

**Solution**:
```typescript
await openAddAndApplyFilters(page, apiHelper, [
  { attributeName: 'Name', startOption: 'Like', option: 'Like', value: 'A', type: 'text' },
  { 
    attributeName: 'Name', 
    startOption: 'Like', 
    option: 'Not equal', 
    value: 'AB', 
    type: 'text',
    operationNth: 1,  // Second dropdown
    valueNth: 1       // Second input
  }
]);
```

### Form Issues

#### Form field not accepting input

**Cause**: Field disabled, readonly, or covered by overlay.

**Solutions**:
1. Check field state:
```typescript
await expect(page.getByLabel('Name')).toBeEnabled();
await expect(page.getByLabel('Name')).toBeEditable();
```

2. Wait for loading to complete:
```typescript
await page.waitForLoadState('networkidle');
await fillPrimitiveField(page, "Name", "Value");
```

3. Check for overlays:
```typescript
// Wait for loading overlay to disappear
await page.locator('.MuiBackdrop-root').waitFor({ state: 'hidden' });
```

#### Enum combobox doesn't open

**Cause**: Click target wrong or options not loaded.

**Solution**:
```typescript
// Ensure clicking the right element
await page.getByLabel('Status').click();
await page.waitForTimeout(200);  // Wait for dropdown animation

// Or force click
await page.getByLabel('Status').click({ force: true });
```

#### Text input value is lost or Create reports a missing required attribute

**Cause**: Generated text fields (`DebouncedTextField`) hand the value to the form state after a debounce (200 ms by default). Clicking Create/Update right after `fill()` can submit before the value is stored.

**Solution**: Type with real key presses, blur the field, and wait for the Create/Update button to be enabled before clicking:
```typescript
const field = page.getByRole('textbox', { name: 'Name' });
await field.pressSequentially('Value', { delay: 20 });
await field.blur();
await expect(page.getByRole('button', { name: /Create|Update/ })).toBeEnabled();
```

#### File upload button not found by role

The generated binary input is a text field showing the file name, plus an icon button with only a `title` (`Upload file`) that wraps a hidden file input. `getByRole('button', { name })` does not find it. Use the title and the file chooser event:
```typescript
const chooser = page.waitForEvent('filechooser');
await page.getByTitle('Upload file').click();
(await chooser).setFiles('path/to/file.png');
```

### Relation Issues

#### Autocomplete doesn't show options

**Cause**: Range API not triggered or no matching results.

**Solution**:
```typescript
// Use fillSingleRelationElement which handles API wait
await fillSingleRelationElement(page, page, "Owner", "John");

// Manual approach with proper wait
await apiHelper.triggerAndWaitWithRegex(
  page,
  page.getByRole('combobox', { name: 'Owner' }),
  /.*range$/
);
await page.getByRole('combobox', { name: 'Owner' }).fill('John');
await page.waitForTimeout(200);
await page.getByRole('option', { name: 'John Doe' }).click();
```

#### Selector dialog is empty

**Cause**: Range API not fetching data.

**Solution**: Apply filter to narrow results:
```typescript
await openSingleRelationSelector(page, page, "Owner");
await openAddAndApplyFilters(page, apiHelper, [
  { attributeName: 'Name', startOption: 'Like', option: 'Like', value: 'John', type: 'text' }
]);
await page.getByRole('gridcell', { name: 'John Doe' }).click();
```

### Operation Issues

#### Operation button disabled

**Cause**: Precondition not met (data validation, state check).

**Solution**: Ensure required data exists:
```typescript
// Check button state
await expect(page.getByRole('button', { name: '󰖕 Process' })).toBeDisabled();

// Create required data
await createCollectionRelationElement(page, page, [
  { type: 'string', name: 'Name', value: 'Required Item' }
]);

// Save
await updateAccessViewPage(page);

// Button should be enabled now
await expect(page.getByRole('button', { name: '󰖕 Process' })).toBeEnabled();
```

#### Operation input form doesn't open

**Cause**: Wrong regex pattern for template endpoint.

**Solution**:
```typescript
// Check pattern matches API
await apiHelper.triggerAndWaitWithRegex(
  page,
  page.getByRole('button', { name: '󰅂 Operation' }),
  /.*template$/  // or /.*~template$/
);
```

### Action not visible in an action group

An action group shows only its first `featuredActions` actions as buttons; the remaining actions are inside a dropdown button with `data-testid` `<XMIID>-button-group`. Open the dropdown first, then click the menu item (menu items carry their own id as `data-testid`). The featured count is a model property of the action group.

### Environment Issues

#### Tests work locally but fail in CI

**Causes**:
1. Different timing (CI is slower)
2. Missing dependencies
3. Different browser versions

**Solutions**:
1. Retries: the generated `playwright.config.ts` already sets `retries: 4` unconditionally (the template comment says "Retry on CI only", but the value is not conditional), so failing tests are retried 4 times locally as well. To retry only on CI, change it yourself:
```typescript
// playwright.config.ts
retries: process.env.CI ? 4 : 0,
```
Note that `workers` is already CI-dependent (`process.env.CI ? 2 : undefined`) and `trace` is `on-first-retry`.

2. Increase timeouts for CI:
```typescript
timeout: process.env.CI ? 5 * 60 * 1000 : 2 * 60 * 1000,
```

3. Use consistent browser:
```typescript
projects: [
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] }
  }
]
```

#### `ACCESS_TOKEN_EXPIRED` in a long test

An expired Keycloak access token makes the backend answer HTTP 401 with code `ACCESS_TOKEN_EXPIRED`. The token lifetime is a Keycloak realm setting (access token lifespan), so a single long test (many steps, screenshots at several widths) can outlive it. Keep each test shorter than the lifespan or split it into tests that each log in.

#### APP_URL not working

**Cause**: Environment variable not loaded.

**Solution**: Ensure .env file exists and dotenv is configured:
```bash
# .env file in playwright directory
APP_URL='http://localhost:8181'
```

```typescript
// playwright.config.ts
import 'dotenv/config';

export default defineConfig({
  use: {
    baseURL: (process.env.APP_URL || 'http://localhost:8181') + '/AppName/Actor'
  }
});
```

#### Backend test suite reports green but test classes never ran

**Cause**: The JUDO backend/integration suite forks several JVMs, each with its own heap (configured in `test/pom.xml`). Memory builds up from class to class; when a JVM dies with `Java heap space`, every class still queued on it never runs, yet the aggregate result can still look green (for example "524 tests, 0 failures" while hundreds of classes were never executed).

**Solutions**:
1. Raise the per-JVM heap (for example to 4 GB) in `test/pom.xml`.
2. Do not run scenarios in parallel on a local machine; run them one after another or class by class.
3. Do not trust the aggregate pass count: confirm that all test classes actually ran (compare the number of executed classes with the number of test classes, and check the build exit code and logs for `OutOfMemoryError`).

## Debugging Techniques

### Visual Debugging

```bash
# Run with UI mode (interactive)
npx playwright test --ui

# Run with browser visible
npx playwright test --headed

# Debug specific test
npx playwright test tests/MyTest.spec.ts --debug

# Slow down execution
npx playwright test --slow-mo=500
```

### Screenshots and Videos

```typescript
// playwright.config.ts
use: {
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
  trace: 'on-first-retry'
}
```

### Console Logging

```typescript
test('Debug test', async ({ page }) => {
  // Log page console
  page.on('console', msg => console.log('PAGE:', msg.text()));
  
  // Log network
  page.on('response', response => {
    console.log('API:', response.status(), response.url());
  });
  
  // Pause execution
  await page.pause();
  
  // Take screenshot
  await page.screenshot({ path: 'debug.png' });
});
```

### View Test Report

```bash
# Generate and open HTML report
npx playwright show-report
```

### Test Data Accumulates Between Runs

The E2E database and Keycloak users persist between runs. Failed or repeated runs leave rows that break counts, strict-mode locators and paging.

- Use unique, stamped names (for example `` `Item ${Date.now()}` ``) and filter by your own stamp.
- Clean up leftovers in the seed or an `afterAll`.
- Never assert absolute row counts.

### Shared Data and Parallel Workers

Tests that share seeded data (one cart, one stock level, one user) interfere when run by parallel workers. Run such suites serially (`workers: 1`) or give each test its own user and its own records.

### Hidden Columns and Rows in the Data Grid

The generated table is an MUI DataGrid: it renders only the visible columns and the current page of rows. Use a wide viewport (or scroll the grid horizontally) before reading a late column, and filter before looking for a row that may be on another page.

### Helpers Imported Across Generated Playwright Projects

Each generated Playwright project (one per actor) has its own `node_modules`. Importing helpers from another actor's project loads a second copy of `@playwright/test`, and Playwright reports `Requiring @playwright/test second time` and `No tests found`. Copy the helpers, or share them from one package that is not part of either project.

## Performance Tips

### Speed Up Tests

1. **Reuse authentication**:
```typescript
// Save auth state
await page.context().storageState({ path: 'auth.json' });

// Reuse in tests
test.use({ storageState: 'auth.json' });
```

2. **Parallel execution**:
```typescript
// playwright.config.ts
fullyParallel: true,
workers: process.env.CI ? 2 : undefined
```

3. **Skip unnecessary waits**:
```typescript
// Use waitForTimeout sparingly
await page.waitForTimeout(200);  // Only when necessary

// Prefer element-based waits
await page.getByRole('button').waitFor({ state: 'visible' });
```

4. **Batch test data creation**:
```typescript
// Create all test data in single setup
test.beforeAll(async ({ browser }) => {
  const page = await browser.newPage();
  await createTestData(page);
  await page.close();
});
```

### Run a Smoke Subset Per Change

Suggestion: tag a small set of tests with `@smoke`, run the new spec plus `--grep @smoke` after each change, and run the full suites once at the end.

## Getting Help

1. **Playwright Documentation**: https://playwright.dev/docs/intro
2. **Check trace viewer**: Detailed execution timeline
3. **Review test videos**: Visual confirmation of failures
4. **Use Playwright Inspector**: Step through test interactively
