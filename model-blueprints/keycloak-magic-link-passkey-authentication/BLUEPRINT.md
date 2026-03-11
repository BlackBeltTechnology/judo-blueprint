---
id: keycloak-magic-link-passkey-authentication
title: "Keycloak Magic Link and Passkey Authentication Integration"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A comprehensive Keycloak integration pattern that implements passwordless authentication via magic link emails and passkey (WebAuthn) support. This is an implementation-only blueprint -- it does not correspond to a specific model-level entity or enum, but rather implements authentication infrastructure as a separate Maven module ecosystem.

The pattern includes:
- A `keycloak-client` module (OSGi components) that manages realm creation, user provisioning, magic link generation, and passkey registration via the Keycloak Admin API
- A `keycloak-extensions` module (Keycloak SPI) that deploys a custom MagicLink authenticator, action token handler, and REST resource endpoint directly into the Keycloak server
- An activator that configures the realm on startup with retry logic, including SMTP, browser flows, native app OIDC client, WebAuthn policy, and branding
- Service interfaces in a `common` module (KeycloakUserService, MagicLinkService, ForgotPasswordService) that abstract the Keycloak Admin API behind OSGi services consumed by custom operations

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
