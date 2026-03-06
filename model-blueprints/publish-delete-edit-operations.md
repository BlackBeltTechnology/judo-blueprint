---
id: "publish-delete-edit-operations"
title: "Publish/Delete/Edit Content Operations Pattern"
score: 68.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
---
## Description

A recurring set of instance operations on content transfer objects that implement editorial workflow: `publish` (transitions status from DRAFT to PUBLISHED), `delete` (soft-deletes by setting status to DELETED), and an `edit*` operation (updates content while preserving status). Some content types add `expired` (marks time-sensitive content as EXPIRED) and `moderationDelete` (admin-initiated removal with reason). The transfer objects carry boolean guard attributes like isNotPublisheable, isNotDeletable, isNotExpireble to control UI button visibility based on current state. This operation triple appears on every content-managing transfer object.

## Detection Query

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%News%" } }) {
  items { fqn name
    operations { items { name operationType } }
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{CONTENT_TO}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}", name: "publish",
  operationType: "INSTANCE", binding: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}.publish"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}", name: "delete",
  operationType: "INSTANCE", binding: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}.delete"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}", name: "edit{{CONTENT_TYPE}}",
  operationType: "INSTANCE", binding: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}.edit{{CONTENT_TYPE}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}", name: "isNotPublisheable"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{CONTENT_TO}}", name: "isNotDeletable"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
Content transfer objects in the `companyadmin` service package all follow this pattern:
- **News**: publish, delete, editNews, moderationDelete; guards: isNotPublisheable, isNotDeletable
- **Offer**: publish, delete, editOffer, expired, moderationDelete; guards: isNotPublisheable, isNotDeletable, isNotExpireble
- **Request**: publish, delete, editRequest, expired, moderationDelete; guards: isNotPublisheable, isNotDeletable, isNotExpireble
- **Announcement** (admin service): publish, delete, editAnnouncement; guards: isEditable, isDeletable, isPublishable
- All operations are INSTANCE type, non-custom (generated from model behavior)
