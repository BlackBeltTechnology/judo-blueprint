---
id: "token-based-verification-entity"
title: "Token-Based Verification Entity"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

An entity that implements a token-based verification workflow with attributes: a verification/invitation token (string), an expiration timestamp (verificationExpiresAt or expiresAt), a verified-at timestamp (verifiedAt), and a status enum following the PENDING -> VERIFIED -> APPROVED/REJECTED lifecycle. This pattern supports email verification, invitation acceptance, and registration approval flows. The entity is typically non-CRUD (created only through custom operations) and carries a rejectionReason for denied requests. A corresponding status enum has members: PENDING, VERIFIED, APPROVED, REJECTED, EXPIRED.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
