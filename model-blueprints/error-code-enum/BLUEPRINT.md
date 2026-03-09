---
id: "error-code-enum"
title: "Error Code Enumeration with Business Error Transfer Object"
score: 71.3
usage_count: 6
first_seen: "2026-03-05"
last_updated: "2026-03-09"
projects:
  - indamedia-adtrack
  - park-here
  - ubives
  - workflow-poc
  - trivia
  - mlszksz-platform
---
## Description

An ErrorCode enumeration that catalogs all domain-specific error conditions the system can produce. Members follow the pattern `ENTITY_NOT_FOUND`, `PERMISSION_DENIED`, `CONNECTION_FAILED`, `PLATFORM_NOT_SUPPORTED`, etc. -- each representing a specific failure scenario. A companion BusinessError or DeclarationError unmapped transfer object carries an `errorCode` (or `code`) attribute (typed to the enum) and a `message` string for human-readable details. Custom operations raise these structured errors instead of generic exceptions, allowing the frontend to provide targeted error messages and the backend to maintain a centralized error vocabulary.

This pattern provides type-safe error handling across the operation boundary: every possible error condition is declared in the model, making error responses part of the API contract. Some variants are domain-scoped (e.g., DeclarationErrorCode for workflow validation errors) rather than application-wide. Some variants scope the ErrorCode enum to a specific actor namespace rather than the shared entities package. Some simplified variants omit the ErrorCode enum entirely and use a plain unmapped BusinessError TO with `code` (string) and `message` attributes, relying on application code rather than model-level enum to define error codes.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
