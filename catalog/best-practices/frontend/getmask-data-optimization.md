---
id: getmask-data-optimization
title: Custom getMask() Override for Data Fetch Optimization
description: "Override the `getMask()` action in page hooks to specify exactly which fields to fetch from the backend, optimizing network payload for list views."
aliases: [custom getMask, list mask override]
keywords: [getMask, _mask, X-Judo-Mask, mask, page action hook, list view, payload, projection]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/utils/masks.ts", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/pages/registerServicesFault_registry_servicesMyTaskPanelMyTaskPanel_View_EditCreateFaultRegistryOutputViewActionsHook.ts"]
alternatives: []
related: [pandino-action-hook-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A list page with a complex entity should request only the fields it displays, so payload and backend query stay small.

## Practice

### Platform base

- The transport carries a projection: the REST operations read the `X-Judo-Mask` request header (`__mask`) as "projection of the response", and the React client declares it in `headers.ts` ([protocol headers](../../agent-docs/backend/platform-behavior-reference.md)). The frontend client sends it from a `_mask` string on the `QueryCustomizer`.
- On the backend side, masks decide which attributes and relations are loaded, and narrow masks are the documented performance lever ([masks](../../agent-docs/backend/data-access-guide.md)).
- Page behavior is customised with page action hooks: a per-page key `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY`, a hook receiving `(data, editMode, storeDiff, ...)` and returning handlers, registered from the application customizer ([page actions](../../agent-docs/frontend/hooks/action-hooks.md)).
- Not covered by the agent-docs: the `getMask()` handler itself and the exact `_mask` string syntax. The pieces below are practice from one example, not documented platform behavior; check the generated hook type of your page for `getMask`.

### Practice notes: return a narrow mask from the page hook

Implement `getMask()` in the page actions hook and return only the list's columns and the needed nested relations:

```typescript
const hookImpl = (data, editMode, storeDiff, refresh, submit) => ({
  getMask(): string {
    return '{closedDate,created,orderNumber,' +
      'assignedTo{email,name},' +
      'customer{customerName},' +
      'lineItems{productName,productTypeName}}';
  },
});
```

- Plain fields: `{a,b}`; nested relation: `{rel{x,y}}`; deeper nesting as `{r1{r2{f}}}`.
- Update the mask whenever columns change. A missing field shows as empty data and nothing validates the string at compile time.
- Keep the mask next to the page's other hook logic so both change together.

## Rationale

Generated pages fetch all visible fields; relations the list never shows still cost network and database work. A hand-written mask trades maintenance for smaller, faster lists.

## Example

One app's list page: the hook returns a constant mask from a shared `masks.ts` file. The mask fetches dates, the identifier, status flags, `assignedTo{email,name}`, `customer{customerName}` and a few nested line-item fields, and skips the heavy nested details and item data the list does not show.

## When to avoid

- Small entities or pages whose default fields are already what the list shows.
- Fields that change often: the mask becomes a source of silent missing data.

## Related

- [[pandino-action-hook-override]] — how page action hooks are registered
- [[generated-service-layer-reuse]] — the same `_mask` customizer in custom UIs
