---
id: error-handler-interceptor-customization
title: Error Handler Interceptor Customization
description: "A frontend hook that intercepts business errors (HTTP 422) and shows their message as a snackbar, instead of the generated fault dialog, while other errors keep the default handling."
aliases: [error interceptor hook, 422 snackbar handler]
keywords: [error, handler, interceptor, customization, 422, business error, snackbar, frontend]
tags: ["domain:model", "layer:frontend", "project:rackinspect", "project:park-here", "status:emerging"]
category: pattern
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-09
---
## Intent

Show a business error to the user as a short message, instead of the generated fault dialog. The backend already sends the business error as HTTP 422 with its message; the frontend only chooses how to display it.

### The hook decides what to intercept

A predicate says whether the hook handles an error. Everything the predicate rejects keeps the generated handling. The hook never takes over validation or server errors.

### The backend stays the source of the rule

The business rule is enforced in the backend, as a modeled business fault. The hook is a display choice. Removing the hook must not change what the backend allows.

## Structure

The application registers one error handler hook with the platform's error-handler interceptor key. The hook has two parts: a predicate that matches a 422 business error, and a handler that reads the message from the response and shows it as a snackbar with an automatic hide. Both parts share one detection function, so they always agree.

## Constraints

- The hook intercepts only the 422 business error. Field validation (400) and server errors keep their default handling.
- The message is read from the response body. The body is keyed by the fault's type name, so the reader takes the first key's message.
- The hook must not show a message for an error it did not intercept.
- The hook is registered once per application, through the customizer's registration function.

## Variations

- **Fault dialog fallback.** When the body has no message, fall back to the generated fault dialog, so the user still sees the error.
- **Matched fault translations.** Use the fault's full type name as the business error's type, so the generated fault dialog finds its own translations (`faults.<fqn>.<attr>`). With any other type name, no translation matches, and the hook has to supply the text itself.
- **Several predicates.** Add a predicate for each error scenario, and share the detection callback between the predicate and the handler.
- **Location-less errors.** Show a 400 error that has no field location as a message, because the generated handling would otherwise show only a generic toast.

## When to use

- Business errors are frequent and the generated dialog is too heavy for them (a short message is enough).
- The application already sends business errors as 422 with a message in the body.
- A project-wide consistent look for business errors is wanted.

## When to avoid

- The application wants the generated fault dialog with its full translations. Keep the default and translate the fault.
- The business error needs a choice from the user (retry, confirm). A dialog is better.
- The errors are field-level. Those belong under their fields.

## Related

- [[error-code-enum]] — the business error vocabulary whose message this hook shows
- [[validation-exception-hierarchy]] — field-level validation errors, which this hook does not intercept
- [[typed-exception-error-handling]] — typed exception handling in the backend
