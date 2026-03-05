---
id: "flutter-frontend-framework"
title: "JUDO Flutter Frontend Framework"
domain: "frontend"
category: "framework"
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
  - zero-customization-generated-frontend
---
## Description

The JUDO platform supports Flutter/Dart as an alternative frontend framework to React/TypeScript. Flutter frontends are generated from the same ESM/UI models but produce Dart source files instead of TypeScript/React. The Flutter generator uses Handlebars (.hbs) templates, MobX for reactive state management, auto_route for navigation, get_it for dependency injection, and Dio for HTTP. Each actor becomes a standalone Flutter web application with its own entry point, router, and navigation drawer. Customization is achieved through Handlebars template overrides rather than Pandino hooks.

## Structure

```
project/
  model/
    Model-ui.model              # UI model (shared)
    Model-esm.model             # ESM model (shared)
  generator-overrides/
    templates/
      flutter.yaml              # Override registry
      flutter/                  # Handlebars template overrides
  model__actor__name/           # Per-actor Flutter app
    lib/
      main.dart                 # Entry point
      actor_name/
        app.dart                # Root MaterialApp + Drawer
        app_theme.dart          # Material theme + AppDesignCustomizer
        oauth.dart              # OAuth config
        auth/                   # Auth implementations
        config/                 # Table configuration
        injector/               # get_it DI setup
        l10n/                   # ARB localization
        repository/             # Repository API wrappers
        rest/                   # OpenAPI-generated REST client
        store/                  # MobX stores (one per entity)
        ui/
          pages/                # Generated page widgets
          routes/               # auto_route router
          navigation/           # NavigationState (MobX)
          widgets/              # Shared UI widgets
    assets/                     # Images
    fonts/                      # Font files
    web/                        # Web-specific (favicon, manifest)
    test/                       # Widget tests
```

Key technology stack:
- **State**: MobX (`flutter_mobx`, `mobx`)
- **Routing**: auto_route (`@MaterialAutoRouter`)
- **DI**: get_it + injectable
- **HTTP**: Dio + OpenAPI
- **Components**: `judo_flutter_components` library

## Examples

### SkillMatrix
Three actor Flutter web apps (Admin: 147 files, HR Employee: 1,093 files, Professional: 994 files) totaling 2,237 Dart source files. All generated from the same UI model with 6 Handlebars template overrides for file download functionality. Uses Flutter SDK >=2.7.0 <3.0.0, SourceSansPro font, and OAuth authentication.

### kozut-eugyfel-client
Three actor Flutter web apps (Munkatars: ~1,200 files, Admin: ~1,000 files, E-Ugyfel: ~330 files) totaling ~2,530 Dart files. 12 Handlebars template overrides including download, upload, custom theme, user widget, and logo. Uses deep blue (#002f5f) and orange (#ec6a04) palette. Public citizen portal actor supports anonymous access.

### kozut-eugyfel-model-test
ESM model defining 3 actors (Admin, Munkatars, EugyfelAlkalmazas) with 16+ entity stores, 7 enums, and bound operations. Model drives generation of ~2,530 Dart files in companion client project. Defines clone-edit-save workflow and bound operation input/output pages.

### ams-frontend
Two actor Flutter web apps (Admin: 250 Dart files, Manager: 411 files) for application access management. 7 Handlebars template overrides adding custom Excel download, widget overrides, and Invitech branding. Uses Dart SDK >=2.7.0 <3.0.0, SourceSansPro font, and older `auto_route` 0.6.9.

## Trade-offs

- **Pros**: Cross-platform potential (web, mobile, desktop from same codebase); strongly typed Dart; rich widget library; three-layout responsive system built in
- **Cons**: Smaller JUDO community than React; fewer customization hooks (no Pandino service registry); template overrides less granular than React hook overrides; older Flutter SDK version
- **When to use**: When mobile/cross-platform deployment is desired, or when the team has Flutter expertise

## Related Patterns

- [zero-customization-generated-frontend](zero-customization-generated-frontend.md)
- [flutter-generator-template-override](flutter-generator-template-override.md)
- [flutter-mobx-store-architecture](flutter-mobx-store-architecture.md)
