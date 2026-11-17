# troubleshooting.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/troubleshooting.md.

## Common Issues and Solutions
- Test Execution:
  - "Target page, context or browser has been closed": wait for element (`waitFor({state:'visible'})`) or `apiHelper.triggerAndWaitWithRegex(page, locator, regex)`.
  - API timeouts: regexes `/.*~list$/` (list), `/.*~get$/` (get), `/.*template$/`, `/.*~validate$/`, `/.*range$/`. Timeouts in `playwright.config.ts` (`timeout`, `use.actionTimeout`, `expect.timeout`).
  - Element not found: try `--debug`; locator order getRole/getLabel/getText/getTestId/CSS last resort; scope into `getByRole('dialog')`.
  - Duplicate accessible names: prefer `data-testid` = element id (generated `VisualElementIds.ts`); dropdown menu items use id as `data-testid`; else `getByRole('textbox', {name})`.
- Data Grid (MUI DataGrid via TableHelper):
  - Row 0 is header; data from row 1. Dialog tables: `tableHelper.getRow(page.getByRole('dialog'), 1)`.
  - Cell names = `data-field` (case-sensitive, model attribute name): `getCell(row, "name")`.
  - Boolean cells: classes `mdi mdi-check-circle JUDO-mdi-icon true` / `…mdi-close-circle … false` / `mdi mdi-minus … undefined`; or `assertCellContent(..., {textOperation:'BooleanValue', value})`.
- Filters:
  - Use `openAddAndApplyFilters(page, apiHelper, [...])` (waits for API). Manual: `openFilter`, `addFilter`, `applyFilters(page, apiHelper, 1, true)`.
  - Multiple filters on same field: `operationNth` (dropdown index) and `valueNth` (input index).
- Forms:
  - Disabled/readonly: `toBeEnabled()` / `toBeEditable()`; `waitForLoadState('networkidle')`; overlay `.MuiBackdrop-root` hidden.
  - Enum combobox: click label, `waitForTimeout(200)`, or `{force:true}`.
  - Text fields are `DebouncedTextField` (200 ms debounce): `pressSequentially`, `blur()`, then wait for Create/Update enabled.
  - File upload: no role button; `getByTitle('Upload file')` + `waitForEvent('filechooser')` + `setFiles(path)`.
- Relations:
  - Autocomplete: `fillSingleRelationElement(page, page, "Owner", "John")` or trigger `/.*range$/`, then option click.
  - Empty selector dialog: `openSingleRelationSelector` then `openAddAndApplyFilters`, click `gridcell`.
- Operations:
  - Button disabled: precondition data missing; create data (`createCollectionRelationElement`), save (`updateAccessViewPage`), then expect enabled.
  - Input form not opening: wait for `/.*template$/` (or `~template`).
- Action groups: only first `featuredActions` shown as buttons; rest in dropdown `data-testid` `<XMIID>-button-group`. Open dropdown first. Featured count is a model property.
- Environment:
  - CI vs local: generated `playwright.config.ts` sets `retries: 4` unconditionally (template comment says CI-only). Make it `process.env.CI ? 4 : 0` yourself.
  - `workers` already CI-dependent (`process.env.CI ? 2 : undefined`); `trace` is `on-first-retry`.
  - CI timeouts: `process.env.CI ? 5*60*1000 : 2*60*1000`.
  - Browser: `devices['Desktop Chrome']`.
  - `ACCESS_TOKEN_EXPIRED` (HTTP 401): Keycloak access token lifespan (realm setting). Keep tests shorter or log in per test.
  - `APP_URL`: `.env` in playwright dir (`APP_URL='http://localhost:8181'`), `import 'dotenv/config'`, `baseURL: (APP_URL || 'http://localhost:8181') + '/AppName/Actor'`.
  - Backend suite green but classes never ran: forked JVMs (`test/pom.xml`) run out of heap ("Java heap space"); queued classes never run yet aggregate looks green.
    - Raise per-JVM heap (e.g. 4 GB) in `test/pom.xml`; don't run scenarios in parallel locally; compare executed class count to test class count; grep logs for `OutOfMemoryError`.

## Debugging Techniques
- Visual: `npx playwright test --ui`, `--headed`, `<file> --debug`, `--slow-mo=500`.
- Config: `screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`, `trace: 'on-first-retry'`.
- Console: `page.on('console')`, `page.on('response')`, `page.pause()`, `page.screenshot`.
- Report: `npx playwright show-report`.
- Test data accumulates (E2E DB and Keycloak users persist): use stamped names (`` `Item ${Date.now()}` ``), clean up in seed or `afterAll`, never assert absolute row counts.
- Shared data + parallel workers: run serially (`workers: 1`) or per-test user/records.
- DataGrid renders only visible columns and current page: widen viewport or scroll horizontally; filter before looking for a row on another page.
- Helpers across generated projects (one per actor, own `node_modules`): importing loads a second `@playwright/test` → "Requiring @playwright/test second time" / "No tests found". Copy helpers or share from a package in neither project.

## Performance Tips
- Reuse auth: `context().storageState({path})`, `test.use({storageState})`.
- `fullyParallel: true`, `workers: process.env.CI ? 2 : undefined`.
- Avoid `waitForTimeout` except ~200 ms; prefer element waits.
- Batch test data in `beforeAll` (`browser.newPage()`, then close).
- Smoke subset: tag `@smoke`; run new spec + `--grep @smoke` per change; full suites once at end.

## Getting Help
- Playwright docs: https://playwright.dev/docs/intro
- Trace viewer for timeline; videos for failure visuals; Inspector to step through.
