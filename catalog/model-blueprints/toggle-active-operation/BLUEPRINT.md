---
id: toggle-active-operation
title: Toggle Active Boolean Operation Pattern
description: "An entity with a required active boolean (default true) and an instance operation that flips it, giving soft enable and disable without deletion."
aliases: [toggleActive, activateToggle, enable disable operation, toggle active inactive, activate deactivate operation]
keywords: [toggle, active, boolean, operation, instance operation, custom implementation]
tags: ["domain:model", "layer:model", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "status:emerging"]
category: pattern
status: emerging
projects: [rackinspect, mlszksz-platform]
evidence: ["rackinspect:model/rackinspect.model", "mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let an entity be switched on and off without deleting it. The entity carries a required boolean `active` that defaults to true, and an instance operation flips it. The same shape repeats on many entities in one model, so it is a cross-cutting pattern.

### The flag is state, the operation is the only writer

The operation is the single place that changes the flag. Rules about who may change it, or whether it may change at all, live in that operation.

### Siblings flip other flags

Some entities add more flip operations in the same style (primary, billing, headquarters, postal, delivery). Each flips one boolean and follows the same implementation.

## Structure

One entity with a required boolean `active` (stored, default true) and one instance operation `toggleActive` with no input and no output. The operation is declared as a custom implementation, stateful, so the body is Java in the backend. Other attributes of the entity are unrelated to the pattern.

## Constraints

- `active` is required and has a default, so a new row starts enabled and the value is never null.
- Custom operations are never intercepted: interceptors and write guards fire only for built-in operations (see [Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). A check on who may toggle, or on what must stay active, belongs in the operation body.
- A rule that a business error must reach the client as a typed error needs a fault declared on the operation in the model ([Custom operations](../../agent-docs/backend/custom-operations.md)). A plain Java exception reaches the client as a generic 500.
- The flag hides nothing by itself. Queries and views that should skip inactive rows must filter on it.

## Variations

- **Operation on the transfer object.** One project keeps the entity attribute as `isActive` and puts the operation, named `activateToggle`, on the admin transfer object instead of the entity. It is project naming; the shape is the same.
- **Parent revalidation.** For child entities (address, phone, email) the toggle also reloads the owner and re-runs its business rules.
- **Self-lock guard.** On a user entity, the toggle refuses to deactivate the current actor and keeps at least one active user with administrative permission.
- **Status enumeration instead of a boolean.** When there are more than two states, use a status enumeration; see [[active-inactive-status-enum]].

## When to use

- Records must be disabled but kept for history or references.
- Many entities need the same switch and a uniform admin action.
- The switch is a deliberate user action, not a computed state.

## When to avoid

- The record has real lifecycle states beyond on and off. Use a status enumeration with explicit transitions.
- The flag is set only by the system, never by a user action. A plain attribute is enough, no operation needed.
- Rows must disappear from all queries by default. Pair the flag with filters, or model deletion instead.

## Related

- [[active-inactive-status-enum]] — enumeration form of the same on/off state
- [[soft-delete-active-flag]] — the active flag as a soft-delete practice
- [[open-close-status-toggle]] — two-state status moved by open and close operations
