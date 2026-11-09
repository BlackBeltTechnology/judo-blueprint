---
id: content-lifecycle-status-enum
title: Content Lifecycle Status Enum (Draft, Published, Deleted)
description: A status enumeration for user-authored content that moves through draft, published and soft-deleted states, with status changes made by operations rather than by editing the field.
aliases: [content status, publishing lifecycle, draft published deleted]
keywords: [content, lifecycle, status, enum, draft, published, deleted, soft delete]
tags: ["domain:model", "layer:model", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [draft-done-status-enum, active-suspended-deactivated-status-enum]
fragment: content-lifecycle-status-enum
diagram: { kinds: [enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Give user-authored content a small, fixed set of states that matches an editorial workflow. A draft is not visible to the audience, a published item is, and a deleted item is removed from view but kept for audit.

### States are a fixed enumeration

The content holds one status value from a short enumeration. Each value has a fixed order. Extra states, such as expiry or moderation, are added only by content types that need them.

### Status changes are operations

The status is read-only in the generated forms. A change happens through an operation such as publish or delete, which also runs the side effects of that change.

## Structure

The ContentStatus enumeration has three values in order: DRAFT, PUBLISHED and DELETED. Each value has an ordinal. There are no relations and no operations on the enumeration.

A content entity holds one status attribute typed with this enumeration. Its operations change the status. The enumeration itself does not enforce which transitions are allowed; that is a rule of the operations.

## Constraints

- The status field is read-only for the generated edit pages. Only operations change it.
- A new item starts as DRAFT. Publishing sets PUBLISHED and records a publication time.
- Deletion is soft: the status becomes DELETED and the row stays in place.
- Interceptors do not run for the status operations, which are custom. Each one must check the current status and its own permission.
- Values must keep their ordinals once saved, because stored data refers to them by position.

## Variations

- **Expiry.** Time-based content adds an EXPIRED value, set by a scheduled operation when its end date passes.
- **Moderation.** Content that needs review adds a PENDING_REVIEW value, set when the item is submitted and cleared by a moderator. A moderation removal is a separate operation with its own role check.
- **Separate enumeration per content type.** Each content type can have its own enumeration with the values it needs, rather than one shared list with unused states.

## When to use

- User-authored items need a draft stage before they are visible.
- Removal must keep the record for audit or recovery.
- The states are few and ordered, and the transitions are simple.

## When to avoid

- The states are many or change often. Use a state machine with a history of transitions instead.
- The status is a business state with many transitions and guards, such as an order. Use a workflow with its own history.
- Visibility depends on the reader rather than on one status. Use a derived access rule instead.

## Related

- [[draft-done-status-enum]] — a two-state draft and done enumeration, for work items rather than published content
- [[active-suspended-deactivated-status-enum]] — a status for accounts, with suspension rather than publication
- [[document-review-state-machine]] — a richer state machine for documents, with transitions and history
- [[safe-failure-pattern]] — the rule for audit writes that must not block a status change
