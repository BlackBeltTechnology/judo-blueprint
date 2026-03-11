---
id: "user-with-role-and-rolegroup-entities"
title: "User Entity with Role and RoleGroup Entities (Hierarchical Role Assignment)"
score: 33.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - sanctuary-backend
---
## Description

A User entity with identity and profile attributes, associated to Role entities via a bidirectional many-to-many relation, and to RoleGroup entities via a separate bidirectional many-to-many relation. RoleGroups aggregate multiple Roles into named collections, enabling bulk role assignment. This provides a two-level role hierarchy: individual roles can be assigned directly to users, and role groups can be assigned to users to grant all roles within the group at once.

The core entities are:

- **User** -- an identity with personal details (email, firstName, lastName), profile attributes (profilePhoto, sex), a status attribute (active/archived enum), and contact information (phoneNumber). The User has composed settings entities (UserPrivacySettings, UserSettings) for user preferences, and a derived `effectiveRoles` relation that computes the aggregate set of roles from direct assignments and role group memberships.
- **Role** -- a named role entity with a bidirectional association to Users. Roles represent individual permission sets or functional access levels.
- **RoleGroup** -- a named group that aggregates multiple Roles (one-way association to Role) and has a bidirectional association to Users. RoleGroups enable batch role assignment by collecting related roles under a single group name.
- **PositionTitle** -- a reference data entity representing a user's job title, with a title attribute and status (active/archived). Users have an optional association to a PositionTitle.
- **UserPrivacySettings** -- a composition child of User that controls visibility of user data fields (phoneNumber, peerBadges, specialBadges, systemBadges) using a PrivacyVisibility enum with granular levels (publicForPeers, publicForTeam, publicForUnit, publicForEveryone).
- **UserSettings** -- a composition child of User for UI preferences (e.g., darkMode boolean).

Key structural patterns:
- Bidirectional many-to-many between User and Role, and between User and RoleGroup
- RoleGroup has a one-way association to Roles (groups contain roles but roles do not back-reference groups)
- Derived `effectiveRoles` relation on User aggregates roles from direct assignment and group membership
- Composition pattern for user settings/preferences (User owns UserPrivacySettings and UserSettings)
- PrivacyVisibility enum for per-field visibility control

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
