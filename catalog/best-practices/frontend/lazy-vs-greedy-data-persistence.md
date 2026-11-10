---
id: lazy-vs-greedy-data-persistence
title: Lazy vs Greedy Data Persistence Modes for Custom Components
description: Custom components that manage their own data can implement two data persistence strategies.
aliases: []
keywords: [lazy persistence, greedy persistence, storeDiff, custom component, immediate save, batch save]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: state
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A custom component that edits its own data must decide when changes reach the backend. This practice offers two modes: greedy (batch the changes into the page form and save with it) and lazy (persist each change at once, independent of the page form).

## Practice

### Platform base

- Generated pages keep edits as a diff in page state. Hooks receive `(data, editMode, storeDiff, ...)`; `storeDiff(attributeName, value)` records a change so validation and diff tracking stay consistent, and the page save sends the diff ([data hooks](../../agent-docs/frontend/hooks/data-hooks.md)).
- Authorization and validation are enforced by the backend whatever the mode ([hooks overview](../../agent-docs/frontend/hooks/README.md)).
- A bound call needs the instance's current signed identifier, which changes after every update of the entity. In lazy mode take it from the latest response and never cache it ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).
- A model-designated custom element renders your component ([[custom-visual-element-override]]).

### Project practice: two modes in one component

The two modes are project practice (rackinspect), not platform features. The component picks a mode from its context.

- **Greedy** (creation forms): template data is fetched up front, every change goes through `storeDiff`, and everything is submitted with the form save.
- **Lazy** (view/edit pages): every change calls a backend service immediately. Local state is kept apart from the page form so the page does not enter edit mode or block the page save. Show a spinner while syncing, and on error revert the value and show the message.
- Rows can be added or deleted independently in lazy mode, and selectable enum values can be loaded when a dropdown opens.

```typescript
// Example project code: greedy
const onValueChange = (id: string, value: unknown) => {
  storeDiff('groups', updateValue(groups, id, value)); // saved with the form
};

// Example project code: lazy
const onValueChange = async (id: string, value: unknown) => {
  setLoading(id);
  try {
    await itemService.updateParameter(id, value); // service name illustrative
    refreshLocalState();
  } catch (e) {
    revertValue(id);
    showError(e);
  } finally {
    setLoading(null);
  }
};
```

## Rationale

Creation forms need all-or-nothing saves, so batching fits. On an existing record a field-by-field edit is natural and should not force the user through the page save. The cost is two code paths and the risk of local state drifting from the server.

## Example

In rackinspect a dimension-parameters component runs greedy in the fault element creation form and lazy in the rack view/edit page, where rows are added and deleted directly.

## When to avoid

- The component sits in one context only: implement only that mode.
- Immediate persistence would skip validation the page save performs.
- The component is a plain field: use the generated input and `storeDiff`.

## Related

- [[custom-visual-element-override]] — the component these modes live in
