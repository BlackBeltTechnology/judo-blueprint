---
id: "user-with-boolean-role-flags"
title: "User Entity with Boolean Role Flags (Instead of Role Enum/Entity)"
score: 34.7
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
  - skillmatrix-model
---
## Description

A User entity that represents application users with individual boolean attributes for each role/permission level, rather than using a Role enum, a Role entity association, or a single role attribute. Each boolean flag indicates whether the user has access to a specific functional area: isAdmin, isEnterpriseArchitect, isDeveloper, isOperator, etc. All boolean flags are required, ensuring an explicit yes/no decision for each role at user creation time.

This approach trades the flexibility of a Role entity/enum (where new roles require schema changes) for simplicity and directness: role checks become simple boolean reads rather than relation traversals or enum comparisons. It is suitable for systems with a small, fixed set of roles unlikely to change. The User entity also carries standard identity attributes (firstName, lastName, email, phone) and a created timestamp.

The User entity may also serve as the mapping target for a Dashboard transfer object (providing a personalized landing page) and host factory operations for creating domain entities (createApplication, createHighLevelConnection, createUser).

A corresponding CreateUserInput unmapped TO provides the input structure for user creation, with boolean flags renamed for clarity (e.g., hasAdminAccess, hasEnterpriseArchitectAccess, hasDeveloperAccess, hasOperatorAccess) while the entity attributes use the is-prefix convention. In some projects, the boolean flags use an `isActive<RoleName>` naming pattern (e.g., isActiveAdmin, isActiveHREmployee, isActiveProfessional) to indicate both the role assignment and its active state.

A derived `isInactiveUser` attribute may combine all role flags to detect users with no active roles: `not (self.isActiveAdmin or self.isActiveHREmployee or self.isActiveProfessional)`.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
