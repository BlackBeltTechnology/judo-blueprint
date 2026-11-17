---
id: user-with-boolean-role-flags
title: User with Boolean Role Flags
description: A User entity that stores one required boolean flag per role instead of a role enumeration or a role entity, so each role check is a plain attribute read.
aliases: [role flags on user, boolean roles]
keywords: [user, boolean, role, flags, permission, enum]
tags: [domain:model, layer:model, project:InterfaceRegister, project:skillmatrix-model, status:emerging]
category: pattern
status: emerging
projects: [InterfaceRegister, skillmatrix-model]
evidence: ["InterfaceRegister:unrecorded", "skillmatrix-model:unrecorded"]
alternatives: [user-with-organization-and-role]
related: [user-with-organization-and-role]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give each user an explicit yes or no for every role, and keep the role check to a single attribute read. A small, fixed set of roles does not need a role entity or an enumeration with relations.

### Each role is a required boolean

Every role has its own required flag. Creating a user forces a decision for each role. A missing role is never silently treated as a grant.

### Trade flexibility for directness

A new role needs a schema change, because the flags are part of the entity. This is the cost. The benefit is that every check is a boolean read, with no relation traversal or enumeration comparison.

## Structure

The User entity has identity attributes (first name, last name, email as the identifier, optional phone) and a created timestamp. It has one required boolean per role, for example admin, enterprise architect, developer and operator. There are no role relations and no role enumeration. Input transfer objects can rename the flags (for example, to a "has access" form) so that the input reads clearly. A dashboard transfer object can map the same user for a landing page.

## Constraints

- Every role flag is required. A user is created with an explicit value for each flag.
- Role checks read the flag directly. They do not compare against a list of roles. In expressions, a managed mapped principal exposes the flag under the `ACTOR` category, see [Role flags on the principal entity](../../agent-docs/model/advanced-modeling-patterns.md#pattern-role-flags-on-the-principal-entity).
- Renamed input flags must map one-to-one onto the entity flags. Each rename is a field on the input, not a new role.
- Adding a role changes the entity and its input and output transfer objects.
- Interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)), so any rule about who may change a flag must be in the operation that changes it, or in the access that exposes the flag (an update access limited to administrators).

## Variations

- **Active state in the flag name.** Flags named like `isActive<Role>` record both the role assignment and whether it is currently active. A derived attribute can then report a user with no active role.
- **Actor per role.** When each role authenticates as its own actor, each actor type reads its flag in the actor's guard expression (`isActiveExpression` in the ESM metamodel, `guard` in JSL), which decides whether that actor may sign in ([ActorType](../../agent-docs/model/esm_metamodel/accesspoint.md#actortype)). A single user can then hold several actor types.
- **Role entity instead.** When roles must be added by administrators without a release, use a role entity with an association. See [[user-with-organization-and-role]] for an alternative that ties the user to an organization and a role.

## When to use

- The set of roles is small, fixed and unlikely to change often.
- Role checks happen often, and each check should be a simple read.
- A user may hold several roles at once.

## When to avoid

- Roles must be created or renamed by administrators at run time. Use a role entity.
- Roles carry their own permissions or data. Model the role as an entity.
- Users belong to organizations that each define their own roles. See [[user-with-organization-and-role]].

## Related

- [[user-with-organization-and-role]] — a user with a role that depends on an organization
