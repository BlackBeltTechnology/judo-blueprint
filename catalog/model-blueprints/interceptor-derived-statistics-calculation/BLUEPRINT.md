---
id: interceptor-derived-statistics-calculation
title: "Interceptor-Based Derived Statistics Calculation"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
---

## Description

A pattern for computing derived statistics fields that cannot be expressed in JUEL (the model's expression language) by using `OperationCallInterceptor` postCall hooks. The interceptor intercepts list/refresh operations on statistics transfer objects, executes DAO count queries with date-arithmetic filters, and injects the computed values directly into the response payload.

This is an implementation-only blueprint -- it addresses a JUEL limitation (no date arithmetic) by performing the calculation in a Java interceptor rather than in the model's derived attribute expressions.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
