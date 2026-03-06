---
id: "history-audit-trail-entity"
title: "History Audit Trail Entity (Who/What/When)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A minimal History entity that records an audit trail of actions with three attributes: whoDid (the user who performed the action), whatDid (description of the action), and whenDid (timestamp of the action). The entity is non-CRUD and composed by a parent entity (typically a Task or work item) via a history (0..*) composition relation. Unlike the full AuditLog pattern which uses enums and entity references, this is a lightweight, denormalized approach where the actor and action are stored as plain text strings. This is suitable when a simple chronological log of human-readable events is sufficient.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "History" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "History",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whoDid"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whatDid"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::History", name: "whenDid"
} }) { success fqn } }
```

## Examples

### rackinspect
- **Entity**: `rackinspect::entities::History` (non-CRUD)
  - Attributes: whoDid (req), whatDid (req), whenDid (req)
  - No relations on the entity itself
- Composed by Task entity via `history` (0..* COMPOSITION)
- Task entity also has: created (default: now()), modified (default: now()), registryNumber; relations: documents (0..* COMPOSITION to Document), lastDocument (0..1 ASSOC), assignedTo (1..1 ASSOC to User)
- Provides a simple chronological audit log per task without structured enum-based action types
