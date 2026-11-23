---
id: glassmorphic-styled-components
title: Glassmorphic MUI Styled Components Library
description: "A project library of MUI `styled()` components that give custom pages a frosted-glass look, built on top of the theme."
aliases: [frosted glass components, BlurCard]
keywords: [glassmorphic, MUI styled, backdrop-filter, BlurCard, CustomComponents.tsx, theme, custom components]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: component
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [dark-theme-override, custom-component-directory]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Custom pages that need a distinct visual identity beyond theme overrides share one set of styled components, so the look is defined once.

## Practice

### Platform base

- The frontend uses MUI with Emotion; styling is done with the `sx` prop, `styled()` components that read the `theme` (palette, spacing, shape, shadows), or `useTheme()` ([CSS-in-JS styling](../../agent-docs/frontend/theming.md)).
- App-wide colors belong in the actor's palette in the model; one component's styling can be handled by a theme override fragment or a sub-theme. Taking over the theme file is a last resort ([theming](../../agent-docs/frontend/theming.md)).
- Hand-written code lives in `src/custom/`; files you add there are not generated ([extension points](../../agent-docs/frontend/extension-points.md)). The documented layout does not prescribe a file for shared styled components.

### Practice notes: one glassmorphic component file

The example keeps all of its styled components in a single `CustomComponents.tsx` in the custom component directory and reuses them in every custom page:

```typescript
export const BlurCard = styled(Card)(({ theme }) => ({
  backgroundColor: 'rgba(0,0,0,0.6)',
  backdropFilter: 'blur(3px)',
  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  borderRadius: '15px',
  border: '1px solid rgba(255, 255, 255, 0.18)',
}));

export const ThreeDGlossyButton = styled(Button)({
  borderRadius: '15px',
  boxShadow: '0px 5px 15px rgba(0, 0, 0, 0.2)',
  '&::before': {
    background: 'linear-gradient(145deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 50%)',
    opacity: 0.6,
  },
});
```

- Semi-transparent backgrounds, `backdrop-filter: blur()`, a light border and a gradient overlay are the shared recipe.
- Prefer theme values (`theme.palette`, `theme.spacing`) over hardcoded colors where a value exists; the sample above hardcodes colors for the dark theme.
- Generated components keep the theme look; mix them with these components with care.

## Rationale

One component library keeps custom pages consistent and avoids repeating long style blocks. The cost is a custom design system that generated components do not share.

## Example

One app's participant frontend: `CustomComponents.tsx` holds its styled components (`BlurCard`, `BlurDialog`, `ThreeDGlossyButton`, `OptionButton`, `OptionAvatar`, `UnderlineTypography`, `TransitionWrapper`, `TransitionHolder`, `Ranking board`, `NumberInputAutoFocus`), all on `rgba(0,0,0,0.6)` backgrounds with a 3px blur, over the dark theme.

## When to avoid

- Theme-level changes cover the need: use the palette, fragments or sub-themes.
- Targets without `backdrop-filter` support.
- Mostly generated pages: the glass look will not match generated components.

## Related

- [[dark-theme-override]] — the dark theme these components sit on
- [[custom-component-directory]] — where the component file lives
