---
id: "platform-configuration-singleton"
title: "Platform Configuration Singleton Entity"
score: 75.7
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - rackinspect
  - park-here
---
## Description

A singleton Configuration entity that stores platform-wide settings. It is updateable but not createable or deleteable (exactly one instance exists, seeded at initialization). Typical attributes include email sender address (senderEmail), base URL, platform name, and various configurable parameters like expiry durations (invitationExpiryDays, verificationExpiryMinutes). It also holds email templates as text fields (invitationEmailTemplate, verificationEmailTemplate, approvalEmailTemplate). The configuration is exposed via a transfer object with an updateConfiguration operation. Some variants store document templates as binary fields and business-specific settings (margin percentages, closing times). Other variants are fully non-CRUD (all flags false) where updates go through custom operations or are admin-managed.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
