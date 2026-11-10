---
id: task-list-with-checkout-release
title: Task List with Checkout and Release
description: A task list transfer object over a pool of work items, where a user claims an unassigned item with checkout, returns it with release, and sees the list split into my tasks and all tasks.
aliases: [checkout release task list, claimable task pool]
keywords: [task, list, checkout, release, assignment, claim, pool]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:workflow-poc, status:single-project]
category: pattern
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: [task-entity-with-assignment]
related: [workflow-engine-state-machine-cluster, task-entity-with-assignment]
fragment: task-list-with-checkout-release
diagram: { kinds: [entity, transfer, operation], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let a team work from a shared pool of tasks. Unassigned items sit in the pool. A user claims one with checkout, works on it, and either finishes it or returns it with release. The list shows the user's own items separately from the full pool, so the next action is easy to find.

### Unassigned work sits in a shared pool

An item with no assignee is visible to every user who may act on it. Claiming it is an explicit action, so two users cannot both take the same item.

### The list is a view, not the storage

The task list and the task are transfer objects over existing entities. The list counts and filters the items. The task exposes the operations and the guard flags that decide which buttons are available.

## Structure

The model has a Task transfer object mapped to the Token entity and a TaskList transfer object mapped to the User entity. Task has display attributes, boolean guard attributes (for example whether the current user is the assignee), and mapped operations for checkout, release and execute. TaskList has count attributes and a relation to the user's own tasks. The Token entity owns the assignee and status attributes. A LogEntry entity records who completed each step.

## Constraints

- Checkout is allowed only on an unassigned item. Release is allowed only for the current assignee.
- Each mapped operation on Task must bind to an operation of the same name on Token. The binding is the operation name, not an FQN.
- Guard attributes control which operations are shown. They do not replace checks inside the operation.
- Interceptors do not run for custom operations. A check that must hold on checkout or release has to be in the operation.
- Operations that change state must be in the transaction that writes the log entry, so a failed transition does not leave a log row behind.

## Variations

- **Pool with preference.** When an item is returned to the pool, the next assignee can be chosen from the completion history. This keeps work with the user who last touched it. The example project does this in its shared workflow utilities.
- **Assign by a supervisor.** A supervisor can assign an item to a named user. This adds an assign operation with its own guard. Use it only when managers must direct work.
- **Pool without release.** If items never return to the pool, drop the release operation and keep checkout only.

## When to use

- Several people draw from one pool, and each item needs one owner at a time.
- The list needs separate counts for my items and the pool.
- Items move through workflow steps driven by an engine.

## When to avoid

- Each task has a fixed, known assignee from the start. Use [[task-entity-with-assignment]].
- The work is a single approval with a fixed set of states. A plain entity with a state enumeration is simpler.
- Items must be claimed by a system process, not by users. The pool and the guard flags have no meaning there.

## Related

- [[workflow-engine-state-machine-cluster]] — the workflow engine that produces the tokens this list shows
- [[task-entity-with-assignment]] — a task with a fixed assignee, without a pool
