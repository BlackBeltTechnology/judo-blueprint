# language-independent-testing.md — index

Pull-only condensed map. Source: catalog/agent-docs/e2e-testing/language-independent-testing.md.

## Overview
- Prefer `data-testid`, `href` patterns and structural selectors over i18n labels.
- Tests then work across locales unchanged.

## Authentication with Keycloak
- Actor with a principal needs Keycloak login; use a Playwright `setup` project (`testMatch: /auth\.setup\.ts/`).
- Dependent `chromium` project: `dependencies: ["setup"]`, `storageState` = `.auth/user.json`.
- `auth.setup.ts`: `page.goto("/")`, wait `#kc-form-login`, fill `#username` and `#password`, click `#kc-login`, wait title, `storageState({ path })`.
- Keycloak ids: `#kc-form-login`, `#username`, `#password`, `#kc-login`, `#kc-registration`, `#kc-forgot-password`.
- `.auth/` is generated and gitignored.

## Language-Independent Selectors
- 1. Menu: `a[href*="/Service/Actor/Administration/"]`; patterns Administration, Dashboard, `/Service/Actor/{PageName}/`.
- 2. Tabs: `getByTestId` with ESM-generated ids.
- 3. Tab testid pattern: `Actor/(esm/_<ESM_ID>)/GroupTab-tab`.
- 4. View container: `Actor/(esm/_<id>)/TransferObjectViewVisualElement` (not `PageContainer`).
- 5. Generated `VisualElementIds` from `../helpers/visualElementIds/VisualElementIds`; access `.id` or `._id`.
- 6. Duplicate testids: add `.first()`.

## When i18n Labels Are Unavoidable
- Column headers have no testids; match locale text with `[role="columnheader"]` and `hasText`.
- Regex for multiple locales: `/Settlements|Települések/i`.

## Complete Navigation Example
- Helper: click Administration link, `waitForResponse` for `/api/` 200, wait view testid (15 s timeout), click tab, wait table `.first()`.
- Uses `ApiHelper.gotoWithWait(page, "/")`.

## Nested Tab Navigation
- Click parent group tab, then nested tab testid; wait nested table.

## Discovering Testids
- Debug test: `page.locator("[data-testid]").all()`, log tag and `data-testid`.

## CRUD Flags and UI Element Visibility
- Flags: C create button; R view and View button on rows; U edit fields and Attach/Detach; D Delete button on rows.
- Check model flags (`isCreateAllowed`, `isUpdateAllowed`, `isDeleteAllowed`) before writing tests; do not test absent buttons.
- Patterns: full CRUD, read-only (R), CR, RU. Use `pageActions.<name>.id` (create, delete, filter, refresh, attach, detach).
- Attach/Detach only with U flag.
- Parent flags govern navigated child: parent U=false → child view-only; parent D=false → no delete. Applies to grid row view, tag click, single relation link.
- Runtime override in JSON: `__updateable: false` disables edit for that record; `__deleteable: false` hides delete.
- Precedence: model flag false → disabled; model true + JSON false → disabled for that record; model true + JSON true or absent → enabled.
- Read-only relation example: test display and filter only.

## Summary: Selector Priority
1. Best: generated `VisualElementIds`.
2. Good: `href` patterns for menu links.
3. Good: model-based tab testids.
4. Acceptable: role selectors with regex for multiple locales.
5. Last resort: hardcoded i18n text; document locale.
- Always add `.first()` for possible duplicate testids in nested UI.
