---
id: http-error-interceptor
title: HTTP Error Interceptor for Global Error Handling
description: "Register the platform's error handler interceptor hook to show HTTP 422 business messages as a snackbar instead of the default fault dialog."
aliases: [422 snackbar interceptor, global error snack]
keywords: [error handler interceptor, ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY, 422, snackbar, shouldInterceptError, interceptError, fault dialog, Pandino]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: component
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/register-error-handler-interceptor.ts"]
alternatives: [centralized-error-handling-validation-map]
related: [error-code-mapping-pattern, application-customizer-hub, centralized-error-handling-validation-map]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Show a short message for business errors everywhere, instead of the default fault dialog, without try/catch in every service call.

## Practice

### Platform base

- The generated `src/utilities/error-handling.ts` (`useErrorHandler`) maps HTTP statuses to feedback, by status code only: 400 validation toast (inline field errors only when `errorList[0].location` exists), 401 clears security storage and reloads, 403/404/500 toasts, other statuses `error.unknown`, and 422 opens the operation fault dialog ([handling matrix](../../agent-docs/frontend/error-handling.md)).
- A custom error handler interceptor runs before the default handling and can take over a response. It is registered with `registerErrorHandlerInterceptorHook` under `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`, from the scaffold `src/custom/hooks/register-error-handler-interceptor.ts.default` ([interceptor hook](../../agent-docs/frontend/advanced-patterns.md)).
- The hook is a React hook (it may call `useSnacks`, `useFaultDialog`, `useTranslation`) returning `{ shouldInterceptError(error, options), interceptError(error, options, payload, dataPath) }`. The 422 body is keyed by the modeled fault object: `{ <faultKey>: { <attribute>: value } }`. The 400 body is a list of `{ code, message, location }`.
- Replacing the 422 handling skips the fault dialog, but the batch/CRUD dialog (`useCRUDDialog`) still renders `faults.*` messages itself, so test both paths ([customizing 422](../../agent-docs/frontend/error-handling.md)).

### Practice notes: 422 as a snackbar

The example intercepts every 422 and shows the `message` of the first fault key:

```typescript
const hook: ErrorHandlerInterceptorHook = () => {
  const { showErrorSnack } = useSnacks();
  return {
    shouldInterceptError: (error) => error.response?.status === 422,
    interceptError: (error) => {
      const data = error.response.data;
      const key = Object.keys(data)[0];
      showErrorSnack(data[key].message, { autoHideDuration: 3000 });
    },
  };
};
// register in application-customizer.tsx via registerErrorHandlerInterceptorHook(context)
```

- This works only if the modeled fault carries a `message` attribute; otherwise show a translated text per fault key.
- Intercept narrowly. Do not turn every 5xx into one subsystem message, the docs flag that as an anti-pattern.
- The snackbar cannot start special UI flows such as re-registration; leave those statuses to the default handling.

## Rationale

One interceptor gives uniform error display and no per-call boilerplate. It replaces the default dialog, which lists all fault attributes, with one line of text.

## Example

One app intercepts HTTP 422 globally, takes the first key of the response body, reads its `message` and shows an error snackbar that hides after 3 seconds. Backend validation and business rule errors from all service calls appear this way.

## When to avoid

- The default fault dialog with translated `faults.*` attribute labels is what users should see.
- Errors need field mapping or code-specific flows: see [[error-code-mapping-pattern]] and [[centralized-error-handling-validation-map]].

## Related

- [[error-code-mapping-pattern]] — mapping codes to messages
- [[application-customizer-hub]] — where the hook is registered
- [[centralized-error-handling-validation-map]] — the per-field alternative
