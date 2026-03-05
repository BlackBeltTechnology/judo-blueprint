---
id: "mui-extensive-component-overrides"
title: "Extensive MUI Component Theme Overrides"
domain: "frontend"
category: "theme"
score: 9.9
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
alternatives:
  - dark-theme-override
---
## Description

Customize the MUI theme with extensive `components` overrides covering 15+ component types. Beyond basic palette changes, this pattern overrides default props, style overrides, and variant behavior for AppBar, Button, TextField, FilledInput, InputLabel, Select, DataGrid, Paper, Drawer, Tabs, IconButton, Tooltip, Divider, ListItemButton, ListItemText, ListItemIcon, Avatar, and Card. Includes custom palette extensions (e.g., `subtitleColor`) and shape/typography modifications. Creates a cohesive, branded visual identity.

## Structure

```typescript
// Custom palette extension
declare module '@mui/material/styles' {
  interface Palette { subtitleColor: Palette['primary']; }
  interface PaletteOptions { subtitleColor?: PaletteOptions['primary']; }
}

const theme = createTheme({
  palette: { mode: 'light', primary: { main: '#3C4166FF' }, secondary: { main: '#E7501DFF' } },
  shape: { borderRadius: 8 },
  components: {
    MuiButton: { defaultProps: { variant: 'contained', size: 'small' },
      styleOverrides: { root: { textTransform: 'none', borderRadius: '20px', boxShadow: 'none' } } },
    MuiTextField: { defaultProps: { fullWidth: true, variant: 'filled', color: 'secondary' } },
    MuiFilledInput: { styleOverrides: {
      root: { '&.Mui-readOnly': { background: 'transparent', borderBottom: '1px solid ...' } } } },
    // ... 13+ more component overrides
  },
});
```

## Examples

### ActionGroupTestReact
Theme at `src/theme/index.tsx` overrides 16 MUI components. Key customizations: pill-shaped buttons (20px radius), filled TextFields with white background and read-only styling, borderless DataGrid with custom toolbar padding, Paper with 16px radius and subtle shadow, borderless Drawer with shadow, orange IconButtons, small 32x32 Avatars. Custom `subtitleColor` palette extension for form labels.

## Trade-offs

- **Pros**: Cohesive branded design; consistent component behavior; centralized style management; MUI theme system handles cascading
- **Cons**: Large theme file (280+ lines); must track MUI version changes; overrides can conflict with component-level sx props; hard to maintain
- **When to use**: Projects requiring a distinctive visual identity beyond simple palette changes

## Related Patterns

- [dark-theme-override](dark-theme-override.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [model-defined-color-palette](model-defined-color-palette.md)
