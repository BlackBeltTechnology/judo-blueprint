---
id: "entity-crud-at-service-layer"
title: "CRUD Permissions Controlled at Service Layer"
domain: "model"
category: "access"
score: 80.1
usage_count: 15
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - skillmatrix-model
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

All entities are defined with `createable=false`, `updateable=false`, `deleteable=false` at the entity level. CRUD permissions are instead controlled at the access/transfer layer, where each actor's access points specify which operations (C/R/U/D) are allowed. This enforces that all mutations go through the service layer.

## Structure

- Entity level: all CRUD flags set to `false`
- Access level: each access point specifies individual C, R, U, D boolean flags
- Different actors can have different CRUD permissions for the same underlying entity
- Read is almost always `true`; write permissions vary by actor role

## Examples

### Trivia
All 9 entities have `createable=false, updateable=false, deleteable=false`. Admin access `Admin.questions` has full CRUD (C=yes, R=yes, U=yes, D=yes). Admin access `Admin.tests` is read-only (C=no, R=yes, U=no, D=no). All Player accesses are read-only.

### RackInspect
All 72 entities have `createable=false, updateable=false, deleteable=false`. CRUD is managed via 214 transfer objects organized into service packages, with a single GenericUser actor and permission-based access control via `PermissionFlag` enum (23 flags).

### itracker
All 8 entities have `createable=false, updateable=false, deleteable=false`. UserActor.initiatives is update-only (C=false, U=true, D=false). Admin has full CUD on reference data (users, categories, regions). Initiative creation is handled via a static `createInitiative` operation rather than direct CRUD.

### SkillMatrix
CRUD controlled per-actor per-access: AdminActor.users (C, U), HREmployeeActor.professionals (U only), HREmployeeActor.competencies (C, U, D). ProfessionalActor.myProfession (U only), while composition children like `Professional.skills` have relation-level CRUD (create, update, delete).

### Alba
All 11 entities have `createable=false, updateable=false, deleteable=false`. CRUD permissions at access layer: `adminProfiles` (C, U), `curriculumsForAdmins` (C, U), `audiencesForAdmins` (C, U), `institutionsForAdmins` (C, U). Filter accesses are read-only. Product creation handled via static `createProduct` operations on AuthorProduct/AdminProduct transfers.

### SkillMatrix-Model
Model source confirms 140 occurrences of `createable="false"` across all entity and relation declarations. CRUD granted selectively at access level: `AdminActor.users` (create, update), `HREmployeeActor.professionals` (update only), `ProfessionalActor.myProfession` (update only). Composition children use `targetDefinedCRUD="true"` for relation-level CRUD control.

### Viterra Demo
All 7 entities have `createable=false, updateable=false, deleteable=false`. Admin access grants C+U (no delete) on all 5 access points (periods, silos, clients, commodities, reports). Partner access is read-only at the access level, but `PartnerOpenReportTransfer.stocks` overrides to `updateable=true` and `ReportTransfer.stocks` overrides to full CRUD at the relation level. No entity has delete permission -- soft delete via active flags is used instead.

### MJSZ
All 10 entities have CRUD flags at entity level (Player has full CRUD, License is read-only). The `Munkatars` actor grants full CRUD on all 6 access points (season, tournament, player, club, match, transfer) with `accessType="ALL"` and `targetDefinedCRUD="false"`. All access collections use `[0..*]` cardinality with unlimited upper bound.

### judo-demo-miniworkflow
All 4 entities have `createable=false, updateable=false, deleteable=false`. All mutations happen through operations: `createDocument` (static factory), `accept`/`reject`/`close`/`requestReview` (workflow transitions). Only `FilesTransfer` is writable (C+U+D) at the transfer level. The `users` access point grants full CRUD for admin user management, while `myDocuments` is update-only (no create/delete at access level).

