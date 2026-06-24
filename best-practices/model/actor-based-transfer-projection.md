---
id: "actor-based-transfer-projection"
title: "Actor-Based Transfer Object Projection"
domain: "model"
category: "transfer"
score: 47.0
usage_count: 10
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - itracker
  - alba
  - skillmatrix-model
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - sanctuary-backend
  - reserve-app
alternatives:
  - service-based-transfer-organization
---
## Description

Each actor (user role) in the system gets its own dedicated set of transfer objects that project different views of the same underlying entities. Admin actors see full data with management capabilities, while restricted actors see curated, read-only views optimized for their use case. Transfer objects are organized into actor-specific packages (e.g., `actors::admin::`, `actors::player::`) or role-prefixed names.

## Structure

- Entity types live in a shared `entities` package
- Each actor gets its own sub-package under `actors::` or `services::`
- Actor-specific transfer objects reuse entity names but provide different attribute selections, derived fields, and permission settings
- Admin projections tend to expose more attributes and CRUD operations
- Restricted actor projections tend to use heavily derived (read-only) attributes

## Examples

### Trivia
Entity `Contest` has two projections: `admin::Contest` (full CRUD, status management, open/close operations) and `player::Contest` (read-only with only `title` and `description`, plus an `enter` operation). The admin sees 6+ attributes; the player sees 2 derived attributes.

### itracker
Entity `Initiative` (18 attributes) has actor transfer `user::Initiative` (21 attributes): adds 7 UI-control fields (`label`, `editable`, `hideSendForApproval`, `hideApproval`, `hideReject`, `hideArchive`, `initiator`), omits 4 internal fields (`id`, `riskLevel`, `actionDueMonth`, `version`), and relaxes `status` from required to optional. Admin actor manages only reference data (Users, Categories, Regions) with full CRUD, not Initiatives.

### SkillMatrix
4 actors with 37 transfer objects. `Competence` entity has 5 projections: `hrEmployee::Competence` (full CRUD with tags, delete guard), `hrEmployee::SelectedCompetence` (picker, name-only), `professional::Competence` (read-only name), `manager::Competence` (read-only name + required), `report::Competence` (transient denormalized row). `User` entity has 7+ views across actors.

