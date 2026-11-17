---
title: Frontend Error Handling
description: How the generated React frontend handles 400, 401, 403, 404, 422 and 500 responses, the operation fault dialog and fault translation keys.
aliases: [frontend error handling, HTTP error toast, operation fault dialog, business fault message, validation error field, customize 422 handling]
keywords: [useErrorHandler, error-handling.ts, useFaultDialog, openFaultDialog, OperationFaultDialog, registerErrorHandlerInterceptorHook, ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY, X-Fault, errorList, judo.error.validation-failed]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Frontend Error Handling

How the generated React frontend reacts to HTTP errors from the backend, how modeled faults are displayed, and how to customize this.

## Generated Error Handling Matrix

The generated `src/utilities/error-handling.ts` (hook `useErrorHandler`) maps HTTP statuses to UI feedback. Detection is by status code only; the `X-Fault` response header is never read.

| Status | Behaviour |
|--------|-----------|
| 400 | Toast `judo.error.validation-failed`. Inline field errors are shown only when `errorList[0].location` exists. |
| 401 | The axios response error handler clears the security storage and reloads the page, so a toast is mostly never seen. |
| 403, 404 | Toast (`judo.error.*` keys). |
| 422 | Operation fault: opens the fault dialog (see below). |
| 500 | Toast `judo.error.internal-server-error`. |
| other | Toast `error.unknown`. |

A custom error handler interceptor (`src/custom/hooks/register-error-handler-interceptor.ts.default`, interface key `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`, registered with `registerErrorHandlerInterceptorHook`) runs before the default handling and can take over a response.

The generated `FeedbackLevel` type is `'ERROR' | 'WARNING '`. The `WARNING` literal has a trailing space, so a comparison with `'WARNING'` does not match the type.

## Operation Fault Dialog (HTTP 422)

On 422 the handler takes only the first key of the response body (`Object.keys(data)[0]`) and calls `openFaultDialog(key, data[key])`. The `useFaultDialog()` hook returns `(faultObjectKey: string, payload: any) => void`; it opens an `OperationFaultDialog` in the stackable dialog provider with title `judo.error.error` and body `judo.error.business-fault`. Every payload entry is rendered as a key/value pair:

- label: `t('faults.<faultPrefix>.<faultObjectKey>.<attribute>', { defaultValue: <attribute name> })`
- `data-testid`: `faults.<faultObjectKey>.<attribute>`

Add the `faults.*` keys to your translation files (see [i18n](./i18n.md)); without them the raw attribute name is shown. The batch/CRUD dialog variant (`useCRUDDialog`) builds messages from `error.response.data` keys as `faults.<faultPrefix>.<object>.<attribute>` and renders them itself, so it is not affected by an interceptor that replaces the 422 handling.

## Validation Errors Without Location

For 400 responses, field mapping happens only when the first error has a `location`. Errors without `location` are grouped under an empty key and no field shows them; only the generic validation toast appears. The generated `system_en-US.json` translates the platform validation codes (21 keys, for example `MISSING_REQUIRED_ATTRIBUTE`, `MAX_LENGTH_VALIDATION_FAILED`, `PATTERN_VALIDATION_FAILED`, `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION`, `NOT_ACCEPTED_BY_RANGE`); any other code falls back to the raw code string. Add `judo.error.validation-failed.<CODE>` keys for your own codes.

Validation errors (HTTP 400) are translated with the key `judo.error.validation-failed.<CODE>`, falling back to the raw code (`defaultValue: error.code` in `utilities/error-handling.ts`). Example: `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION` ("Identifier attribute is not unique") is returned when a value is already used by another instance of an entity whose attribute is marked as identifier; its details carry `feature` (attribute name) and `value`. Override the text by adding that key to the app's i18n files.

## Customizing the 422 Handling

To show the business message in a snack instead of the fault dialog, register an error handler interceptor that intercepts 422 responses (see [Error Handler Interceptor Customization](../../model-blueprints/error-handler-interceptor-customization/BLUEPRINT.md)). A project can do this: its interceptor intercepts all 422 responses and shows a short snack with `data[firstKey].message`. Because `useCRUDDialog` still renders `faults.*` itself, test both paths.

## Known Issue: Long-Running Operations

If a long-running operation seems to be dropped with HTTP 503 after about 30 seconds, check proxy and gateway timeouts in front of the backend first; no request timeout is configured in the generated service layer templates.
