---
id: "generator-override-extra-dependencies"
title: "Generator Override for Extra NPM Dependencies"
domain: "frontend"
category: "build"
score: 59.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - workflow-poc
---
## Description

Add extra npm dependencies to the generated `package.json` without modifying the generated file directly. The JUDO generator supports Handlebars fragment files that are injected into the generated output. By placing a `package.json.dependencies.extra.fragment.hbs` file in `generator-overrides/ui-react/actor/`, additional dependencies are merged into the generated `package.json` dependencies block during code generation.

## Structure

```
application/
  frontend-react/
    generator-overrides/
      ui-react/
        actor/
          package.json.dependencies.extra.fragment.hbs
```

Fragment file content (comma-separated JSON entries):
```json
"@react-pdf-viewer/core": "^3.12.0",
"@react-pdf-viewer/page-navigation": "^3.12.0",
"pdfjs-dist": "3.11.174",
```

Note: The trailing comma is handled by the generator's template merging.

## Examples

### RackInspect
Adds three PDF viewer dependencies (`@react-pdf-viewer/core`, `@react-pdf-viewer/page-navigation`, `pdfjs-dist`) via `package.json.dependencies.extra.fragment.hbs`. These support inline PDF preview for assessment sheet and review report documents. The `react-imask` library used for VAT ID masking is already included in the base generated dependencies.

### workflow-poc
Adds visualization dependencies via `package.json` (protected in `.generator-ignore`): `mermaid` (^11.4.1) for diagram rendering, `svg-pan-zoom` (^3.6.2) for interactive diagram navigation, and `react-syntax-highlighter` (^15.6.1) for code syntax highlighting. These support the Mermaid and CodeViewer custom visual elements.

## Trade-offs

- **Pros**: Survives regeneration; no `.generator-ignore` needed for package.json; clean separation of generated and custom dependencies
- **Cons**: Fragment file syntax must match generator expectations; version conflicts possible with generated dependencies; no lock file management
- **When to use**: Whenever custom components require npm packages not included in the generated dependencies

## Related Patterns

- [pdf-preview-inline-display](pdf-preview-inline-display.md)
- [generator-ignore-app-theme](generator-ignore-app-theme.md)
