---
id: "permission-flag-enum"
title: "Permission Flag Enumeration for Role-Based Access"
domain: "model"
category: "enum"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

A single-actor system implements role-based access control through a `Permission` entity with a `PermissionFlag` enumeration. Each enum member corresponds to a module/feature area. Roles have sets of Permissions, and Users are assigned Roles. The User entity has derived boolean `permissionTo*` attributes computed from their aggregated role permissions, enabling UI visibility control per module.

## Structure

- `Permission` entity with `flag: PermissionFlag` attribute
- `PermissionFlag` enum with one member per feature/module (e.g., `FAULT_REGISTRIES`, `OFFERS`, `USERS`)
- `Role` entity with `permissions -> Permission [0..*]` association
- `User` entity with:
  - `roles -> Role [0..*]` association
  - `permissions -> Permission [0..*]` DERIVED relation (aggregated from all roles)
  - `permissionTo*: Boolean` (one per feature, computed from permissions)
- A `recalculatePermissions` operation on User to refresh the boolean flags

## Examples

### RackInspect
`PermissionFlag` enum has 23 members covering all modules: `FAULT_REGISTRIES`, `OFFERS`, `ITEMS`, `PARTNERS`, `USERS`, `CONFIGURATION`, etc. User has 23 corresponding `permissionTo*` booleans (all default: false): `permissionToFaultRegistries`, `permissionToOffers`, `permissionToUsers`, etc. `User.recalculatePermissions` refreshes these flags from the role-permission chain.

## Trade-offs

- Pros: Fine-grained feature-level permissions, roles are composable, boolean flags enable simple UI permission checks
- Cons: Adding a new feature requires enum + boolean + recalculation logic changes, denormalized booleans on User
- Prefer when: Single-actor system needs role-based access control per feature/module

## Related Patterns

- [entity-crud-at-service-layer](entity-crud-at-service-layer.md)
- [toggle-operation-pattern](toggle-operation-pattern.md)
