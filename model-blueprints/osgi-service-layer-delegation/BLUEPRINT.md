---
id: osgi-service-layer-delegation
title: "OSGi Service Layer Delegation (Shared Business Services)"
impl_only: true
usage_count: 4
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
  - rackinspect
  - indamedia-adtrack
  - park-here
---

## Description

An architectural pattern where custom operations delegate business logic to shared OSGi service interfaces defined in a `common` module, with implementations spread across multiple Maven modules (`common`, `keycloak-client`, `firebase`). This is an implementation-only blueprint -- it describes the structural pattern of how JUDO custom operations are decomposed into reusable, testable service components rather than putting all logic directly in the custom operation class.

The pattern addresses several concerns:
- **Code reuse:** Multiple custom operations (across different actors) share the same business logic without duplication
- **Testability:** Service implementations can be unit-tested independently of the JUDO dispatcher
- **Module separation:** External integrations (Keycloak, Firebase) are isolated in their own Maven modules, implementing interfaces defined in the common module
- **DI composition:** OSGi Declarative Services wires everything together at runtime -- custom operations `@Reference` service interfaces, not implementations

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
