---
id: operation-call-logging-interceptor
title: Operation Call Logging Interceptor (Cross-Cutting Debug Logger)
description: "A cross-cutting `OperationCallInterceptor` that logs every operation invocation for debugging and monitoring purposes."
aliases: []
keywords: [operation, call, logging, interceptor, cross, cutting, debug, logger]
tags: ["domain:model", "layer:backend", "project:rackinspect", "project:park-here", "status:emerging"]
category: pattern
status: emerging
projects: [rackinspect, park-here]
evidence: ["rackinspect:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

A cross-cutting `OperationCallInterceptor` that logs every operation invocation for debugging and monitoring purposes. This is an implementation-only blueprint -- it is a minimal interceptor that hooks into the JUDO dispatcher pipeline to log the fully qualified name of every operation as it is called, without modifying the request or response.

Unlike entity-specific interceptors (which target specific CRUD operations), this interceptor applies globally (or to a configurable set of operations) and serves as a development/debugging aid or an audit logging foundation. The pattern demonstrates how to implement the `OperationCallInterceptor` interface with a `preCall()` hook that extracts operation metadata via `AsmUtils.getOperationFQName()`.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
