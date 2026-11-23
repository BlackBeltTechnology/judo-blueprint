---
id: dark-theme-override
title: Custom Dark MUI Theme Override
description: Give a frontend a fixed dark look by overriding the generated MUI theme file, once the model palette and theme override fragments are not enough.
aliases: [fixed dark theme, custom MUI theme]
keywords: [dark theme, MUI, createTheme, palette, generator-ignore, theme override fragments, actor palette]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: theme
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: [model-defined-color-palette, mui-extensive-component-overrides]
related: [generator-ignore-app-theme, glassmorphic-styled-components, model-defined-color-palette, mui-extensive-component-overrides]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An application should always render dark with its own brand colors. Start from the platform's theming layers and take over the theme file only when they cannot express the design.

## Practice

### Platform base

- Theming is two-layered. The actor type in the UI model carries seven palette colors (primary, secondary, background, paper background, primary and secondary text, subtitle) plus `applicationLogo`; the generator renders them into `src/theme/palette.ts`. To change the app-wide palette, change the actor in the model, not `palette.ts`. If `applicationLogo` is an SVG, give it explicit `width` and `height` attributes, or the generated image renders wrongly ([theming](../../agent-docs/frontend/theming.md)). Component sub-themes (a `subTheme` name on a widget) cover per-card or per-table colors ([theming overview](../../agent-docs/frontend/theming.md)).
- The generated `src/theme/index.tsx` is assembled from fixed fragments (`index.ts.mui-<component>.fragment.hbs`, theme options, extra components, palette attributes). Overriding one fragment is preferred over taking over the whole file when only some component styles change ([theme override fragments](../../agent-docs/frontend/theming.md)).
- Editing a generated theme file by hand requires a `.generator-ignore` entry; the file is then no longer regenerated and cross-actor consistency is lost ([customizing theme](../../agent-docs/frontend/theming.md)).
- The docs show a dark palette variant (`mode: 'dark'`) and an in-app dark mode toggle that registers a component in the AppBar; the toggle is the choice when users must switch, a fixed dark theme when they must not.

### Practice notes: take over the theme file

Use only when palette plus fragments are insufficient. A replaced theme uses one `createTheme` call, listed in `.generator-ignore`:

```typescript
// src/theme/index.tsx (listed in .generator-ignore)
createTheme({
  palette: {
    mode: 'dark',
    primary: { main: BRAND, contrastText: LIGHT },
    secondary: { main: LIGHT },
    text: { primary: LIGHT },
  },
  typography: { h6: { fontSize: '1rem' } },
  components: {
    MuiCard: { styleOverrides: { root: { borderRadius: 10 } } },
    MuiDialog: { styleOverrides: { root: { /* ... */ } } },
  },
})
```

- Define the brand and text colors as constants in one place and derive card and dialog backgrounds from them.
- Set `palette.mode` to `dark` so MUI defaults (inputs, dividers, ripples) follow.
- After each platform upgrade, compare your file with the regenerated one to pick up new theme tokens.

## Rationale

One explicit theme gives complete control over the visual identity. The price is manual upkeep: the file no longer receives generator changes and can miss new tokens.

## Example

One app's participant frontend uses a hardcoded dark theme with an orange primary, light grey text, semi-transparent black card and dialog backgrounds, extra-bold dialog titles and compact h6 typography. Its admin frontend keeps the generated theme.

## When to avoid

- A palette change fits the actor's model colors: change the model, see [[model-defined-color-palette]].
- Only a few components differ: override those theme fragments or use sub-themes.

## Related

- [[generator-ignore-app-theme]] — protecting the theme file from regeneration
- [[glassmorphic-styled-components]] — translucent surfaces on top of a dark theme
- [[model-defined-color-palette]] — palette from the model instead of code
- [[mui-extensive-component-overrides]] — component-level style overrides
