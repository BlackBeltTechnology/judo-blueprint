---
id: "soft-delete-active-flag"
title: "Soft Delete via Active Boolean Flag"
domain: "model"
category: "entity"
score: 77.8
usage_count: 11
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - judo-demo-miniworkflow
  - sanctuary-backend
  - park-here
  - indamedia-adtrack
  - judo-partner
  - reserve-app
---
## Description

Entities include a required boolean `active` or `isEnabled` attribute (default: `true`) to implement soft delete. Instead of physically deleting records, they are marked inactive/disabled. This preserves referential integrity and audit history while allowing records to be hidden from active views. Some implementations include a `toggleActive` operation while others manage the flag through standard CRUD updates. An alternative approach uses a status enum with a DELETED member for richer lifecycle tracking.

## Structure

- Entity has `active: Boolean, required, default: true` or `isEnabled: Boolean, default: true`
- Optionally, entity has a `toggleActive` instance operation
- Soft-deleted records remain in the database but are excluded from active queries
- Pattern is applied uniformly across reference data, contact information, and user entities
- Often combined with the toggle operation pattern for flag mutation
- Alternatively, status enums include a DELETED member (e.g., PostStatus.DELETED)
- Variant: an ActiveStatus enum (active/archived) can serve the same purpose
- Variant: `isArchived` flag (inverted semantics, default: false) marks records as deleted

## Examples

### RackInspect
15+ entities use the active flag pattern: `Address`, `BankAccount`, `CompanyAddress`, `CompanyBankAccounts`, `CompanyEmail`, `CompanyPhone`, `EmailAddress`, `Partner`, `PaymentDeadline`, `PaymentMethod`, `PhoneNumber`, `Unit`, `User`, `UserAddress`, `UserEmail`, `UserPhone`. All default to `active=true` with `toggleActive` operations.

### Alba
4 reference data entities use `isEnabled: Boolean, default: true`: `Audience`, `Curriculum`, `ResultType`, `Institution`. No toggle operation -- the flag is managed through admin CRUD updates. Access points filter by `isEnabled` to exclude disabled entries from user-facing views while preserving referential integrity for existing product associations.

### SkillMatrix-Model
`Competence.active` (required, default: `true`) serves as the soft-delete flag. The `Competence.delete()` operation guards against deleting active competences: `if (this.active) { return; }`. Range expressions filter by active status: `Competence!filter(c | c.active)!sort(c | c.name ASC)` ensures only active competences appear in pickers. `TrainingPlan.closed` (default: `false`) uses a similar boolean-flag lifecycle concept.

### MLSZKSZPlatform
Uses status enum-based soft delete instead of boolean flags: `PostStatus.DELETED` and `AnnouncementStatus.DELETED` mark content as deleted without physical removal. Content remains in the database for audit trail purposes and feed integrity. This approach provides richer lifecycle tracking (DRAFT -> PUBLISHED -> DELETED) compared to a simple boolean, but serves the same purpose of preserving data while hiding it from active views.

### Viterra Demo
`Client.active` and `Silo.active` are required Boolean attributes (default: `true`) used for soft delete. Admin access has no delete permission on any entity. The `Client` range expression in `ReportTransfer` filters by active: `viterra::Client!filter(c | c.active)` ensures only active clients appear in selectors. Partner actor checks `self.active` in its `isActiveExpression` to prevent deactivated partners from logging in.

### judo-demo-miniworkflow
`User.active` (required Boolean, default: `true`) serves as the soft-delete/deactivation flag. The `GenericActor.isActiveExpression` can check `self.active` to prevent deactivated users from accessing the system. No toggle operation is defined -- the flag is managed through direct CRUD updates on the `users` access point (admin only).

### Sanctuary Backend
Uses the `ActiveStatus` enum (active/archived) on `User.status` and `PositionTitle.status` for soft delete. This enum variant provides a binary active/archived lifecycle without requiring a boolean flag. Entities with `archived` status are logically hidden while data is preserved. The enum approach is shared across multiple entity types via a root-level enum definition.

### ParkHere
5 entities use the soft delete pattern: `Car.isArchived` (inverted flag, default: false), `User.isActive`, `ParkingGarage.isActive`, `ParkingSlot.isActive`, `Doorman.isActive` (all default: true). Car uses the `isArchived` variant, where `true` means deleted. The `deleteCar` operation sets `isArchived=true` rather than physically removing the record, preserving historical reservation references.

### IndamediaAdTrack
`Client.isActive` and `Account.isActive` are required Boolean attributes (default: `true`) for soft-delete/deactivation. The `updateAccount` operation sets `isActive=false` to deactivate accounts, causing sync operations to skip inactive accounts. `untrack` operation on TrackedCampaign similarly acts as a soft delete by removing the aggregation association while preserving historical Cost and FetchedData records.

### judo-partner
`Partner.isArchived` (required Boolean) uses the inverted-flag variant for soft deletion. The derived `Partner.status` attribute computes `PartnerStatus` (ACTIVE/DRAFT/DELETED) from the `isArchived` flag and other entity state. The `Partner.delete` operation sets `isArchived = true` rather than physically removing the record. This preserves partner data for registry document references and audit logs.

### ReserveApp
11 reference/lookup entities use `active: Boolean, default: true`: Gate, Partner, Company, LoadingType, VehicleType, Project, Spot, ProductCategory, LoadingTime, Unit, StorageType. Range expressions enforce active filtering: `Company!filter(c | c.active)`, `Project!filter(p | p.active)`, etc. Item entity uses a separate `deleted` Boolean for true soft-delete semantics.

## Trade-offs

- Pros: Preserves data for audit, no referential integrity violations, easy to "undelete"
- Cons: Requires filtering inactive records in all queries, database grows over time
- Prefer when: Records have references from other entities and physical deletion would break integrity

## Related Patterns

- [toggle-operation-pattern](toggle-operation-pattern.md)
- [default-value-patterns](default-value-patterns.md)
