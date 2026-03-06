---
id: "initializer-operation"
title: "Static Initializer Operation for Data Seeding"
domain: "model"
category: "operation"
score: 55.4
usage_count: 14
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - actiongroup-test-react
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - InterfaceRegister
  - judo-partner
  - reserve-app
---
## Description

A static operation on a singleton entity marked as an initializer runs automatically on application startup. It seeds default data (admin users, reference data, sample records) using idempotent checks (e.g., `EntityType!empty()`) to avoid duplicate seeding on subsequent startups.

## Structure

- Static operation with `initializer=true` on a singleton entity
- Body checks for existing data before creating: `if (EntityType!empty()) { ... }`
- Creates default admin/system users, reference data (categories, enums), and optionally sample data
- May call other instance operations for complex seeding (e.g., `generate()`, `approveAll()`)

## Examples

### Trivia
`Application.init` (static, initializer=true): checks if admin exists, creates default admin (`trivia@blackbelt.hu`). If Application is empty (first run): creates 10 categories, calls `generate()` to create 50+ sample questions, calls `approveAll()` to approve them, creates a default contest.

### RackInspect
`Initializer.init` on the `Initializer` entity (a dedicated singleton with a single `initialized` boolean flag, default: true). Separate dedicated entity for initialization rather than using an Application entity.

### itracker
`Application.init` (static, initializer=true): seeds 3 SRTCategories ("SRT-MRO/SER", "SRT-Labor", "Non-SRT"), 2 Regions ("Europe", "US"), and 3 Users (1 finance, 2 regular). No idempotency guard -- creates unconditionally. Creates User instances via actor-level transfer type (`itracker::actors::user::User`) rather than entity type directly.

### SkillMatrix
`User.initializer` (static): seeds SkillLevels (JUNIOR/MEDIOR/SENIOR/EXPERT with scores 1-4), Countries (HU), Competences (Java 8/9/11, Python, Oracle, MySQL), Tags (Java, Database, Programming), Units (R&D, PDU, SDU), a default admin, an HR employee, and 7 professional users with pre-assigned skills.

### ActionGroupTest
`Galaxy.init` is a STATIC operation on the Galaxy entity, serving as the sole initializer. Unlike other projects that use a dedicated Application or singleton entity, here the initializer is placed directly on a domain entity. No input or output parameters.

### SkillMatrix-Model
Model source confirms `User.initializer` as STATIC with `initializer="true"`. Seeds comprehensive test data including entity-as-enum instances (`SkillLevel` with name/score pairs), reference data (`Country`, `Competence`, `Tag`, `Unit`), and multiple user accounts with pre-assigned role flags and skills. Also has `createTestData` as a custom-implemented STATIC operation for additional test data generation.

### MLSZKSZPlatform
`Initializer.init` on a dedicated `Initializer` entity (static operation, custom implementation). The Initializer entity has a `createdAt: Timestamp` attribute to track initialization time. Implementation is fully custom (body deferred to backend Java), consistent with the project's pattern of using custom implementations for complex operations. The `Initializer` entity follows the same dedicated-singleton pattern as RackInspect.

### Viterra Demo
`Application.init()` (static, initializer=true, `customImplementation=false`): creates comprehensive demo data -- 7 Commodities, 4 Silos, 4 Periods, 2 Clients, and 4 Reports with attached Stocks. Uses inline JQL body (not custom Java). Seeds reports in various workflow states (PENDING, SUBMITTED) with stock data showing quantity variances for demonstration purposes.

### KozutEugyfelClient
`init()` operation present on the model, providing application initialization. The `szinkronizal()` (synchronize) and `getLezartNemSzinkronizaltEsemenyek()` (get closed unsynchronized events) operations serve as scheduled/batch initialization and synchronization hooks for external system integration.

