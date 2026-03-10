---
id: "transfer-object-multiplicity"
title: "Transfer Object Multiplicity per Entity"
domain: "model"
category: "transfer"
score: 45.2
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - skillmatrix-model
  - viterra_demo
  - judo-demo-miniworkflow
  - ams-model
  - workflow-poc
  - reserve-app
---
## Description

A single entity is exposed through multiple transfer objects, each tailored for a specific actor and purpose. This goes beyond simple actor-based projection -- the same entity may have 5-7+ distinct transfer objects varying in attribute selection, CRUD permissions, derived fields, and operational capabilities. This includes full-CRUD views, read-only summaries, picker/selector views, and transient report views.

## Structure

- One entity maps to N transfer objects (where N can be 5+)
- Transfer object categories:
  - **Full CRUD view**: Complete attribute set with create/update/delete (actor-specific)
  - **Summary/read-only view**: Subset of attributes, all derived (for display in lists/tables)
  - **Picker/selector view**: Minimal transfer with just identifier/name (for dropdowns)
  - **Extended view**: Inherits from a base transfer and adds relations/operations (via generalization)
  - **Transient/report view**: Unmapped, all attributes transient (for report generation)
- Different actors may share the same transfer object (cross-actor reuse)

## Examples

### SkillMatrix
`Competence` entity has 5 transfer objects: `hrEmployee::Competence` (full CRUD with tags, hasReferences guard, delete op), `hrEmployee::SelectedCompetence` (picker: name-only, derived), `professional::Competence` (read-only: name-only), `manager::Competence` (read-only: name + required), `report::Competence` (transient: denormalized row with user/unit/tag/score). `User` entity has 7+ views including `Admin`, `HREmployee`, `Professional`, `MyProfessional`, `Subordinate`, `UnapprovedSkillsView`, `ReportedUser`.

### Alba
`Product` entity has 4+ role-based TOs: `AuthorProduct` (own products, create/finalize/version), `AdminProduct` (full access, impersonation, approval), `GuestProduct` (public read-only), `ApproverProduct` (approval workflow). `User` entity has 4+ TOs: `UserTransfer` (self-view), `AuthorTransfer`, `AdminAuthorProfile`, `PublicAuthorProfile`. `Task` has 3 role TOs: `AuthorTask`, `ApproverTask`, `AdminTask`. Total: 44 TOs from 11 entities (4:1 ratio).

### SkillMatrix-Model
37 transfer objects for 21 entities confirmed (nearly 2:1 ratio). User entity alone has 10 TOs: `Admin`, `User`, `Professional`, `HREmployee`, `MyProfessional`, `Subordinate`, `UnitMember`, `UnitManager`, `ReportedUser`, and `UnitOfProfessional`. Context-specific TOs include `UnapprovedSkillsView` (approval workflow), `SelectedCompetence` (picker), and `ResultHelper` (report utility).

### Viterra Demo
10 transfer objects for 7 entities (1.4:1 ratio). `Report` entity has 3 TOs: `ReportTransfer` (admin: full CRUD + accept/review ops), `PartnerOpenReportTransfer` (partner: PENDING only, update stocks, submit op), `PartnerClosedReportTransfer` (partner: non-PENDING, read-only). `Stock` has 2 TOs: `StockTransfer` (admin, with diff calculations) and `PartnerOpenStockTransfer` (partner, editable reported fields only). `Client` has 2 TOs: `ClientTransfer` (admin) and `PartnerClientTransfer` (partner self-view with `hasNoOpenReport` derived).

### judo-demo-miniworkflow
10 transfer objects for 4 entities (2.5:1 ratio). `Document` has 2 TOs: self-mapped `Document` (default API) and `DocumentTransfer` (enhanced API with negative permissions, mixed operations, full UI). `User` has 2 TOs: self-mapped `User` and `GenericUser` (actor-specific with `isNotAdmin`/`isNotApprover`). `Files` has 2 TOs: self-mapped `Files` (read-only) and `FilesTransfer` (writable C+U+D). Plus 2 transient input DTOs (`Message`, `NewDocument`).

### AMS-Model
7 transfer objects for 7 entities (1:1 ratio), but User entity maps to 3+ distinct views: `Subordinate` (read-only summary with fullName, email, subordinate count), `manager::ManagerApprovalList` (approval-centric view with requests collection and approveAll operation), and `admin::User` (full CRUD management view). The `Request` transfer maps to the `ConfirmationRequest` entity (not the abstract `Request` base), demonstrating a naming collision where the TO name differs from the entity name.

### workflow-poc
50 transfer objects for 21 entities (2.4:1 ratio). `Token` entity maps to the `Task` transfer (user-facing task view with 13+ derived attributes, 6 operations, and 3 derived relations) plus the auto-generated `Token` transfer. `User` maps to `TaskList` (task dashboard with derived counts and filtered task collections), plus `test::User`. `Workflow` has 2 projections: public `Workflow` (name only) and `admin::Workflow` (full management with version tracking and upload operation). The model demonstrates purpose-based renaming where `Task` maps to `Token` and `Activity` maps to `Transition`.

### ReserveApp
40 transfer objects for 15 entities (2.67:1 ratio). Entity-layer TOs (15) mirror entities exactly. Admin TOs (17) provide full management views. Partner-scoped TOs (8) restrict fields -- e.g., `Partner` entity has 3 projections: `entities::Partner` (default), `services::Partner` (admin, all fields), `PartnerForPartner` (partner actor, name/phone/address only). `FreightReservation` has `ReservationForPartner` with 6 computed display attributes not on the entity.

## Trade-offs

- Pros: Each consumer gets exactly the data it needs, fine-grained security, supports diverse UI requirements from one entity
- Cons: Large number of transfer objects to maintain, changes to the entity may require updates to many TOs, naming must be clear to avoid confusion
- Prefer when: A core entity serves multiple actors with significantly different data and permission needs

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [derived-attribute-flattening](derived-attribute-flattening.md)
- [unmapped-transfer-dto](unmapped-transfer-dto.md)
