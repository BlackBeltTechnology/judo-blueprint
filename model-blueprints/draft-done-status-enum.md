---
id: draft-done-status-enum
title: "Draft/Done Two-State Workflow Enum"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---

## Description

A minimal two-state status enumeration with DRAFT and DONE members, representing the simplest possible workflow: an item starts in DRAFT (being prepared), then transitions to DONE (finalized/completed). This is used for document-producing processes like fault registries and offers where the document is first assembled and then finalized. Unlike content lifecycle enums (DRAFT/PUBLISHED/DELETED), this pattern has no soft-delete state -- the entity is either in-progress or completed.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with exactly two members: DRAFT and DONE.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DRAFT", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DONE", ordinal: 2
} }) { success fqn } }
```

## Examples

### rackinspect
- **FaultRegistryStatus**: `rackinspect::entities::FaultRegistryStatus` -- DRAFT(1), DONE(2)
  - Used by: FaultRegistry entity (status attribute, default: DRAFT)
  - FaultRegistry transitions from DRAFT to DONE when the fault inspection is completed
- **OfferStatus**: `rackinspect::entities::OfferStatus` -- DRAFT(1), DONE(2)
  - Used by: Offer entity (status attribute)
  - Offer transitions from DRAFT to DONE when the pricing offer is finalized
