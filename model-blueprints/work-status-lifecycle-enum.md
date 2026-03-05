---
id: work-status-lifecycle-enum
title: "Work Status Lifecycle Enum (Not Started/In Progress/Done/Won't Fix)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---

## Description

A four-state work/task lifecycle enumeration with members: NOT_STARTED, IN_PROGRESS, DONE, and WONT_FIX. This models entities that track repair or maintenance work items: they begin as NOT_STARTED, transition to IN_PROGRESS when work begins, and end at either DONE (completed) or WONT_FIX (abandoned/deferred). The WONT_FIX terminal state distinguishes this from simpler lifecycle enums by acknowledging that not all work items reach completion. Used by both JobSheet and WorkReport entities as their workStatus attribute.

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%WorkStatus%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "WorkStatus"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "IN_PROGRESS", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "DONE", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "WONT_FIX", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::WorkStatus", name: "NOT_STARTED", ordinal: 4
} }) { success fqn } }
```

## Examples

### rackinspect
- **Enum**: `rackinspect::entities::WorkStatus` -- IN_PROGRESS(1), DONE(2), WONT_FIX(3), NOT_STARTED(4)
- **JobSheet entity**: `rackinspect::entities::JobSheet` -- workStatus (req, default: IN_PROGRESS)
  - Relations: jobSheetItem (0..* COMPOSITION), workReport (0..1 ASSOC), offer (1..1 ASSOC), jobTaskFinishedDocuments (0..1 COMPOSITION)
  - Generalizes from a base document entity
- **WorkReport entity**: `rackinspect::entities::WorkReport` -- workStatus (req, default: IN_PROGRESS), startTime, endTime, numberOfWorkers
  - Relations: jobSheet (1..1 ASSOC), finishedJobSheetItems (0..* ASSOC), signedWorkReportDocument (0..1 COMPOSITION)
  - Generalizes from a base document entity
