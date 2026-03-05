---
id: "viewmodel-context-pattern"
title: "ViewModel Context Pattern for Generated Pages"
domain: "frontend"
category: "state"
score: 21.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - itracker
---
## Description

Each generated JUDO page uses a React Context-based ViewModel pattern. A `context.tsx` file defines a `ViewModel` interface extending the page props with setters for loading, edit mode, and a refresh function. The context is created and provided by the page component, making page state accessible to nested child components without prop drilling.

## Structure

Each generated page directory contains 4 files:

```
SomePage/
  index.tsx         # Page component (creates and provides ViewModel)
  context.tsx       # ViewModel interface and Context definition
  customization.ts  # Action hook interface key
  types.ts          # Extended action types
```

Context definition:

```typescript
// context.tsx
export interface SomeViewModel extends SomePageProps {
  setIsLoading: Dispatch<SetStateAction<boolean>>;
  setEditMode: Dispatch<SetStateAction<boolean>>;
  refresh: () => Promise<void>;
}

export const SomeViewModelContext = createContext<SomeViewModel>({} as any);
```

## Examples

### Trivia
Admin frontend pages (e.g., Categories AccessViewPage) each have `context.tsx` defining the ViewModel. The page component in `index.tsx` creates the ViewModel with `setIsLoading`, `setEditMode`, and `refresh` methods, then wraps children in `SomeViewModelContext.Provider`.

### itracker
All 15 pages across both actors (9 UserActor + 6 Admin) follow the identical pattern. Each page directory contains `index.tsx`, `context.tsx`, `customization.ts`, and `types.ts`. Container components (24 UserActor + 6 Admin) also use this structure with DialogContainer and PageContainer variants.

## Trade-offs

- **Pros**: Clean separation of page state and UI; nested components access state without prop drilling; consistent pattern across all pages
- **Cons**: Generated boilerplate per page; context can cause unnecessary re-renders if not optimized; tight coupling between ViewModel and page
- **When to use**: This is the standard JUDO generated page pattern -- automatically created for all pages

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [event-bus-refresh-coordination](event-bus-refresh-coordination.md)
