---
id: "centralized-error-handling-validation-map"
title: "Centralized Error Handler with Validation Map"
domain: "frontend"
category: "component"
score: 34.2
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
alternatives:
  - http-error-interceptor
---
## Description

A centralized `errorHandling()` utility function that processes Axios errors and maps them to either field-level validation errors (displayed inline on form fields) or toast notifications. HTTP 400 responses are parsed into a `Map<string, string>` (field name to error message) and passed to `setValidation`. HTTP 422 responses show form-level error toasts. Other errors show generic toast notifications. Every service call wraps its catch block with this single function.

## Structure

```typescript
// error_handling.ts
export const errorHandling = (
  error: any,
  enqueueSnackbar: EnqueueSnackbar,
  options?: { setValidation?: (v: Map<string, string>) => void }
) => {
  if (error?.response?.status === 400) {
    // Map field errors to validation state
    const validationMap = new Map<string, string>();
    // ... parse error.response.data into field -> message pairs
    options?.setValidation?.(validationMap);
  } else if (error?.response?.status === 422) {
    enqueueSnackbar('Validation error', { variant: 'error' });
  } else {
    enqueueSnackbar('Something went wrong', { variant: 'error' });
  }
};

// Usage in every service call
try {
  await service.update(data);
} catch (error) {
  errorHandling(error, enqueueSnackbar, { setValidation });
}
```

## Examples

### ActionGroupTestReact
`errorHandling()` in `src/utilities/error_handling.ts` is used in every CRUD operation across 20+ pages. 400 errors populate `validation` Map state which drives `error` and `helperText` props on TextFields. 422 errors show form-level toasts. Validation is cleared on edit mode toggle or successful save.

## Trade-offs

- **Pros**: Single error handling function for all service calls; field-level validation feedback; consistent toast behavior; simple to use
- **Cons**: Error response parsing is tightly coupled to backend error format; no support for nested field errors; per-call try/catch still required
- **When to use**: Any JUDO React frontend needing consistent error handling with inline field validation

## Related Patterns

- [http-error-interceptor](http-error-interceptor.md)
- [error-code-mapping-pattern](error-code-mapping-pattern.md)
- [view-edit-mode-toggle](view-edit-mode-toggle.md)
