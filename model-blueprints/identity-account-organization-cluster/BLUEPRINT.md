---
id: "identity-account-organization-cluster"
title: "Identity-Account-Organization Multi-Tenant Cluster"
score: 44.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---
## Description

A multi-tier entity cluster for identity and multi-tenant organization management. The structure consists of:

- **IdentityEntity** -- the authentication root, representing a unique person identified by email. An identity links to multiple accounts (different platform contexts) and multiple users (organization-scoped identities), plus optional biometric identifiers (face recognition IDs).
- **AccountEntity** -- a platform-level account with userName, email, and a superAdmin flag. An account links to a single identity (1..1 ASSOCIATION) and composes organization accesses (0..* COMPOSITION) that define which organizations the account can manage and with what role.
- **UserEntity** -- an organization-scoped user with userName, email, and an enabled/disabled flag. Users link back to their identity (1..1 ASSOCIATION) and their owning organization (0..1 DERIVED). Enable/disable operations toggle user access.
- **OrganizationEntity** -- a tenant/workspace entity with a name, a registration feature toggle (isRegistrationFeatureSupported), and compositions for applications, invitations, users, and a realm. Organizations also associate to organization accesses.
- **OrganizationAccessEntity** -- a junction entity connecting accounts to organizations with a type (OWNER/ADMIN enum), an enabled flag, and denormalized userName/organizationName. Operations allow changing access level (changeAccessToAdmin, changeAccessToOwner), enabling/disabling access, and canceling access.

The separation of Identity from Account from User enables a single person to have one identity, multiple platform accounts, and multiple organization-scoped users -- supporting true multi-tenancy where a person can participate in many organizations through a single login.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
