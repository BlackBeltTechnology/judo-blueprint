---
id: user-with-role-and-rolegroup-entities
title: User with Role and RoleGroup Entities
description: A User entity linked to Role entities and to RoleGroup entities by many-to-many associations, where a group bundles roles so that roles can be granted one by one or as a group.
aliases: [role group assignment, hierarchical role assignment, user roles and groups]
keywords: [user, role, rolegroup, many-to-many, effective roles, derived relation, bulk assignment]
tags: [domain:model, layer:model, project:sanctuary-backend, status:single-project]
category: pattern
status: single-project
projects: [sanctuary-backend]
evidence: ["sanctuary-backend:unrecorded"]
alternatives: [user-with-boolean-role-flags, user-with-role-permission-entity]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let administrators grant roles to users at run time, either one role at a time or through a named group of roles. Roles are data, not code, so a new role or group needs no release.

### Two levels of assignment

A user holds roles directly and holds role groups. A group collects several roles under one name, so a bundle of rights is granted with one assignment.

### The user reads one effective set

A derived relation on the user, `effectiveRoles`, is meant to answer "which roles does this user have". The example project defines it as the direct roles only (`self.roles`); roles that come through groups are not added. A model that needs group roles must extend the getter expression to include them.

## Structure

- **User**: identity attributes (email, first name, last name), plus optional profile attributes in the example. A bidirectional many-to-many association to Role (`roles` / `users`), a bidirectional many-to-many association to RoleGroup (`roleGroups` / `users`), and the derived `effectiveRoles` relation to Role.
- **Role**: a required name and the back-reference `users`.
- **RoleGroup**: a required name, a one-way association `roles` to Role (the role does not know its groups), and the back-reference `users`.
- Around the shape the example also composes user settings and privacy settings under the user, adds a job-title reference entity, and types visibility fields with an enumeration (see [[privacy-visibility-enum]]). They are project additions, not part of the pattern.

## Constraints

- Both user relations are many-to-many associations, never compositions: roles and groups outlive any one user.
- Role-to-group is one-way, so changing a group's roles does not touch the role entity.
- `effectiveRoles` is a derived relation. It is computed on read and cannot be assigned. See [Derived relation navigation](../../best-practices/model/derived-relation-navigation.md).
- A user that must keep at least one administrator needs that rule in the operation that changes roles or groups: interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Transfer objects that expose users, roles and groups to an administrator actor control who may edit these relations. The example gives one admin actor full create, update and delete access to all four.

## Variations

- **Group roles in the effective set.** Define `effectiveRoles` as the union of the direct roles and the roles of the user's groups.
- **Groups only.** Drop the direct user-to-role relation and grant rights only through groups.
- **Permissions per role.** Give each role its own permission entity. See [[user-with-role-permission-entity]].
- **Fixed roles as flags.** Replace the entities with one boolean per role. See [[user-with-boolean-role-flags]].

## When to use

- Administrators create and rename roles without a release.
- Many users receive the same bundle of roles, so grouping saves repeated assignment.
- A user may hold several roles.

## When to avoid

- The set of roles is small and fixed. Use [[user-with-boolean-role-flags]].
- Each role belongs to one organization. See [[user-with-organization-and-role]].
- Roles never need grouping. A plain role entity is enough.

## Related

- [[user-with-boolean-role-flags]] — fixed roles as flags on the user
- [[user-with-organization-and-role]] — a role that belongs to an organization
- [[user-with-role-permission-entity]] — roles with explicit permissions
- [[privacy-visibility-enum]] — visibility levels used by the example's privacy settings
