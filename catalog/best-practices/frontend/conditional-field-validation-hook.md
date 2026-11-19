---
id: conditional-field-validation-hook
title: Conditional Field Validation via Action Hook
description: Make a form field required or optional depending on other field values by returning a handler from a page or container actions hook, without editing generated code.
aliases: [conditional required field, dynamic required validation]
keywords: [conditional, field, validation, action hook, required, page actions hook, scaffold]
tags: ["domain:frontend", "layer:frontend", "project:reserve-app", "project:rackinspect", "status:emerging"]
category: hook
status: emerging
projects: [reserve-app, rackinspect]
evidence: ["reserve-app:unrecorded", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/containers/registerServicesItem_serviceItemItem_View_EditContainerActionsHook.ts"]
alternatives: []
related: [pandino-action-hook-override, hook-scaffold-default-pattern, application-customizer-hub, approval-workflow-conditional-visibility]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A form field should be mandatory only when another field has a certain value (for example a name that is required only for active records). The rule lives in a frontend action hook, so the generated page stays untouched.

## Practice

### Platform base

- The generator emits per-page and per-container hook points. A page hook has the key `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY` and the type `<Container>ActionsHook`, both exported from the page's generated `customization` module (dialogs: `~/dialogs/<path>/customization`). Container hooks use `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` from `~/containers/<path>/customization` ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).
- The hook is a function that receives the page data (`data`, `editMode`, `storeDiff`, depending on the page kind) and returns the handlers. The object you return must match the generated action type, so read the generated `customization.ts` and `types.ts` for the available handler names; the handler names in the docs are illustrative ([validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md)). The contents of the generated page files (`context.tsx`, `customization.ts`, `types.ts`, and the app-wide `src/config/layout.ts`) are described in [generated page files](../../agent-docs/frontend/model-screen-layout.md#generated-page-files); this page links to that description and does not repeat it.
- Scaffolds are `.default` files under `src/custom/hooks/{pages,dialogs,containers}/`. Copy one to the name without `.default`, implement it and call its `register...Hook(context)` from `src/custom/application-customizer.tsx` ([using .default scaffolds](../../agent-docs/frontend/hooks/README.md)). The copy is not generated, so no `.generator-ignore` entry is needed.
- Conditional requiredness is a model switch: with `generateVisualPropertiesHook` set, the generated container hook type has `is<Field>Hidden`, `is<Field>Disabled`, `is<Field>Readonly` and `is<Field>Required` handlers ([hook generation](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)). Requiredness can also be driven by the model's `requiredBy` attribute, static or set dynamically by a backend interceptor ([access control attributes](../../agent-docs/frontend/model-screen-layout.md)).
- Validation hooks can express other conditional rules by looking at the form data ([conditional validation](../../agent-docs/frontend/hooks/validation-hooks.md)).

### Practice notes: a required-predicate handler

One frontend returned a single `isFieldRequired` predicate from the dialog actions hook of a view page. The agent-docs name per-field `is<Field>Required` handlers instead, so use the handler names in the generated `customization.ts` and `types.ts`; the shape below is one such variant.

```typescript
// src/custom/hooks/dialogs/register<Dialog>ActionsHook.ts (from the scaffold)
import type { BundleContext } from '@pandino/pandino-api';
import {
  ENTITY_ACCESS_VIEW_PAGE_ACTIONS_HOOK_INTERFACE_KEY,
  type EntityActionsHook,
} from '~/dialogs/Entity/AccessViewPage/customization';

export function registerEntityAccessViewPageActionsHook(context: BundleContext) {
  context.registerService<EntityActionsHook>(
    ENTITY_ACCESS_VIEW_PAGE_ACTIONS_HOOK_INTERFACE_KEY,
    entityActionsHook,
  );
}

const entityActionsHook: EntityActionsHook = () => ({
  // required only while the other field is set (handler name per generated type)
  isSomeFieldRequired: (data) => !!data.someOtherField,
});
```

- Keep the predicate a pure function of `data`; one hook file serves one page or dialog.
- Enforce the same rule in the backend as well (a model constraint or interceptor); the hook only changes the form.

### Variation: container action hooks

A second frontend sets required and disabled state per field from hooks on container actions, rather than a single required-predicate handler.

## Rationale

The rule stays out of generated code and survives regeneration, because the scaffold copy lives in `src/custom/`. The cost is that the handler contract is tied to the generated types, and the check is client-side only.

## Example

One app, with an admin actor, has a view page dialog where `name` is required only when the `active` flag is set; inactive records may leave it empty. It is the only hook override across five actor frontends.

## When to avoid

- The rule must hold for every client: enforce it in the model or backend, and use the hook only for UX.
- The rule needs several fields or async checks: use a validation hook, see [validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md).

## Related

- [[pandino-action-hook-override]] — the hook mechanism this uses
- [[hook-scaffold-default-pattern]] — activating the `.default` scaffold
- [[application-customizer-hub]] — where the registration is called
- [[approval-workflow-conditional-visibility]] — conditional visibility instead of requiredness
