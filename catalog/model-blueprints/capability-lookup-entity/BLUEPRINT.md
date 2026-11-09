---
id: capability-lookup-entity
title: Capability/Tag Lookup Entity
description: A Capability (or Tag/Category) entity that serves as a reusable lookup/classification entity.
aliases: []
keywords: [capability, tag, lookup]
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

A Capability (or Tag/Category) entity that serves as a reusable lookup/classification entity. It has a name, optional description, and an isActive boolean flag (default: true) for soft-enabling/disabling. Multiple entities reference it via many-to-many ASSOCIATION relations (e.g., Organization has capabilities, Offer has capabilities, Request has capabilities). This provides a flexible tagging system where platform admins can create and manage capabilities, and other entities can be associated with any combination of them. The transfer object exposes an activateToggle operation for toggling the isActive flag.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
