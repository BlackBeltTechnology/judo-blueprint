---
id: viewmodel-context-pattern
title: ViewModel Context Pattern for Generated Pages
description: "Every generated page directory holds a context file with a ViewModel type and a React context, so nested components and hooks reach page state without prop drilling."
aliases: [page view model, page context]
keywords: [viewmodel, context, generated pages, context.tsx, customization.ts, types.ts, page state, hooks]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:itracker", "status:emerging"]
category: state
status: emerging
projects: [trivia, itracker]
evidence: ["trivia:unrecorded", "itracker:unrecorded"]
alternatives: []
related: [pandino-action-hook-override, event-bus-refresh-coordination, hook-scaffold-default-pattern]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Know what each generated page directory contains and how page state is shared with nested components, so custom code uses the generated structure instead of inventing its own state plumbing.

## Practice

### Platform base

This is a generator convention observed in two apps, not something to build:

- Each generated page lives in `src/pages/<PagePath>/` with an `index.tsx` and a `context.tsx` ([file path patterns](../../agent-docs/frontend/model-screen-layout.md)). In the observed apps the directory also holds `customization.ts` and `types.ts`.
- `customization.ts` carries the hook interface key and hook type of the page; `types.ts` carries the action definition types. A page action hook uses the per-page key `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY`; the object it returns must match the generated types, so read `customization.ts` and `types.ts` before writing one ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md)).
- The scaffolds that implement those hooks are generated only when the hook flag is set in the model; they sit under `src/custom/hooks/` as `.default` files ([hook files](../../agent-docs/frontend/extension-points.md)).
- The agent-docs do not describe the contents of `context.tsx`. The shape below is taken from two example apps and may differ by generator version; check the generated file.

```
SomePage/
  index.tsx          page component, creates and provides the ViewModel
  context.tsx        ViewModel interface and React context
  customization.ts   hook interface key and hook type
  types.ts           action definition types
```

### Observed ViewModel shape

```typescript
// context.tsx (generated)
export interface SomeViewModel extends SomePageProps {
  setIsLoading: Dispatch<SetStateAction<boolean>>;
  setEditMode: Dispatch<SetStateAction<boolean>>;
  refresh: () => Promise<void>;
}
export const SomeViewModelContext = createContext<SomeViewModel>({} as any);
```

The page component builds the ViewModel with its loading and edit-mode setters and a refresh function, then wraps its children in the context provider.

### Practice notes: consume it, do not copy it

- Custom components placed inside a generated page read the context (loading, edit mode, refresh) instead of receiving props through every level.
- Generated files carry a checksum and are not edited; change behaviour through hooks, not by editing `context.tsx` ([hook system](../../agent-docs/frontend/hooks/README.md)).

## Rationale

One consistent structure across all pages (in one two-actor app, every page of both actors) lets a developer find state, hooks and action types in the same place. Costs: generated boilerplate per page, possible extra re-renders when the context value changes, and tight coupling between the ViewModel and the page.

## Example

- A game app: admin pages such as a category view page each have a `context.tsx` defining the ViewModel, created in `index.tsx` with the setters and `refresh`.
- A two-actor app: all pages of both actors and their containers follow the same layout.

## When to avoid

- Do not hand-write a parallel context for a generated page; extend it through hooks.
- Do not rely on the ViewModel field names across generator upgrades without checking the generated type.

## Related

- [[pandino-action-hook-override]] — hooks that customize the page actions
- [[event-bus-refresh-coordination]] — sharing refresh across pages
- [[hook-scaffold-default-pattern]] — the `.default` scaffolds next to the page structure
