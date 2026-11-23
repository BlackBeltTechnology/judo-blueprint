---
id: dirty-check-before-update
title: Dirty-Check Before Update to Avoid Unnecessary Writes
description: When code recomputes many fields of an entity, compare the new values with the loaded ones and call the DAO update only if something changed.
aliases: [skip unchanged update, change detection, avoid redundant write]
keywords: [dirty check, update, DAO, toMap, compare, mask, recursion, interceptor, unnecessary write]
tags: ["domain:backend", "layer:backend", "project:alba", "status:single-project"]
category: data-access
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: []
related: [mutable-entity-update-pattern, permission-denormalization]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Bulk recalculations and aggregation hooks often set many derived fields, most of which end up with their old value. Every DAO update still increments the entity's `__version` and writes rows. Skip the update when nothing changed.

## Practice

### Compare before writing

Load the entity once, remember its values, apply the computed values, and call `update` only when at least one value differs. Two forms are in use:

- Snapshot compare: copy `entity.toMap()` into a new map before the changes and compare it with `entity.toMap()` afterwards. Short for many fields.
- Field compare: for each computed field, set it and raise a `changed` flag only when the new value differs from the current one. Read optional attributes through their `Optional` getter (`getX().orElse("")`), because attributes that are not `required` are `Optional` in the generated DTO (see [Absent, Null and Empty Are Different](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)).

Pass a mask to both the load and the `update`, listing only the fields the code touches. Without a mask the call loads and writes everything (see [Using Masks](../../agent-docs/backend/data-access-guide.md#using-masks-projections)).

### Mind the `toMap` edge cases

`toMap()` makes a full copy. Compare maps only after loading with a mask, so absent attributes are absent on both sides. A key that is missing is not the same as a key with `null`, so make sure the load and the comparison use the same mask.

### Inside interceptors

The pattern is used in `postCall` hooks that write derived values back (aggregation, denormalization, see [Data Denormalization and Aggregation](../../agent-docs/backend/interceptors.md#data-denormalization-and-aggregation)). The interceptor runs inside the operation's transaction, so an exception in `preCall` or `postCall` rolls back the operation's write as well. Interceptors fire only for built-in operations (see [Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)); a custom operation that recalculates data must run the comparison itself.

### Version handling

Each write increments `__version`, and the signed identifier of the entity changes with it. Clients that hold the old identifier see a stale-update error on their next write. Skipping needless writes keeps identifiers stable (see [Signed Identifiers](../../agent-docs/backend/platform-behavior-reference.md#signed-identifiers) and [Optimistic Locking](../../agent-docs/backend/platform-behavior-reference.md#optimistic-locking-and-__version)).

## Rationale

- Fewer writes and fewer version bumps in cascades.
- Limit: the comparison costs memory and code. For a single field that is always set, an unconditional update is simpler.
- This is a practice built on the platform. The platform does not detect unchanged payloads for you.

## Example

- A permission recalculation iterates all users and recomputes a set of boolean flags from roles. It copies each user's map first and updates only the users whose map changed.
- A product update interceptor builds aggregated strings from related entities, compares each with the stored value, and calls update only if one differs.

## When to avoid

- The write itself is the point, for example you want the version bumped or a timestamp refreshed.
- The entity is cheap to write and rarely recalculated: the check adds code without benefit.
- Concurrency is the concern: a dirty check is not a lock. Optimistic locking handles that (see [[mutable-entity-update-pattern]]).

## Related

- [[mutable-entity-update-pattern]] — how updates are issued
- [[permission-denormalization]] — the recalculation that benefits most
