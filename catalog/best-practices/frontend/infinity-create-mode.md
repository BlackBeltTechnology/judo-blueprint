---
id: infinity-create-mode
title: Infinity Create Mode with Template Copying
description: Enable rapid sequential creation of similar entities by generating a template that copies most field values from the previously created entry while resetting specific fields.
aliases: []
keywords: [infinity create, template, copy previous, dialog hook, storeDiff, rapid data entry]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: form
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, post-operation-navigation-hook]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Data entry often creates many similar records in a row (for example inspection findings that share most fields). This practice reopens the create dialog after each save, prefilled from the previous record, with only selected fields reset.

## Practice

### Platform base

- The create form is prepopulated from a template: the REST layer serves a blank prototype of the transfer object under `<TO>/~template` (operation `GET_TEMPLATE`, see [operation reference](../../agent-docs/model/esm_metamodel/operation.md)), and the generated dialogs call it when they open.
- Dialog and page hooks receive `(data, editMode, storeDiff, ...)`; `storeDiff(attributeName, value)` updates page state so validation and diff tracking stay consistent ([data hooks](../../agent-docs/frontend/hooks/data-hooks.md)). Generated dialog hook types also accept optional `post<Action>` handlers, as documented for `postRefreshAction` ([advanced patterns](../../agent-docs/frontend/advanced-patterns.md)).
- Hooks are registered from the `register<Dialog>ActionsHook` scaffolds under `src/custom/hooks/dialogs/` ([hooks overview](../../agent-docs/frontend/hooks/README.md)).

### Project practice: copy the previous entry into the next template

The agent-docs do not describe a `postGetTemplateAction` handler by name; this practice (rackinspect) assumes the generated dialog exposes it after the template is fetched, so confirm the handler exists in your generated dialog types before relying on it.

- Keep the last saved record in a module-level variable.
- A template function maps the fields to carry over and sets the fields that must always restart to defaults.
- In the dialog hook, after the template loads, push each template field into the page with `storeDiff`.
- After a successful create, reopen the dialog instead of closing it (see [[post-operation-navigation-hook]]).

```typescript
// Example project code
export function createTemplateForItem(previous: ItemStored) {
  return {
    row: previous.row,          // carried over
    category: previous.category, // carried over
    withMaterial: true,         // always reset
  };
}

// Dialog hook (names illustrative)
async postGetTemplateAction(ownerData, data, storeDiff) {
  if (previousData) {
    Object.entries(createTemplateForItem(previousData)).forEach(([k, v]) => storeDiff(k, v));
  }
}
```

## Rationale

Consecutive records share most values, so carrying them over saves typing and avoids mistakes in the common fields. The cost is that stale values can slip through unnoticed, and entities with many relations need careful field selection.

## Example

rackinspect copies row, level, position, error placement, rack element, error code and type, repair type, quantity, input groups, rack and registry header from the previous fault element, and resets a material flag to true. Inspectors then create fault elements in quick succession.

## When to avoid

- Consecutive records rarely share values.
- Carried-over values are risky if left unchecked (for example financial or safety data).
- Server-side defaults from the template operation already cover the need.

## Related

- [[pandino-action-hook-override]] — how the dialog hook is registered
- [[post-operation-navigation-hook]] — reopen or navigate after a create
