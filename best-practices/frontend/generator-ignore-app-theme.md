---
id: "generator-ignore-app-theme"
title: "Generator-Ignore for App.tsx and Theme"
domain: "frontend"
category: "build"
score: 69.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
---
## Description

Protect the application root component (`src/App.tsx`) and theme configuration (`src/theme/index.tsx`) from being overwritten by the JUDO code generator by listing them in `.generator-ignore`. This is the foundational step for any frontend customization -- once these files are ignored, developers can freely modify the app shell and theme without losing changes on regeneration.

## Structure

`.generator-ignore` file in the actor frontend root:

```
.generator-ignore
.gitignore
src/App.tsx
src/theme/index.tsx
```

The generator will skip these files during code generation. All other generated files continue to be regenerated normally.

## Examples

### Trivia
Player frontend `.generator-ignore` protects `src/App.tsx`, `src/theme/index.tsx`, and `public/manifest.json`. The Admin frontend only protects `.generator-ignore` and `.gitignore` (no customizations). This shows two extremes: heavily customized vs. fully generated.

### RackInspect
`.generator-ignore` protects `src/custom/application-customizer.tsx`, `src/config/layout.ts`, and two i18n files (`public/i18n/application_hu-HU.json`, `public/i18n/system_hu-HU.json`). Notably does NOT ignore App.tsx or theme files -- customization is done through hooks and custom components instead.

## Trade-offs

- **Pros**: Simple mechanism; files are fully under developer control; generator continues to work for everything else
- **Cons**: Protected files may drift from framework changes; developer must manually apply framework updates to ignored files
- **When to use**: Any time you need to customize the app shell, theme, or other generated files

## Related Patterns

- [complete-frontend-replacement](complete-frontend-replacement.md)
- [dark-theme-override](dark-theme-override.md)
- [pwa-manifest-customization](pwa-manifest-customization.md)
- [generator-ignore-i18n-layout](generator-ignore-i18n-layout.md)