### AMS-Model
All 7 entities (User, Application, Request, Campaign, ConfirmationRequest, AccessRequest, Admin) have `createable=false, updateable=false, deleteable=false`. All 12 relations also have CRUD disabled. Manager actor access points (`subordinates`, `approvalAll`, `approvalList`) are all read-only at the access level. CRUD is entirely deferred to the access/transfer layer, with operations (`approve`, `reject`, `open`, `close`, `load`, `approveAll`) handling all mutations.

### ParkHere
All 12 entities have `createable=false, updateable=false, deleteable=false`. All data mutations go through custom-implemented operations: car management via `createCar`/`deleteCar`/`favoriteCar`, reservations via `reservation`/`deleteReservation`/`cancelReservation`/`modificateReservation`, configuration via `configuration`/`createDoorman`/`createDay`. Access points specify CRUD per access: `parkingGarages` (C+U), `users` (C+U), `profileSettings` (U only), `reservationsAccess` (read-only).

### IndamediaAdTrack
All 12 entities have `createable=false, updateable=false, deleteable=false`. All data mutations go through 17 custom-implemented operations. No direct CRUD is exposed to the UI. Operations like `createClient`, `updateClient`, `newAccount`, `setGoogleCredential`, `syncData` handle all entity lifecycle management through the service layer with `BusinessError` faults for validation.

### InterfaceRegister
23 of 25 entities have `createable=false, updateable=false, deleteable=false`. Only `Initializer` and `User` have CRUD enabled. The single EnterpriseArchitect actor's 14 access points grant varied CRUD: most collections have C+U (e.g., `applications`, `vendors`, `highLevelConnections`) but no delete. `interfaceSpecifications` is read-only. Entity creation also handled via mapped operations: `createApplication`, `createHighLevelConnection`, `createUser`.

### judo-partner
Single Actor with 11 access points providing varied CRUD: `users` (C/U/D), `countries` (read-only), `partnerList` (U only), `NAVConfig` (U only), `imports` (read-only), `registers`/`deliveryMethods`/`caseTypes`/`cases`/`documentTypes` (C/U/D), `records` (read-only). Entity mutations for partners happen through operations (`createPartner`, `delete`, `validate`), not direct CRUD on the partner access point.

### KozutEugyfelModelTest
Most entities have `createable=false, updateable=false, deleteable=false`. Only `Kep` (Image) has full CRUD enabled as a composed child. All complaint lifecycle mutations are handled through operations (`tovabbitas`, `lezaras`, `megjegyzes`) rather than direct CRUD. The Admin actor gets user management CRUD, while KOZUT-realm actors get read-only `bejelentesek` and DERIVED actionable `intezendoBejelentesek`.

### workflow-poc
All 21 entities have `createable=false, updateable=false, deleteable=false` at the entity level. Model source confirms this across all entity declarations (Token, WorkflowVersion, State, Transition, Action, etc.). All mutations are handled through operations (`trigger`, `checkout`, `release`, `assign`, `execute`, `navigate`, `commit`, `upload`, `publish`, `startWorkflow`). Access points grant read-only access at the actor level.

### ReserveApp
All 15 entities have `createable=false, updateable=false, deleteable=false` at the entity level. CRUD is controlled through transfer objects and actor accesses. AdminActor has 13 access points to manage reference data (gates, partners, companies, etc.) and users. PartnerActor has 2 restricted accesses (profile + reservations). Three actors (Logistician, Doorman, Readonly) have no accesses defined yet.

### AMS-Frontend
All 7 entities have CRUD disabled at entity level. Admin actor grants CRUD on `campaigns` (C+U+D), `applications` (C+U+D), and read-only on `users`. Manager actor accesses are read-only -- all mutations handled via MAPPED operations (`approve`, `reject`, `open`, `close`, `load`, `approveAll`).

## Trade-offs

- Pros: Centralized permission control, different actors get different permissions, follows CQRS principles
- Cons: Entity-level flags may seem redundant (always false), requires careful access configuration
- Prefer when: Always in JUDO -- this is the standard architecture pattern

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [derived-access-filtering](derived-access-filtering.md)
