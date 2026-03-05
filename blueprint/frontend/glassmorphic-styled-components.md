---
id: "glassmorphic-styled-components"
title: "Glassmorphic MUI Styled Components Library"
domain: "frontend"
category: "component"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

A reusable library of MUI `styled()` components implementing a glassmorphic (frosted glass) design language. Components use semi-transparent backgrounds, `backdrop-filter: blur()`, decorative borders, and gradient overlays. Typically stored in a single `CustomComponents.tsx` file within the custom component directory.

## Structure

Common glassmorphic component patterns:

```typescript
// BlurCard - frosted glass card
export const BlurCard = styled(Card)(({ theme }) => ({
  backgroundColor: 'rgba(0,0,0,0.6)',
  backdropFilter: 'blur(3px)',
  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  borderRadius: '15px',
  border: '1px solid rgba(255, 255, 255, 0.18)',
}));

// ThreeDGlossyButton - button with gradient overlay
export const ThreeDGlossyButton = styled(Button)({
  borderRadius: '15px',
  boxShadow: '0px 5px 15px rgba(0, 0, 0, 0.2)',
  '&::before': {
    background: 'linear-gradient(145deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 50%)',
    opacity: 0.6,
  },
});
```

## Examples

### Trivia
`CustomComponents.tsx` provides 10 styled components: `BlurCard`, `BlurDialog`, `ThreeDGlossyButton`, `OptionButton`, `OptionAvatar`, `UnderlineTypography`, `TransitionWrapper`, `TransitionHolder`, `Scoreboard`, and `NumberInputAutoFocus`. All share the glassmorphic design language with `rgba(0,0,0,0.6)` backgrounds and `blur(3px)` backdrop filter.

## Trade-offs

- **Pros**: Consistent visual language; reusable across all custom pages; leverages MUI's styled() API and theme access
- **Cons**: Requires backdrop-filter browser support; may not integrate well with generated JUDO components; design system is project-specific
- **When to use**: When building custom UI with a distinct visual identity that goes beyond MUI theme overrides

## Related Patterns

- [dark-theme-override](dark-theme-override.md)
- [custom-component-directory](custom-component-directory.md)
