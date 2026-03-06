---
id: "error-code-mapping-pattern"
title: "Backend Error Code to UI Flow Mapping"
domain: "frontend"
category: "component"
score: 69.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
---
## Description

Map backend error codes from API responses to specific UI actions or flows. Instead of showing generic error messages, the frontend inspects the error response structure, extracts error codes, and triggers contextual actions (e.g., re-registration flow on INVALID_CODE, specific error messages for validation failures). This creates a richer user experience by handling known error scenarios gracefully.

## Structure

```typescript
try {
  await someServiceCall();
} catch (e: any) {
  const keys = Object.keys(e?.response?.data);
  if (keys.length) {
    const errorData = e?.response?.data[keys[0]];
    const code = errorData.code;

    switch (code) {
      case 'INVALID_CODE':
        openRegistrationDialog();  // Trigger re-registration
        break;
      case 'PATTERN_VALIDATION_FAILED':
        showError(errorData.message);  // Show server message
        break;
      case 'IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION':
        showError('Nickname already taken!');  // Custom message
        break;
      default:
        showError('Something went wrong.');
    }
  }
}
```

## Examples

### Trivia
Player frontend maps 3 error codes: `INVALID_CODE` triggers re-registration dialog, `PATTERN_VALIDATION_FAILED` shows the server-provided error message, `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION` shows "Nickname already taken!". Error codes are extracted from `e.response.data[firstKey].code` using `getErrorCodeLiteralByOrdinal()`.

### RackInspect
Registers a global HTTP error interceptor via `register-error-handler-interceptor.ts` that intercepts all 422 responses. Extracts the first error key from `error.response.data` and shows the `message` field as an error snackbar with 3-second auto-hide. This is a centralized approach vs Trivia's per-call handling.

## Trade-offs

- **Pros**: Better UX than generic errors; enables recovery flows (re-auth, retry); backend can communicate specific issues
- **Cons**: Tight coupling between frontend and backend error code contract; requires maintaining error code mappings; error structure parsing can be fragile
- **When to use**: Any application with known error scenarios that require specific UI responses

## Related Patterns

- [generated-service-layer-reuse](generated-service-layer-reuse.md)
- [localstorage-session-persistence](localstorage-session-persistence.md)
- [http-error-interceptor](http-error-interceptor.md)
