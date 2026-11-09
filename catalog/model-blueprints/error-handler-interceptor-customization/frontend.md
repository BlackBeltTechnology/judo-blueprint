## Overview

A Pandino hook that intercepts specific HTTP error responses (e.g., 422 business validation errors) and shows user-friendly snackbar notifications instead of the default fault dialog. Framework: React.

## Implementation Pattern

- **Hook type**: `ErrorHandlerInterceptorHook` from `~/utilities/error-handling`
- **Registration key**: `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY`
- **Registration**: A `registerErrorHandlerInterceptorHook(context: BundleContext)` function called from `application-customizer.tsx`
- **Hook shape**: Returns an object with `shouldInterceptError(error, options)` (boolean predicate) and `interceptError(error, options, payload, dataPath)` (handling logic)
- **Internal hooks**: Uses `useTranslation()` for i18n, `useSnacks()` for `showErrorSnack`, and `useFaultDialog()` as a fallback
- **Error matching**: Typically checks `error.response?.status === 422` for business validation errors; can be extended with additional checks on response body structure
- **Message extraction**: Reads the first key from `error.response.data` and displays its `.message` property via snackbar with auto-hide
- **Extensibility**: Multiple error scenarios can be handled by adding more predicate functions (extracted via `useCallback` for reuse between `shouldInterceptError` and `interceptError`)

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/register-error-handler-interceptor.ts`
- Pattern: Intercepts HTTP 422 errors and shows the first validation error message as a snackbar notification with 3-second auto-hide, replacing the default fault dialog for business rule violations
- Notable: Uses a shared `isSomethingError` callback for both `shouldInterceptError` and `interceptError` to ensure consistent error detection; logs all errors to console for debugging

### park-here
- Framework: React
- Key files: `custom/hooks/register-error-handler-interceptor.ts`
- Pattern: Intercepts HTTP 422 errors and displays the first validation error message as a snackbar with 3-second auto-hide, identical structure to the rackinspect implementation
- Notable: Same `isSomethingError` useCallback pattern; confirms this is a stable, project-independent pattern that follows the generated template with minimal customization needed
