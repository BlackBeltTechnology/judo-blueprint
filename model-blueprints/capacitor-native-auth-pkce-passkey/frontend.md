## Overview

A platform-aware authentication system for JUDO React frontends that run inside Capacitor (Android). On native, it bypasses the standard OIDC redirect and provides a custom login screen with username/password (ROPC) and WebAuthn passkey (PKCE + Chrome Custom Tab) flows. On web, the standard `react-oidc-context` AuthProvider is used unchanged. Framework: React.

## Implementation Pattern

The pattern involves several coordinated modules:

- **NativeAuthProvider** (`custom/auth/NativeAuthProvider.tsx`) -- A React component that wraps the entire app on native platforms. It manages cold-start token restoration from `capacitor-secure-storage-plugin`, automatic token refresh scheduling, PKCE callback handling via `App.addListener('appUrlOpen')`, and renders either a loading spinner, the `NativeLoginScreen`, or the authenticated app.
- **NativeLoginScreen** (`custom/auth/NativeLoginScreen.tsx`) -- MUI-based login form with username/password fields, "Forgot password" link (opens Keycloak reset in Chrome Custom Tab), and "Sign in with Passkey" button. Error messages are i18n-aware (`custom.login.error.*` keys).
- **auth-service** (`custom/auth/auth-service.ts`) -- Low-level Keycloak token endpoint calls: `login()` (ROPC), `refreshTokens()`, `exchangeCode()` (authorization code exchange after passkey flow), `logout()`, plus URL builders for passkey auth, passkey registration, password update, and browser logout.
- **pkce-utils** (`custom/auth/pkce-utils.ts`) -- PKCE code verifier/challenge generation using Web Crypto API, state management in SecureStorage with double-tap guard and 5-minute auto-expiry. Tracks flow type (`passkey-login`, `passkey-register`, `password-update`).
- **token-storage** (`custom/auth/token-storage.ts`) -- Dual-layer storage: `capacitor-secure-storage-plugin` for encrypted persistence, `sessionStorage` as write-through cache. Syncs to OIDC format (`oidc.user:{realm}:{clientId}`) so existing axios interceptors work without modification. Also syncs auth state to Capacitor Preferences for native Firebase messaging service.
- **useLogout** (`custom/auth/useLogout.ts`) -- Platform-aware logout hook: native path deactivates push device, clears tokens, revokes Keycloak session; web path uses standard `signoutRedirect`.
- **auth-constants** (`custom/auth/auth-constants.ts`) -- Native redirect URI (`hu.mlszksz.platform://auth/callback`) and Keycloak client ID.

**Registration in application-customizer.tsx**: The auth system is not registered via Pandino hooks -- it is integrated at the app bootstrap level by overriding `src/main.tsx`, `src/AuthenticatedApp.tsx`, and `src/auth/Auth.tsx` (listed in `.generator-ignore`). The NativeAuthProvider conditionally wraps the app tree when `Capacitor.isNativePlatform()` is true.

**Key design decisions**:
- Offline tokens (30-day) survive network errors -- `TokenRejectedError` (HTTP 400/401) clears tokens; generic errors retry
- Passkey preferences (`passkey.owner`, `passkey.email`) persist across logout so users can "Sign in with Passkey" without re-registering
- Keyboard blur delay (400ms) before React re-render prevents Android WebView touch dispatch corruption

## Examples

### mlszksz-platform
- Framework: React (Capacitor Android)
- Key files: `custom/auth/NativeAuthProvider.tsx`, `custom/auth/auth-service.ts`, `custom/auth/pkce-utils.ts`, `custom/auth/token-storage.ts`, `custom/auth/NativeLoginScreen.tsx`, `custom/auth/useLogout.ts`
- Pattern: Full Keycloak ROPC + PKCE passkey auth for native Android, synced to OIDC sessionStorage for axios compatibility
- Notable: Chrome Custom Tab deep link handling with WebView kill recovery; passkey registration via `kc_action=webauthn-register-passwordless`; `TokenRejectedError` class distinguishes server rejection from network failure
