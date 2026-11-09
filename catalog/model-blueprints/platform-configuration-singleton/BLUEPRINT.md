---
id: platform-configuration-singleton
title: Platform Configuration Singleton Entity
description: A singleton Configuration entity that stores platform-wide settings.
aliases: []
keywords: [platform, configuration, singleton]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:mlszksz-platform", "project:rackinspect", "project:park-here", "status:emerging"]
category: pattern
status: emerging
projects: [mlszksz-platform, rackinspect, park-here]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A singleton Configuration entity that stores platform-wide settings. It is updateable but not createable or deleteable (exactly one instance exists, seeded at initialization). Typical attributes include email sender address (senderEmail), base URL, platform name, and various configurable parameters like expiry durations (invitationExpiryDays, verificationExpiryMinutes). It also holds email templates as text fields (invitationEmailTemplate, verificationEmailTemplate, approvalEmailTemplate). The configuration is exposed via a transfer object with an updateConfiguration operation. Some variants store document templates as binary fields and business-specific settings (margin percentages, closing times). Other variants are fully non-CRUD (all flags false) where updates go through custom operations or are admin-managed.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
