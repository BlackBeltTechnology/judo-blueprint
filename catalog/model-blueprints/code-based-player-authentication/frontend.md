## Overview

The code-based player authentication pattern manifests in the React frontend as a fully custom registration and activation dialog flow that bypasses the JUDO-generated UI entirely. The player frontend overrides `App.tsx` to implement a custom single-page application with localStorage-based session management, where registration and activation are handled through purpose-built dialog components that call the generated service layer directly.

## Implementation Pattern

- **Complete App override**: The player frontend overrides `App.tsx` (listed in `.generator-ignore`) to replace the generated page-based navigation with a custom SPA. The app manages authentication state via `localStorage` keys for user ID, nickname, and code.
- **Two-step dialog flow**: Registration and activation are separate dialog components. `RegistrationDialog` collects email and nickname, calls `PlayerServiceForApplicationImpl.register()`. On success, it opens `ActivationDialog` which presents a 4-digit code input using a `NumberInputAutoFocus` custom component (individual digit fields with auto-advance).
- **Auto-submit on code completion**: The activation dialog auto-submits when all 4 digits are entered (checking `value.length === 4`), providing a streamlined UX without requiring a button click.
- **Error handling with ErrorCode enum**: The `Contest` component intercepts errors from the `enter` operation, parses the response for `ErrorCode.INVALID_CODE`, and re-opens the registration dialog when the stored code is no longer valid.
- **Session persistence**: User credentials (email, nickname, code) are stored in `localStorage` and restored on page load, enabling session continuity across browser refreshes. A "Reset" bottom navigation action clears all stored data.
- **Custom styled components**: `BlurDialog`, `BlurCard`, `ThreeDGlossyButton`, and `NumberInputAutoFocus` are shared across the registration flow, providing a glassmorphism design with frosted-glass backgrounds and glossy buttons.

## Examples

### trivia
- Framework: React
- Key files: `src/trivia/RegistrationDialog.tsx`, `src/trivia/ActivationDialog.tsx`, `src/trivia/CustomComponents.tsx`, `src/App.tsx`
- Pattern: Custom two-step registration flow using `PlayerServiceForApplicationImpl.register()` and `.activate()`. Email + nickname collected first, then a 4-digit activation code with auto-submit. Session state persisted in localStorage with keys `trivia-user-id`, `trivia-nickname-id`, `trivia-user-code-id`.
- Notable: The entire player frontend is a custom SPA -- no JUDO generated pages are used. The `NumberInputAutoFocus` component implements a PIN-entry UX with individual digit fields that auto-focus the next field on input.
