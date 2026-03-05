---
id: "flutter-generator-template-override"
title: "Flutter Generator Handlebars Template Override"
domain: "frontend"
category: "build"
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
  - generator-override-extra-dependencies
---
## Description

Customize the JUDO Flutter code generator output by overriding specific Handlebars (.hbs) templates. Override files are placed in `generator-overrides/templates/flutter/` at the same relative path as the original generator template. A `flutter.yaml` file registers completely new templates (not just overrides). This is the primary customization mechanism for Flutter frontends, analogous to the React hook/Pandino system but operating at code generation time rather than runtime.

## Structure

```
generator-overrides/
  templates/
    flutter.yaml                          # Registry for new templates
    flutter/
      lib/download.dart.hbs              # New file template
      lib/upload.dart.hbs                # New file template
      lib/app_theme.dart.hbs             # Override theme template
      lib/ui/pages/page/package_extra.dart.hbs  # Override existing template
      lib/ui/pages/widgets/formatted.dart.hbs   # Override column rendering
      lib/ui/pages/widgets/textinput.dart.hbs   # Override input rendering
      lib/ui/widgets/user.dart.hbs       # Override user widget
      pubspec.yaml.hbs                   # Override dependencies
      pubspec.flutter.yaml.hbs           # Override flutter section
      pubspec.dependency_overrides.yaml.hbs  # Override dep overrides
      assets/mk_logo.png                # Copy custom assets
```

flutter.yaml registration for new templates:
```yaml
- overwriteExpression: true
  factoryExpression: "{#application}"
  pathExpression: >
    'lib/' + #path(#application.actor.name) + '/' + 'download.dart'
  templateName: flutter/lib/download.dart.hbs
```

Templates placed at matching paths automatically override without yaml registration.

## Examples

### SkillMatrix
Six Handlebars template overrides (~200 lines total): (1) `download.dart.hbs` adds a file download handler using browser Blob API with auth token injection for internal file store references, (2) `package_extra.dart.hbs` adds download/url_launcher imports to all pages, (3-4) `formatted.dart.hbs` and `textinput.dart.hbs` transform URL-type fields into download buttons, (5) `pubspec.yaml.hbs` adds url_launcher, mime_type, file_picker dependencies.

### kozut-eugyfel-client
Twelve Handlebars template overrides -- the most extensive Flutter override set found. Adds file download AND upload functionality (download.dart.hbs + upload.dart.hbs), overrides app_theme.dart.hbs with custom blue/orange palette, overrides user.dart.hbs to show mk_logo.png, provides custom pubspec sections (dependencies, flutter assets/fonts, dependency_overrides with custom git refs for openapi_generator), and copies a custom logo asset.

### kozut-eugyfel-model-test
Model project paired with 12 Handlebars overrides in companion client. Overrides cover file I/O (download + upload), theme (app_theme.dart.hbs with navy/orange palette), URL-type field rendering, and dependency management.

### ams-frontend
Seven Handlebars template overrides: (1) `download_campaign_status_excel.dart.hbs` adds custom Excel download via `-custom/campaign/excel/{id}` endpoint with auth headers, (2) `package_extra.dart.hbs` adds extra imports to page packages, (3-4) `formatted.dart.override.hbs` and `textinput.dart.override.hbs` override widget rendering, (5-7) three pubspec overrides adding http, url_launcher, mime_type, file_picker dependencies plus SourceSansPro font and Invitech logo asset. flutter.yaml registers the download function and logo copy rule.

## Trade-offs

- **Pros**: Changes apply to all generated pages automatically; survives regeneration; powerful template-level control over any generated output
- **Cons**: Requires Handlebars template knowledge; changes affect all actors globally; harder to target individual pages; must maintain template compatibility with generator updates
- **When to use**: When a new data type, widget pattern, or cross-cutting functionality needs to be added to all generated Flutter pages

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
- [generator-override-extra-dependencies](generator-override-extra-dependencies.md)
