---
id: timed-attempt-lifecycle-entity
title: Timed Attempt Lifecycle Entity with Status Tracking
description: An Attempt entity that records one participant's run through a timed activity, with a status enumeration from creation to completion, failure or exclusion and a timestamp per stage.
aliases: [test-attempt-lifecycle-entity, test attempt, timed attempt]
keywords: [attempt, lifecycle, status, timestamps, timed]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:trivia, status:single-project]
category: pattern
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: [work-status-lifecycle-enum, ongoing-finished-deleted-status-enum]
related: [ranking-personal-best-pattern, accept-reject-operations, work-status-lifecycle-enum, ongoing-finished-deleted-status-enum]
fragment: timed-attempt-lifecycle-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Record one participant's run through a timed activity, from the moment the attempt is created to the moment it is finished, failed or removed by an administrator. The status enumeration says where the run is. Each stage has its own timestamp, so the duration can be computed exactly.

### Each stage has its own timestamp

Creation, start and finish are stored as separate timestamps. A single created or updated pair cannot give the exact duration of the timed part.

### Operations move the status, not the caller

Start, submit and exclude are custom operations that check the current status before they change it. The status is the only source of truth for which step is allowed.

## Structure

The Attempt entity has a required status (AttemptStatus enumeration, default Created), three timestamps (creation, start, finish), a score, a personal-best flag (default false), and a required link to its Participant. It has a required link to a Session (the timed activity) and a list of Item entities, one per question or step. The AttemptStatus enumeration lists Created, Started, Finished, Failed and Excluded.

## Constraints

- A new attempt starts in the Created status.
- Start is allowed only from Created. Submit is allowed only from Started. Exclude is allowed from any status.
- Custom operations must check the status themselves. Interceptors do not run for custom operations, so an interceptor cannot enforce these transitions.
- An invalid transition must raise a modeled fault (HTTP 422). A bad field value is a validation exception (HTTP 400).
- The personal-best flag belongs to one attempt per participant and session. Excluding the attempt that holds it must recompute the flag for the remaining attempts.

## Variations

- **Fixed status set.** Five statuses, as in the example. Drop Excluded if administrators never remove attempts.
- **Score and duration stored.** The example stores the score and the duration after finishing. Compute them on read instead if the scoring rule changes often.
- **Shared status enumeration.** Use [[work-status-lifecycle-enum]] or [[ongoing-finished-deleted-status-enum]] when a generic work or time-bounded status fits and the stage timestamps are not needed.

## When to use

- A participant runs a timed activity once or several times, and each run needs its own record.
- The duration must be exact, so each stage needs its own timestamp.
- Administrators must be able to remove a run without deleting it.

## When to avoid

- The record is just the current value of one entity. Use a plain status attribute instead.
- Runs have no time limit and no stages to track. A simpler status enum is enough.
- Runs must be scored by a process that is not part of this model. Keep the scoring outside the entity.

## Related

- [[ranking-personal-best-pattern]]: the personal-best flag and its recomputation on exclude
- [[accept-reject-operations]]: status guards on custom operations, the same rule this entity follows
- [[work-status-lifecycle-enum]]: a generic status enumeration without stage timestamps
- [[ongoing-finished-deleted-status-enum]]: a three-state status for time-bounded entities
