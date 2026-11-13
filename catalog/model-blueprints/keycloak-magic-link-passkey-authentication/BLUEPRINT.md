---
id: keycloak-magic-link-passkey-authentication
title: Keycloak Magic Link and Passkey Authentication
description: A backend-only integration that gives Keycloak a magic-link sign-in and a passkey (WebAuthn) first flow, driven from an identity client service and a Keycloak extension.
aliases: [passwordless keycloak, magic link login, passkey login]
keywords: [keycloak, magic link, passkey, webauthn, passwordless, action token, authenticator, realm]
tags: [domain:backend, layer:backend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/keycloak-extensions/src/main/java/hu/blackbelt/mlszksz/platform/keycloak/extensions/auth/token/MagicLinkActionTokenHandler.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/MagicLinkService.java"]
alternatives: [capacitor-native-auth-pkce-passkey]
fragment: none: backend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Let users sign in without a password. A user gets a magic link by email, or registers a passkey, and the identity provider handles the sign-in. The JUDO platform does not implement authentication itself: it trusts a Keycloak access token and resolves its principal to an actor. The platform can already generate the realm and one client per actor from a `realm` annotation on the actor type (the platform's defaults are minimal: login with email, direct access grants). Everything in this entry on top of that, the extra realm setup, the magic link and the passkey flow, is project practice and not platform behaviour. The application configures Keycloak, calls Keycloak's admin interface, and adds a small extension to Keycloak for the magic-link step.

### Passwordless sign-in lives in the identity provider

The sign-in flows, the magic-link authenticator and the passkey step are Keycloak features, added through Keycloak's extension points. The application only starts and calls them.

### Passkey is the first factor on native apps

On native apps the flow tries a passkey first. A password form is the fallback. The user sees the password form only when no passkey is available.

## Structure

This entry has no model shape. The integration is backend code in two parts. A client part wraps the Keycloak administration interface and exposes services for user creation, magic-link requests and forgot-password emails. An extension part runs inside the Keycloak server and provides the magic-link authenticator, the action token that starts a session, and a REST endpoint that issues magic links on request.

## Constraints

- The magic link is an action token. It is single-use and expires.
- The passkey registration link adds a required action to the user, then issues a magic link that starts the registration in a browser session.
- The realm is set up once at startup, with retries. This is project code that goes beyond the realm and client the platform generates from the model, so the two must not disagree on names (the client id is the actor FQN with dots replaced by dashes). A failed setup must not leave a partly configured realm without a log entry.
- Administration calls run under a class loader that can see the Keycloak client libraries. Without it the JAX-RS calls fail inside the bundle runtime.
- Keycloak's email settings must be set for the realm, or the magic link is never delivered.

## Variations

- **Magic link only.** The browser flow offers a magic link and no passkey.
- **Passkey first on native apps.** A discoverable credential is tried first; the password form is a sub-flow.
- **Backend-issued magic link.** The backend asks the extension endpoint for a link and sends it with its own email template.

## When to use

- The product should offer passwordless sign-in.
- Keycloak already manages the users and realms.
- Native apps and browsers should share one identity provider.

## When to avoid

- The product has no identity provider. Build sign-in on the platform's own account model instead.
- Users must sign in only with a password by policy.
- Email delivery is not reliable. A magic link then leaves users locked out.

## Related

- [[idm-realm-keycloak-integration]] — the per-organization realm and the admin integration this pattern runs on
- [[capacitor-native-auth-pkce-passkey]] — a native-app authentication pattern with PKCE and passkeys
- [[invitation-with-key-based-acceptance]] — a key-based link acceptance, a related link-driven flow
