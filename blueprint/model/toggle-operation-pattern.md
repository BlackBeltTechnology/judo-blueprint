---
id: "toggle-operation-pattern"
title: "Toggle Operation for Boolean Flag Mutation"
domain: "model"
category: "operation"
score: 23.8
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - mlszksz-platform
---
## Description

Entities with boolean flags expose dedicated `toggle*` or `activate*` operations (e.g., `toggleActive`, `togglePrimary`, `activateToggle`, `changeVisibility`) rather than allowing direct attribute mutation. This ensures that business logic (mutual exclusivity, cascade updates, parent reference management) is executed whenever a flag changes. The toggle pattern is the most pervasive operation pattern in large JUDO models.

## Structure

- Entity has one or more boolean attributes (e.g., `active`, `isBilling`, `isDefault`)
- Each boolean has a corresponding `toggle*` instance operation
- The toggle operation encapsulates side effects: updating parent references, enforcing mutual exclusivity, cascading changes
- Toggle operations are exposed at the transfer/service layer via MAPPED delegation
- Operation names follow the convention `toggle` + PascalCase flag name, or `activateToggle`

## Examples

### RackInspect
~30 toggle operations across 16 entities. `Address` has 5 toggles: `toggleActive`, `toggleBilling`, `toggleDelivery`, `toggleHeadquarters`, `togglePostal`. `BankAccount`, `EmailAddress`, `PhoneNumber` each have `toggleActive` and `togglePrimary`. Toggle operations are mirrored in service TOs (e.g., `partner_service::Address.toggleActive`).

### MLSZKSZPlatform
`activateToggle` operations on reference data entities: `City.activateToggle`, `Capability.activateToggle`, `Region.activateToggle` toggle active status for geographic and business capability data. `User.changeVisibility` toggles the `isVisible` boolean flag. Unlike RackInspect's `toggle*` naming, this project uses `activateToggle` (verb+noun) and `changeVisibility` (verb+noun) naming convention.

## Trade-offs

- Pros: Business logic centralized in operation body, prevents inconsistent flag states, supports side effects (e.g., unsetting other "primary" items)
- Cons: More operations to define and maintain, simple flag flips require round-trip to server
- Prefer when: Boolean flag changes have side effects or business rules; always for `active` and `primary` flags

## Related Patterns

- [soft-delete-active-flag](soft-delete-active-flag.md)
- [primary-selection-pattern](primary-selection-pattern.md)
- [mapped-operation-delegation](mapped-operation-delegation.md)
