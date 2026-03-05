---
id: content-lifecycle-status-enum
title: "Content Lifecycle Status Enum (Draft/Published/Deleted)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---

## Description

A status enumeration for content entities that follow a publishing lifecycle: DRAFT (initial creation), PUBLISHED (visible to audience), and DELETED (soft-removed). Some variants add EXPIRED (time-based content) and PENDING_REVIEW (moderation). The corresponding transfer objects expose publish, delete, and edit operations. This pattern appears on any entity that represents user-authored content needing editorial workflow.

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%Status%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{TYPES_NAMESPACE}}", name: "{{CONTENT_TYPE}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{CONTENT_TYPE}}Status", name: "DRAFT", ordinal: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{CONTENT_TYPE}}Status", name: "PUBLISHED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{TYPES_NAMESPACE}}::{{CONTENT_TYPE}}Status", name: "DELETED", ordinal: 2
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **PostStatus**: `MLSZKSZPlatform::types::PostStatus` -- DRAFT(0), PUBLISHED(1), EXPIRED(2), DELETED(3), PENDING_REVIEW(4)
- **AnnouncementStatus**: `MLSZKSZPlatform::types::AnnouncementStatus` -- DRAFT(0), PUBLISHED(1), DELETED(2)
- Both share the DRAFT->PUBLISHED->DELETED core lifecycle
- PostStatus extends with EXPIRED and PENDING_REVIEW for moderated content
- Transfer objects (News, Offer, Request, Announcement) expose publish/delete/edit operations
