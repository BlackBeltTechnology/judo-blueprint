---
id: "conditional-field-validation-hook"
title: "Conditional Field Validation via Action Hook"
domain: "frontend"
category: "hook"
score: 19.2
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - reserve-app
---
## Description

Override a generated page's field validation behavior using a Pandino action hook that returns conditional `isFieldRequired` functions. The hook examines the current entity data and returns `true` or `false` to dynamically control whether a field is required. This pattern allows field-level required/optional status to depend on other field values without modifying generated page code. The hook is registered via `application-customizer.tsx` and the scaffold `.ts.default` file is renamed to `.ts` to activate it.

## Structure

```typescript
// src/custom/hooks/dialogs/registerEntityAccessViewPageActionsHook.ts
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

const entityActionsHook: EntityActionsHook = () => {
  return {
    isFieldRequired: (data) => !!data.someOtherField,
  };
};
```

The generated page component checks for `isFieldRequired` in its actions object and uses it to set the `required` prop on the corresponding form field.

## Examples

### reserve-app
AdminActor StorageTypes AccessViewPage dialog hook makes `name` conditionally required based on `active` flag: `isNameRequired: (data) => !!data.active`. Active storage types must have a name; inactive ones can have an empty name. This is the project's only hook override across 5 actor frontends, demonstrating that even minimal customization uses the standard Pandino hook pattern.

## Trade-offs

- **Pros**: Clean separation from generated code; leverages existing hook infrastructure; simple boolean logic; no page modifications needed
- **Cons**: Must understand the hook interface contract (which `isFieldRequired` names are available); validation is frontend-only unless backend also enforces it; one hook file per page/dialog
- **When to use**: When a form field should be conditionally required based on other field values in the same entity

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [hook-scaffold-default-pattern](hook-scaffold-default-pattern.md)
- [application-customizer-hub](application-customizer-hub.md)
- [approval-workflow-conditional-visibility](approval-workflow-conditional-visibility.md)
