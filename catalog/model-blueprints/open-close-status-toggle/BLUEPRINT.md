---
id: open-close-status-toggle
title: Open/Close Two-State Status Toggle with Operations
description: "A two-state status enumeration (OPEN and CLOSED) on an entity, changed by open and close instance operations, for availability windows that an admin can turn on and off."
aliases: [open close toggle, availability window]
keywords: [open, close, two-state, status, toggle, operations, availability]
tags: [domain:model, layer:model, project:trivia, project:ams-model, project:skillmatrix-model, status:emerging]
category: pattern
status: emerging
projects: [trivia, ams-model, skillmatrix-model]
evidence: ["trivia:unrecorded", "ams-model:unrecorded", "skillmatrix-model:unrecorded"]
alternatives: []
fragment: open-close-status-toggle
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Model an availability window that is explicitly turned on and off, such as a contest, a registration period or a campaign. The entity starts closed, an admin opens it, and it can be closed again.

### The state changes only through the operations

Create, update and delete are off. The open and close operations are the only way to move between states, so the state is always a deliberate action.

### The state is a two-value enumeration

OPEN and CLOSED are the two members. Use an enumeration instead of a boolean so the value reads clearly in queries and in the UI.

## Structure

The Contest entity has a required status (ContestStatus) and a required title. The ContestStatus enumeration lists OPEN and CLOSED. The entity has two instance operations, open and close, which each set the status to their state. The status defaults to CLOSED.

## Constraints

- Createable, updateable and deleteable are all false on Contest, so the generated UI shows no create, edit or delete controls.
- Status and title are required. Status must be OPEN or CLOSED.
- Both operations are custom implementations. They have `customImplementation` true: the body is Java in the backend, and the editor does not validate it as a JCL script.
- An operation that opens an already open entity, or closes a closed one, is a choice for the backend. The model does not prevent it.
- Custom operations are never intercepted (interceptors fire only for built-in operations). A check that the entity may be opened or closed belongs in the operation.

## Variations

- **Default OPEN.** When the entity should be available as soon as it is created, set the default to OPEN. The ams campaign example uses this form.
- **Boolean flag.** A closed boolean (default false) replaces the enumeration. The skillmatrix example uses this form. It has less detail in queries but the same two states.
- **Guard attributes on the view.** Derived boolean attributes, such as isOpen and isClosed, tell the UI which action is available: the operation's `hiddenBy` or `enabledBy` references such a boolean on the same transfer object. Use them when the admin view should show only the valid operation.
- **Load while empty.** A bulk load operation is allowed only while the entity has no children. The ams campaign example guards it with an isEmpty attribute.

## When to use

- An entity is available for a period and must be explicitly activated and deactivated.
- The states are exactly two and the transitions are repeatable.
- An admin controls the window, not the users.

## When to avoid

- The states form a line with one terminal state, such as draft to done. Use a linear status with a single final value.
- There are more than two states. Use a full enumeration with explicit transitions.
- Availability comes from a user account, not from the entity. Use an account status instead.

## Related

- [[multiple-choice-question-entity]] — a review status enumeration with three values, not a two-state toggle
- [[notification-entity]] — a status enumeration with three delivery states
- [[multi-actor-role-based-projections]] — the admin projection shows the open and close actions, the restricted one does not
