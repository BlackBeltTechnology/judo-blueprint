# README.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/README.md.

## Introduction
- Hook-based customization of generated React frontend; hooks registered in `src/custom/application-customizer.tsx` via Pandino.

## Core Concepts
- Hooks = customization points: modify components, add UI, filter/transform data, control navigation, customize validation, override operations.
- Benefits: no generated edits (all in `src/custom/`), upgrade-safe, type-safe.
- Not recommended: editing generated files (checksum fails build); `.default` stub or new file in `.generator-ignore`; template overrides.

## Hook Architecture
- `customize(context: BundleContext)` in `DefaultApplicationCustomizer`; `context.registerService<T>(INTERFACE_KEY, impl, props)`.
- Interface keys (e.g. `TABLE_ROW_HIGHLIGHTING_HOOK_INTERFACE_KEY`) exported from the owning module (`~/theme/table-row-highlighting`, `~/layout/Footer`) or generated `~/containers/<path>/customization` for container hooks. No `~/generated` barrel.
- Service properties filter scope: `{ component, column, page }`, e.g. `{ component: 'ServiceActivityForm', column: 'name' }`.
- Hook implementations must be React hooks for DI support; follow TS interfaces; return functions or config objects.
- Precedence: page-level overrides container-level; more specific overrides general.

## Available Hook Categories
- Data: `usePrincipal`, `useViewData` → `data-hooks.md`.
- UI: AppBar extras, hero/logo, footer text, menu manipulation (also guest page, sub-theme hooks, menu actions in `../extension-points.md`) → `ui-hooks.md`.
- Table: row highlighting, custom columns, sidekick (above-table UI), column customization → `table-hooks.md`.
- Action: container actions, page actions, operation flow, post-operation navigation → `action-hooks.md`.
- Navigation and access: redirect service, access filtering, hotkeys, navigation interception → `navigation-and-access.md`.
- Validation: Date/DateTime, field rules, custom messages → `validation-hooks.md`.

## Using .default Scaffold Files
- Generated scaffolds under `src/custom/hooks/`: error handler interceptor, `pages/`, `dialogs/`, `containers/`, `custom-implementations/`, `components/cards/`, `sub-themes/`, `registerMenuActionsHook.ts.default`, `default-guest-page-hook-registration.tsx.default`. Only hooks enabled in the model get one (e.g. `generateActionsHook`).
- `application-customizer.tsx` is NOT `.default`: plain generated file, empty `customize(context)`; call your `register...Hook(context)` there. Add it to `.generator-ignore` on first edit (One Rule case 1), else checksum fails or regeneration overwrites.
- Activate: `cp X.ts.default X.ts` (same dir, no `.default`), implement, call its register function from the customizer. Not compiled as-is.
- Copy is not generated → no `.generator-ignore` entry. Never edit the `.default` itself (regenerated each build). `src/custom/` is not gitignored; only `.default` files are.

## Common Template Patterns
- `hooks/pages/register<Page>ActionsHook.ts.default` — page action hooks → copy without `.default`.
- `hooks/containers/register<Container>ActionsHook.ts.default` — container action hooks → copy without `.default`.
- `hooks/dialogs/register<Dialog>ActionsHook.ts.default` — dialog action hooks → copy without `.default`.
- `hooks/sub-themes/register<Name>SubThemeHook.tsx.default` — sub-theme hooks → copy without `.default`.
- `src/theme/*.ts` (palette, typography, table-row-highlighting): plain generated → edit only with `.generator-ignore` entry.

## Complete Workflow Example
- Table row highlighting: `find src/custom -name "*.default"`; write hook in `src/custom/hooks/` (typed `TableRowHighlightingHook<T>` from `~/theme/table-row-highlighting`, returns array of `{name,label,backgroundColor,condition(params)}`); register in customizer; `pnpm run dev` (no `.generator-ignore` for hand-written files).

## Hook Registration Patterns
- Single: `registerService<TableRowHighlightingHook>(KEY, hook, { component: 'ServiceActivitiesTable' })`.
- Multiple: row highlighting, `TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY` (`{component, column}`), `SIDEKICK_COMPONENT_INTERFACE_KEY` (FC).
- Conditional: `process.env.NODE_ENV === 'production'`; `localStorage` feature flags.

## Understanding .generator-ignore
- Gitignore-style matching, scoped to generator output. Purpose: stop re-emitting a file at path X you hand-edited. NOT a "custom" marker; not needed for files the generator never produces.
- Three cases:
  1. Generator emits X, you hand-edit X in place → add X. Only legitimate case (e.g. `src/custom/application-customizer.tsx`, `src/theme/palette.ts`, edited file under `src/generated/`).
  2. `.default` rename: generator emits `X.default`; rename to `X` once. X is outside generator scope; NO entry. Do NOT add `X.default` either.
  3. Brand-new hand-written file at a path the generator never emits → NO entry.
- Purely custom entries are noise; remove them.
- Add when: generated file outside `src/custom/` edited directly (not preferred); custom file outside `src/custom/` collides with generated path.
- Don't add: own files under `src/custom/` (only `application-customizer.tsx`, `index.tsx`, `custom-element-types.ts`, `interfaces.ts` there are generated); unmodified `.default` or generated files.
- Verify: `grep` the file in `.generator-ignore`; `mvn clean install`; `git diff src/custom/` should show no unwanted changes.

## Best Practices
- Prefer hooks over direct edits to generated components.
- Activate scaffolds by copying; never edit `.default` in place.
- A copied scaffold survives `generate`. If its model element is removed, the `.default` is dropped but the copy still imports missing keys → build fails (e.g. `TS2305: Module has no exported member`). Delete or update the copy.
- Organize custom code under `src/custom/` (`hooks/`, `components/`, `utils/`, `application-customizer.tsx`).
- Document customizations with a doc comment (applied to component, updated date).
- Re-test after every `mvn clean install` + `pnpm run dev`.

## Troubleshooting
- Hook not executing: log in customizer; check component name with `grep -rn "component=" src/containers`.
- File overwritten after build: diagnose first; don't blindly add to `.generator-ignore`.
  - Brand-new file the generator never emits → case 3, no entry; investigate build output, formatter, git.
  - Generator emits stub and you hand-edited → case 1: add path to `.generator-ignore`.
  - `.default` stub exists → rename pattern (case 2).
- Type errors with hook interface: import from the defining module (`~/theme/table-row-highlighting`); `~/generated` barrel does not exist.

## Related Documentation
- `data-hooks.md`, `ui-hooks.md`, `table-hooks.md`, `action-hooks.md`, `navigation-and-access.md`, `validation-hooks.md`, `../README.md`.
