---
id: centralized-error-handling-validation-map
title: Centralized Error Handling with Validation Map
description: One error-handling function turns failed service calls into a field-to-message validation map for inline form errors, or into toasts, so every call site uses the same catch block.
aliases: [errorHandling utility, validation map]
keywords: [error handling, validation map, 400, 422, snackbar, toast, field errors, helperText, location]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: component
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: [http-error-interceptor]
related: [http-error-interceptor, error-code-mapping-pattern, view-edit-mode-toggle]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Every service call can fail with validation errors that belong to form fields or with errors that need a toast. Handling this once, in a shared function, gives uniform inline feedback and keeps call sites short.

## Practice

### Platform base

- The backend returns a failed request as JSON results with `code`, an optional `location` (for validation errors usually the attribute or relation name) and a `details` map. HTTP 400 is used for model-constraint violations such as missing required values or a value outside the range ([error response structure](../../agent-docs/backend/error-handling-guide.md)).
- The generated frontend already maps statuses: 400 shows a validation toast and inline field errors **only when the first error has a `location`**; 422 is a modeled operation fault shown in a fault dialog; 401 clears the session; 403 and 404 give toasts; 500 gives an internal-error toast. Detection is by status code only ([generated error handling matrix](../../agent-docs/frontend/error-handling.md)).
- Errors without `location` are grouped under an empty key and no field shows them; only three validation codes have default translations, others show the raw code ([validation errors without location](../../agent-docs/frontend/error-handling.md)).
- A custom error handler interceptor runs before the default handling and can take a response over ([customizing the 422 handling](../../agent-docs/frontend/error-handling.md)).

### Project practice: one function with a validation map

This layer is project practice (actiongroup-test-react), a hand-written frontend that does not use the generated handler:

- A single `errorHandling(error, enqueueSnackbar, { setValidation })` function wraps every catch block of every service call.
- For 400 it parses the response list into a `Map<fieldName, message>` keyed by `location` and passes it to `setValidation`; the form turns the map into `error` and `helperText` of each field. Errors without a `location` still need a toast, because no field can show them.
- For 422 it shows a form-level toast; for other errors a generic toast.
- Clear the map on edit-mode toggle and on a successful save.

```typescript
// Example project code
export const errorHandling = (error: any, enqueueSnackbar: EnqueueSnackbar,
    options?: { setValidation?: (v: Map<string, string>) => void }) => {
  const status = error?.response?.status;
  if (status === 400) {
    const map = new Map<string, string>();
    // parse the response list into location -> message pairs
    options?.setValidation?.(map);
  } else if (status === 422) {
    enqueueSnackbar('Business fault', { variant: 'error' });
  } else {
    enqueueSnackbar('Something went wrong', { variant: 'error' });
  }
};
```

## Rationale

One function gives consistent toasts and inline field feedback. The cost: parsing is coupled to the backend error shape, nested field errors are not supported, and every call still needs its own try/catch. With the generated frontend, prefer an error handler interceptor over a parallel utility ([[http-error-interceptor]]).

## Example

actiongroup-test-react uses the function in every create, update and delete call across more than twenty pages. 400 responses fill a validation map held in page state that drives the fields; 422 responses show a toast. The map is cleared when edit mode toggles or the save succeeds.

## When to avoid

- You use the generated frontend: its handler already covers these statuses, customize it through an interceptor instead.
- Errors rely on translated modeled faults, which the generated fault dialog shows; see [[error-code-mapping-pattern]].

## Related

- [[http-error-interceptor]] — central handling at the HTTP layer instead of per call
- [[error-code-mapping-pattern]] — mapping error codes to messages
- [[view-edit-mode-toggle]] — the toggle that clears the validation map
