---
id: identity-account-organization-cluster
title: Identity, Account and Organization Cluster
description: "An entity cluster for multi-tenant identity: one identity per person, platform accounts and organization-scoped users linked to it, and organization accesses with owner or admin roles."
aliases: []
keywords: [identity, account, organization, multi-tenant, access, cluster]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:ubives, status:single-project]
category: pattern
status: single-project
projects: [ubives]
evidence: ["ubives:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let one person sign in once and take part in several organizations. The identity is the single root for a person. Accounts and organization-scoped users hang off it, and organization accesses say which organization each account manages and in what role.

### One identity, many contexts

The identity holds the person's email. It links to any number of accounts, which are platform-level contexts, and to any number of organization-scoped users. Each link is a separate record, so one person can belong to many organizations without duplicating the identity.

### Roles live on the access, not the account

An organization access records one account's role in one organization (owner or admin). The account itself carries no organization role, so the same account can be an owner in one organization and an admin in another.

## Structure

The identity entity has a required email. It is associated with zero or more accounts, zero or more organization-scoped users and zero or more face identifiers.

The account entity has a required user name and email, a super-admin flag and a single-organization flag, both with defaults. It is linked to exactly one identity and composes zero or more organization accesses.

The organization-scoped user has a required user name and email and an enabled flag with a default. It is linked to exactly one identity.

The organization entity has a required name, a registration-feature flag with a default and an optional realm name. It composes applications, invitations, users and at most one realm. It is also associated with the organization accesses that point to it.

The organization access has a required enabled flag with a default and a required role, one of the two members of the organization access type enumeration. It is linked to exactly one organization and, through the account, to one account.

The organization access type enumeration has two members: OWNER and ADMIN.

## Constraints

- The identity email, the account user name and email, and the organization-scoped user's user name and email are required.
- Each account and each organization-scoped user links to exactly one identity.
- The organization access role must be one of the enumeration members.
- An organization composes its applications, invitations, users and realm. Removing the organization removes those records with it.
- Guard flags on the account (super-admin, single-organization) control what the interface shows. They do not grant access by themselves.

## Variations

- **Account as the organization role holder.** Store the role on the account and keep one account per organization. This is simpler but duplicates the person's accounts across organizations.
- **One user per identity.** Drop the account entity and use only organization-scoped users. This fits products with no platform-level context.
- **Shared realm for all organizations.** Put every organization's users in one realm. See [[idm-realm-keycloak-integration]] for per-organization realms.

## When to use

- One person must sign in once and work in several organizations.
- Organization owners and admins must be managed separately from ordinary users.
- Each organization has its own applications, invitations and users.

## When to avoid

- Every person belongs to exactly one organization and the account and user are the same record.
- The system has no organization concept.
- Roles must be a free set of permissions rather than the owner and admin levels.

## Related

- [[idm-realm-keycloak-integration]]: the identity server and per-organization realms that these records use
- [[capacity-reservation-cluster]]: a domain cluster whose partners and users link to organizations
- [[audit-log-entity]]: recording who changed an organization access
