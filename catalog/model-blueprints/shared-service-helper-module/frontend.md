## Frontend guidance

All names here are examples from the source project, not platform API.

### Function shape

```ts
export function autoSetTimes(data: Input, storeDiff: (key: keyof Input, value: unknown) => void, workEnd: string) {
  if (!data.startTime) {
    storeDiff('startTime', new Date(Date.now() + 3 * 60_000));
    storeDiff('endTime', toTimeToday(workEnd));
  }
}
```

A hook calls it: `onUserBlurAction(data, storeDiff, editMode, submit) { onUserFieldBlurSetDefaults(data, storeDiff, editMode, submit); }`. The hook callback names and arguments come from the generated hook type of the page. See [action hooks](../../agent-docs/frontend/hooks/action-hooks.md).

### Function groups

- Field auto-computation, such as default times from the current time and working hours.
- Visibility flags set from an enumeration value (`storeDiff('hiddenByCustom', true)`; the flag is a project attribute).
- Defaults after the template loads, from preferences or related data.
- Date picker constraints returned as `{ minDate, maxDate }`.
- Enumeration option filtering by user permissions or flags.
- Warning text based on time proximity.
- Async defaults that call the REST client, for example a preferred resource whose availability is checked through the range call.

### Reuse across hooks

One module can be imported by several hook registrations, for example the panel for all reservations and the panel for one user's reservations. Keep the module free of page-specific keys.

### Async helpers

An async helper may create a client for the generated service with the project's HTTP provider. It may pass a mask so the related user comes back with nested data (cars, working times, preferred resource) in one request. A hook that awaits it must handle failure and return a safe default. See [[generated-service-layer-reuse]].

### Source project

React. One module has about fourteen exported functions and is used by four or more dialog hooks (reservation form logic). A second module handles holiday form defaults and looks up the affected reservations. See [[reservation-booking-entity]].
