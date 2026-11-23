---
id: error-handler-interceptor-customization
title: Error Handler Interceptor Customization
description: "A frontend hook that intercepts business errors (HTTP 422) and shows their message as a snackbar, instead of the generated fault dialog, while other errors keep the default handling."
aliases: [error interceptor hook, 422 snackbar handler]
keywords: [error, handler, interceptor, customization, 422, business error, snackbar, frontend]
tags: ["domain:model", "layer:frontend", "project:park-here", "project:mlszksz-platform", "status:emerging"]
category: pattern
status: emerging
projects: [park-here, mlszksz-platform]
evidence: ["park-here:unrecorded", "mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/src/custom/hooks/register-error-handler-interceptor.ts"]
alternatives: []
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Show a business error to the user as a short message, instead of the generated fault dialog. The platform already sends a modeled business fault as HTTP 422, with a body keyed by the fault; the generated frontend opens a fault dialog for it. This blueprint is common practice on top of that: the frontend registers an error handler interceptor and chooses a different display.

### The hook decides what to intercept

A predicate says whether the hook handles an error. Everything the predicate rejects keeps the generated handling. The hook never takes over validation or server errors.

### The backend stays the source of the rule

The business rule is enforced in the backend, as a modeled fault (or a fault thrown from an interceptor through `InterceptorCallBusinessException`). The hook is a display choice. Removing the hook must not change what the backend allows.

## Structure

The application registers one error handler interceptor hook with the platform's interceptor key (`ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`). The platform runs it before the default handling. The hook returns two parts (`shouldInterceptError`, `interceptError`): a predicate that matches a 422 business error, and a handler that reads the message from the response and shows it as a snackbar with an automatic hide. The message exists only when the fault carries a message attribute; that is a project convention, not something the platform adds. Both parts share one detection function, so they always agree.

## Constraints

- The hook intercepts only the 422 business error. Field validation (400) and server errors keep their default handling.
- The message is read from the response body. The 422 body is keyed by the fault's full name (and also carries a `code` key after it), so the reader takes the first key's entry and its `message` attribute. The platform's own fault dialog reads the first key the same way.
- The generated batch/CRUD dialog renders faults itself and is not affected by the interceptor. Test both paths.
- The hook must not show a message for an error it did not intercept.
- The hook is registered once per application, through the customizer's registration function.

## Variations

- **Fault dialog fallback.** When the body has no message, fall back to the generated fault dialog, so the user still sees the error.
- **Matched fault translations.** Use the modeled fault's full name as the business error's type (for a fault thrown from an interceptor, the `type` argument). The generated fault dialog then finds its translations (`faults.<fqn>.<attr>`). With any other type name, the request still returns 422, but the dialog falls back to raw attribute names, and the hook has to supply the text itself.
- **Several predicates.** Add a predicate for each error scenario, and share the detection callback between the predicate and the handler.
- **Location-less errors.** Show a 400 error that has no field location as a message, because the generated handling would otherwise show only a generic validation toast. The platform's example hook also intercepts a 400 that carries an explicit `code`.
- **Open the fault dialog from the hook.** The hook may call the fault dialog itself with the first key and its payload, for example to keep the dialog for some faults.

## When to use

- Business errors are frequent and the generated dialog is too heavy for them (a short message is enough).
- The application already sends business errors as 422 with a message in the body.
- A project-wide consistent look for business errors is wanted.

## When to avoid

- The application wants the generated fault dialog with its full translations. Keep the default and translate the fault.
- The business error needs a choice from the user (retry, confirm). A dialog is better.
- The errors are field-level. Those belong under their fields.

## Related

- [[error-code-enum]]: the business error vocabulary whose message this hook shows
- [[validation-exception-hierarchy]]: field-level validation errors, which this hook does not intercept
- [[typed-exception-error-handling]]: typed exception handling in the backend
