---
id: "flutter-user-widget-template-override"
title: "Flutter User Widget and Drawer Logo Override"
domain: "frontend"
category: "layout"
score: 32.3
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---
## Description

Override the Flutter navigation drawer's user identity widget via a Handlebars template override to display a custom organization logo alongside user information. The `user.dart.hbs` template is placed in `generator-overrides/templates/flutter/lib/ui/widgets/` and replaces the default user widget with a custom version showing an organization logo (from custom assets), the authenticated user's name, and their email. This customizes the drawer branding for all actors without modifying generated code.

## Structure

```
generator-overrides/templates/flutter/
  lib/ui/widgets/user.dart.hbs    # User widget template override
  assets/mk_logo.png              # Custom logo asset (copy rule)
```

```yaml
# flutter.yaml - asset copy registration
- overwriteExpression: false
  factoryExpression: "{#application}"
  pathExpression: "'assets/mk_logo.png'"
  templateName: flutter/assets/mk_logo.png
  copy: true
```

The generated widget uses `AssetImage('assets/mk_logo.png')` and displays user name and email from `auth.getAuthInfo()` using `JudoComponentCustomizer.get()` text styles.

## Examples

### kozut-eugyfel-client
Custom `user.dart.hbs` displays the Magyar Kozut (Hungarian Road) organization logo (`mk_logo.png`, 80x43px) above the user's name and email in the navigation drawer. The asset is deployed via a `copy: true` rule in `flutter.yaml` with `overwriteExpression: false` to avoid overwriting on regeneration. Applied identically across all 3 actor apps (Munkatars, Admin, E-Ugyfel).

### kozut-eugyfel-model-test
Model project paired with user widget override in companion client. The MK (Magyar Kozut) logo branding is applied consistently across all 3 actors defined in the ESM model via the shared template override mechanism.

## Trade-offs

- **Pros**: Branded drawer across all actors; survives regeneration; simple template override; custom asset deployment built in
- **Cons**: Affects all actors equally (no per-actor branding); template must match generator's expected API; asset must be small for performance
- **When to use**: When the organization requires custom branding in the navigation drawer of a JUDO Flutter application

## Related Patterns

- [custom-public-assets](custom-public-assets.md)
- [flutter-generator-template-override](flutter-generator-template-override.md)
