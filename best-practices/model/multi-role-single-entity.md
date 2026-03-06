---
id: "multi-role-single-entity"
title: "Multi-Role Single Entity with Boolean Flags"
domain: "model"
category: "entity"
score: 46.4
usage_count: 7
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - skillmatrix-model
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - reserve-app
---
## Description

A single entity serves as the unified identity for all actor types in the system. Rather than using separate entities or generalization hierarchies for different roles, the entity uses boolean flags (e.g., `isActiveAdmin`, `isActiveHREmployee`, `isActiveProfessional`) to control which actors a user can authenticate as. Each ActorType uses an `isActiveExpression` that evaluates the corresponding flag. This allows a single user to hold multiple roles simultaneously.

## Structure

- Single entity (typically `User`) with boolean role flags, all defaulting to `false`
- Each ActorType references the same entity as its principal
- Each actor's `isActiveExpression` checks the corresponding flag: `self.isActiveAdmin`, `self.isActiveProfessional`, etc.
- A derived attribute computes "no role": `isInactiveUser = not (self.isActiveAdmin or self.isActiveHR or ...)`
- All actors share the same authentication realm and are identified by a common claim (e.g., EMAIL)
- Admin actor controls role assignment by toggling the boolean flags on user records

## Examples

### SkillMatrix
`User` entity with 3 boolean role flags: `isActiveAdmin` (default: false), `isActiveHREmployee` (default: false), `isActiveProfessional` (default: false). 4 actors share realm `SKILL_MATRIX` with EMAIL claim. `HREmployeeActor.isActiveExpression = self.isActiveHREmployee`, `ProfessionalActor.isActiveExpression = self.isActiveProfessional`. Derived: `isInactiveUser = not (self.isActiveAdmin or self.isActiveHREmployee or self.isActiveProfessional)`.

### SkillMatrix-Model
Model source confirms 4 ActorTypes: `AdminActor`, `UserActor` (`isActiveExpression="false"`, always disabled), `HREmployeeActor` (`isActiveExpression="self.isActiveHREmployee"`), `ProfessionalActor` (`isActiveExpression="self.isActiveProfessional"`). All share realm `SKILL_MATRIX`. The 32 references to role flag attributes demonstrate pervasive use across access filtering, UI control, and derived relations.

### KozutEugyfelClient
`Felhasznalo` entity with `admin: Boolean` stored flag plus 3 derived role booleans: `ugyfelszolgalatiMunkatars = self.munkakorNev == "Ugyfelszolgalati_Munkatars"`, `szervezetiEgysegMunkatars`, `szervezetiEgysegVezeto`. Role is determined by the `Munkakor` (job position) relation rather than stored booleans, demonstrating a variant where roles are derived from organizational data rather than explicitly stored flags.

### judo-demo-miniworkflow
`User` entity with 3 boolean flags: `admin` (default: false), `approver` (default: false), `active` (default: true). A single `GenericActor` serves all users; role-based visibility is controlled via `GenericUser` transfer's derived negatives (`isNotAdmin`, `isNotApprover`) used in menu item `hiddenBy` bindings. Admin menu hidden when `isNotAdmin`, approval queue hidden when `isNotApprover`.

### AMS-Model
`User` entity serves as requester, approver, manager, and issuer through relation-based roles rather than boolean flags. Manager role is activated via `isActiveExpression = self.subordinates!count() > 0` (derived from the self-referencing `User.manager <-> User.subordinates` hierarchy). Admin is a separate entity extending User functionality. The same User holds 6 two-way relations (requests, approvals, applications, subordinates, issues) defining implicit roles.

### ParkHere
`User` entity with 5 boolean role flags: `isAdministrator` (default: false), `isNormalReservation` (default: false), `isQuickReservation` (default: true), `isGuestReservation` (default: false), `isLongReservation` (default: false). A single Actor serves all users; admin-only features use `hiddenBy` with derived `isNotAdministrator = not self.isAdministrator`. Roles control which reservation types a user can create and are not mutually exclusive, allowing flexible permission combinations.

### IndamediaAdTrack
`User` entity with `isAdmin: Boolean` (required) and `isNotAdmin: Boolean` (optional) as a boolean pair for admin role management. The `isNotAdmin` serves as a query optimization pattern, avoiding negation in filter expressions. Operations check `isAdmin` to enforce `PERMISSION_DENIED` error codes on privileged operations like `createClient`, `updateClient`, and account management.

### InterfaceRegister
`User` entity with 4 boolean role flags: `isAdmin`, `isEnterpriseArchitect`, `isDeveloper`, `isOperator`. The single `EnterpriseArchitect` actor uses `isActiveExpression="self.isEnterpriseArchitect"` with EMAIL claim. The `CreateUserInput` DTO renames these to `hasAdminAccess`, `hasEnterpriseArchitectAccess`, `hasDeveloperAccess`, `hasOperatorAccess` (all defaulting to false), demonstrating transfer-level renaming for clearer UI labels.

### ReserveApp
`User` entity with a `Role` enum attribute (PARTNER, LOGISTICIAN, DOORMAN, READ_ONLY, ADMIN) instead of boolean flags. Each of 5 ActorTypes uses EMAIL claim for authentication, but roles are determined by the single `role` enum rather than boolean flags. This is a variant where an enum-based role field replaces multiple boolean flags, ensuring users have exactly one role at a time (mutually exclusive).

### AMS-Frontend
`User` entity serves multiple implicit roles through relations rather than boolean flags. Manager role dynamically activated via `isActiveExpression = self.subordinates!count() > 0` -- a user becomes a manager when they have subordinates. `Admin` is a separate entity with its own principal. The User entity holds 6 bidirectional relations defining role contexts (requests, approvals, applications, subordinates, issues).

## Trade-offs

- Pros: Single user record, no data duplication, users can hold multiple roles, simple role assignment via boolean toggle
- Cons: All role data on one entity (may grow large), cannot have role-specific attributes on the entity, requires careful access filtering per role
- Prefer when: Users can hold multiple roles simultaneously and role assignment is a simple enable/disable

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [default-value-patterns](default-value-patterns.md)
- [derived-access-filtering](derived-access-filtering.md)
