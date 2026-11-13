---
id: user-with-organization-and-role
title: User with Organization and Role Enumeration
description: A User entity with identity attributes, a required role typed to a role enumeration, a required status, and a required association to one Organization. The role applies to that organization.
aliases: [organization user with role enum]
keywords: [user, organization, role, enum, status]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [user-with-boolean-role-flags, identity-account-organization-cluster]
related: [organization-entity, identity-account-organization-cluster, user-with-boolean-role-flags]
fragment: user-with-organization-and-role
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Tie each user to one organization, with a role that is meaningful inside that organization. A small fixed set of roles is stored as an enumeration, and the organization is a required association.

### The role belongs to the organization

A role such as owner or member describes what the user may do in its organization. The association to the organization is required, so every user has exactly one organization. The enumeration gives the set of roles a fixed meaning in the model.

### A separate access record is the stronger option when accounts can span organizations

When one account can belong to several organizations with a different role in each, the role must sit on an access record between the account and the organization, not on the user. The identity-account cluster uses this structure.

## Structure

The User entity has a name, an email as the identifier, a required role (UserRole enumeration with its members), and a required association to one Organization. The Organization entity is a separate entity. The example in this entry also keeps a required status enumeration and some optional notification flags, which are project specific.

## Constraints

- The organization association is required. A user is always inside one organization.
- The role must be one of the enumeration members. An unknown role value is a validation error, not a default.
- A role check that is about the organization must read the role of the user in that organization, not a global role.
- If one account can join several organizations, do not keep the role on the user. Use an access record (see [[identity-account-organization-cluster]]).
- Interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)), so role-changing rules must be in the operation.

## Variations

- **Role on the user.** One organization per user, and a role that is fixed for that user. This is the example in this entry.
- **Role on an access record.** Several organizations per account, each with its own role. See [[identity-account-organization-cluster]].
- **Role as flags.** When the roles are few and checked often, use one boolean per role instead of an enumeration. See [[user-with-boolean-role-flags]].

## When to use

- Each user belongs to exactly one organization.
- The set of roles is fixed and small, and it is the same for every organization.
- Role checks need the organization as context.

## When to avoid

- A user may belong to several organizations with different roles. Use an access record.
- Roles differ per organization or are created by administrators. Use a role entity.

## Related

- [[organization-entity]] — the organization the user belongs to
- [[identity-account-organization-cluster]] — the same question with roles on an access record
- [[user-with-boolean-role-flags]] — roles as flags on the user
