---
id: "organization-entity"
title: "Organization Entity with Contact Info and Membership"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

An Organization entity representing a company or group in a multi-tenant platform. It has a name, contact information (contactEmail, contactName, contactPhone), a status enum (ACTIVE/SUSPENDED/DEACTIVATED), an address via composition, a logo (binary), membership metadata (membershipStart, membershipDescription), and associations to users, capabilities, posts, and invitations. The OrganizationStatus enum follows the same tri-state lifecycle as UserStatus. Denormalized fields like cityName and fullAddress provide quick display without joins. A userCount attribute and isUserCountHidden flag support privacy controls.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
