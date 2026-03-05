---
id: "script-driven-operations"
title: "Script-Driven Operations (Zero Custom Java)"
domain: "backend"
category: "operation"
score: 78.8
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - viterra_demo
  - judo-demo-miniworkflow
  - reserve-app
  - doors-model
---
## Description

A JUDO architecture pattern where all business logic is defined as model scripts in the ESM model file and compiled to Java via the `script2operation.jar` artifact. No custom Java implementations are created -- all `.java.default` scaffolds remain uncustomized. The model script engine handles entity creation, status transitions, relation management, and data aggregation. This pattern is viable when the business logic is fully expressible in the JUDO model scripting language and no external integrations (email, file storage, SOAP/REST clients) are needed.

## Structure

Model scripts are defined directly in the ESM model and compiled during the build:

```
ESM Model (.model)
  |-- [judo-tatami] --> script2operation.jar (compiled scripts as Java)
  |-- Deployed as separate OSGi bundle
  |-- Registered as default implementation for all operations
```

The `.java.default` files in `custom/` remain as scaffolds:
```java
// .java.default file -- NOT customized
throw new java.lang.UnsupportedOperationException(
    "Operation not implemented: ...");
```

Model script examples (from Javadoc in .default files):
```
// Status transition
this.status = itracker::entities::InitiativeStatus#REVIEW

// Entity creation with relations
var initiative = new Initiative(title, source, location, ...)
initiative.monthlyForecasts += new MonthlyForecast(month=0..11, savingPotential=input.monthlySavingPotential)

// Actor context resolution
var user = User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()

// Collection aggregation
var sum = this.monthlyForecasts!sum(f | f.savingPotential)
```

## Examples

### itracker
11 `.java.default` scaffolds, zero custom Java implementations. All 10 operations (CreateInitiative, SendForApproval, Approve, Reject, ArchiveForecast at both actor and entity levels) plus Init are model-script-driven. The `script2operation.jar` handles status transitions, entity creation with 12 monthly forecasts, forecast versioning with collection aggregation, and reference data seeding.

### viterra_demo
7 `.java.default` stubs, zero custom Java implementations. Operations for Report lifecycle (Accept, Review, Submit) and Init data seeding remain as unimplemented stubs. Model scripts in `script2operation.jar` bundle provide the actual runtime logic. Javadoc in stubs documents the expected model script behavior (e.g., `this.status = viterra::ReportStatus#ACCEPTED`).

### judo-demo-miniworkflow
10 `.java.default` stubs, zero custom Java implementations. Model scripts handle document workflow: state transitions (Accept, Reject, Close, RequestReview), entity creation (CreateDocument with owner + initial history), and user seeding (InitUsers with idempotency). Javadoc in stubs contains the full model script logic including actor resolution, `DocumentHistoryEntry` creation, and collection updates (`this.documentHistoryEntries += newEntry`).

### ReserveApp
Single `InitCustomImplementation.java.default` scaffold for the `User.init` operation. The model defines `customImplementation: false`, meaning the operation uses the model-defined script rather than custom Java. Zero custom Java operations activated. All backend customization is done via interceptors instead. Demonstrates the most minimal script-driven approach: one model-script operation with interceptor-only Java customization.

### doors-model
Extensive inline business logic in JUDO expression language across 10+ model-level operations. `startApproval` calls validate, sets PENDING status, creates ContractStage entries, and advances workflow. `setNextStage` implements a state machine with SKIP/EXECUTE conditions based on net value thresholds. `approve`/`reject` manage stage completion. `Initializer.init` uses versioned migration counter (`executedInitialization`) for incremental seed data. Only 11 operations requiring Java-specific capabilities (file handling, document templating) are marked `customImplementation="true"`.

## Trade-offs

- Pros: Zero custom Java code to maintain, model is the single source of truth, faster development cycle, no build/deploy needed for logic changes in model
- Cons: Limited to what the model scripting language can express, no external service integration, no complex error handling, harder to debug compiled scripts
- Alternative: Custom Java implementations via `CustomImplementation` classes for operations requiring external integrations, complex algorithms, or fine-grained error handling

## Related Patterns

- custom-operation-osgi-component
- state-lifecycle-operation
- init-data-seeding
