## Overview

The error code / BusinessError pattern manifests in the React frontend through a custom error handler interceptor hook that intercepts HTTP 422 responses and displays the `message` field from the BusinessError transfer object as a user-facing error snack. Projects with an ErrorCode enum also include i18n translations for each enum member, enabling localized error display. In fully custom frontends, the ErrorCode enum may be consumed directly in component code for programmatic control flow (e.g., redirecting to registration on INVALID_CODE).

## Implementation Pattern

- **Error handler interceptor**: A Pandino hook registered with `ERROR_HANDLER_INTERCEPTOR_INTERFACE_KEY` provides `shouldInterceptError` and `interceptError` callbacks. The hook checks for HTTP 422 status (business error), extracts the message from the response data, and displays it via `showErrorSnack` with auto-hide.
- **Response parsing**: The interceptor reads `error.response.data`, extracts the first key, and uses its `.message` property -- accommodating the JUDO backend convention where business errors are keyed by the TO type name.
- **i18n for enum members**: Projects with an ErrorCode enum provide localized translations for each member (e.g., `enumerations.ErrorCode.PERMISSION_DENIED`) and for the BusinessError TO fields (`faults.*.BusinessError.errorCode`, `faults.*.BusinessError.message`).
- **No enum-level rendering in interceptor**: The error handler interceptor typically only displays the `message` text, not the enum code -- the enum code is used for programmatic error handling on the backend.
- **Direct enum consumption (custom SPA variant)**: In fully custom frontends that bypass the generated UI, the ErrorCode enum is imported directly into component code and used for programmatic branching. The `getErrorCodeLiteralByOrdinal()` utility converts numeric codes from error responses into typed enum values for conditional logic.

## Examples

### mlszksz-platform
- Framework: React
- Key files: `custom/hooks/register-error-handler-interceptor.ts`
- Pattern: The interceptor checks `error.response?.status === 422`, extracts the message with `error.response.data[key].message`, and shows it as an error snack with 3-second auto-hide duration.
- Notable: This project uses the simplified BusinessError variant (string code + message, no enum), so the frontend only needs to display the message text without enum translation.

### park-here
- Framework: React
- Key files: `custom/hooks/register-error-handler-interceptor.ts`, `public/i18n/application_hu-HU.json`
- Pattern: Uses the same HTTP 422 interceptor pattern as mlszksz-platform. The interceptor extracts `error.response.data[key].message` and shows it via `showErrorSnack` with 3-second auto-hide. The i18n file provides Hungarian translations for all 8 ErrorCode enum members (e.g., `enumerations.ErrorCode.TOO_MANY_RESERVATION`) and fault dialog labels for the BusinessError TO fields.
- Notable: Unlike mlszksz-platform, park-here has a typed ErrorCode enum with 8 members, and the i18n file includes translations for every member. However, the error handler interceptor still relies on the `message` string rather than translating the enum code client-side.

### trivia
- Framework: React
- Key files: `src/App.tsx`, `src/trivia/Contest.tsx`, `src/trivia/ActivationDialog.tsx`
- Pattern: The player frontend imports `ErrorCode` and `getErrorCodeLiteralByOrdinal` directly from generated model types. In `Contest.tsx`, error responses from the `enter` operation are parsed to extract the error code, converted via `getErrorCodeLiteralByOrdinal(code)`, and compared against `ErrorCode.INVALID_CODE` to trigger re-registration. In `ActivationDialog.tsx`, the error key `trivia.actors.player.Error` is used to extract the message from business error responses.
- Notable: This is a custom SPA variant that does not use the Pandino error handler interceptor. Instead, error codes are consumed programmatically in component-level catch blocks for control flow (e.g., `INVALID_CODE` reopens the registration dialog rather than just showing a snackbar). The actor-scoped `ErrorCode` enum (5 members: INVALID_CODE, CONTEST_NOT_OPEN, TEST_NOT_STARTED, TEST_ALREADY_STARTED, TEST_CLOSED) maps to quiz workflow preconditions.
