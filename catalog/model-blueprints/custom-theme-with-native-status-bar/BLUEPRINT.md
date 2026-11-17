---
id: custom-theme-with-native-status-bar
title: Custom MUI Theme with Capacitor Status Bar Sync
description: A project-owned Material UI theme that overrides the generated theme (palette, density, fonts, locale) and can sync the Android status bar color with the theme mode through a Capacitor plugin.
aliases: [custom mui theme, theme override with status bar]
keywords: [theme, mui, palette, dark mode, capacitor, status bar, generator-ignore, locale]
tags: [domain:model, layer:frontend, project:mlszksz-platform, project:park-here, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, park-here]
evidence: [mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/android/app/src/main/java/hu/mlszksz/platform/StatusBarThemePlugin.java, mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/src/theme/index.tsx, park-here:unrecorded]
alternatives: [model-defined-color-palette]
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Brand a React application beyond what the model-defined palette gives: custom palette colors, dark mode, custom fonts, density and a non-default locale. On Capacitor Android, the native status bar follows the theme mode.

## Structure

The theme files under `src/theme/` are replaced by application code and listed in `.generator-ignore`, so the generator stops overwriting them. The pieces are a palette pair (light and dark), a theme builder that wires locale bundles and component overrides, a density configuration, a font setup, and optional i18n JSON and layout overrides. The native part is an optional Capacitor plugin (`StatusBarTheme`) that sets the Android background color, while `StatusBar` sets icon style. No model element is involved.

## Constraints

- A file listed in `.generator-ignore` no longer receives generator updates. Re-review it after every generator upgrade.
- Brand colors belong in the ActorType of the model when the app-wide palette is enough. Use an override only when the model palette cannot express the design. See [[model-defined-color-palette]].
- The status bar plugin runs only on native builds. Guard the calls so the web build does not fail.
- Locale bundles must cover every language the app ships, including the Material, DataGrid and DatePicker bundles.

## Variations

- **Full native variant.** Palette, fonts, density, locale and the Capacitor status bar sync. Used by the Android app.
- **Web-only variant.** Palette, fonts, density and locale, without the Capacitor plugin.
- **Logo and favicon only.** Replace assets in `public/` and the logo component, and keep the generated theme.

## When to use

- The brand needs colors, fonts or density the model cannot express.
- The app ships to Android through Capacitor and the status bar must match the theme.
- The app needs a locale the generator does not bundle.

## When to avoid

- The change is only a brand color. Set it on the ActorType instead.
- A per-card or per-table color change. Use a sub-theme. See [[model-defined-color-palette]].
- The app is a plain web app with no custom branding need.

## Related

- [[model-defined-color-palette]]: set brand colors in the model before writing theme code
- [[dark-theme-override]]: dark mode override pattern that this entry builds on
