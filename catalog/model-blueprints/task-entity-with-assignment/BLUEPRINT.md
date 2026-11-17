---
id: task-entity-with-assignment
title: Task Entity with Assignment, Type and State Enums
description: A Task entity with a creator, an assignee and a target entity, typed by an enumeration and closed by a custom operation, for approval or review work that lives inside a domain model.
aliases: [assignable task, approval task]
keywords: [task, assignee, type, state, enumeration, assignment, approval]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:alba, status:single-project]
category: pattern
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: []
related: [task-list-with-checkout-release, accept-reject-operations, toggle-active-operation]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model work items that one user creates and another user must complete, such as an approval or a review, as plain domain entities. The task has a type, a state and an assignee. It is created as a side effect of a domain operation, not from a generic workflow engine.

### Task is a domain entity, not a workflow token

The task carries its own type and state enumerations. There is no state machine engine and no generic process definition. The domain operation that needs the approval decides when tasks are created.

### Each task has a creator, an assignee and a target

The creator and the assignee are both required links to User. The target is an optional link to the entity the task is about, so one task can be listed from the user side and from the target side.

## Structure

The Task entity has a required creation timestamp, a required type (TaskType enumeration), a required state (TaskState enumeration) and an active flag that defaults to false. It has two required links to User (created by, and assignee) and an optional link to a target entity (Product in the example). The User entity gets the reverse links automatically. The TaskType enumeration lists the kinds of work. The TaskState enumeration lists the progress values.

## Constraints

- The creator and the assignee are required. A task without either cannot be stored.
- The state and the type must be values of their enumerations.
- The active flag defaults to false. Visibility rules are a separate concern handled by the operations that set the flag.
- Interceptors do not run for custom operations. Any check that must hold when a task is closed (for example, that the result is not the initial state) has to live in the custom operation or in the service it calls.
- Built-in operations on the entity can be guarded by interceptors, but only with the exception type `InterceptorCallBusinessException`.

## Variations

- **Created inside a domain operation.** A domain operation (for example, one that starts an approval) creates one task per selected assignee. The task is linked to the domain entity as its target. This is the example project's approach.
- **Role-specific task views.** Separate transfer objects expose the same task to the author, the approver and the administrator. Each view shows only the operations that role may use. Use this when different roles need different actions on one task.
- **Result input transfer object.** A transfer object carries the chosen result (a TaskState value) into the close operation. The example also filters the value list in the form so the initial state cannot be chosen.

## When to use

- A user must complete work that another user assigned, and the work has a small, fixed set of types and states.
- The task is a side effect of one domain operation and does not need its own process definition.
- Several roles need different views of the same task.

## When to avoid

- The work needs several steps with guards, timers or parallel branches. Use a workflow engine instead, see [[workflow-engine-state-machine-cluster]].
- Tasks must be checked out, released and handed over between users. See [[task-list-with-checkout-release]].
- The status of the target must be changed only through accept or reject steps. See [[accept-reject-operations]] for the guard pattern.

## Related

- [[task-list-with-checkout-release]] — a task list with checkout and release, for a pool of work instead of a fixed assignee
- [[accept-reject-operations]] — guards for accept and reject steps on a target entity
- [[toggle-active-operation]] — the active flag that this entity sets and clears
- [[workflow-engine-state-machine-cluster]] — the workflow engine alternative for multi-step processes
- [[audit-log-entity]] — records who created and closed a task
