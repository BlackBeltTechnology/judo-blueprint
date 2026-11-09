---
id: recaptcha-waf-interceptor
title: reCAPTCHA WAF Interceptor for Public Operations
description: "An `OperationCallInterceptor` that validates reCAPTCHA tokens on public-facing operations (e.g., registration, verification) to block bot traffic."
aliases: []
keywords: [recaptcha, waf, interceptor, public, operations]
tags: ["domain:model", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

An `OperationCallInterceptor` that validates reCAPTCHA tokens on public-facing operations (e.g., registration, verification) to block bot traffic. This is an implementation-only blueprint -- it is a cross-cutting security concern implemented entirely in backend Java code, with no model-level representation.

The interceptor extracts a `recaptcha` field from the operation's input payload in `preCall()`, rejects requests with missing tokens, and supports a bypass mode (via system property or environment variable) for development and testing.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
