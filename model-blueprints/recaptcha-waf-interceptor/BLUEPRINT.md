---
id: recaptcha-waf-interceptor
title: "reCAPTCHA WAF Interceptor for Public Operations"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

An `OperationCallInterceptor` that validates reCAPTCHA tokens on public-facing operations (e.g., registration, verification) to block bot traffic. This is an implementation-only blueprint -- it is a cross-cutting security concern implemented entirely in backend Java code, with no model-level representation.

The interceptor extracts a `recaptcha` field from the operation's input payload in `preCall()`, rejects requests with missing tokens, and supports a bypass mode (via system property or environment variable) for development and testing.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
