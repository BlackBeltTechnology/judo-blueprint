---
id: autocomplete-range-override
title: Autocomplete Range Override for Context-Filtered Queries
description: A dialog or page hook replaces the data source of a relation autocomplete so the options are filtered by the owner's current context instead of the generic range query.
aliases: [dependent dropdown hook, context-filtered autocomplete]
keywords: [autocomplete, range, hook, dialog, query customizer, dependent dropdown, filtered options]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [interceptor-range-override]
related: [pandino-action-hook-override, interceptor-range-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

By default a relation autocomplete offers every instance the generic range query returns. When the valid choices depend on the parent record or another selected value, a frontend hook can redirect the options to a query filtered by that context.

## Practice

### Platform base

- A relation selector gets its options from a generated range operation (`GET_RANGE`): an unbound operation whose input carries the owner and whose output is the range type ([operation reference](../../agent-docs/model/esm_metamodel/operation.md)). The generated frontend calls it with a query customizer for paging and the typed text ([service generation](../../agent-docs/frontend/model-screen-layout.md)).
- Container, dialog and page hooks are registered as Pandino services from `register...Hook(context)` functions called in `application-customizer.tsx`. A container hook receives `(data, editMode, storeDiff, context)` and returns handler functions; the hook type and its member names are generated per container in its `customization` module ([container actions](../../agent-docs/frontend/hooks/action-hooks.md)).
- Autocomplete handlers in hooks may fetch options through `context.actions.getRangeAction('<relation>')({ query, page, size })` ([typeahead/autocomplete](../../agent-docs/frontend/hooks/action-hooks.md)).
- The agent-docs do not list the exact name of the range-override member for a relation. Take it from the generated `customization` module of the container instead of guessing it.

### Project practice: redirect the range call to a context-filtered service

This layer is project practice (rackinspect), not a platform feature:

- In the hook, override the range member of each dependent relation. It receives the query customizer and calls a specialized service that filters by the owner data held in the hook closure (for example only racks of the partner of the current record).
- Wrap each filtered call in a small utility function, shared by all hooks that need the same filter.
- The filter is applied in the client. If the restriction is a security boundary, enforce it on the server too, for example in a range interceptor ([[interceptor-range-override]]).

```typescript
// Example project code: member and service names are illustrative, check the generated hook type
const hookImpl = (ownerData) => ({
  async rackAutocompleteRangeAction(queryCustomizer) {
    return getRackRangeForPartner(ownerData, queryCustomizer);
  },
});
```

## Rationale

Users see only relevant options, which cuts selection errors, and the filtering runs on the backend. The cost: specialized backend endpoints, more hooks to maintain, and context dependencies that get complex.

## Example

rackinspect has several dialog hooks that override rack, warehouse and rack-element ranges. One shows only racks of the partner of the current fault registry; another filters rack elements by the rack type of the current fault. Shared utilities in one helper module hold the range query logic.

## When to avoid

- The filter is a security rule: a client-side hook can be bypassed, use a server-side range interceptor.
- All instances are valid choices.
- The context needed for the filter is not available in the hook's data.

## Related

- [[pandino-action-hook-override]] — how the hook is registered
- [[interceptor-range-override]] — the server-side alternative for the same filtering
