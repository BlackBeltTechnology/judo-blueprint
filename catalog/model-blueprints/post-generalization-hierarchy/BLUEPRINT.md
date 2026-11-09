---
id: post-generalization-hierarchy
title: Abstract Post with Concrete Content Subtypes
description: "An abstract Post base entity with common content attributes (title, description, status, createdAt, publishedAt, postType) and relations (author -> User, organization -> Organization, inquiries -> Inquiry via composition)."
aliases: []
keywords: [abstract, post, concrete, content, subtypes, generalization, hierarchy]
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

An abstract Post base entity with common content attributes (title, description, status, createdAt, publishedAt, postType) and relations (author -> User, organization -> Organization, inquiries -> Inquiry via composition). Concrete subtypes extend Post via generalization: News (adds image), Offer (adds validFrom, validUntil, price, isExpired, capabilities), Request (adds deadline, isExpired, capabilities), and Announcement (adds isSensitive, isStrategic, documents). Each subtype carries its own specific attributes while inheriting the common publishing lifecycle. The PostStatus enum (DRAFT, PUBLISHED, EXPIRED, DELETED, PENDING_REVIEW) and PostType enum (NEWS, OFFER, REQUEST, ANNOUNCEMENT) provide state and type discrimination.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
