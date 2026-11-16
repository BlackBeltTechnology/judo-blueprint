---
id: promise-based-dialog-system
title: Promise-Based Dialog System with Context Provider
description: "In a hand-built JUDO frontend, expose filter, range selection, confirmation and page-in-dialog as React Context dialogs opened through hooks that return a Promise, so callers use await instead of callbacks."
aliases: [async dialog hooks, awaitable dialogs, DialogProvider]
keywords: [promise, dialog, react context, dialog provider, openConfirmDialog, range dialog, filter dialog, page dialog, async await, hand-built frontend]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: component
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [complete-frontend-replacement, action-group-input-output-routing]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Replace callback-style dialogs with `await openXDialog(...)` calls in a frontend that does not use the generated dialogs.

## Practice

### Platform base

- The generated frontend already creates its dialogs from the model: input forms for operations and create or edit, range selection dialogs for relations, with hook extension points for the dialog's behaviour ([UI model to frontend mapping](../../agent-docs/frontend/model-screen-layout.md), [action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). Use those first.
- A hand-built UI that consumes only the generated service layer and transfer object types has to supply its own dialogs; see [[complete-frontend-replacement]]. This pattern is for that case.

### Practice notes: a context-provided Promise dialog set

This is custom code, not a platform feature:

- A `DialogProvider` wraps the app and renders four dialogs once: filter, range, confirmation and page.
- Each dialog is opened by its own hook returning a function that returns a Promise: `openFilterDialog(options, current)` resolves with the chosen filters, `openRangeDialog({ columns, rangeCall, single, alreadySelectedItems, filterOptions })` with the selected entities, `openConfirmDialog(message, title)` with a boolean, and `openPageDialog(component)` renders an output component in a modal.
- The range dialog is generic over the stored transfer object type and the query customizer, and pages through the range call of the service layer on the server side.
- The filter dialog covers boolean, numeric, string, enumeration, date, dateTime and trinary-logic filters.
- Cancel must be handled: decide whether the Promise resolves with nothing or rejects, and make every caller handle it.

```typescript
// Illustrative caller code
const { openConfirmDialog } = useConfirmDialog();
if (await openConfirmDialog('Are you sure?', 'Title')) {
  await service.remove(row);
}
```

## Rationale

Linear async/await flows are easier to read than nested callbacks, and dialog state lives in one place with a consistent look. The cost is one shared state container, no stacked dialogs, and cancel handling at each call site.

## Example

A hand-built app: `DialogProvider` in `src/components/dialog/DialogContext.tsx` combines the four dialogs. `PageDialog` renders action group output components in modals.

## When to avoid

- The generated frontend is used; customize its dialog hooks instead.
- Dialogs must open from within other dialogs; the single-context design does not nest them.

## Related

- [[complete-frontend-replacement]] — the hand-built frontend this belongs to
- [[action-group-input-output-routing]] — output pages shown through the page dialog
