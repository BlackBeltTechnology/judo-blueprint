---
id: "error-code-enum"
title: "Error Code Enumeration with Business Error Transfer Object"
score: 65.7
usage_count: 5
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
  - park-here
  - ubives
  - workflow-poc
  - trivia
---
## Description

An ErrorCode enumeration that catalogs all domain-specific error conditions the system can produce. Members follow the pattern `ENTITY_NOT_FOUND`, `PERMISSION_DENIED`, `CONNECTION_FAILED`, `PLATFORM_NOT_SUPPORTED`, etc. -- each representing a specific failure scenario. A companion BusinessError or DeclarationError unmapped transfer object carries an `errorCode` (or `code`) attribute (typed to the enum) and a `message` string for human-readable details. Custom operations raise these structured errors instead of generic exceptions, allowing the frontend to provide targeted error messages and the backend to maintain a centralized error vocabulary.

This pattern provides type-safe error handling across the operation boundary: every possible error condition is declared in the model, making error responses part of the API contract. Some variants are domain-scoped (e.g., DeclarationErrorCode for workflow validation errors) rather than application-wide. Some variants scope the ErrorCode enum to a specific actor namespace rather than the shared entities package.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
