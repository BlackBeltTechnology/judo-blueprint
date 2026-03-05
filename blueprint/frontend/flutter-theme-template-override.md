---
id: "flutter-theme-template-override"
title: "Flutter Theme Customization via Handlebars Template Override"
domain: "frontend"
category: "theme"
score: 30.3
usage_count: 2
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
alternatives:
  - model-defined-color-palette
---
## Description

Customize the Flutter AppTheme and AppDesignCustomizer by overriding the `app_theme.dart.hbs` Handlebars template in `generator-overrides/templates/flutter/lib/`. This approach allows setting a fully custom color palette, typography, button styles, input decoration, and all AppDesignCustomizer methods at the template level, ensuring every generated actor app receives identical theming. Unlike model-defined color palettes (which only set 7 color slots), this gives full control over all ThemeData properties and the 30+ AppDesignCustomizer methods.

## Structure

```
generator-overrides/templates/flutter/
  lib/app_theme.dart.hbs          # Full theme template override
```

The template produces a complete `app_theme.dart` with two classes:
1. `AppTheme` - static `of(BuildContext)` method returning customized `ThemeData`
2. `AppDesignCustomizer` - extends `DefaultJudoComponentsCustomizer` with 30+ method overrides

Key customizable properties:
- Primary/secondary colors with alpha variants
- SourceSansPro font across all text themes (text, primary, accent)
- StadiumBorder buttons with custom padding
- Rounded-top input fields with underline emphasis
- Responsive content margin formula (linear interpolation 10-116px)
- Input box shadows, error states, label colors
- Breadcrumb, menu, tab bar, divider theming

## Examples

### kozut-eugyfel-client
Custom `app_theme.dart.hbs` sets deep blue (#002f5f) primary, orange (#ec6a04) secondary, off-white (#fafafa) background with semi-transparent variants (primaryVariant at 0xc0 alpha). All 3 actor apps receive identical theme. Includes custom display (#17191d) and body (#434448) text colors, 72px line height, 304px menu width, and the full responsive margin formula scaling 10-116px for 1300-2000px viewports.

### kozut-eugyfel-model-test
The ESM model defines the corporate color identity (KOZUT navy/orange) that the companion client implements via `app_theme.dart.hbs` override. Template provides full ThemeData and 30+ AppDesignCustomizer methods including StadiumBorder buttons, SourceSansPro typography, and responsive content margins.

## Trade-offs

- **Pros**: Complete theme control beyond model-defined palette slots; affects all actors uniformly; survives regeneration; can customize all AppDesignCustomizer methods
- **Cons**: Template must be maintained across generator version updates; Handlebars syntax required; no per-actor theme variation possible (all actors get same theme)
- **When to prefer model-defined-color-palette**: When only basic brand colors need changing and 7 color slots are sufficient

## Related Patterns

- [model-defined-color-palette](model-defined-color-palette.md)
- [flutter-app-design-customizer](flutter-app-design-customizer.md)
- [flutter-generator-template-override](flutter-generator-template-override.md)
