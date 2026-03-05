---
id: "generator-ignore-rest-client"
title: "Generator-Ignore for REST Client File"
domain: "frontend"
category: "build"
score: 20.0
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - ams-frontend
---
## Description

Protect the generated REST API client file from being overwritten by the JUDO code generator by listing it in `.generator-ignore`. Unlike the common pattern of ignoring theme, layout, or i18n files, this pattern protects the REST client layer (`lib/{actor}/rest/{actor}.dart`), indicating that the generated REST client has been manually modified -- typically to add custom API endpoints, adjust serialization, or fix compatibility issues. This is an unusual and more risky customization since the REST client contains the entire API communication layer.

## Structure

```
.generator-ignore:
  lib/admin/rest/admin.dart       # Protected REST client for Admin actor
```

or:

```
.generator-ignore:
  lib/manager/rest/manager.dart   # Protected REST client for Manager actor
```

Each actor's `.generator-ignore` protects only its own REST client file, with no other files listed (no theme, layout, i18n, or customizer files). This is the most minimal `.generator-ignore` usage pattern seen.

## Examples

### ams-frontend
Admin actor's `.generator-ignore` contains only `lib/admin/rest/admin.dart`. Manager actor's contains only `lib/manager/rest/manager.dart`. Both protect the OpenAPI-generated REST client files, likely because the generated client needed manual adjustments for the custom campaign Excel download endpoint or Dart SDK compatibility. No theme, layout, or customizer files are protected -- all other files remain fully generated.

## Trade-offs

- **Pros**: Allows manual REST client modifications; fixes compatibility issues with generated API layer
- **Cons**: Most risky file to protect -- API changes require manual integration; model changes may add new endpoints that are not reflected; entire API communication layer becomes manually maintained
- **When to use**: Only when the generated REST client has bugs or needs custom endpoint integration that cannot be achieved through template overrides

## Related Patterns

- [generator-ignore-app-theme](generator-ignore-app-theme.md)
- [generator-ignore-i18n-layout](generator-ignore-i18n-layout.md)
- [flutter-generator-template-override](flutter-generator-template-override.md)
