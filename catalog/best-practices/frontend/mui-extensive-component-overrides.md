---
id: mui-extensive-component-overrides
title: Extensive MUI Component Theme Overrides
description: "Customize the MUI theme with extensive `components` overrides covering 15+ component types."
aliases: []
keywords: [MUI theme, component overrides, styleOverrides, defaultProps, theme fragments, branding]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "project:indamedia-adtrack", "status:emerging"]
category: theme
status: emerging
projects: [actiongroup-test-react, indamedia-adtrack]
evidence: ["actiongroup-test-react:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: [dark-theme-override]
related: [model-defined-color-palette, generator-ignore-app-theme, dark-theme-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-11
---
## Intent

A distinctive, branded look needs more than seven palette colors. This practice overrides the MUI theme's `components` for many component types (buttons, inputs, tables, paper, drawer, avatars, ...), plus shape and palette extensions, in one theme.

## Practice

### Platform base

- Theming has two layers: the model-driven actor palette and frontend code. The seven palette colors are set on the actor, not in code ([theming](../../agent-docs/frontend/theming.md), [[model-defined-color-palette]]).
- The generated theme (`src/theme/index.tsx`) is assembled from fixed fragments. A same-named file in the application's `actor/src/theme/` override directory replaces one: `index.ts.mui-<component>.fragment.hbs` for app-bar, autocomplete, avatar, button, card, chip, data-grid, dialog, divider, drawer, form-control, icon, input-base, list, paper, radio, select, stack, tab, text-field and tooltip, plus `index.ts.extra-components.fragment.hbs`, `index.ts.theme-options.fragment.hbs` and the `palette.ts.*` fragments ([theme override fragments](../../agent-docs/frontend/theming.md)).
- The docs advise a fragment override over a full `.generator-ignore` of `index.tsx` when only a few components change.
- Per-widget colors are done with sub-themes: a model `subTheme` name selects a registered `SubThemeHook` that returns `{ components: { ... } }` overrides ([extension points](../../agent-docs/frontend/extension-points.md)).

### Practice notes: one broad theme file

This is practice: the whole theme file is taken over and carries many component overrides. Choose it only when most components change; otherwise use fragments.

- Set default props and style overrides together per component, so one place holds a component's look (for example buttons with a pill radius and no shadow; filled text fields with a styled read-only state).
- Extend the palette type with extra slots through module augmentation (for example a subtitle color) and read them in component overrides.
- Set shared shape (border radius) once, and reuse it in components.
- Check each MUI upgrade against the overrides, and keep component-level `sx` to exceptions, since both fight over the same properties.

```typescript
// Example code
declare module '@mui/material/styles' {
  interface Palette { subtitleColor: Palette['primary']; }
  interface PaletteOptions { subtitleColor?: PaletteOptions['primary']; }
}

const theme = createTheme({
  shape: { borderRadius: 8 },
  components: {
    MuiButton: {
      defaultProps: { variant: 'contained', size: 'small' },
      styleOverrides: { root: { textTransform: 'none', borderRadius: 20, boxShadow: 'none' } },
    },
    MuiTextField: { defaultProps: { fullWidth: true, variant: 'filled' } },
    MuiFilledInput: {
      styleOverrides: { root: { '&.Mui-readOnly': { background: 'transparent' } } },
    },
  },
});
```

## Rationale

Centralised theme code gives one coherent look and relies on MUI's cascade instead of styling every screen. The cost is a large file, tracking MUI changes, conflicts with `sx` props and a protected file that no longer follows generator updates.

## Example

One app's theme overrides many MUI components: pill buttons, filled text fields with a white background and a read-only style, a borderless data grid, rounded paper with a light shadow, a borderless drawer with shadow, orange icon buttons and small avatars, plus a subtitle color palette extension for form labels.

## When to avoid

- Only the brand colors change: set them on the actor ([[model-defined-color-palette]]).
- Only a few components change: use the generator's per-component fragments, which keep the rest generated.
- Variations per card or view: use sub-themes.

## Related

- [[model-defined-color-palette]] — brand colors from the model, no code
- [[generator-ignore-app-theme]] — protecting the theme file from regeneration
- [[dark-theme-override]] — another full theme takeover
