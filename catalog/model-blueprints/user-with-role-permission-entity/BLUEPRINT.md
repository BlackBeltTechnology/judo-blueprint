---
id: user-with-role-permission-entity
title: User Entity with Role and Permission Entities
description: "A User entity with core identity attributes (name, email) and an association to Role entities (many-to-many)."
aliases: []
keywords: [user, role, permission, entities]
tags: ["domain:model", "layer:model", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A User entity with core identity attributes (name, email) and an association to Role entities (many-to-many). Each Role has a name and a permissions relation (0..*) to Permission entities. Permissions are represented as entities (rather than enum members directly) with a flag attribute typed to a PermissionFlag enum. The PermissionFlag enum lists all controllable areas of the application (e.g., PARTNERS, USERS, ROLES, COMPANY_DATA, CONFIGURATION). The User entity carries denormalized boolean attributes for each permission (permissionToPartners, permissionToUsers, etc., all default: false) so that access control can be checked without traversing relations. A `recalculatePermissions` operation updates these denormalized booleans from the role/permission graph.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
