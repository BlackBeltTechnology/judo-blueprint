---
id: "complete-frontend-replacement"
title: "Complete Frontend Replacement with Custom SPA"
domain: "frontend"
category: "page"
score: 20.3
usage_count: 2
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - actiongroup-test-react
alternatives:
  - zero-customization-generated-frontend
---
## Description

Replace the entire generated JUDO UI with a hand-built single-page application while retaining the generated TypeScript service layer. This is used when the UX requirements fundamentally diverge from the standard CRUD page model (e.g., gamified experiences, mobile-first immersive UIs, real-time interactions), or when the project serves as a reference/test application demonstrating specific JUDO patterns. The generated services, transfer object types, and Axios client implementations are still consumed, but all pages, routing, layout, and components are custom.

## Structure

1. Add `src/App.tsx` and `src/theme/index.tsx` to `.generator-ignore` so the generator never overwrites them.
2. Create a custom component directory (e.g., `src/trivia/`, `src/custom-app/`) that the generator does not know about.
3. In the custom `App.tsx`, import generated service implementations directly (e.g., `new PlayerServiceForContestsImpl(judoAxiosProvider)`).
4. Implement all navigation, state management, and UI components from scratch.
5. Generated files (services, containers, routes, etc.) are still produced but effectively unused.

```
.generator-ignore:
  src/App.tsx
  src/theme/index.tsx
  public/manifest.json

src/
  App.tsx                  # Custom app root (hand-written)
  theme/index.tsx          # Custom theme (hand-written)
  custom-app/              # All custom components (generator-unaware)
    Component1.tsx
    Component2.tsx
    ...
  services/                # Generated (kept and used)
```

## Examples

### Trivia
Player frontend replaces the entire generated JUDO UI with a custom quiz game SPA. `App.tsx` acts as a single state-machine controller, rendering custom `Contests`, `Contest`, and dialog components while importing `PlayerServiceForContestsImpl`, `PlayerServiceForTestsImpl`, etc. from the generated service layer.

### ActionGroupTestReact
Entirely hand-built React app (no JUDO generator, no Pandino, no `.generator-ignore`). All 20+ pages, layout, theme, dialogs, and utilities are hand-written in `src/`. Imports generated Axios services and types from `src/generated/`. Demonstrates JUDO action group patterns (input/output routes), CRUD, many-aggregation, and single-access entity patterns as a reference application.

## Trade-offs

- **Pros**: Maximum UI flexibility; no constraints from generated page patterns; can implement any UX paradigm
- **Cons**: No benefit from generated pages, tables, or forms; all UI must be maintained manually; framework upgrades may require manual migration
- **When to use**: When the application UX is fundamentally different from CRUD (games, dashboards, wizards, real-time apps), or for reference/test applications

## Related Patterns

- [generated-service-layer-reuse](generated-service-layer-reuse.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [custom-component-directory](custom-component-directory.md)
- [dialog-based-navigation](dialog-based-navigation.md)
- [zero-customization-generated-frontend](zero-customization-generated-frontend.md)
