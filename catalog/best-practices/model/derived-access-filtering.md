---
id: "derived-access-filtering"
title: "Derived Access Point with Getter Filtering"
domain: "model"
category: "access"
score: 77.7
usage_count: 13
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
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

Access points use the DERIVED access type with getter expressions to filter or restrict the data visible to an actor. This enforces data visibility rules at the model level, ensuring actors only see records matching specific criteria (e.g., only OPEN contests, only the singleton application instance).

## Structure

- Access link set to type `DERIVED` (not `ALL`)
- A `getterExpression` defines what data is accessible
- Common patterns:
  - **Status filtering**: `EntityType!filter(e | e.status == Status#VALUE)` -- restrict by lifecycle state
  - **Singleton access**: `EntityType!any()` with cardinality `0..1` -- access a single instance
  - **Back-reference navigation**: Derived association pointing to parent entity (container pattern)
  - **Ownership + role filtering**: Combined filter checking ownership AND role-based visibility
  - **Self-reference**: `self` -- access the logged-in user's own record
  - **Navigation from self**: `self.relation!sort(...)` -- access data reachable from logged-in user
  - **Actor variable + status combined**: Filter by actor email AND entity status simultaneously
- `ALL` access type is used when no filtering is needed (typically for admin actors)

## Examples

### Trivia
`Player.contests` is DERIVED with getter `Contest!filter(c | c.status == ContestStatus#OPEN)` -- players only see open contests. `Player.application` is DERIVED with getter `Application!any()` and cardinality 0..1 -- singleton access. All Admin accesses use `ALL` type (unfiltered).

### RackInspect
Derived associations used as container back-references on 14+ entities: `Address.container -> Partner`, `BankAccount.container -> Partner`, `Warehouse.container -> Address`, `Rack.container -> Warehouse`, etc. These enable child-to-parent navigation without stored foreign keys.

### itracker
`UserActor.initiatives` is DERIVED with a complex getter combining ownership and role: regular users see only their own initiatives (`i.user.email == ACTOR.email`), while finance users additionally see all non-NEW initiatives from other users. All Admin accesses use `ALL` type for reference data management.

### SkillMatrix
HREmployeeActor uses DERIVED accesses with filter+sort: `professionals = User!filter(u | u.isActiveProfessional)!sort(p | p.indexName ASC)`, `competencies = Competence!sort(c | c.name ASC)`. ProfessionalActor uses self-referencing: `myProfession = self` (own profile), `subordinates = self.subordinates!sort(u | u.indexName ASC)` (navigation from self), `allForApproval = self` (consolidated approval view).

### Alba
Role-scoped access points: `authorProducts` derived to show only products where current user is author, `publicProfiles` derived to show only active users, `userProfile` derived to current user's own record (0..1). Admin-specific accesses: `adminProfiles`, `curriculumsForAdmins`, `audiencesForAdmins` with full CRUD. Filter accesses for reference data: `curriculumsForFilter`, `resultTypesForFilter` (read-only for all users).

### SkillMatrix-Model
Model source confirms DERIVED access points on 3 of 4 actors. `HREmployeeActor` accesses filter by role flag and sort by name. `ProfessionalActor` uses `self` access for own profile and `self.subordinates!sort(...)` for navigation from self. `AdminActor` uses broader access. `UserActor` (`isActiveExpression="false"`) is always disabled, serving as a managed principal placeholder.

### Viterra Demo
Partner actor uses DERIVED access with combined status + actor email filtering: `openReports = Report!filter(r | r.status == ReportStatus#PENDING and r.client.email == String!getVariable("ACTOR", "email"))`, `closedReports` uses `status != PENDING` with same email filter. `partnerData = Client!filter(c | c.email == String!getVariable("ACTOR", "email"))!any()` (0..1, singleton partner record). Admin uses `ALL` access type for all 5 access points.

### KozutEugyfelClient
3 actors with role-scoped access: Admin accesses Felhasznalo records broadly, Munkatars (worker) accesses their assigned Bejelentes (complaints) filtered by organizational unit and role, EUgyfelAlkalmazas (e-Government app) accesses only integration-specific operations. The `Erkezteto` (dispatcher) entity filters by `bejelentesTipus` to route complaints to the appropriate organizational unit.

