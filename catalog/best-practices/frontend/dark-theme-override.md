---
id: dark-theme-override
title: Custom Dark MUI Theme Override
description: "Override the generated JUDO theme with a fully custom MUI `createTheme()` configuration, typically in `src/theme/index.tsx`."
aliases: []
keywords: [custom, dark, mui, theme, override]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: theme
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: [model-defined-color-palette, mui-extensive-component-overrides]
related: [generator-ignore-app-theme, glassmorphic-styled-components, model-defined-color-palette, mui-extensive-component-overrides]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Override the generated JUDO theme with a fully custom MUI `createTheme()` configuration, typically in `src/theme/index.tsx`. This pattern sets a custom color palette (mode, primary, secondary, text), typography adjustments, and component-level style overrides (MuiCard, MuiDialog, etc.). The file must be listed in `.generator-ignore` to prevent overwriting.

## Structure

```typescript
// src/theme/index.tsx (generator-ignored)
createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#eb5a29', contrastText: '#dddddd' },
    secondary: { main: '#dddddd' },
    text: { primary: '#dddddd' },
  },
  typography: {
    h6: { fontSize: '1rem' },
  },
  components: {
    MuiCard: { styleOverrides: { root: { borderRadius: 10, background: 'rgba(0,0,0,0.75)' } } },
    MuiDialog: { styleOverrides: { root: { /* ... */ } } },
  },
})
```

## Examples

### Trivia
Player frontend uses a hardcoded dark theme with orange primary (`#eb5a29`), light grey text (`#dddddd`), semi-transparent black card/dialog backgrounds (`rgba(0,0,0,0.75)`), extra-bold dialog titles (`fontWeight: 900`), and compact h6 typography (`1rem`).

## Trade-offs

- **Pros**: Full control over visual identity; can create branded experiences far from the JUDO default
- **Cons**: Must be maintained manually on framework upgrades; may miss new theme tokens added by the framework
- **When to use**: Any project requiring a branded visual identity different from the default JUDO theme

## Related

- [[generator-ignore-app-theme]]
- [[glassmorphic-styled-components]]
- [[model-defined-color-palette]]
- [[mui-extensive-component-overrides]]

