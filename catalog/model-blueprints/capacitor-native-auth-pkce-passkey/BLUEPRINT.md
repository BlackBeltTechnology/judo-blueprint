---
id: capacitor-native-auth-pkce-passkey
title: "Capacitor Native Auth with PKCE and Passkey Support"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A comprehensive native authentication system for Capacitor (Android) apps that replaces the standard OIDC redirect flow with a dual-mode login: Direct Access Grants (ROPC) for username/password and PKCE-secured Chrome Custom Tab flows for WebAuthn passkey login/registration. The system manages token lifecycle (SecureStorage-backed persistence, automatic refresh, offline resilience), syncs auth state to OIDC sessionStorage format for axios compatibility, and handles edge cases like WebView kill recovery, required password updates, and browser logout cookie cleanup. Web users continue to use the standard OIDC redirect flow unmodified.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
