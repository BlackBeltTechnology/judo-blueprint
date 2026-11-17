---
id: user-with-role-permission-entity
title: User with Role and Permission Entities
description: A User associated to Role entities, each role holding Permission entities typed by a permission enumeration, with denormalized permission booleans on the user that a recalculation operation keeps in sync.
aliases: [role permission graph, denormalized permissions, permission flags]
keywords: [user, role, permission, enumeration, denormalized, boolean, recalculate]
tags: [domain:model, layer:model, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [user-with-boolean-role-flags, user-with-role-and-rolegroup-entities]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let administrators define roles and the permissions each role carries, and still make every permission check a cheap boolean read. The role and permission graph is the source of truth. Booleans on the user are a stored copy of it.

### Permissions are entities typed by an enumeration

A Permission entity holds one required flag from a PermissionFlag enumeration. The enumeration lists every controllable area of the application. Roles collect permissions, users collect roles.

### The user carries a denormalized copy

For each area the user has a required boolean (for example `permissionToPartners`, default false). Access expressions and generated UI visibility read these booleans without walking the graph. The cost is that the copy can go stale.

### One operation rebuilds the copy

An instance operation `recalculatePermissions` on the user recomputes the booleans from the roles and permissions. It must run after every change to a user's roles or to the permissions of a role they hold.

## Structure

- **PermissionFlag** enumeration: one member per controllable area (for example partners, users, roles, configuration). The example has 23 members.
- **Permission** entity: a required flag of type PermissionFlag.
- **Role** entity: a required name and a one-way association `permissions` to Permission (0..*).
- **User** entity: required name and email, a one-way association `roles` to Role (0..*), a derived collection `permissions` (the permissions of its roles), one required boolean per permission area defaulting to false, and the custom instance operation `recalculatePermissions`.

## Constraints

- The graph is the source of truth. The user booleans are derived data stored for speed. Nothing but `recalculatePermissions` may write them.
- `recalculatePermissions` is a custom operation. Interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)), so the rule about who may trigger it, and the calls after role changes, must be in the backend code.
- Each new permission area needs an enumeration member and a user boolean, so the entity changes with the enumeration.
- The derived `permissions` relation is computed on read ([Derived relation navigation](../../best-practices/model/derived-relation-navigation.md)). The booleans can instead be derived attributes of the same expression, which removes the stale copy at the cost of a query on each read.
- Rows are meant to be maintained by an administrator through access to mapped transfer objects. The example turns off create, update and delete on the three entities themselves.

## Variations

- **Derived booleans.** Replace stored booleans with derived attributes that test whether the user's permissions contain the flag. No recalculation operation, no stale copy, more work per read.
- **Groups of roles.** Add role groups so that many roles are granted at once. See [[user-with-role-and-rolegroup-entities]].
- **Fixed flags only.** Drop role and permission entities. See [[user-with-boolean-role-flags]].

## When to use

- Roles and their permissions are edited by administrators at run time.
- Permission checks are frequent and must be a plain boolean read.
- The set of permission areas is known and changes rarely.

## When to avoid

- The set of roles is small and fixed. Use [[user-with-boolean-role-flags]].
- Rights depend on an organization. See [[user-with-organization-and-role]].
- Permission checks are rare. Derive them instead of storing a copy.

## Related

- [[user-with-boolean-role-flags]] — flags on the user without role entities
- [[user-with-role-and-rolegroup-entities]] — roles grouped into bundles
- [[user-with-organization-and-role]] — a role that belongs to an organization
