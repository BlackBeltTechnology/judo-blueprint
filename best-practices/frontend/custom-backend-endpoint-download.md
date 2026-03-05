---
id: "custom-backend-endpoint-download"
title: "Custom Backend Endpoint Download via Handlebars Template"
domain: "frontend"
category: "component"
score: 20.0
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - ams-frontend
---
## Description

Add a custom file download feature that calls a non-standard backend API endpoint (outside the generated REST API) by creating a Handlebars template that generates a dedicated download function. The function constructs a custom URL (e.g., `{apiUrl}-custom/campaign/excel/{id}`), injects authentication headers, performs an HTTP GET, and triggers a browser download via Blob/AnchorElement. This pattern is used when the backend provides custom endpoints for file generation (Excel reports, PDFs, etc.) that are not part of the standard JUDO REST API. The template is registered in `flutter.yaml` as a new file generation rule.

## Structure

```
generator-overrides/
  templates/
    flutter.yaml                                    # Registers the new template
    flutter/
      lib/download_feature.dart.hbs                # Custom download function template
```

flutter.yaml registration:
```yaml
- overwriteExpression: true
  factoryExpression: "{#application}"
  pathExpression: >
    'lib/' + #path(#application.actor.name) + '/' + 'download_feature.dart'
  templateName: flutter/lib/download_feature.dart.hbs
```

Generated function pattern:
```dart
void downloadFeature(String id) async {
  var headers = {'Content-Type': 'application/octet-stream', 'Accept': 'application/octet-stream'};
  var url = await UrlUtil.getApiUrl();
  if (_auth.isAuthenticationRequired()) {
    headers['Authorization'] = 'Bearer ' + await _auth.getAccessToken();
  }
  url = url + '-custom/endpoint/' + id;
  Response res = await get(url, headers: headers);
  if (res.statusCode == 200) {
    final blob = html.Blob([res.bodyBytes]);
    // ... trigger browser download via AnchorElement
  }
}
```

The function is imported into page widgets via `package_extra.dart.hbs` and called from button `onPressed` handlers in generated view pages.

## Examples

### ams-frontend
`download_campaign_status_excel.dart.hbs` generates a `downloadCampaignStatusExcel(String id)` function per actor. It calls `{apiUrl}-custom/campaign/excel/{id}` with Bearer auth token, receives an octet-stream response, detects the MIME type via `mime_type` package, and triggers download using browser Blob + AnchorElement. Called from the Campaign View page's Download button. Additional dependencies (http, mime_type, url_launcher) are added via `pubspec.yaml.hbs` override.

## Trade-offs

- **Pros**: Clean integration of custom backend features into generated frontend; auth-aware; survives regeneration; applies to all actors
- **Cons**: Requires custom backend endpoint; bypasses generated REST API layer; browser-only (uses HTML APIs); template must match generator conventions
- **When to use**: When the backend provides specialized file generation endpoints (reports, exports) that need frontend download buttons

## Related Patterns

- [flutter-generator-template-override](flutter-generator-template-override.md)
- [url-type-field-download-override](url-type-field-download-override.md)
- [custom-public-assets](custom-public-assets.md)