### Alba
4 role projections for `Product`: `AuthorProduct` (teacher's own products, create/finalize/version), `AdminProduct` (full access including impersonation and approval assignment), `GuestProduct` (public read-only), `ApproverProduct` (approval workflow). 4 role projections for `User`: `UserTransfer` (self-view), `AuthorTransfer`, `AdminAuthorProfile`, `PublicAuthorProfile`. Task views per role: `AuthorTask`, `ApproverTask`, `AdminTask`. Total: 44 transfer objects from 11 entities.

### SkillMatrix-Model
4 ActorTypes confirmed in source: `AdminActor`, `HREmployeeActor`, `ProfessionalActor`, `UserActor`. Each actor uses `isActiveExpression` for role gating (e.g., `self.isActiveHREmployee`). 37 transfer objects across actors project 21 entities with varying CRUD permissions and attribute selections. Same entity operation exposed to different actors: e.g., `User.approveAllSkills` mapped to both Subordinate and UnapprovedSkillsView transfers.

### Viterra Demo
2 actors (Admin, Partner) with 10 transfer objects from 7 entities. `Report` entity has 3 projections: `ReportTransfer` (admin: full CRUD, accept/review operations), `PartnerOpenReportTransfer` (partner: PENDING reports only, update stocks, submit operation), `PartnerClosedReportTransfer` (partner: non-PENDING reports, read-only). `Client` has 2: `ClientTransfer` (admin) and `PartnerClientTransfer` (partner self-view). Partner transfers use actor-prefixed naming (e.g., `PartnerOpen*`, `PartnerClosed*`).

### KozutEugyfelClient
3 actors (Admin, Munkatars, EUgyfelAlkalmazas) with 20 transfer objects from 13 entities. `Felhasznalo` entity has 2 principal projections: `AdminPrincipal` (email + name only) and `MunkatarsPrincipal` (9 attributes including role/organizational data). `Bejelentes` has 3 projections: `BejelentesAzonosito` (minimal 4-field identifier), `Bejelentes` (5-field summary), `BejelentesMegtekinto` (23 fields with 7 permission booleans for full viewer).

### MJSZ
Single actor `Munkatars` with 7 TOs in `actors::munkatars::` namespace, one per entity. Each TO mirrors the entity name (Club, Player, Season, Tournament, Match, Team, Transfer). All TOs use AGGREGATION for relations and have `createable=false, updateable=false, deleteable=false` -- CRUD is granted at the access level. Simple 1:1 entity-to-TO mapping since there is only one actor role.

### judo-demo-miniworkflow
Single actor `GenericActor` with `GenericUser` as its principal, mapping to `User` entity with additional derived attributes (`isNotAdmin`, `isNotApprover`) for UI hiding. `DocumentTransfer` provides the enhanced API projection of `Document` with negative permission attributes and mixed operations (static factory + mapped workflow ops). Self-mapped transfers coexist alongside actor-specific transfers.

### AMS-Model
2 actors (Manager, Admin) with actor-specific transfer projections. `User` entity has 3 TOs: `manager::Subordinate` (4 attributes for displaying subordinates), `manager::ManagerApprovalList` (empty TO for bulk approval context), and `admin::User` (3 attributes). `ConfirmationRequest` entity has `manager::Request` (11 attributes with MAPPED approve/reject operations). Manager access uses `self.subordinates` and campaign status filtering; Admin manages campaigns and data loading.

### Sanctuary Backend
Single `Admin` actor with 6 transfer objects (one per entity) using "TO" suffix naming: `UserTO`, `RoleTO`, `RoleGroupTO`, `PositionTitleTO`, `UserPrivacySettingsTO`, `UserSettingsTO`. All TOs are 1:1 mappings of their entities with MAPPED attributes. Admin has full CRUD access to all 4 primary access points (users, roles, roleGroups, positionTitles). This represents the simplest form of actor-based projection: single actor, direct entity mapping.

### KozutEugyfelModelTest
3 KOZUT-realm actors (UgyfelszolgalatiMunkatars, SzervezetiEgysegMunkatars, SzervezetiEgysegVezeto) each with near-identical but separately defined transfer packages. Each actor gets `Bejelentes`, `Esemeny`, `BejelentesTipus` TOs plus `IntezendoBejelentes` extending `Bejelentes` with bound operations. A shared `KozosTransferObjectek` package provides common TOs (`Felhasznalo`, operation inputs) reused across actors.

### ReserveApp
5 actors (Admin, Partner, Logistician, Doorman, Readonly) with 40 TOs from 15 entities. AdminActor sees full admin TOs (e.g., `services::Partner` with all fields including `externalIdentifier` and `active`). PartnerActor sees restricted `*ForPartner` TOs (e.g., `PartnerForPartner` exposes only name, phone, address, contact). `ReservationForPartner` adds derived display attributes (`duration`, `projectAsString`, `gateAsString`) not on the entity.

### AMS-Frontend
2 actors (Manager, Admin) with 7 TOs from 7 entities. `User` entity projected 3 ways: `manager::Subordinate` (email renamed to `identifier`, plus name fields), `manager::ManagerApprovalList` (relation-only TO with filtered `approvals` and `approveAll` operation), and `admin::User` (3 basic attributes). Manager sees only open-campaign confirmation requests; Admin has full CRUD on campaigns and applications.

## Caveats — multi-TO same-entity for principal entities

Principal entities (entities backing `ActorType.principal`) support multiple actor-based projections, but two framework constraints govern the design.

**1. Only one TO per actor holds `actorType`.** `TransferObjectType.actorType` is the eOpposite of `ActorType.principal`. Single-valued on both sides. Setting `actorType=<Actor>` on a second TO mapping the same entity transparently reassigns `ActorType.principal` to that TO; the previous TO loses the back-link (cleared to null). Pick one principal TO; other projections on the same entity exist as plain mapped TOs without `actorType`.

**2. Keycloak managed-realm sync (`managed=true`) is bound to the principal TO's DAO metadata.** Framework-injected create / update / delete against the Keycloak realm fires only when the DAO layer is invoked with the principal TO's metadata. Admin user-management TOs and list TOs mapping the same principal entity do NOT auto-sync — entity row updates; Keycloak realm user does not.

**Design rule for principal entities.** Keep ONE lean principal TO that owns `actorType` and (when `managed=true`) framework-managed Keycloak sync. Add separate mapped TOs for admin / list projections on the same entity. When an admin surface must also sync Keycloak, expose the mutation as a custom operation on the admin TO that re-dispatches through the **principal TO's DAO**. Direct CUD on the admin TO is DB-only.

**Empirical validation (2026-05-11, `compsych-letter-demo`).** `compsychletter::services::UserPrincipal` (lean principal) and `compsychletter::services::UserTO` (admin) both map `User` entity; actor = `compsychletter::actors::LetterUser`. Reassigning `UserTO.actorType=LetterUser` swapped `LetterUser.principal` from `UserPrincipal` to `UserTO`. Build broke at `esm2ui/claim.etl`: *"Could not find attribute: userName"*. Restoring `LetterUser.principal=UserPrincipal` cleared `UserTO.actorType` to null. Build succeeded.

**No `<X>ListTO` for relation target.** Reinforces the one-TO-per-relation-target rule — admin / list projections coexist as plain mapped TOs but the relation row TO + detail TO must be the same mapped TO. Separate `<X>ListTO` forces a custom row-click handler to navigate to the detail TO and creates dual-maintenance. See [relation-driven-crud-with-custom-input.md — §1](relation-driven-crud-with-custom-input.md#1-relation-auto-wiring-from-mapped-target-to).

**Worked admin example.** Canonical admin user-management surface combining the multi-TO same-entity constraint with read-only access + custom-op delegation through the principal TO's DAO: [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md).

## Trade-offs

- Pros: Strong separation of concerns per actor, fine-grained data exposure control, each UI gets exactly the data it needs
- Cons: More transfer objects to maintain, potential duplication of mapping logic across actors
- Prefer when: Multiple user roles need different views of the same data

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md)
- [unmapped-transfer-dto](unmapped-transfer-dto.md)
- [derived-access-filtering](derived-access-filtering.md)
- [service-based-transfer-organization](service-based-transfer-organization.md) (alternative: per-service domain organization)
