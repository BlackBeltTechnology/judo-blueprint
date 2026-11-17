# validation-hooks.md — index

Pull-only condensed map. Source: catalog/agent-docs/frontend/hooks/validation-hooks.md.

## Overview
- Hook type names (`Service<Entity><Kind>ContainerHook`) are generated per container in `~/containers/<path>/customization`. Handler names in examples are illustrative: the returned object must match the generated container action type.
- Register with `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` from the same module, normally via scaffold `register<Container>ActionsHook` (see action-hooks.md).
- Server validation results: `{ location, code, message }` (see ../error-handling.md).

## Date/DateTime Validation
- Hook `getDateFieldValidationProps(formData)` returns `{ minDate, maxDate, shouldDisableDate(date), helperText }`.
- Date time variant: `getDateFieldTimeValidationProps` → `minDateTime`, `shouldDisableTime(value, clockType)` (`'hours'`), `helperText`.
- Named per field: `get<Field>ValidationProps` (e.g. `getFromDateValidationProps`, `getToDateValidationProps`).
- Business days: `shouldDisableDate: d => !isBusinessDay(d)`; holiday keys must use LOCAL date parts (`getFullYear/getMonth/getDate` padded). `toISOString()` is UTC and shifts the day for users off UTC, while `getDay()` is local.
- Patterns: date range (to ≥ from + 7 days), item within entity period, weekdays-only from parent entity.
- Registration: `context.registerService(SERVICE_<X>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, hook)` in `src/custom/hooks/containers/register<Container>ActionsHook.ts`.

## Field Validation
- Field validators go in `src/custom/application-customizer.tsx`: `applicationCustomizer.validators['<Form>'].<field>(value)` returns error string or nothing.
- Return string, never throw.
- Member names: required handler `is<Field>Required` (first letter upper, e.g. `isNameRequired`); also `is<Field>Hidden`, `is<Field>Disabled`, `is<Field>Readonly`; signature `(data, editMode, isLoading...) => boolean`. Take exact signature from generated `types.ts`. `isFieldRequired` is a placeholder only.
- Relation actions: `<relation><Kind>Action`; kinds `refreshAction`, `<relation>AutocompleteRangeAction`, `<relation>SelectorRangeAction`. Relation omitted on container's own table. Range override gets `(queryCustomizer)`, returns target rows.
- Cards container config: see Extension Points, Cards Configuration Hook.
- Examples: email regex, phone (strip spaces/dashes, 10 digits), URL (`new URL` try/catch), number ranges (parseFloat/parseInt, isNaN checks), conditional required via `validateField(fieldName, value, formData)`.

## Async Validation
- Call custom validation operations via `context.actions.getAction('<opName>')({ ...args })`; result in `result.data`.
- Return error string on failure; catch errors and return a message (no throw).
- Debounce with promise-based `debounceAsync` (put in `src/custom/utils/debounceAsync.ts`), 500 ms. Lodash `debounce` is wrong: it returns the previous call's result.
- Related-entity example passes `settlementId: data.settlement?.__identifier`; checks `isValid`, `message`, `qualityScore === 'LOW'`.

## Cross-Field Validation
- `validateForm(formData)` returns `Record<field, message>`; empty object = valid.
- Examples: from < to; amount per unit bounds (amount/quantity); password strength (report first failing rule only, else later check overwrites) plus `confirmPassword` match.

## Real-Time Validation
- `onFieldChange(fieldName, value, formData)` returns `{ error }`, optional `value` (truncate), or `{ helperText }`. `{ error: null }` clears.
- Character counter pattern: `${length}/${max} characters` helper text.

## Best Practices
- Specific error messages (e.g. "between 3 and 100 characters", not "Invalid title").
- Check value exists first (`if (!value) return 'Field is required'`).
- Debounce async calls; never call API per keystroke.
- Try/catch API validation; return message on failure.
- Custom validators live under `src/custom` (only `.default` twin generated; no `.generator-ignore` entry needed).

## Complete Example
- One `containerActions.tsx` combining `getFromDateValidationProps`, `getToDateValidationProps`, `validateTitle` (debounced availability check via `context.actions`), `validateForm` (cross-field).

## Troubleshooting
- Validation not triggering: check `context.registerService(...ACTIONS_HOOK_INTERFACE_KEY, hook)` registration.
- Async too slow: use `debounceAsync(fn, 500)`.
- Error not showing: return the string, do not throw.

## Related Documentation
- README.md (hook system overview), action-hooks.md, data-hooks.md, ../development-workflow.md
