---
id: pandino-action-hook-override
title: Pandino Service Registry for Action Hook Overrides
description: The JUDO framework uses Pandino (an OSGi-like service registry for JavaScript) to enable runtime action hook injection in generated pages.
aliases: []
keywords: [Pandino, action hook, registerService, useTrackService, hook override, page actions, scaffold]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:rackinspect", "project:itracker", "project:reserve-app", "project:park-here", "status:established"]
category: hook
status: established
projects: [trivia, rackinspect, itracker, reserve-app, park-here]
evidence: ["trivia:unrecorded", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/application-customizer.tsx", "itracker:unrecorded", "reserve-app:unrecorded"]
alternatives: []
related: [hook-scaffold-default-pattern, application-customizer-hub, custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Customize the behaviour of a generated page or dialog without editing generated code. The generated component asks the Pandino service registry for an actions hook and spreads whatever it returns over its default actions, so a registered hook overrides only the actions it names.

## Practice

### Platform base

- Hooks register through Pandino in `src/custom/application-customizer.tsx`: `context.registerService<HookType>(INTERFACE_KEY, hook, { component: '<Component>' })`. The interface key is exported by the module that owns the hook or by the generated `~/containers/<path>/customization` module; the service properties (`component`, `column`, `page`) pick which component the hook applies to ([hook architecture](../../agent-docs/frontend/hooks/README.md)).
- Hook scaffolds are generated only when the model sets `generateActionsHook` (or `generateVisualPropertiesHook`) on the element, as inactive `register<Name>ActionsHook.ts.default` files under `src/custom/hooks/{pages,dialogs,containers}/` ([hook generation](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)). Copy the scaffold without `.default`, implement it and register it ([[hook-scaffold-default-pattern]]).
- Page and dialog hooks have the signature `(data, editMode, storeDiff, refresh, submit)`, and the real type and key names are generated per page ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).
- `src/custom/` is not generated and needs no `.generator-ignore` entry. Hooks are the documented route; editing generated files fails the checksum check ([why hooks](../../agent-docs/frontend/hooks/README.md)).

### Practice notes: override only the actions that differ

The generated page does the lookup, shown here as a simplified sketch (names are generated per page and are not a fixed API):

- The page tracks the registered service for its hook key, calls it with the page data, edit mode, `storeDiff`, `refresh` and `submit`, and spreads the result last over the default actions (`getPageTitle`, `backAction`, `refreshAction`, `updateAction`, `deleteAction`, `getMask`, ...).
- A hook therefore returns a partial object: only the actions to replace or add. Extended page types also allow `post<Action>` handlers such as `postRefreshAction`.
- Return an empty object when the hook has nothing to say; the scaffold does this by default.
- Registration is by interface key plus component name, so one hook serves exactly one page or dialog.

```typescript
// Example code (generated page, simplified)
const customActions = customActionsHook?.(data, editMode, storeDiff, refresh, submit);
const actions = {
  getPageTitle,
  backAction,
  refreshAction,
  updateAction,
  deleteAction,
  getMask,
  ...(customActions ?? {}), // custom overrides win
};
```

## Rationale

The generated code stays untouched and upgrade-safe, hooks resolve at runtime, and partial overrides keep each customization small. The cost is learning the registry, and debugging a missing registration is harder than reading a direct call: a wrong key or component name silently leaves the default behaviour.

## Example

- A heavily customized frontend registers many hooks in its application customizer: dialog files, page hook files, form and view/edit hooks, table row highlighting hooks and custom visual element implementations.
- A game frontend has two page overrides whose scaffolds are in place but still return empty objects.
- A two-actor frontend is generated with the hook lookup in every page and dialog, yet registers none (all scaffolds stay inactive): zero customization costs nothing at runtime.
- A frontend registers one page hook that makes a name field required depending on an `active` flag.

## When to avoid

- The change is structural (layout, markup): use a template override or a custom visual element ([[custom-visual-element-override]]).
- The page needs no custom behaviour: leave the scaffold inactive.
- The model can express it: prefer model flags over hooks.

## Related

- [[hook-scaffold-default-pattern]] — activating the `.default` scaffolds
- [[application-customizer-hub]] — where registrations are collected
- [[custom-visual-element-override]] — replacing a rendered element, also via Pandino
