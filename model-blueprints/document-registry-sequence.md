---
id: "document-registry-sequence"
title: "Document Registry Sequence Number Generator"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A DocumentRegistry entity that manages sequential document numbering for different document types. It maintains a prefix (string), financial period boundaries (financialPeriodStart, financialPeriodEnd), a transition period (transitionPeriodStart, transitionPeriodEnd), and a numeric sequence range (startIndex, endIndex, currentIndex). The documentType attribute (typed to a DocumentType enum) identifies which kind of document this registry tracks. Each document type gets its own registry instance so that fault registries, offers, assessment sheets, review reports, job sheets, and work reports each maintain independent sequence counters. The currentIndex is incremented by backend code when a new document is generated.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%DocumentRegistry%" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "DocumentType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DocumentType", name: "{{DOC_TYPE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "DocumentRegistry",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "documentType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "prefix"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "financialPeriodStart"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "financialPeriodEnd"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "startIndex"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "endIndex"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DocumentRegistry", name: "currentIndex"
} }) { success fqn } }
```

## Examples

### rackinspect
- **Entity**: `rackinspect::entities::DocumentRegistry` (non-CRUD)
  - Attributes (9): documentType (req), prefix (req), financialPeriodStart (req), financialPeriodEnd (req), transitionPeriodStart (req), transitionPeriodEnd (req), startIndex (req), endIndex (req), currentIndex
- **DocumentType enum**: `rackinspect::entities::DocumentType` -- WORK_REPORT(1), FAULT_REGISTRY(5), OFFER(6), ASSESSMENT_SHEET(7), REVIEW_REPORT(8), JOB_SHEET(9)
- Each document type has its own DocumentRegistry instance with independent prefix and sequence range
- The currentIndex is incremented by backend operations when generating new numbered documents
