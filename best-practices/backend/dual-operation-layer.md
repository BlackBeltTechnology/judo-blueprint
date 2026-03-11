---
id: "dual-operation-layer"
title: "Dual Operation Layer (Actor-Level and Entity-Level)"
domain: "backend"
category: "operation"
score: 61.0
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - viterra_demo
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - InterfaceRegister
  - doors-model
---
## Description

Every entity operation in a JUDO project exists in two parallel namespaces: (1) the actor-level layer under `actors/<actorName>/<entity>/` which is exposed to the frontend and includes security context, and (2) the entity-level layer under `_default_transferobjecttypes/entities/<entity>/` which provides direct entity operations. The actor-level operations may have enriched signatures (returning values, additional computed fields) compared to their entity-level counterparts. Both layers generate separate `.java.default` scaffolds and can be independently customized.

## Structure

```
custom/
  <app>/actors/<actor>/<entity>/
    CreateEntityCustomImplementation.java.default    # Actor-level (frontend-facing)
    ApproveCustomImplementation.java.default
  <app>/_default_transferobjecttypes/entities/<entity>/
    CreateEntityCustomImplementation.java.default    # Entity-level (internal)
    ApproveCustomImplementation.java.default
```

Signature differences between layers:
- Actor-level `CreateInitiative`: `Initiative apply(Input input)` -- returns created entity
- Entity-level `CreateInitiative`: `void accept(Input input)` -- returns nothing

Actor-level transfer objects may include computed UI-hint fields not on the entity:
- `editable`, `hideSendForApproval`, `hideApproval`, `hideReject`, `hideArchive` (visibility flags)
- `label`, `initiator` (derived display fields)

## Examples

### itracker
5 operations duplicated across both layers (10 total + 1 Init): CreateInitiative, SendForApproval, Approve, Reject, ArchiveForecast. Actor-level `CreateInitiative` returns the created `Initiative` with UI hints; entity-level returns void with simpler field mapping. Actor-level `Initiative` transfer object adds 7 computed fields for frontend UI control.

### viterra_demo
Operations span entity-level (`_default_transferobjecttypes/report/`) and transfer-object-level (`reporttransfer/`, `partneropenreporttransfer/`). Accept and Review exist on both `Report` (entity) and `ReportTransfer` (transfer object). Submit exists on both `Report` and `PartnerOpenReportTransfer`, returning `PartnerClosedReportTransfer` to represent the state transition from open to closed report view.

### judo-demo-miniworkflow
Operations duplicated across entity-level (`_default_transferobjecttypes/document/`) and transfer-object-level (`documenttransfer/`). Accept, Reject, Close, RequestReview exist in both layers with identical signatures (`void method(Entity _this, Message input)`). CreateDocument exists only in `documenttransfer/` (factory operation returning `DocumentTransfer`). InitUsers exists only in `_default_transferobjecttypes/user/`. Total 10 scaffolds: 4 entity-level + 5 transfer-object-level + 1 user operation.

### Ubives
Same operations duplicated across 4+ service domains (dashboardorganization, organization, partnerdashboard, profile, account). CreateOrganization exists in account, partnerdashboard, and profile views. InviteUser/InviteAccount exist in dashboardorganization, invitation, organization, partnerdashboard, organizationaccount, and user views. Each copy delegates to the same shared service, resulting in 42 custom operations from ~15 unique operations. Entity-level init operations under `_default_transferobjecttypes/entities/initializer/`.

### ParkHere
Same operations appear across multiple panel contexts (service-level views): Holiday operations exist in HolidayPanel, ReservationsPanel, and UserReservationPanel -- all 3 implementations delegate to HolidayService. Reservation operations exist in ReservationsPanel and UserReservationPanel. CreateCar exists in UserSettings and ProfileSettings. FavoriteCar and DeleteCar exist in Car and CarSettings contexts. 20 custom operations derive from ~12 unique business operations, with each copy delegating to shared services.

### InterfaceRegister
3 operations duplicated across User entity-level and Dashboard actor-level contexts (6 total): CreateUser, CreateApplication, CreateHighLevelConnection. Entity-level operations are bound to `User _this` context, while Dashboard operations are bound to `Dashboard _this` context. Both share the same input transfer objects (CreateUserInput, CreateApplicationInput, CreateHighLevelConnectionInput). All remain as `.java.default` stubs. Demonstrates context-specific operation overloading where the same logical operation can behave differently based on calling context.

### doors-model
Two actor packages (admin, employee) with different views and capabilities. Admin actor manages companies, employees, divisions, positions. Employee actor handles contract creation, viewing, and approval workflow interaction. Transfer objects include actor-specific types: `CreateContractInputTO`, `StartApprovalResult`, `ValidateContractResult`, navigation data TOs. Custom operations like `createContract` are bound to the employee actor's `ContractType` view, while entity-level operations reside on `doors::entities::Contract`.

## Trade-offs

- Pros: Actor layer provides security scoping and UI-optimized views, entity layer provides unrestricted access for internal use, separation of concerns between frontend and backend
- Cons: Operation logic may be duplicated across layers, twice as many scaffolds to maintain, can be confusing which layer to customize
- Alternative: Single operation layer with access control handled by interceptors or model-level expressions

## Related Patterns

- custom-operation-osgi-component
- dual-dao-pattern
- script-driven-operations
