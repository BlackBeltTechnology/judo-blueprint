---
id: post-refresh-validation-propagation
title: Post-Refresh Validation Propagation from Backend Errors
description: "Use the `postRefreshAction` hook to map backend-computed validation errors to field-level validation messages in the UI."
aliases: []
keywords: [post, refresh, validation, propagation, from, backend, errors]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, error-code-mapping-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Use the `postRefreshAction` hook to map backend-computed validation errors to field-level validation messages in the UI. After a page refresh loads fresh data from the backend, the hook inspects an errors array on the data object and calls `setValidation` to populate a Map of field names to error messages. This allows complex backend validation rules to display as inline field errors without custom error handling logic.

## Structure

```typescript
const hookImpl = (data, editMode, storeDiff, refresh, submit) => ({
  async postRefreshAction(data, storeDiff, setValidation) {
    setValidation((prevValidation) => {
      const copy = new Map<keyof EntityType, string>([]);
      data.entityErrors?.forEach((error) => {
        copy.set(
          error.location as keyof EntityType,
          error.errorMessage as string
        );
      });
      return copy;
    });
  },
});
```

The backend provides an errors array (e.g., `partnerErrors`) on the entity data with `location` (field name) and `errorMessage` properties.

## Examples

### RackInspect
Partner view/edit hook maps `data.partnerErrors` array to field-level validation. Each error has a `location` (cast to `keyof Servicespartner_servicePartner`) and `errorMessage`. After every refresh, the validation Map is rebuilt from the current errors, allowing backend-computed rules to appear as inline field errors.

## Trade-offs

- **Pros**: Complex validation stays on backend; frontend displays errors without reimplementing logic; field-level granularity
- **Cons**: Requires backend to provide structured error arrays; validation is only updated on refresh (not real-time); tight coupling to error array structure
- **When to use**: When backend validation rules are too complex for frontend-only validation (cross-entity checks, database lookups, etc.)

## Related

- [[pandino-action-hook-override]]
- [[error-code-mapping-pattern]]

