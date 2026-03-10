---
id: shared-service-helper-module
title: "Shared Service Helper Module for Form Logic"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - park-here
---

## Description

A frontend-only pattern for extracting shared form logic (field auto-computation, validation constraints, default initialization, and business rule application) into standalone TypeScript service modules under `src/custom/services/`. These modules export pure or async functions that are consumed by multiple dialog/page action hooks, avoiding code duplication across hook registrations. Each function typically accepts the form data object and a `storeDiff` callback to apply computed field changes. The pattern centralizes domain-specific business logic such as date/time auto-setting based on current time, enum-driven field visibility toggling, relation-based default value resolution, and dynamic warning text computation. Multiple action hooks for different pages/dialogs import from the same service module, ensuring consistent behavior across all views that operate on the same input transfer object.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
