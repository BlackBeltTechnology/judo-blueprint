---
id: "custom-component-directory"
title: "Custom Component Directory Outside Generator Scope"
domain: "frontend"
category: "component"
score: 71.7
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - workflow-poc
  - reserve-app
---
## Description

Place all hand-written custom components in a dedicated directory (e.g., `src/trivia/`, `src/custom/`) that the JUDO code generator does not know about. Since the generator only manages files listed in its manifest, any directory outside the manifest is safe from overwriting. This is a best practice for organizing custom UI code alongside generated code.

## Structure

```
src/
  trivia/                    # Custom directory (generator-unaware)
    CustomComponents.tsx     # Reusable styled components
    Contest.tsx              # Custom page component
    Contests.tsx             # Custom list component
    RegistrationDialog.tsx   # Custom dialog
    utils.ts                 # Utility functions
    commons.ts               # Shared types/styles
  pages/                     # Generated pages (managed by generator)
  containers/                # Generated containers
  services/                  # Generated services
```

The key insight is that any directory not in the generator's file manifest is inherently safe. No `.generator-ignore` entry is needed for files in these directories.

## Examples

### Trivia
Player frontend uses `src/trivia/` containing 11 custom files: `ActivationDialog.tsx`, `CheckboxList.tsx`, `commons.ts`, `Contest.tsx`, `Contests.tsx`, `CustomComponents.tsx`, `PromptListDialog.tsx`, `RegistrationDialog.tsx`, `ResultsDialog.tsx`, `ScoreboardDialog.tsx`, and `utils.ts`.

### RackInspect
Uses `src/custom/` with 87 files organized into subdirectories: `hooks/custom-implementations/` (13 files), `hooks/dialogs/` (48 files), `hooks/pages/` (10 files), `hooks/FormActionsHooks/` (3 files), `hooks/ViewEditActionHooks/` (3 files), `hooks/TableRowHighlightingHooks/` (2 files), `hooks/utils/` (5 files), plus `application-customizer.tsx` and `register-error-handler-interceptor.ts`.

### workflow-poc
Uses `src/custom/components/` with 4 files: `Mermaid.tsx` (interactive diagram renderer using `mermaid` + `svg-pan-zoom`), `CodeViewer.tsx` (YAML syntax highlighter using `react-syntax-highlighter`), plus their Pandino registration files `registerMermaidComponent.tsx` and `registerCodeViewerComponent.tsx`.

### reserve-app
AdminActor uses `src/custom/hooks/dialogs/` with a single file: `registerServicesAdminActorStorageTypesAccessViewPageActionsHook.ts`. The other 4 actor frontends have no custom files at all. Demonstrates the minimal usage of `src/custom/` -- a single hook override file in the standard subdirectory structure.

## Trade-offs

- **Pros**: Zero risk of generator overwriting; clean separation of custom vs. generated code; no `.generator-ignore` entries needed
- **Cons**: Custom components cannot leverage generated page scaffolding; import paths cross between custom and generated directories
- **When to use**: Whenever adding custom React components that are not page overrides or hook overrides

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [glassmorphic-styled-components](glassmorphic-styled-components.md)
- [application-customizer-hub](application-customizer-hub.md)
