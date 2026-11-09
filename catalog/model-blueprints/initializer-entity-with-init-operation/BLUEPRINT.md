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

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
