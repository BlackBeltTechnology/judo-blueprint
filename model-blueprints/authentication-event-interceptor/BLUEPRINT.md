---
id: authentication-event-interceptor
title: "Authentication Event Interceptor (Login Tracking and Audit)"
impl_only: true
usage_count: 3
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
  - indamedia-adtrack
  - park-here
---

## Description

An `AuthenticationInterceptor` that hooks into the JUDO authentication pipeline to perform side effects on user login. Common behaviors include updating a `lastLogin` timestamp, creating an audit log entry, or auto-provisioning a User entity on first login from JWT claims. This is an implementation-only blueprint -- it intercepts the `_principal` operation (which resolves the authenticated user) and performs updates that cannot be expressed declaratively in the model.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
