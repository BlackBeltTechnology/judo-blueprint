---
id: error-handler-interceptor-customization
title: "Error Handler Interceptor Customization"
impl_only: true
usage_count: 2
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
  - park-here
---

## Description

A frontend-only pattern for intercepting and customizing error handling behavior in JUDO React applications. A custom `ErrorHandlerInterceptorHook` is registered via Pandino using the `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`. The hook intercepts specific HTTP error responses (e.g., 422 Unprocessable Entity for business validation errors) and displays user-friendly snackbar messages instead of the default fault dialog. The pattern allows selective interception -- `shouldInterceptError` determines if the hook handles a given error, and `interceptError` provides the custom handling logic. This is an implementation-only blueprint -- it provides a cross-cutting error handling customization layer.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