### judo-demo-miniworkflow
2 DERIVED access points on `GenericActor`: `myDocuments` navigates from current user to their documents via `User!filter(u | u.email == Email!getVariable('ACTOR', 'email'))!any().documents`, and `waitingForApproval` filters for documents in REVIEW_REQUESTED state owned by other users. The `users` access point uses `ALL` type for admin-level user management, with menu visibility controlled by `hiddenBy` on `isNotAdmin`.

### AMS-Model
Manager actor uses DERIVED access with relation navigation and status filtering: `approvalList = self.approvals!filter(r | r.campaignStatus == CampaignStatus#OPEN)` shows only confirmation requests from open campaigns. `subordinates = self.subordinates` navigates from self. Manager's `isActiveExpression = self.subordinates!count() > 0` activates only for users with subordinates. Admin uses `ALL` access for campaigns, applications, and users.

### ParkHere
Single Actor with 9 DERIVED access points combining admin role filtering and user-scoped views. Admin-only accesses: `parkingGarages`, `parkingSlots`, `users` filter out non-admin users. User-scoped accesses: `userReservations` shows current user's reservations, `profileSettings` shows own profile, `userHolidays` shows own holidays. `configurationSettings` provides admin-only singleton configuration access. `usersForInput` uses ALL type for user selection dropdowns.

### InterfaceRegister
Single EnterpriseArchitect actor with 14 access points. One DERIVED access: `dashboard` (0..1) uses `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()` to resolve the current user's personalized Dashboard view. All other 13 access points use `ALL` type for unfiltered entity collections (businessDataTypes, brands, vendors, applications, highLevelConnections, interfaceSpecifications, etc.), reflecting a single-role admin-style application.

### judo-partner
Single Actor with 11 access points mixing DERIVED and default patterns: `partnerList [0..1]` uses `self` getter (user-scoped dashboard), `NAVConfig [0..1]` uses `NAVConfig!any()` (singleton access for tax authority API configuration). Most collection accesses (`users`, `countries`, `imports`, `registers`, `cases`, etc.) use default access for unfiltered entity collections with varying CRUD permissions (some C/U/D, some read-only).

### KozutEugyfelModelTest
3 KOZUT-realm actors use DERIVED access for `intezendoBejelentesek` with getter `self.intezendok`, navigating from the principal to assigned complaints. This gives each actor only their personally assigned actionable complaints, while `bejelentesek` uses broader access for all-complaints viewing. The `felhasznalok` access provides shared read-only user lookup.

### workflow-poc
Single anonymous actor with 4 access points mixing DERIVED and ALL: `taskList [0..1]` is DERIVED with `User!filter(u | u.email == String!getVariable("ACTOR", "email"))!any()` for personalized task view, while `documents`, `urls`, and `workflows` use ALL type for unrestricted collection access. The DERIVED taskList access resolves the current user and provides the workflow-scoped task management entry point.

### ReserveApp
AdminActor has 13 access points (menu item accesses) to manage all reference data and users. PartnerActor has 2 accesses: `profile` (principal self-view via `PartnerUser`) and `reservationsForPartner` (partner-scoped reservations). Three actors (Logistician, Doorman, Readonly) have no accesses defined yet, indicating planned but not-yet-implemented role-based filtering.

### AMS-Frontend
Manager actor uses 3 DERIVED accesses: `subordinates = self.subordinates` (navigation from self), `approvalAll = self` (self-access for bulk approval), `approvalList = self.approvals!filter(r | r.campaignStatus == CampaignStatus#OPEN)` (status-filtered relation navigation). Manager's `isActiveExpression = self.subordinates!count() > 0` dynamically activates the role. Admin uses `ALL` access for campaigns, applications, and users.

## Trade-offs

- Pros: Server-side data filtering enforced in the model, no client-side trust required, declarative
- Cons: Filter expressions limited to JQL, complex multi-tenant logic may need custom code
- Prefer when: Different actors need different subsets of the same entity data

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [singleton-entity](singleton-entity.md)
- [range-expression-filtering](range-expression-filtering.md)
- [container-back-reference](container-back-reference.md)
