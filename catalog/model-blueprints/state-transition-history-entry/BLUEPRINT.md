---
id: state-transition-history-entry
title: State Transition History Entry Entity
description: "An append-only entry composed by a stateful parent that records each state change: previous state, new state, time, optional message and the user who did it."
aliases: []
keywords: [state, transition, history, entry]
tags: ["domain:model", "layer:model", "project:judo-demo-miniworkflow", "status:single-project"]
category: pattern
status: single-project
projects: [judo-demo-miniworkflow]
evidence: ["judo-demo-miniworkflow:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Record every state change of an entity that has an enumeration-based state. Each change becomes one entry with the old state, the new state, the time, an optional message and the user who made the change. The entries give a complete, ordered path through the state machine.

### Structured states instead of text

Unlike a plain history row with free-text actor and action, the entry stores the two states as enumeration values. The path through the state machine can be rebuilt and filtered. The user is a real association, not a name string.

### The entry is composed by its parent

Entries belong to one parent and are deleted with it. The parent shows its entries as a read-only timeline.

## Structure

An entry entity with: `fromState` (the enumeration of the parent, optional because the first entry has no previous state), `toState` (required), `eventTime` (required timestamp), `message` (optional text, such as a rejection reason) and a `user` relation (association, exactly one) to the user entity.

The parent entity composes entries through a 0..* composition relation. A transfer object for the parent exposes the entries as a read-only list. A transfer object for the entry may carry a derived `userRepresentation` string, so the table shows the user name without loading the user.

## Constraints

- The entry entity has its create, update and delete flags off. Nothing generated can write it ([CRUD flags](../../agent-docs/model/README.md#crud-flags)); the parent's custom state-changing operations create the entry.
- Interceptors do not fire for custom operations, so the entry is written by the operation itself, in the same call as the state change ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Writing the state and the entry in one operation keeps them consistent.
- `toState` and `eventTime` are required. `fromState` is empty only on the first entry.
- The user comes from the caller's identity. Resolving the user entity from the signed-in principal is project code (an actor or user service), not a platform feature.
- Entries are never edited. A correction is a new entry.

## Variations

- **Message from an input object.** A reject operation takes a small input transfer object with a reason. The operation copies it into `message`.
- **Without a user relation.** Store the user name as text if users can be deleted. See [[history-audit-trail-entity]].
- **Shared log.** One audit entity for all parents instead of an entry per parent. See [[audit-log-entity]].
- **Derived current state.** Derive the current state from the latest entry instead of storing it on the parent. See [[derived-state-from-history]].

## When to use

- The parent has an enumeration-based state machine and each transition must be auditable.
- Reviewers need to see who moved the entity to which state and why.
- The history is read on the parent's detail page.

## When to avoid

- A free-text log of events is enough. Use [[history-audit-trail-entity]].
- Transitions of many entity types need one shared table. Use [[audit-log-entity]].
- Changes to ordinary attributes must be tracked. Use [[entity-change-history-snapshot]].

## Related

- [[document-review-state-machine]] — the state machine whose transitions this entry records
- [[enum-state-machine]] — the enumeration-based state practice
- [[history-audit-trail-entity]] — simpler text-based history
- [[audit-log-entity]] — shared audit table
- [[derived-state-from-history]] — current state computed from the entries
- [[composition-ownership]] — why entries are deleted with the parent
