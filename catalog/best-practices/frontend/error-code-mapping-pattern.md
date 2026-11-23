---
id: error-code-mapping-pattern
title: Backend Error Code to UI Flow Mapping
description: Map backend error codes from failed calls to specific UI reactions in custom frontend code, instead of showing one generic message.
aliases: [error code switch, error code handling, contextual error handling]
keywords: [error code, validation, location, 400, 422, fault, switch, snackbar, error interceptor]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:rackinspect", "status:emerging"]
category: component
status: emerging
projects: [trivia, rackinspect]
evidence: ["trivia:unrecorded", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/register-error-handler-interceptor.ts"]
alternatives: []
related: [generated-service-layer-reuse, localstorage-session-persistence, http-error-interceptor]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A custom frontend call can fail in known ways (invalid registration code, duplicate name, pattern mismatch). Reading the error code from the response and reacting per code gives users a precise message or a recovery flow instead of a generic failure.

## Practice

### Platform base

- Validation failures are HTTP 400 with a list of results `{ code, message, location }`. `location` is optional (usually the attribute or relation name), and the platform emits some results without it (for example `AUTHENTICATION_REQUIRED`, `ACCESS_DENIED`, `INVALID_IDENTIFIER`). Platform codes include `MISSING_REQUIRED_ATTRIBUTE`, `MAX_LENGTH_VALIDATION_FAILED`, `PATTERN_VALIDATION_FAILED`, `NOT_ACCEPTED_BY_RANGE` ([backend error handling guide](../../agent-docs/backend/error-handling-guide.md)).
- Modeled faults and business exceptions are HTTP 422 with an `X-Fault` header and a body keyed by the fault type (`{ "<type>": { details }, "code": ... }`). Unexpected errors are 500 with code `INTERNAL_SERVER_ERROR`. A fault buried in a cause chain surfaces as 500.
- The generated frontend handles errors by status only: 400 shows the validation toast and inline field errors only when the first error has a `location`; 422 opens the fault dialog from the first body key; the `X-Fault` header is never read. Only three validation codes are translated by default; other codes fall back to the raw code string, and you add `judo.error.validation-failed.<CODE>` keys for your own ([frontend error handling](../../agent-docs/frontend/error-handling.md)).
- A custom error handler interceptor (scaffold `register-error-handler-interceptor.ts.default`, key `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`) runs before default handling and can take over a response globally.

### Practice notes: switch on the code in custom calls

For custom code that calls the generated service layer directly (see [[generated-service-layer-reuse]]), inspect the response and branch on the code:

```typescript
try {
  await someServiceCall();
} catch (e: any) {
  const body = e?.response?.data;
  const results = Array.isArray(body) ? body : Object.values(body ?? {});
  const first = results[0] as { code?: string; message?: string } | undefined;
  switch (first?.code) {
    case 'ACCESS_CODE_INVALID': // app-defined code
      openAccessDialog();
      break;
    case 'PATTERN_VALIDATION_FAILED':
      showError(first.message);       // server text
      break;
    default:
      showError(t('error.generic'));
  }
}
```

- Handle both shapes: a list for 400 and a fault-keyed object for 422; do not assume one first key.
- Show the server `message` when it is already translated; use your own text keyed by code when the product wording differs.
- Keep the code-to-action table in one module so it follows the backend contract; app-defined codes come from your modeled faults or validations.
- For one app-wide rule (for example a snack for every 422), use the error handler interceptor instead ([[http-error-interceptor]]); per-call mapping is for flows that need an action, such as opening a dialog.

## Rationale

Specific reactions improve recovery (re-registration, retry) and message quality. The price is coupling to the backend's code contract and parsing that can break when response shapes differ.

## Example

- A game frontend with three mapped codes: an invalid-code error reopens the access dialog, a pattern failure shows the server message, a uniqueness violation shows a fixed text. Codes are read from the first key of the response body.
- A frontend with a global error handler interceptor that takes every 422 response and shows its message as a short snackbar: the centralized alternative.

## When to avoid

- The generated handling (toast, fault dialog, field errors) is enough.
- One uniform reaction fits all errors: register an interceptor instead.

## Related

- [[generated-service-layer-reuse]] — calling the generated services from custom code
- [[localstorage-session-persistence]] — state kept across the re-registration flow
- [[http-error-interceptor]] — global handling of error responses
