---
id: single-access-entity-pattern
title: Single Access Entity Fetch and Create-If-Missing
description: "For an actor access that holds at most one instance (settings, a single item), fetch the instance first and send the user to a create page when it does not exist, then refresh the full view with a mask using the returned signed identifier."
aliases: [singleton fetch or create, create-if-missing page]
keywords: [single access, singleton, signed identifier, create if missing, refresh with mask, two-phase fetch, view page, empty key, hand-built frontend]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: page
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [singleton-entity, action-group-input-output-routing, view-edit-mode-toggle]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Handle an access that yields zero or one instance: show it when it exists, offer creation when it does not.

## Practice

### Platform base

- The platform has no singleton construct. A single-instance access is a model access with upper bound 1, often a derived getter ending in `!any()`; nothing enforces that a row exists, so reading code must handle the missing case ([[singleton-entity]]).
- Every instance the REST layer returns carries `__identifier` and `__signedIdentifier`. Bound operations and instance updates take the signed identifier, not the plain id. The signed identifier changes after every update (the version is part of it), and client code cannot mint one, so take the current one from a response ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).
- Loading related data for a detail view is done with a mask ([masks for detail views](../../agent-docs/backend/data-access-guide.md)). The generated frontend builds this page for you from the access; the steps below matter for hand-built pages.

### Practice notes: fetch, then refresh with a mask

The names below belong to an example's generated service layer, not to the platform docs:

1. Ask the root access service for the instance with an empty key (`settingsServiceImpl.get('{}')` in the example; the empty-key call is a convention of that generated service layer, so check yours).
2. If an instance with a signed identifier comes back, keep the identifier and load the full entity with the view service's `refresh`, passing the identifier and a query customizer with the mask for relations. Two steps: existence check first, data second.
3. If none exists, navigate to the create page; the create call goes through the same root service. Provide a way back from the create page.
4. Catch errors in one handler (snackbar), and drive the action buttons of the view from entity state.
5. Re-read the signed identifier after each update before the next bound call, since it changes.

```typescript
const { __signedIdentifier } = await settingsServiceImpl.get('{}');
if (__signedIdentifier) {
  setData(await viewSettingsServiceImpl.refresh({ __signedIdentifier }, queryCustomizer));
} else {
  navigate('/settings/create');
}
```

## Rationale

The user always lands on the right screen for an optional single instance, and the cheap existence check is separate from the heavier mask load. The cost is one extra call and a convention that can surprise developers.

## Example

A hand-built app: the settings entity is checked with the empty-key get. When found, the view loads with its related table; otherwise the user goes to `/settings/create`. The view shows action buttons depending on state (active, archived, draft).

## When to avoid

- The generated frontend is used; its pages already handle a single-instance access.
- Several instances are possible; use a table access.

## Related

- [[singleton-entity]] — the model side of the single-instance access
- [[action-group-input-output-routing]] — routing after the operations on this entity
- [[view-edit-mode-toggle]] — the view and edit behaviour of such a page
