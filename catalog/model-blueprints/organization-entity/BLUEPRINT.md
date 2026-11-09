---
id: organization-entity
title: Organization Entity with Contact Info and Membership
description: An Organization entity representing a company or group in a multi-tenant platform.
aliases: []
keywords: [organization, contact, info, membership]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

An Organization entity representing a company or group in a multi-tenant platform. It has a name, contact information (contactEmail, contactName, contactPhone), a status enum (ACTIVE/SUSPENDED/DEACTIVATED), an address via composition, a logo (binary), membership metadata (membershipStart, membershipDescription), and associations to users, capabilities, posts, and invitations. The OrganizationStatus enum follows the same tri-state lifecycle as UserStatus. Denormalized fields like cityName and fullAddress provide quick display without joins. A userCount attribute and isUserCountHidden flag support privacy controls.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
