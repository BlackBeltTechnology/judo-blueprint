---
id: "bulk-json-upload-entity"
title: "Bulk JSON Upload Entity with Question/Data Import"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

An Upload entity that records bulk data imports via JSON. The entity captures the raw JSON payload, a timestamp of when the upload occurred, and a count of how many items were imported. It maintains an association (0..*) to the entities that were created from the upload, providing traceability from imported items back to their source batch.

The transfer object layer provides:
- A **JsonData** unmapped TO with a single `json` attribute, used as the input parameter for the upload operation
- An **Upload** mapped TO showing the upload metadata and the imported items via an aggregation relation
- The upload operation is a STATIC operation on the target entity's transfer object (e.g., Question.upload)

A companion **download** STATIC operation exports the same data back as JSON, completing a round-trip import/export cycle.

This pattern is suitable for applications that need batch data ingestion from external sources (e.g., importing quiz questions, product catalogs, reference data) while maintaining audit trail of which import batch produced each record.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Upload" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { eq: "JsonData" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

## Creation Mutations

### Upload entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Upload",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Upload", name: "json"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Upload", name: "timestampOfUpload"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Upload", name: "nrOfUploadedQuestions"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Upload", name: "{{ITEMS_RELATION}}",
  target: "{{NAMESPACE}}::{{ITEM_ENTITY}}", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### JsonData input TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "JsonData"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::JsonData", name: "json"
} }) { success fqn } }
```

### Upload/Download operations on target TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{TARGET_TO}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{TARGET_TO}}", name: "upload",
  operationType: "STATIC", binding: "{{SERVICE_NAMESPACE}}::{{TARGET_TO}}.upload"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{TARGET_TO}}", name: "download",
  operationType: "STATIC", binding: "{{SERVICE_NAMESPACE}}::{{TARGET_TO}}.download"
} }) { success fqn } }
```

## Examples

### trivia
- **Upload entity** (`trivia::entities::Upload`): non-CRUD
  - Attributes: json (req), timestampOfUpload (req, default: Timestamp!now()), nrOfUploadedQuestions (req)
  - Relations: questions (0..* ASSOC to Question)
  - Each upload records the raw JSON, when it happened, and how many questions were created
- **Question entity** has a back-reference: upload (0..1 ASSOC to Upload)
  - Allows querying which upload batch a specific question came from
- **Admin JsonData TO** (`trivia::actors::admin::JsonData`): unmapped
  - Attributes: json (req)
  - Used as input parameter for the Question.upload operation
- **Admin Upload TO** (`trivia::actors::admin::Upload`): mapped
  - Attributes: json, timestampOfCreation, nrOfUploadedQuestions -- all optional in the TO view
  - Relations: question (0..* AGGREGATION to Question) -- shows uploaded questions
- **Admin Question TO** (`trivia::actors::admin::Question`):
  - Operations: upload (STATIC) -- takes JsonData input, parses JSON, creates questions
  - Operations: download (STATIC) -- exports questions as JSON
  - The upload operation creates an Upload record, parses the JSON, creates Question entities, sets the upload back-reference on each question, and records the count
