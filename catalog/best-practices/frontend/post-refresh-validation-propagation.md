---
id: post-refresh-validation-propagation
title: Post-Refresh Validation Propagation from Backend Errors
description: "Use the page or dialog post-refresh handler to turn a backend-computed list of field errors on the loaded data into field-level validation messages, rebuilt after every refresh."
aliases: [postRefresh validation, backend validation to field errors]
keywords: [post refresh, validation, field errors, setValidation, backend computed errors, location, hook, derived error list]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, error-code-mapping-pattern, form-blur-action-hook]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Show complex, server-computed validation results (cross-entity checks, lookups) as inline field errors without reimplementing the rules in the frontend.

## Practice

### Platform base

- Page and dialog hook types have an optional `post<RefreshAction>` handler (for example `postRefreshAction`), whose parameters are generated for the page. There is no generic `PostRefreshActionHook` type or interface key: return the handler from the page actions hook built from the `register<Page>ActionsHook` scaffold ([PostRefresh action hook](../../agent-docs/frontend/advanced-patterns.md), [action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).
- Platform validation errors from the backend use `{ location, code, message }`. Inline field errors from a failed request appear only when the first error has a `location`; otherwise only the generic toast shows ([error handling](../../agent-docs/frontend/error-handling.md), [validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md)).

### Project practice: error list on the data (rackinspect)

This is a project convention layered on the platform, not a platform feature:

- The entity carries a model-defined list of errors (for example `partnerErrors`), each with a field `location` and an `errorMessage`. Because it is part of the loaded data, it is recomputed by the backend on each load. It is the project's own transfer object field, separate from the platform's error response.
- The post-refresh handler rebuilds the whole validation map from the current list on every refresh through `setValidation`, so cleared errors disappear.
- The map keys are the form field names; a `location` that matches no field is not shown.
- Handler parameters and the error field names in the sketch are illustrative; use the generated types.

```typescript
// Illustrative; names come from the generated hook type and project model.
async postRefreshAction(data, storeDiff, setValidation) {
  setValidation(() => {
    const next = new Map<keyof EntityType, string>();
    data.entityErrors?.forEach((e) => next.set(e.location as keyof EntityType, e.errorMessage));
    return next;
  });
}
```

## Rationale

Complex rules stay in the backend and the frontend only displays them, with field-level granularity. The cost is a modeled error structure, updates only on refresh (not while typing), and coupling to that structure.

## Example

rackinspect: the partner view/edit hook maps the partner error list to field validation. After each refresh the map is rebuilt from the current errors, so backend rules appear as inline field errors.

## When to avoid

- Rules are simple and local to a field; use frontend validation hooks.
- Errors must appear while typing; refresh-driven updates are too slow, so use a blur hook ([[form-blur-action-hook]]).

## Related

- [[pandino-action-hook-override]] — how action hooks are registered
- [[error-code-mapping-pattern]] — mapping backend error codes to messages
- [[form-blur-action-hook]] — field-level server checks on blur
