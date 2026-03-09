## Overview

Implements passwordless authentication via Keycloak magic link emails and WebAuthn passkey support. Spans two Maven modules: a `keycloak-client` (OSGi services wrapping the Keycloak Admin API) and `keycloak-extensions` (Keycloak SPI deployed into the Keycloak server for custom authenticators and action tokens).

## Implementation Pattern

The pattern is split across three architectural layers:

**1. Keycloak Extensions Module (SPI)** -- deployed into the Keycloak server as a JAR:
- `MagicLinkAuthenticator` / `MagicLinkAuthenticatorFactory` -- custom Keycloak `Authenticator` SPI that sends a magic link email containing an action token
- `MagicLinkActionToken` / `MagicLinkActionTokenHandler` -- custom `ActionToken` SPI that establishes a session when the user clicks the magic link
- `MagicLinkResource` / `MagicLinkResourceProvider` -- custom REST resource endpoint (`/realms/{realm}/magic-link`) that generates magic links programmatically (called by the backend)
- `MagicLink` utility class -- shared logic for creating action tokens, validating emails, sending emails, and setting up default flows

**2. Keycloak Client Module (OSGi)** -- backend services that call the Keycloak Admin API:
- `KeycloakFactory` -- builder-pattern factory that creates `Keycloak` admin client instances with `CompositeClassLoader` for OSGi compatibility
- `KeycloakConnectorActivator` -- `@Component(immediate=true)` that configures the realm on startup with retry logic (resilience4j): creates realm, SMTP, browser flows, native client, WebAuthn policy, branding
- `KeycloakFlowCreator` -- static utility for programmatic authentication flow creation (magic link browser flow, native app passkey-first flow, WebAuthn configuration)
- `RealmManager` -- `@Component(service=RealmManager.class)` that provides user CRUD, magic link generation, passkey registration link, and forgot-password email via the Keycloak Admin REST API
- `KeycloakUserServiceImpl` / `MagicLinkServiceImpl` / `ForgotPasswordServiceImpl` -- thin OSGi service wrappers that delegate to `RealmManager` with the platform's default realm name

**3. Common Module Service Interfaces** -- consumed by custom operations across the app:
- `KeycloakUserService` -- `createUser(email, firstName, lastName)`, `updateUser(email, firstName, lastName)`
- `MagicLinkService` -- `requestMagicLink(realm, email, clientId, redirectUri, expirationSeconds)` with built-in retry logic
- `ForgotPasswordService` -- `sendForgotPasswordEmail(realm, email, clientId)`

**Key technical details:**
- All Keycloak Admin API calls use `CompositeClassLoader` to bridge the OSGi bundle class loader with the system class loader (required for RestEasy/JAX-RS in OSGi)
- Startup initialization uses resilience4j `Retry` with exponential backoff, running on a daemon thread
- The native app authentication flow is passkey-first: WebAuthn discoverable credentials (resident keys) trigger automatically; password form is a fallback sub-flow
- Magic link generation calls a custom REST endpoint deployed in the Keycloak extensions module (not the Admin API)

## Examples

### mlszksz-platform
- Key files: `keycloak-client/osgi/KeycloakConnectorActivator.java`, `keycloak-client/osgi/RealmManager.java`, `keycloak-client/osgi/KeycloakFlowCreator.java`, `keycloak-extensions/MagicLink.java`, `keycloak-extensions/auth/MagicLinkAuthenticator.java`
- Pattern: Two-module Keycloak integration -- OSGi client module manages realm config + user operations; Keycloak SPI extension module provides custom magic link authenticator and action token handler
- Notable: `KeycloakConnectorActivator` runs async realm setup with resilience4j retry on startup. `KeycloakFlowCreator.createNativeAppBrowserFlow()` builds a passkey-first flow with WebAuthn discoverable credentials as primary and username+password as fallback. `RealmManager.requestPasskeyRegistrationLink()` adds `webauthn-register-passwordless` required action then generates a magic link that opens a browser session triggering the WebAuthn registration ceremony.
- DI wiring: `KeycloakFactory` (OSGi @Component) -> `RealmManager` (@Reference KeycloakFactory) -> `KeycloakUserServiceImpl` / `MagicLinkServiceImpl` (@Reference RealmManager) -> consumed by custom operations via `@Reference KeycloakUserService`
