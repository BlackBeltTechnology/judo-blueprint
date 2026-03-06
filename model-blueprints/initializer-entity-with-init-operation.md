---
id: "initializer-entity-with-init-operation"
title: "Initializer Entity with Static Init Operation"
score: 84.0
usage_count: 13
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - park-here
  - ubives
  - workflow-poc
  - judo-demo-miniworkflow
  - trivia
  - itracker
  - viterra_demo
  - InterfaceRegister
  - mjsz
  - doors-model
  - ams-model
---
## Description

A minimal Initializer entity with a marker attribute and a single static operation `init` with custom implementation. This entity serves as the entry point for data seeding: the init operation is called on application startup (or first deployment) to populate reference data such as cities, postal codes, capabilities, initial admin users, and the singleton Configuration instance. The entity is typically non-CRUD. Some variants use a `createdAt` timestamp as the marker, others use an `initialized` boolean flag, an `executedInitialization` integer counter for multi-step migrations, and some have no attributes at all (bare Initializer with only the init operation). Some variants split initialization into multiple named static operations (e.g., initAdminUser, initDefaultIdm) rather than a single init. In workflow-oriented projects, the initializer may be named "Application" instead of "Initializer" but follows the same pattern. In small demo projects, the init operation may live directly on a domain entity (e.g., User.initUsers, User.init) rather than a separate Initializer entity. Some variants add additional utility operations (generate, approveAll) alongside the init operation for batch data management. The init operation body can be defined in model script (model-defined behavior) or delegated to custom Java implementation. Some variants split reference data seeding into multiple domain-specific init operations (e.g., initUsers, initVendors, initBrands, initBusinessDataTypes) each marked as an initializer with stateful behavior. Advanced variants use a counter-based migration pattern where the `executedInitialization` integer tracks which migration steps have been completed, enabling incremental data migrations across deployments.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Initializer" } }) {
  items { fqn name
    operations { items { name operationType customImplementation } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Application" } }) {
  items { fqn name
    operations { items { name operationType customImplementation } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    operations { items { name operationType customImplementation } }
  }
} } }
```

Look for entities with a static operation named `init`, `initUsers`, `initData`, or similar.

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Initializer",
  createable: true, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Initializer", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::Initializer", name: "init",
  customImplementation: true, operationType: "STATIC", binding: "{{NAMESPACE}}::Initializer"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Initializer`
  - createable=true, updateable=false, deleteable=false
  - Attributes: createdAt
  - Operations: init (STATIC, customImplementation=true)
- The init operation seeds cities, postal codes, capabilities, Configuration singleton, and admin organization/user

### rackinspect
- **Entity**: `rackinspect::entities::Initializer` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: initialized (req, default: true) -- boolean marker instead of timestamp
  - Operations: init (STATIC, customImplementation=true)
- Seeds reference data: currencies, countries, languages, units, payment methods, document registries, exchange rates, error codes, rack types, dimension templates, and the Configuration singleton

### park-here
- **Entity**: `ParkHere::entities::Initializer` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare Initializer with no marker attribute
  - Operations: init (STATIC, customImplementation=true)
- Minimal variant: no marker attribute at all; the init operation seeds the Configuration singleton and initial data for the parking reservation system

### ubives
- **Entity**: `Ubives::entities::Initializer` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare Initializer with no marker attribute
  - Operations: initAdminUser (STATIC), initDefaultIdm (STATIC) -- two separate init operations instead of one
- Multi-operation variant: splits initialization into two named operations: one for seeding the initial admin user account and one for setting up the default identity management (IDM) configuration
- Neither operation has customImplementation=true, indicating they use model-defined behavior rather than backend Java code

### workflow-poc
- **Entity**: `workflow::test::Application` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare entity with no attributes
  - Operations: init (STATIC, customImplementation=false)
- Named "Application" instead of "Initializer" but follows the same pattern: a singleton entity with a static init operation for seeding test data (workflow definitions, users, roles, context types)
- The init operation uses model-defined behavior rather than custom Java implementation

### judo-demo-miniworkflow
- **Entity**: `MiniWorkflow::User` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Operations: initUsers (STATIC, customImplementation=false)
- Inline variant: instead of a separate Initializer entity, the init operation is placed directly on the User entity
- The operation is named `initUsers` (domain-specific) rather than generic `init`, indicating it seeds initial user records
- This is the simplest variant: no dedicated initializer entity, the seeding operation lives on the domain entity it populates

### trivia
- **Entity**: `trivia::entities::Application` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare entity with no attributes
  - Operations: init (STATIC), generate (INSTANCE), approveAll (INSTANCE)
  - All operations have customImplementation=false (model-defined behavior)
- Named "Application" (like workflow-poc) rather than "Initializer"
- Extended variant: adds `generate` (creates sample trivia questions) and `approveAll` (bulk-approves all questions) utility operations alongside the standard `init`
- The generate and approveAll operations are INSTANCE type (operate on the Application singleton) while init is STATIC
- This shows the initializer pattern evolving into a general-purpose admin utility entity

### itracker
- **Entity**: `itracker::entities::Application` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare entity with no attributes
  - Operations: init (STATIC, customImplementation=false)
- Named "Application" (like workflow-poc and trivia) rather than "Initializer"
- Minimal variant: no marker attribute, single init operation with model-defined behavior
- Seeds reference data for the initiative tracking domain (regions, categories, users)

### viterra_demo
- **Entity**: `viterra::Application` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: none -- bare entity with no attributes
  - Operations: init (STATIC, customImplementation=false, initializer=true, stateful=true)