### MJSZ
`Application.init` (static, initializer=true, stateful=true, `customImplementation=false`): uses `Season!empty()` guard for idempotency. Seeds 2 Seasons, 2 Tournaments, 17 Clubs (real Hungarian ice hockey names), 20 Teams, 5 Venues, and 14 Matches with scores. Teams are created and added to clubs via `club.teams += team`. One of the most comprehensive inline initializers across projects.

### judo-demo-miniworkflow
`User.initUsers` (static, initializer=true): uses `!exists()` guard to check before creating default users. Seeds 2 users: `admin@example.org` (admin + approver) and `user@example.org` (approver, not admin). Uses `if (not GenericUser!exists(d | d.email == "..."))` for per-record idempotency rather than global `!empty()` check.

### AMS-Model
`User.init` (static, initializer=true): uses `Admin!count() > 0` guard for idempotency. Seeds 1 Admin, 5 Applications (CM, PLM, SAP, PTIC, VITRIN), 4 Users with manager hierarchy, 2 Campaigns with date ranges and OPEN status, and 15 ConfirmationRequests with real-world role data. Confirmation requests are added to campaigns via `campaign.confirmationRequests += new ConfirmationRequest(...)`. Also `Campaign.load` (instance operation) seeds additional confirmation requests referencing existing entities via `!filter(!any()` lookups.

### ParkHere
`Initializer.init` on a dedicated `Initializer` entity (static operation, `initializer=true`, custom implementation). The Initializer entity has no attributes -- it serves purely as a hook for the `init` operation. Body comment is `// SDK`, indicating implementation is deferred to custom backend Java code for initial data seeding (admin user, default configuration, etc.).

### InterfaceRegister
Multiple initializer operations on a dedicated `Initializer` entity: `initUsers` (seeds 2 users with role flags, guarded by `User!count() == 0`), `initVendors` (seeds 2 vendors, guarded by `Vendor!count() == 0`), `initBrands` (seeds 2 brands, guarded by `Brand!count() == 0`), `initBusinessDataTypes` (seeds 2 data types, guarded by `BusinessDataType!count() == 0`). All use `!count() == 0` idempotency. Unique in splitting initialization across 4 separate initializer operations rather than one monolithic `init`.

### judo-partner
`Application.init` on a dedicated `Application` entity (no attributes). Serves as the application initialization hook. The model also includes `NAVConfig.clearCache` as an operational singleton pattern for managing NAV API cache state.

### KozutEugyfelModelTest
`Inicializalo.init()` (static, initializer=true) on a dedicated `Inicializalo` entity. Seeds 6 test users (2 UgyfelszolgalatiMunkatars, 2 SzervezetiEgysegVezeto, 2 SzervezetiEgysegMunkatars), 2 BejelentesTipus reference data records (JAROKELO, ALTALANOS), then triggers `JarokeloBejelentes.szinkronizal()` for external data sync.

### ReserveApp
`User.init` (static, initializer=true, stateful=true): seeds 5 test users across all roles -- `norbert.herczeg@blackbelt.hu` (ADMIN), `logistician@bb.hu` (LOGISTICIAN), `partner@bb.hu` (PARTNER), `doorman@bb.hu` (DOORMAN), `readonly@bb.hu` (READ_ONLY). Demonstrates one-user-per-role seeding for development/testing.

### AMS-Frontend
`User.init` (static, initializer=true) with `Admin!count() > 0` idempotency guard. Seeds admin, 5 applications (CM, PLM, SAP, PTIC, VITRIN), 4 users with a manager-subordinate hierarchy, and 2 campaigns with 15 confirmation requests. `Campaign.load` instance operation provides additional seeding for demo data.

## Trade-offs

- Pros: Automatic data seeding on first run, idempotent, no manual setup needed
- Cons: Initializer logic can become complex, sample data may need cleanup in production
- Prefer when: Application needs reference data or default configuration on first startup

## Related Patterns

- [singleton-entity](singleton-entity.md)
- [custom-implementation-placeholder](custom-implementation-placeholder.md)
