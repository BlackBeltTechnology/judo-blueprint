---
id: "panel-dashboard-transfer"
title: "Panel/Dashboard Transfer Object as UI Entry Point"
domain: "model"
category: "transfer"
score: 75.9
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-05-13"
projects:
  - rackinspect
  - mlszksz-platform
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - compsychletter
---
## Description

Dedicated transfer objects with a "Panel" or "Dashboard" suffix serve as entry points for UI dashboard views. They aggregate access to entity collections and expose creation operations, acting as view-model containers for list/grid screens. Panel TOs are typically mapped to entities that serve as the user's workspace or task list.

## Structure

- Transfer object named `*Panel` or `*Dashboard` or `*List` (e.g., `FaultRegistryPanel`, `AdminDashboard`, `FeedPanel`, `PartnerList`)
- Contains relations to entity collections visible in the dashboard
- Hosts static or instance operations for entity creation (e.g., `createFaultRegistry`, `createCity`)
- May include bulk operations (e.g., `modifyMarkup` for batch price changes, `inviteBulk` for batch invitations)
- Serves as the root navigation point for a service domain in the UI

## Examples

### RackInspect
5 panel TOs: `FaultRegistryPanel` (fault registry listing + `createFaultRegistry` operation), `MyTaskPanel` (current user's assigned tasks + `createFaultRegistry`), `ItemsPanel` (item listing + `createItem` + `modifyMarkup` bulk operation), `OffersPanel` (offer listing), `ExchangeRatesForUser` (user-scoped exchange rate management + creation/update operations).

### MLSZKSZPlatform
Multiple dashboard/panel TOs across services: `AdminDashboard` (8 operations: createCity, createCapability, createAnnouncement, createOrganization, syncFeed, inviteBulk, exportAuditLog), `OrganizationAdminPanel` (10 operations: user/post CRUD, address/company updates, postal code lookup), `FeedPanel` (requestPost operation). Each dashboard serves as the entry point for a role-specific UI section, aggregating creation operations and entity collection access.

### ParkHere
3 panel TOs: `UserReservationPanel` (user's own reservations with `reservation`, `modificateReservation`, `deleteReservation`, `cancelReservation`, `holiday` operations), `ReservationsPanel` (admin view of all reservations), `HolidayPanel` (user's holidays). Panels serve as the primary navigation targets for menu items, aggregating related operations and collection views into cohesive UI screens.

### IndamediaAdTrack
2 panel TOs: `ClientPanel` (client management view with `createClient` operation) and `CampaignPanel` (campaign management view). Panels serve as navigation entry points for the single-actor UI, providing domain-scoped list views with associated creation operations. Operations on transfer objects (e.g., `ClientTransfer.updateClient`) provide detail-level actions.

### InterfaceRegister
`Dashboard` transfer object mapped to the `User` entity, accessed via a DERIVED access point filtering by actor email: `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()`. Contains a derived `welcomeText = 'Hi, ' + self.firstName` greeting and hosts 3 creation operations: `createApplication`, `createHighLevelConnection`, `createUser`. Serves as the home screen entry point for the EnterpriseArchitect actor.

### judo-partner
`PartnerList` transfer object mapped to `User` (not Partner), using the actor's user context (`self` getter) to provide a personalized dashboard. Exposes derived `partners` and `partnerLogs` collections, plus `isActorPartnerAdmim` and `isActorAdmin` derived authorization fields. Hosts `createPartner` operation. Demonstrates mapping a dashboard TO to the User entity for user-scoped data aggregation.

### AMS-Frontend
`ManagerApprovalList` transfer mapped to `User` entity, accessed via `self` getter on the Manager actor. Provides a bulk approval dashboard with a filtered `approvals` relation (pending requests from open campaigns) and an `approveAll` operation. Used as the "Approve All Pending" navigation entry point, aggregating approval context into a single action view.

### CompSychLetter
Three business-area dashboards on a single actor (`LetterUser`), each accessed via a separate `self`-getter DERIVED access point (`0..1`): `authoring -> AuthoringDashboard`, `documents -> DocumentsDashboard`, (data dashboard planned). Each dashboard maps to `compsychletter::entities::User` with `getterExpression="self"`. `AuthoringDashboard` exposes three DERIVED tab relations — `templates -> TemplateTO (0..*)`, `rules -> RuleTO (0..*)`, `designs -> DesignTO (0..*)` — using Phase-0 unscoped getters: `compsychletter::entities::Template!filter(t | true)`. Per-area projection TOs (`TemplateTO`, `RuleTO`, `DesignTO`, `OriginalBodyTO`, `LanguageVariantTO`) are all-CRUD-false MAPPED projections, reachable only through the dashboard. The `!filter(t | true)` idiom is valid for DERIVED relations on mapped TOs (unlike `ActorType.accesses` where a bare boolean literal is rejected by the ASM validator); it serves as a Phase-0 placeholder until per-user scoping is introduced as a later additive refinement.

## Required Companion

Every dashboard `Access` must be paired with a `MenuItemAccess` on the actor's `menuItems` to appear in the navigation drawer. The React generator drives `useMenus()` and `routes.tsx` from `menuItems`, not from `accesses` — an unpaired access is API-only and invisible. See [access-paired-with-menu-item](access-paired-with-menu-item.md). The CompSychLetter participant above is at Phase-0 with this pairing intentionally deferred (`menuItems.totalCount = 0`); Phase-1 adds three `MenuItemAccess` entries (one per dashboard) with MDI icons.

## Trade-offs

- Pros: Clean UI entry point per domain, centralizes list view and creation in one TO, supports dashboard-specific operations
- Cons: Additional TO layer, may become bloated if too many operations are added; requires a parallel `MenuItemAccess` per dashboard to be user-reachable
- Prefer when: UI needs a dashboard/list view with creation capability for a specific domain

## Related Patterns

- [access-paired-with-menu-item](access-paired-with-menu-item.md) — mandatory menu pairing
- [service-based-transfer-organization](service-based-transfer-organization.md)
- [unmapped-transfer-dto](unmapped-transfer-dto.md)
