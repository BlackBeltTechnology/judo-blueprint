---
id: capacitor-native-auth-pkce-passkey
title: Capacitor Native Auth with PKCE and Passkey Support
description: A native login for a Capacitor Android app that uses a direct username and password grant plus a PKCE passkey flow in a Chrome Custom Tab, while the web keeps the standard OIDC redirect.
aliases: [native passkey login, capacitor auth]
keywords: [capacitor, native, auth, pkce, passkey, webauthn, token, offline]
tags: [domain:model, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/src/custom/auth/pkce-utils.ts", "mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/capacitor.config.ts"]
alternatives: [keycloak-magic-link-passkey-authentication]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Let a Capacitor Android app sign users in without the web redirect that a WebView cannot complete well. The app offers a username and password form and a passkey option, keeps tokens across restarts, and keeps working offline for the refresh-token lifetime.

### Native and web use different login paths

The native path replaces the redirect with a login screen. The web keeps the standard redirect unchanged, so the same code base serves both.

### Passkey login is an authorization-code flow with PKCE

The passkey flow opens in a Chrome Custom Tab and returns through a deep link. PKCE protects the code exchange. The app must finish the exchange even when the WebView was restarted in between.

### Offline use depends on error type

A rejected token clears the session. A network failure does not. This keeps a user signed in while offline, within the refresh-token lifetime.

## Structure

The pattern is a frontend layer. It has a native auth provider that wraps the app on native platforms, a login screen with two methods, an auth service that calls the identity provider's token and URL endpoints, a PKCE helper that holds the flow state, a token store with a mirror in the OIDC format, and a logout hook that takes the native or web path. None of these modules is a platform API; they are application code, and their names are examples only.

## Constraints

- The native path runs only when the app is on a native platform. The web path must not change.
- A password grant is an application choice for the native login. The platform's generated actor client has direct access grants enabled, so the grant itself needs no extra Keycloak setting for that client; a separate native client must enable it. Do not expose it on the web.
- PKCE state expires after a few minutes and blocks a second start while one is pending.
- A server rejection clears tokens; a network failure keeps them.
- The deep-link redirect URI is registered with the identity provider for the native client. A different redirect URI fails the exchange. The platform's generated Keycloak client uses `redirectUris=["*"]`; a separate native client needs its own redirect URIs.
- The backend derives the actor from the token's `azp` claim (dashes become dots, and the result must equal an actor FQN). A native client with another id is rejected unless it is whitelisted in `acceptableClients` (`ActorFQN=client1,client2`) or mapped with the Keycloak login interceptor's `clientToActorMap`.

## Variations

- **Password only.** Drop the passkey option when the identity provider has no WebAuthn support for the realm.
- **Passkey only.** Drop the password form for users who must register a passkey first; keep the password update flow for required resets.
- **Runtime backend switcher.** For test and review builds, a dialog on the login screen changes the backend base URL at runtime. The choice (production, test or custom URL, validated as http or https) is kept in local storage and read first when the app resolves its API base URL on native; the web build ignores it. On apply, the dialog removes only the auth entries (tokens and pending PKCE state) from secure storage, because a token from one server is invalid on another, keeps other secure entries such as push registration, and reloads the app. Keep the test option behind a build-time setting so production builds do not show it.
- **Shared store for web and native.** Use one token store on both platforms when the web also needs offline support. The native-only pieces stay behind the platform check.

## When to use

- A Capacitor Android app must sign users in with a passkey or a password.
- Users must stay signed in offline for a bounded period.
- The web app already uses the standard OIDC redirect and must not change.

## When to avoid

- The app runs only in a browser. The standard redirect flow is enough.
- The identity provider cannot issue a token for the native client. Use a server-side session instead.
- Passkeys are not required and the passwordless magic link is preferred. See [[keycloak-magic-link-passkey-authentication]].

## Related

- [[keycloak-magic-link-passkey-authentication]]: the server-side passwordless integration this native flow can pair with
- [[capacitor-native-file-handling]]: the other native Capacitor concern, file download and open
- [[custom-theme-with-native-status-bar]]: native-only UI behaviour in the same Capacitor app
- [[user-with-organization-and-role]]: the user model that holds the signed-in principal
