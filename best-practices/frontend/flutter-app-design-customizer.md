---
id: "flutter-app-design-customizer"
title: "Flutter AppDesignCustomizer for Component Theming"
domain: "frontend"
category: "theme"
score: 61.8
usage_count: 4
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
alternatives:
  - dark-theme-override
---
## Description

The JUDO Flutter frontend uses an `AppDesignCustomizer` class (extending `DefaultJudoComponentsCustomizer` from `judo_flutter_components`) as the central component theming mechanism. Registered globally via `JudoComponentCustomizer.set()` at app startup, it overrides 30+ methods controlling layout constants (line height, menu width, padding), input field appearance (box shadows, decorations, error states), text styles for every UI element, and responsive content margins. The Material `ThemeData` is configured alongside this customizer in `app_theme.dart`.

## Structure

```dart
// app_theme.dart (generated per actor, identical across actors)
class AppDesignCustomizer with DefaultJudoComponentsCustomizer {
  // Layout
  int getLineHeight() => 72;
  double getMenuWidth() => 304.0;
  EdgeInsets getDefaultPadding() => EdgeInsets.symmetric(horizontal: 10);

  // Responsive margin
  double getContentMargin(BuildContext context) {
    // Linear interpolation: 10px at <=1300px, 116px at >=2000px
  }

  // Input fields
  Decoration getInputBoxCustomizer(bool disabled, bool readOnly) {
    return (disabled || readOnly) ? null : BoxDecoration(boxShadow: [...]);
  }

  // 30+ text style overrides for breadcrumbs, tables, switches, etc.
}

// In main.dart
JudoComponentCustomizer.set(AppDesignCustomizer());
```

Key theme properties: StadiumBorder buttons, rounded-top input fields with underline emphasis, SourceSansPro font, responsive margins.

## Examples

### SkillMatrix
All 3 actors share byte-identical `app_theme.dart` with dark blue-gray primary (#3c4166), orange-red accent (#e7501d), white cards on light gray (#fafafa) background. StadiumBorder (pill-shaped) buttons, 72px line height, 304px menu width, SourceSansPro font (all weights 100-900). Editable inputs get subtle box shadows; errors show red icons, red-tinted background, and bold error text.

### kozut-eugyfel-client
All 3 actors share a custom `app_theme.dart` delivered via Handlebars template override (`app_theme.dart.hbs`). Deep blue primary (#002f5f), orange accent (#ec6a04), government/corporate aesthetic. Same 30+ `AppDesignCustomizer` methods with identical layout constants (72px line height, 304px menu, 10-116px responsive margins). Custom color for `primaryVariant` and `secondaryVariant` with 75% alpha.

### kozut-eugyfel-model-test
Model-driven theming with corporate KOZUT colors (navy #002f5f, orange #ec6a04). The ESM model defines the actor visual identity while the companion client project overrides `app_theme.dart.hbs` to implement 30+ AppDesignCustomizer methods with custom input box shadows, StadiumBorder buttons, and SourceSansPro typography.

### ams-frontend
Both Admin and Manager actors share identical `app_theme.dart` with Invitech branding: primary #3C4166 (dark blue-gray), secondary #E7501D (orange-red), background #FAFAFA. StadiumBorder buttons, 72px line height, 304px menu width, SourceSansPro font. Mandatory fields marked with " *" suffix. Error fields use red-tinted background with bold error text.

## Trade-offs

- **Pros**: Comprehensive component-level control; single customizer class affects all widgets; consistent across all pages; generated from model
- **Cons**: Large class with many overrides; must understand `judo_flutter_components` API; changes require regeneration or manual edit of generated file
- **When to use**: Standard JUDO Flutter theming mechanism -- generated for all actors

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
- [model-defined-color-palette](model-defined-color-palette.md)
- [dark-theme-override](dark-theme-override.md)
