---
id: "service-based-transfer-organization"
title: "Service-Based Transfer Object Organization"
domain: "model"
category: "transfer"
score: 62.0
usage_count: 7
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - reserve-app
alternatives:
  - actor-based-transfer-projection
---
## Description

Transfer objects are organized into service-domain packages (e.g., `services::fault_registry_services`, `services::partner_service`, `services::offer_services`) rather than actor-specific packages. A single actor (GenericUser) accesses all services, with permission-based access control handled at the entity/transfer level. This is an alternative to the actor-based organization where each actor gets its own transfer package.

## Structure

- Root `services` package with sub-packages per business domain
- Each service package contains:
  - Mapped TOs (views of entities for that domain)
  - Unmapped DTOs (operation inputs/outputs)
  - Panel/dashboard TOs (entry points for UI views)
- Single actor type accesses all service packages
- Permission control via entity-level flags (e.g., `User.permissionTo*` booleans)
- Same entity may appear in multiple service packages with different projections

## Examples

### RackInspect
14 service packages with 142 service TOs: `fault_registry_services` (30 TOs, 33 operations), `offer_services` (14 TOs, 22 operations), `partner_service` (22 TOs), `item_service` (9 TOs), `job_task_services` (5 TOs), etc. `ElementFault` appears in fault_registry_services, offer_services, and report_services with different attribute selections per context.

### MLSZKSZPlatform
5 service packages organized by business domain and role: `admin` (AdminDashboard, Announcement, Capability, City, RegistrationRequest, AdminConfigurationTO), `companyadmin` (CompanyUser, News, Offer, Request, OrganizationAdminPanel, UserInvitationRequestTO), `feed` (FeedPanel, Offer, Request), `registration` (RegistrationPoint, RegistrationTransfer), plus the main `MLSZKSZ` service with 5 access point dashboards. Multiple access points per service map to different user roles (feedDashboard for all, adminDashboard for PLATFORM_ADMIN only).

### ParkHere
All 41 transfer objects organized in a single `ParkHere::services` package with a single Actor. Transfer naming uses functional suffixes: `*Input` (CreateCarInput, HolidayInput), `*Settings` (UserSettings, ConfigurationSettings, ParkingGarageSettings), `*Panel` (UserReservationPanel, ReservationsPanel, HolidayPanel). Role-based access control via `User.isAdministrator` flag with `hiddenBy` on menu items for admin-only features. Multiple TOs per entity: `Car` and `CarSettings` provide different contexts for the same entity.

### IndamediaAdTrack
All 22 service transfer objects organized in `AdTrack::services` with a single Actor. Transfer naming uses functional suffixes: `*Transfer` (ClientTransfer, AccountTransfer, TrackedCampaignTransfer), `*Input` (ClientInput, AccountInput, GoogleCredentialInput), `*UpdateInput` (ClientUpdateInput, AccountUpdateInput), `*Panel` (ClientPanel, CampaignPanel), `*Info` (CostInfo). Clear two-namespace separation: `AdTrack::entities` for domain model and `AdTrack::services` for service contracts.

### InterfaceRegister
All 23 transfer objects organized in a single `InterfaceRegister::enterpriseArchitect` package with one `EnterpriseArchitect` actor. Transfer naming uses `{Entity}Transfer` for mapped views (ApplicationTransfer, VendorTransfer, HighLevelConnectionTransfer) and `Create{Entity}Input` for creation DTOs. The single package contains mapped TOs, input DTOs, the Dashboard TO, and protocol-specific transfer objects (Rest, SOAP, DBLink, Email, MessageQueue). Role-based access via `isEnterpriseArchitect` boolean flag on User entity.

### judo-partner
Two-tier service-based organization with a single Actor: **Internal TOs** in `::database` packages are identity-mapped (same FQN as entity) for backend use. **API TOs** in the parent packages (`Partner::partner`, `Partner::registry`) provide curated views with derived fields and operations. Sub-view TOs like `PartnerContacts` and `PartnerAddresses` provide focused views of specific entity aspects.

### ReserveApp
All 40 transfer objects organized in `ReserveApp::services` package with 5 actors sharing the same service namespace. Admin TOs (17) and partner-scoped TOs (8) coexist in the same `services` package. Entity-layer TOs (15) share FQN with entities in `ReserveApp::entities`. This hybrid approach uses service-based organization for the transfer layer while having multiple distinct actors access the same service package.

## Trade-offs

- Pros: Groups related functionality together regardless of actor, scales well for single-actor systems with permission-based access, reduces TO duplication across actors
- Cons: No built-in actor-level data isolation, permission enforcement must be done manually, all services visible to the single actor
- Prefer when: Application has one user type with role-based permissions rather than fundamentally different actor types

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md) (alternative: per-actor organization)
- [unmapped-transfer-dto](unmapped-transfer-dto.md)
- [panel-dashboard-transfer](panel-dashboard-transfer.md)
