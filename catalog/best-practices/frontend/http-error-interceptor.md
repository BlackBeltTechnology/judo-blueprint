---
id: http-error-interceptor
title: HTTP Error Interceptor for Global Error Handling
description: "Register a global HTTP error interceptor via Pandino that catches specific HTTP status codes (e.g., 422 Unprocessable Entity) and displays error messages from the response body as snackbars."
aliases: []
keywords: [http, error, interceptor, global, handling]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: component
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [centralized-error-handling-validation-map]
related: [error-code-mapping-pattern, application-customizer-hub, centralized-error-handling-validation-map]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Register a global HTTP error interceptor via Pandino that catches specific HTTP status codes (e.g., 422 Unprocessable Entity) and displays error messages from the response body as snackbars. This provides centralized error handling that applies to all service calls without requiring per-call try/catch blocks. The interceptor is registered in `application-customizer.tsx` and implemented in a separate file.

## Structure

```typescript
// register-error-handler-interceptor.ts
export const errorHandlerInterceptor = {
  shouldInterceptError: (error) => error.response?.status === 422,
  interceptError: (error) => {
    const key = Object.keys(error.response.data)[0];
    showErrorSnack(
      error.response.data[key].message,
      { autoHideDuration: 3000 }
    );
  },
};

// Registration in application-customizer.tsx
context.registerService(
  ERROR_HANDLER_INTERCEPTOR_KEY,
  errorHandlerInterceptor
);
```

## Examples

### RackInspect
Intercepts HTTP 422 responses globally. Extracts the first error key from `error.response.data`, reads the `message` property, and shows it as an error snackbar that auto-hides after 3 seconds. This handles backend validation errors from all service calls without per-call error handling.

## Trade-offs

- **Pros**: Centralized error handling; consistent error display; no boilerplate per service call; catches errors across the entire application
- **Cons**: Generic handling may not suit all error types; cannot trigger specific UI flows (like re-registration); may conflict with per-call error handling
- **When to use**: As a safety net for common error scenarios (validation failures, business rule violations) that should show a message

## Related

- [[error-code-mapping-pattern]]
- [[application-customizer-hub]]
- [[centralized-error-handling-validation-map]]

