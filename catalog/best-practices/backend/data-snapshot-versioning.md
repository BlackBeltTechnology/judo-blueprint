---
id: data-snapshot-versioning
title: Data Snapshot Versioning (Immutable History Records)
description: Before a significant state transition, copy the current child records into a version entity so the state at that moment stays readable later.
aliases: [snapshot before approval, history copy, version record]
keywords: [snapshot, versioning, history, audit, version entity, child copy, approval]
tags: ["domain:backend", "layer:backend", "project:itracker", "project:indamedia-adtrack", "project:workflow-poc", "status:emerging"]
category: operation
status: emerging
projects: [itracker, indamedia-adtrack, workflow-poc]
evidence: ["itracker:unrecorded", "indamedia-adtrack:unrecorded", "workflow-poc:unrecorded"]
alternatives: [product-versioning-container]
related: [state-lifecycle-operation, builder-pattern-entity-creation, product-versioning-container]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A parent entity owns a set of mutable child records (for example monthly plans). At a significant moment (approval, publication, every change) the owner needs to keep what the data looked like. Copy the children into a version entity with a timestamp and summary values, and never change that copy afterwards.

## Practice

### Copy in the same operation as the transition

The snapshot is plain custom code in a custom operation (or a service it calls). It uses generated DAOs only; the platform has no snapshot feature of its own.

1. Read the parent and its children through the relation query of the DAO. Pass a mask that lists only the fields you copy.
2. Create the version entity through the generated `ForCreate` builder, with the timestamp and the aggregated summary values.
3. Create one copy entity per child, linked to the version. The copies are separate entities with their own identifiers, not references to the live children.
4. Only then change the parent's state.

All of this runs in the transaction of the operation, so an exception in step 4 also rolls back the snapshot. Do not put the snapshot into an `async()` interceptor: it runs outside the transaction and loses its exceptions (see [Interceptors](../../agent-docs/backend/interceptors.md#the-interceptor-contract)).

### Make the history immutable by design

"Immutable" is a convention, not a platform guarantee. Model the version and copy entities without update or delete operations and do not expose them for modification to any actor. Remember that only built-in operations pass interceptors, so a guard that rejects writes to version entities does not cover your own custom operations (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).

### Use one clock for the timestamp

`Timestamp!now()` in model expressions follows the platform parameter `defaultZoneId`, while `LocalDateTime.now()` in custom Java follows the JVM time zone. Take the snapshot timestamp from the same clock that later queries compare it with (see [Time and Time Zones](../../agent-docs/backend/platform-behavior-reference.md#time-and-time-zones) and [[injectable-business-clock]]).

### Decide how summaries are stored

Store the aggregates on the version when readers need them without loading the copies. They duplicate data that could be recomputed, so keep the code that fills them in one place.

## Rationale

- A complete copy makes the historical state cheap to read and to compare with the current one, without replaying changes.
- Doing the copy before the transition, in one transaction, means no version exists for a transition that failed, and no transition without a version.
- Limit: every snapshot is a full copy, so storage grows with each version. There is no delta storage. A mask on the read keeps the copy step from loading unrelated fields.

## Example

Several applications use the idea; names are example code.

- Plan versioning: an `ArchivePlan` operation creates a `PlanVersion` with a timestamp and summed values, and copies each monthly plan into a version copy. `Approve` calls it before setting the status to approved.
- Grouped-item service: writes a `GroupHistory` record on every update (name, dates, budgets, remaining days) for budget audit.
- Workflow example: every upload creates a new `WorkflowVersion` holding states, transitions and roles; the workflow keeps references to its head version and to the published one.

## When to avoid

- A full history of every field change is needed: use an audit log entity that records changes instead.
- The child set is large and snapshots are frequent: store deltas or snapshot only the changed children.
- The versions must be editable drafts that later become live: see [[product-versioning-container]].

## Related

- [[state-lifecycle-operation]] — the transition that triggers the snapshot
- [[builder-pattern-entity-creation]] — creating the version and copies with generated builders
- [[product-versioning-container]] — alternative: a version container that clones whole entities
