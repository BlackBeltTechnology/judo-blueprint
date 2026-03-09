---
id: "user-with-organization-and-role"
title: "User Entity with Organization and Role Enum"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A User entity with core identity attributes (name, email), a role attribute typed to a UserRole enum, a status attribute typed to a UserStatus enum, and an association to an Organization. The user carries notification preference booleans (notifyOffers, notifyRequests, etc.), visibility flags, and maintains relations to Devices and Notifications. The UserRole enum defines platform-level roles (e.g., COMPANY_ADMIN, COMPANY_READER, PLATFORM_ADMIN). The UserStatus enum follows the Active/Suspended/Deactivated tri-state lifecycle.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