- Named "Application" (like workflow-poc, trivia, itracker) rather than "Initializer"
- The init operation has a model-defined script body that seeds all demo data: 7 Commodity entries, 4 Silo entries, 4 Period entries, 2 Client entries, 4 Report entries (with SUBMITTED and PENDING statuses), and 20 Stock entries distributed across the reports
- The `initializer=true` flag marks this as the application startup initializer
- The `stateful=true` flag indicates the operation modifies persistent data
- This is the most comprehensive model-scripted init example: the entire demo dataset is defined inline in the operation body rather than delegated to Java code

### InterfaceRegister
- **Entity**: `InterfaceRegister::entities::Initializer` (createable=true, updateable=true, deleteable=true)
  - Attributes: none -- bare Initializer with no marker attribute
  - Operations: initUsers (STATIC), initVendors (STATIC), initBrands (STATIC), initBusinessDataTypes (STATIC)
  - All four operations have customImplementation=false, initializer=true, stateful=true
- Multi-operation variant with four domain-specific init operations, each seeding a different reference data category: users, vendors, brands, and business data types
- All operations are marked with `initializer=true` and `stateful=true`, indicating they run at application startup and modify persistent data
- This is the most granular split of initialization: four separate operations rather than a single init or two splits (ubives)
- Unlike most other projects, this Initializer is CRUD-enabled (createable=true, updateable=true, deleteable=true), though this may be an oversight since the entity has no data attributes

### mjsz
- **Entity**: `mjsz::Application` (createable=true, updateable=true, deleteable=true)
  - Attributes: none -- bare entity with no attributes
  - Operations: init (STATIC, customImplementation=false, initializer=true, stateful=true)
- Named "Application" (like workflow-poc, trivia, itracker, viterra_demo) rather than "Initializer"
- The init operation has a comprehensive model-defined script body that seeds the entire demo dataset for a Hungarian ice hockey league:
  - 2 Season entries (2021/2022 and 2022/2023)
  - 2 Tournament entries (Erste Liga and Andersen Liga)
  - 17 Club entries (Hungarian ice hockey clubs)
  - 20 Team entries (clubs assigned to tournaments)
  - 5 Venue entries (ice rinks in Hungarian cities)
  - 14 Match entries with scores, dates, times, and venue assignments
- The init operation guards against re-running by checking `mjsz::Season!empty()` before executing
- This is the largest model-scripted init example by entity count, creating a complete sports league dataset with interconnected entities spanning seasons, tournaments, clubs, teams, venues, and matches
- The CRUD-enabled entity (createable=true, updateable=true, deleteable=true) follows the same pattern as InterfaceRegister

### doors-model
- **Entity**: `doors::entities::Initializer` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: executedInitialization (Integer, req, default: 0) -- counter-based migration marker
  - Operations: init (INSTANCE), init1_legacy (INSTANCE), init2_renameBanks (INSTANCE), init3_addBbUsers (INSTANCE), init5_fixEmails (INSTANCE), init6_addMwTestUsers (INSTANCE), init7_addDivisionTestingPositions (INSTANCE)
  - All operations have customImplementation=false (model-defined behavior)
- **Counter-based migration pattern**: the `executedInitialization` integer tracks which migration step has been completed. The `init` operation checks the counter and sequentially runs each numbered migration step (init1_legacy, init2_renameBanks, init3_addBbUsers, etc.), incrementing the counter after each step completes
- This is the most advanced Initializer variant: rather than a single idempotent init, it uses numbered migration steps that only run once each, enabling incremental data migrations across deployments
- The initialization is triggered from `Division.init()` (a STATIC initializer operation on the Division entity) which creates the Initializer singleton if it does not exist, then delegates to `initializer.init()`
- Each numbered step performs a specific data migration: init1 seeds legacy data (workflows, roles, employees, companies, divisions, partners), init2 renames banks, init3 adds test users, init5 fixes emails, init6 adds more test users, init7 adds division-specific testing positions
- The step numbering has a gap (no init4), indicating an obsolete migration step was removed

### ams-model
- **Entity**: `ams::entities::User` (non-CRUD: createable=false, updateable=false, deleteable=false)
  - Attributes: email (req, identifier), firstName (req), lastName (req), fullName (DERIVED)
  - Operations: init (STATIC, customImplementation=false, initializer=true, stateful=true), approveAll (INSTANCE)
- Inline variant: the init operation lives directly on the User entity rather than a separate Initializer entity (similar to judo-demo-miniworkflow)
- The init operation has a comprehensive model-defined script body that guards against re-running by checking `ams::entities::Admin!count() > 0`, then seeds:
  - 1 Admin entry (admin@invitech.hu)
  - 5 Application entries (CM, PLM, SAP, PTIC, VITRIN -- representing IT systems)
  - 4 User entries (1 manager + 3 subordinates with manager relationship)
  - 2 Campaign entries with date ranges and OPEN status
  - 15 ConfirmationRequest entries across multiple applications and users (with login names, roles, effective dates, PENDING status, and approver assignments)
- The `approveAll` INSTANCE operation iterates over all pending approvals and calls approve() on each, enabling bulk approval
- This is the most detailed inline init example: rather than creating simple seed data, it creates a complete access management scenario with users, applications, campaigns, and confirmation requests across multiple IT systems
- Unlike most other init operations, this variant includes extensive Hungarian-language role descriptions (e.g., "USZI - Analog, ISDN2 IN LTO", "Mindentlatok csoportja") reflecting a real enterprise access management use case
