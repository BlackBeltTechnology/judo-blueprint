---
id: content-lifecycle-status-enum
title: Content Lifecycle Status Enum (Draft/Published/Deleted)
description: "A status enumeration for content entities that follow a publishing lifecycle: DRAFT (initial creation), PUBLISHED (visible to audience), and DELETED (soft-removed)."
aliases: []
keywords: [content, lifecycle, status, enum, draft, published, deleted]
tags: ["domain:model", "layer:model", "layer:backend", "project:mlszksz-platform", "status:single-project"]
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

A status enumeration for content entities that follow a publishing lifecycle: DRAFT (initial creation), PUBLISHED (visible to audience), and DELETED (soft-removed). Some variants add EXPIRED (time-based content) and PENDING_REVIEW (moderation). The corresponding transfer objects expose publish, delete, and edit operations. This pattern appears on any entity that represents user-authored content needing editorial workflow.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
