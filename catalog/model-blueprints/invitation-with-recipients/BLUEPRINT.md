---
id: invitation-with-recipients
title: Invitation Entity with Recipient Tracking
description: "An Invitation entity representing a batch invitation with a message, createdAt timestamp, and a createdBy relation to the User who sent it."
aliases: []
keywords: [invitation, recipient, tracking, recipients]
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

An Invitation entity representing a batch invitation with a message, createdAt timestamp, and a createdBy relation to the User who sent it. A recipientCount attribute denormalizes the number of recipients. The Invitation has a one-to-many association to InvitationRecipient entities, each tracking: email address, sentAt timestamp, verificationToken, verificationExpiresAt, and a boolean flag usedForSuccessfulRegistration. The Invitation is owned by an Organization (via composition). This pattern supports bulk user invitations with individual tracking of each recipient's verification status.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
