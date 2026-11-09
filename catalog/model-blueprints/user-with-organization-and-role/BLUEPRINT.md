---
id: user-with-organization-and-role
title: User Entity with Organization and Role Enum
description: "A User entity with core identity attributes (name, email), a role attribute typed to a UserRole enum, a status attribute typed to a UserStatus enum, and an association to an Organization."
aliases: []
keywords: [user, organization, role, enum]
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

A User entity with core identity attributes (name, email), a role attribute typed to a UserRole enum, a status attribute typed to a UserStatus enum, and an association to an Organization. The user carries notification preference booleans (notifyOffers, notifyRequests, etc.), visibility flags, and maintains relations to Devices and Notifications. The UserRole enum defines platform-level roles (e.g., COMPANY_ADMIN, COMPANY_READER, PLATFORM_ADMIN). The UserStatus enum follows the Active/Suspended/Deactivated tri-state lifecycle.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
