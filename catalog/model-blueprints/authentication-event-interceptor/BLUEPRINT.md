---
id: authentication-event-interceptor
title: Authentication Event Interceptor (Login Tracking and Audit)
description: "An `AuthenticationInterceptor` that hooks into the JUDO authentication pipeline to perform side effects on user login."
aliases: []
keywords: [authentication, event, interceptor, login, tracking, audit]
tags: ["domain:model", "layer:backend", "project:mlszksz-platform", "project:indamedia-adtrack", "project:park-here", "status:emerging"]
category: pattern
status: emerging
projects: [mlszksz-platform, indamedia-adtrack, park-here]
evidence: ["mlszksz-platform:unrecorded", "indamedia-adtrack:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

An `AuthenticationInterceptor` that hooks into the JUDO authentication pipeline to perform side effects on user login. Common behaviors include updating a `lastLogin` timestamp, creating an audit log entry, or auto-provisioning a User entity on first login from JWT claims. This is an implementation-only blueprint -- it intercepts the `_principal` operation (which resolves the authenticated user) and performs updates that cannot be expressed declaratively in the model.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
