---
id: "singleton-entity"
title: "Singleton Entity Pattern"
domain: "model"
category: "entity"
score: 50.9
usage_count: 8
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - itracker
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - park-here
  - InterfaceRegister
  - judo-partner
---
## Description

An entity with no attributes or relations that serves as a singleton application-level container for static operations (initialization, registration, bulk actions). It is accessed via `EntityType!any()` and checked for existence with `EntityType!empty()`. Often used as the entry point for application-level functionality exposed to actors.

## Structure

- Entity has no stored attributes or relations
- Contains static and instance operations (e.g., `init`, `register`)
- Checked with `!empty()` for first-run initialization
- Accessed via `!any()` in derived access getters
- Actor access uses cardinality `0..1` with a derived getter: `EntityType!any()`

## Examples

### Trivia
`Application` entity has no attributes. It hosts `init` (static initializer that seeds data), `generate` (creates sample questions), and `approveAll` (bulk status update). Player accesses it via `Player.application` with getter `trivia::entities::Application!any()`.

### itracker
`Application` entity has no attributes or relations. It hosts only `init` (static initializer, `initializer=true`) which seeds 3 SRTCategories, 2 Regions, and 3 Users. Unlike Trivia, it is not exposed to any actor as an access point -- it exists solely for startup data seeding.

### MLSZKSZPlatform
Two singleton entities: **Configuration** (platform settings like `senderEmail`, `baseUrl`, `platformName`, email templates; CRUD: update-only, no create/delete) and **Initializer** (hosts `init` static operation with only `createdAt` timestamp attribute). Configuration is a data-carrying singleton used for system-wide settings, unlike the attribute-less initializer pattern.

### Viterra Demo
`Application` entity has no attributes or relations. It hosts only `init()` (static, initializer=true) which seeds 7 Commodities, 4 Silos, 4 Periods, 2 Clients, and 4 Reports with Stocks. Pure operations-only singleton -- not exposed as an access point to any actor.

### MJSZ
`Application` entity has no attributes or relations. It hosts a single `init()` operation (static, initializer=true, stateful=true) that seeds comprehensive demo data including 17 clubs, 20 teams, 14 matches, and 5 venues for Hungarian ice hockey. Not exposed as an access point -- purely for startup initialization.

### ParkHere
Two singletons: **Initializer** (no attributes, hosts `init` static operation with `initializer=true`) and **Configuration** (data-carrying singleton with 6 email template attributes, doormans/additionalDays relations). Configuration accessed via `Configuration!any()` for global system settings. This dual-singleton approach mirrors MLSZKSZPlatform's pattern of separating initialization from configuration.

### InterfaceRegister
`Initializer` entity with no attributes and full CRUD enabled. Hosts 4 separate static initializer operations (`initUsers`, `initVendors`, `initBrands`, `initBusinessDataTypes`), each seeding a different entity type with idempotent `!count() == 0` guards. Unlike most projects that have a single `init` operation, this splits seeding across domain-specific operations for modularity.

### judo-partner
`Application` entity has no attributes or relations. It hosts only `init` (static operation for application initialization). The `NAVConfig` entity also serves as a singleton-like configuration entity for NAV API credentials (login, passwordHash, taxNumber, signKey), accessed via `NAVConfig!any()` on the Actor.

## Trade-offs

- Pros: Clean entry point for app-level operations, supports initialization logic, works well with actor access patterns
- Cons: Slightly unusual entity pattern (no data), may confuse developers expecting data-carrying entities
- Prefer when: Application needs a global entry point for static operations or initialization

## Related Patterns

- [custom-implementation-placeholder](custom-implementation-placeholder.md)
- [derived-access-filtering](derived-access-filtering.md)
