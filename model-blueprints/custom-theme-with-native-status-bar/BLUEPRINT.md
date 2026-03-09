---
id: custom-theme-with-native-status-bar
title: "Custom MUI Theme with Capacitor Status Bar Sync"
impl_only: true
usage_count: 2
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
  - park-here
---

## Description

A custom Material UI theme system that overrides the generated theme with project-specific branding (custom palette colors, dark mode support, locale bundles) and optionally synchronizes the Android status bar color with the theme mode via a custom Capacitor plugin (`StatusBarTheme`). Includes custom fonts, custom favicon/logo assets, and locale-specific translations. The theme files, i18n files, and layout files are listed in `.generator-ignore` to prevent regeneration. Projects may implement the full pattern with Capacitor integration or a web-only subset with just palette, font, and locale customizations.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
