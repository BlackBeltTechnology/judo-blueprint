## Overview

A custom Material UI theme with project-specific branding, dark mode support, locale bundles, and optionally Capacitor native status bar synchronization. Framework: React, optionally on Capacitor Android.

## Implementation Pattern

The theme system replaces the generated theme files. Each replaced file is listed in `.generator-ignore` so the generator does not overwrite it. The platform also offers a lighter route: a same-named file in the application's `actor/src/theme/` override directory replaces one theme fragment without ignoring all of `index.tsx`, which the theming guide prefers when only one component's styling changes ([theming](../../agent-docs/frontend/theming.md), Theme Override Fragments). The brand palette itself is model-driven (ActorType colors render into `palette.ts`); the full replacement below is project practice for needs the model cannot express:

- **palette.ts** (`src/theme/palette.ts`): custom `paletteThemeLight` and `paletteThemeDark` with project primary and secondary colors, text colors and background colors. Both usually add a `subtitleColor` palette extension, declared with MUI module augmentation.
- **index.tsx** (`src/theme/index.tsx`): the MUI theme builder. It wires locale bundles (for example `huHU` for Material, DataGrid and DatePickers), component overrides and typography, and on Capacitor it calls the status bar plugin.
- **density.ts** (`src/theme/density.ts`): spacing multiplier, font size, button size, border radius, DataGrid density and main margins.
- **fonts.tsx** (`src/theme/fonts.tsx`): the font family, loaded through `@fontsource-variable`.
- **index.css** (optional): custom `@font-face` rules and CSS overrides.
- **Status bar** (optional, Capacitor only): `StatusBar.setStyle()` sets the icon style, and the `StatusBarTheme` plugin sets the Android background color.
- **i18n** files such as `public/i18n/application_hu-HU.json`, listed in `.generator-ignore`.
- **Assets**: logo, favicons and `manifest.json` in `public/`, listed in `.generator-ignore`.
- **Layout overrides** (optional): files such as `src/layout/logo/LogoMain.tsx`, listed in `.generator-ignore`.

### Status bar sync is native-only

Call the status bar plugin only when the app runs inside Capacitor. A web build must skip the call, or the plugin lookup fails at runtime.

```tsx
import { Capacitor } from '@capacitor/core';

export const syncStatusBar = async (isDark: boolean) => {
  if (!Capacitor.isNativePlatform()) return;
  await StatusBar.setStyle({ style: isDark ? Style.Dark : Style.Light });
  await StatusBarTheme.setColor({ color: isDark ? '#1B1D2E' : '#FFFFFF' });
};
```

`StatusBar` and `StatusBarTheme` are project code, not generated code.

## Examples

### mlszksz-platform
- Framework: React (Capacitor Android)
- Key files: `src/theme/palette.ts`, `src/theme/index.tsx`, `src/theme/index.css`, `custom/utilities/status-bar-theme.ts`, `public/i18n/application_hu-HU.json`, `public/i18n/system_hu-HU.json`
- Pattern: generator-ignore theme override with custom palette, Hungarian locale and the Capacitor StatusBar plugin for native status bar sync
- Notable: `StatusBarTheme` is a custom Capacitor plugin for the Android status bar color; the Plus Jakarta Sans font is custom; layout files are overridden for platform-aware logout

### park-here
- Framework: React (web)
- Key files: `src/theme/palette.ts`, `src/theme/density.ts`, `src/theme/fonts.tsx`, `src/theme/index.tsx`, `src/layout/logo/LogoMain.tsx`, `public/i18n/application_hu-HU.json`
- Pattern: generator-ignore theme override with custom palette, Source Sans 3 Variable font, Hungarian locale bundles (`huHU` for Material, DataGrid and DatePickers), custom density and custom logo
- Notable: web-only variant with no Capacitor status bar sync; uses the `subtitleColor` palette extension for input labels; density customizes the spacing multiplier, font size and border radius; custom favicons and `manifest.json` are in `.generator-ignore`
