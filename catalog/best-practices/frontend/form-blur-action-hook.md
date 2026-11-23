---
id: form-blur-action-hook
title: Form Blur Action Hook for Field Auto-Composition
description: Compute or compose a form field value when the user leaves a related field, using the generated on-blur action handlers returned from a page or container actions hook.
aliases: [blur handler, field auto-composition, on blur action]
keywords: [blur, onBlur, BlurAction, storeDiff, actions hook, auto-compose, computed field, form]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/utils/partnerAddressInformation.ts", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/ViewEditActionHooks/customServicesCompanyDataServiceCompanyAddressCompanyAddressViewEditActionsHook.tsx"]
alternatives: []
related: [pandino-action-hook-override, post-refresh-validation-propagation]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A form field should be filled automatically from other fields when the user leaves one of them (for example a full address composed from its parts). A generated blur handler does this without touching generated code.

## Practice

### Platform base

- Blur handling is a model switch: a widget marked `onBlur` makes the generator add an optional `on<Field>BlurAction` handler to the container hook type ([widget mapping](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md), [hook generation](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)). There is no `BlurActionHook` service and no blur interface key ([cascade loading pattern](../../agent-docs/frontend/advanced-patterns.md)).
- The handler is part of the object returned by the container or page actions hook, created from the `register<Container>ActionsHook` scaffold (copy it without `.default`, call its register function from `application-customizer.tsx`). The hook function receives `(data, editMode, storeDiff, ...)`; check `types.ts` of the generated container for the exact handler signature ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md), [hooks overview](../../agent-docs/frontend/hooks/README.md)).
- Without the model switch there is no handler to implement, so first mark the fields in the model.

### Practice notes: compose a field from its parts

```typescript
const hookImpl = (data, editMode, storeDiff) => ({
  onStreetNameBlurAction: async (data) => {
    if (!data.manualAddress) {
      storeDiff('fullAddress', composeAddress(data));
    }
  },
  onNumberBlurAction: async (data) => {
    if (!data.manualAddress) {
      storeDiff('fullAddress', composeAddress(data));
    }
  },
  // one handler per component field
});

function composeAddress(d) {
  return [d.streetName, d.number, d.floor, d.door].filter(Boolean).join(' ');
}
```

- Put the composition in one function shared by all blur handlers.
- Guard with a "manual" flag so users can type the composite value themselves.
- The same entity often has several containers (create form and view/edit page); each needs its own hook registration, so share the handler functions between them.
- Treat blur as a convenience: paste and autofill may not trigger it, so compute the value again on the server (derived attribute or interceptor) if it must be right.

## Rationale

The user sees the composed value immediately, and the logic lives in the hook, not in generated code. The cost is duplicated registrations per container and the blur-based trigger's edge cases.

## Example

One app: address auto-composition for three entities, each with a form hook and a view/edit hook. Blur handlers on street, category, number, building, staircase, floor, door and lot number rebuild the composite address, guarded by a manual-entry toggle.

## When to avoid

- The value is always derivable: model a derived attribute instead of computing it in the browser.
- Cascading lookups that need server data: see the cascade loading pattern in the advanced patterns doc.

## Related

- [[pandino-action-hook-override]] — how action hooks are registered
- [[post-refresh-validation-propagation]] — server-side values pushed to the form after refresh
