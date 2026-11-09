## Overview

A custom Material UI theme with project-specific branding, dark mode support, locale-specific localization, and optionally Capacitor native status bar color synchronization. Framework: React (optionally Capacitor Android).

## Implementation Pattern

The theme system overrides the generated theme files via `.generator-ignore`:

- **palette.ts** (`src/theme/palette.ts`) -- Custom `paletteThemeLight` and `paletteThemeDark` with project-specific primary/secondary colors, text colors, and background colors. Both typically include a custom `subtitleColor` palette extension declared via MUI module augmentation.
- **index.tsx** (`src/theme/index.tsx`) -- Full MUI theme construction with:
  - Locale bundles (e.g., `huHU` for Material, DataGrid, DatePickers)
  - Optional Capacitor status bar integration: `StatusBar.setStyle()` for icon color, `StatusBarTheme.setColor()` for background color
  - Responsive typography, density, and component overrides matching the generated structure
  - Custom `subtitleColor` palette type declaration via `declare module '@mui/material/styles'`
- **density.ts** (`src/theme/density.ts`) -- Custom density configuration (spacing multiplier, font size, button size, border radius, data grid density, main margin values)
- **fonts.tsx** (`src/theme/fonts.tsx`) -- Custom font family (e.g., Source Sans 3 Variable, Plus Jakarta Sans) loaded via `@fontsource-variable`
- **index.css** (optional) -- Custom `@font-face` declarations and CSS overrides
- **StatusBarTheme** (optional) -- Capacitor plugin registration for native Android status bar background color
- **i18n** -- Custom translation files (e.g., `public/i18n/application_hu-HU.json`) listed in `.generator-ignore`
- **Custom assets** -- Logo images, favicons (multiple sizes), manifest.json in `public/` with `.generator-ignore`
- **Layout overrides** (optional) -- `src/layout/logo/LogoMain.tsx` and other layout files listed in `.generator-ignore`

## Examples

### mlszksz-platform
- Framework: React (Capacitor Android)
- Key files: `src/theme/palette.ts`, `src/theme/index.tsx`, `src/theme/index.css`, `custom/utilities/status-bar-theme.ts`, `public/i18n/application_hu-HU.json`, `public/i18n/system_hu-HU.json`
- Pattern: Generator-ignore theme override with custom palette, Hungarian locale, Capacitor StatusBar plugin for native status bar sync
- Notable: StatusBarTheme custom Capacitor plugin for Android status bar color; Plus Jakarta Sans custom font; layout files overridden for platform-aware logout

### park-here
- Framework: React (web)
- Key files: `src/theme/palette.ts`, `src/theme/density.ts`, `src/theme/fonts.tsx`, `src/theme/index.tsx`, `src/layout/logo/LogoMain.tsx`, `public/i18n/application_hu-HU.json`
- Pattern: Generator-ignore theme override with custom palette (orange primary `#DE4E0B`, navy secondary `#2F3257`), Source Sans 3 Variable font, Hungarian locale bundles (`huHU` for Material, DataGrid, DatePickers), custom density configuration, and custom logo
- Notable: Web-only variant without Capacitor status bar sync; uses `subtitleColor` palette extension for input label styling; density.ts customizes spacing multiplier (0.5), font size (1.2), and border radius (5); custom favicons and manifest.json in `.generator-ignore`
