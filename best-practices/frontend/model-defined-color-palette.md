---
id: "model-defined-color-palette"
title: "Model-Defined Color Palette via ESM Actor Properties"
domain: "frontend"
category: "theme"
score: 38.7
usage_count: 3
alternative_count: 2
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - skillmatrix-frontend
  - ams-frontend
alternatives:
  - dark-theme-override
  - flutter-theme-template-override
---
## Description

Define the application color palette directly in the ESM model on actor types rather than overriding theme files in code. Each actor type supports properties like `primaryColor`, `secondaryColor`, `textPrimaryColor`, `textSecondaryColor`, `subtitleColor`, `backgroundColor`, and `paperBackgroundColor`. The JUDO generator produces the corresponding theme file (`src/theme/palette.ts` for React, `app_theme.dart` for Flutter) with these colors mapped to framework theme tokens. This approach requires zero code customization -- no `.generator-ignore` entries for theme files, and theme files remain fully generated and updatable.

## Structure

ESM model actor definition (in JUDO Designer):
```
Actor "UserActor" {
  primaryColor: "#3C4166FF"
  secondaryColor: "#E7501DFF"
  textPrimaryColor: "#17191DFF"
  textSecondaryColor: "#434448FF"
  subtitleColor: "#8C8C8C"
  backgroundColor: "#FAFAFAFF"
  paperBackgroundColor: "#FFFFFFFF"
}
```

Generated `src/theme/palette.ts` (React):
```typescript
export const palette = {
  primary: { main: '#3C4166' },
  secondary: { main: '#E7501D' },
  text: { primary: '#17191D', secondary: '#434448' },
  background: { default: '#FAFAFA', paper: '#FFFFFF' },
};
```

No theme files in `.generator-ignore`. All theme files remain generated.

## Examples

### itracker
Both UserActor and Admin actors define identical branded palette: primary `#3C4166` (dark navy), secondary `#E7501D` (Howmet orange-red), text primary `#17191D` (near-black), background `#FAFAFA` (off-white). All 8 theme files (`palette.ts`, `typography.ts`, `density.ts`, `animations.tsx`, `extras.ts`, `table-row-highlighting.ts`, `types.ts`, `index.tsx`) remain fully generated.

### SkillMatrix (Flutter)
All 3 actors share identical `app_theme.dart` with the same color palette: primary #3c4166 (dark blue-gray), secondary #e7501d (orange-red), background #fafafa, text #17191d/#434448. Colors are encoded in the generated Flutter ThemeData and AppDesignCustomizer. Additionally includes semi-transparent variants (primaryVariant at 75% alpha) and component-specific color assignments (tabs, toggles, indicators all using secondary color).

### ams-frontend
Both Admin and Manager actors use identical model-defined palette: primary #3C4166 (dark blue-gray), secondary #E7501D (orange-red), background #FAFAFA, card #FFFFFF, display text #17191D, body text #434448, input label #8F8F8F, divider #DCDCDC. The `app_theme.dart` is fully generated with SourceSansPro typography and StadiumBorder buttons. No theme template override needed.

## Trade-offs

- **Pros**: Zero code maintenance; survives all generator updates; single source of truth in model; consistent across regeneration
- **Cons**: Limited to properties the generator supports (7 color slots); no component-level overrides; no dark mode toggle; cannot add custom CSS variables
- **When to use**: When the standard MUI palette properties are sufficient for branding and no component-level style overrides are needed

## Related Patterns

- [dark-theme-override](dark-theme-override.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [flutter-app-design-customizer](flutter-app-design-customizer.md)
- [flutter-theme-template-override](flutter-theme-template-override.md)
