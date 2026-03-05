---
id: "url-type-field-download-override"
title: "URL-Type Field to Download Button Override"
domain: "frontend"
category: "form"
score: 43.8
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---
## Description

Transform URL-type data fields from plain text display/input into interactive download buttons by overriding the generator templates for table columns and form inputs. When a field's data type matches a custom URL type, the template renders an `ElevatedButton` that calls a custom `downloadFile()` function instead of displaying the raw URL string. The download handler supports both internal file store references (with auth token injection) and external URLs, using the browser Blob API to trigger file downloads. Can be extended with upload functionality using `FilePicker` and multipart upload to a `FileService/~upload` endpoint.

## Structure

```handlebars
{{!-- In formatted.dart.hbs (table columns) --}}
{{#eq column.attributeType.dataType.name 'ModelName::types.URL'}}
  ElevatedButton(
    child: Text('Download'),
    onPressed: () { downloadFile(target.urlField); },
  ),
{{else}}
  {{!-- Standard formatting --}}
{{/eq}}

{{!-- In textinput.dart.hbs (form fields) --}}
{{#eq attributeType.dataType.name 'ModelName::types.URL'}}
  ElevatedButton.icon(
    label: Text(AppLocalizations.of(context).lookUpValue(context, 'label')),
    icon: Icon(getIconByString('icon_name')),
    onPressed: () { downloadFile(targetStore.urlField); },
  ),
{{/eq}}
```

The `downloadFile()` function handles internal references (`ModelFileStore:{id}` prefix) by constructing API URLs with Bearer auth tokens, and external URLs by direct HTTP GET, both triggering browser downloads via Blob/AnchorElement.

## Examples

### SkillMatrix
HR Employee actor's Report system uses URL-type fields for Excel report downloads. `formatted.dart.hbs` renders "Download" buttons in report result tables. `textinput.dart.hbs` renders icon buttons with localized labels in report view pages. `download.dart.hbs` handles `SkillMatrixFileStore:{id}` references via `FileService/~download/{id}` API endpoint with Bearer auth.

### kozut-eugyfel-client
Extends the download pattern with file UPLOAD capability. `upload.dart.hbs` adds `uploadFile()` using `FilePicker` to select files and `MultipartRequest` to upload to `FileService/~upload`. In create pages, URL-type fields render as "Select file" / "File uploaded" buttons. `textinput.dart.override.hbs` conditionally renders upload on create pages and download on view pages. Handles `e_ugyfelszolgalatFileStore:{id}` internal references.

### kozut-eugyfel-model-test
Model defines `e_ugyfelszolgalat::types.URL` custom data type used on image/file attachment fields (kep entity). Template overrides in companion client detect this type and render download/upload buttons instead of text inputs, with FileService API integration.

## Trade-offs

- **Pros**: Seamless download experience; applies to all URL-type fields globally; supports both internal and external files; auth-aware
- **Cons**: Template-level override affects all actors; requires custom data type in model; web-only implementation (uses browser Blob API); 3 extra npm/pub dependencies
- **When to use**: When the domain model includes downloadable file references that should display as buttons rather than raw URLs

## Related Patterns

- [flutter-generator-template-override](flutter-generator-template-override.md)
- [pdf-preview-inline-display](pdf-preview-inline-display.md)
