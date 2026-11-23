---
id: generator-override-extra-dependencies
title: Generator Override for Extra NPM Dependencies
description: "Add extra npm dependencies to the generated frontend `package.json` through a Handlebars fragment override instead of editing or ignoring the generated file."
aliases: [extra npm dependencies, package.json fragment]
keywords: [generator-overrides, fragment, package.json, npm dependencies, handlebars, ui-react, regeneration]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "project:workflow-poc", "project:park-here", "status:emerging"]
category: build
status: emerging
projects: [rackinspect, workflow-poc, park-here]
evidence: ["rackinspect:application/generator-overrides/ui-react/actor/package.json.dependencies.extra.fragment.hbs", "workflow-poc:unrecorded"]
alternatives: []
related: [pdf-preview-inline-display, generator-ignore-app-theme]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Custom components often need npm packages the generated frontend does not include. Add them in a way that survives regeneration.

## Practice

### Platform base

- Generated files that need project-specific content expose named fragment extension points, marked in the file by paired comments. You fill one by placing a file with the same relative path and name in the override directory; such a file survives regeneration and needs no `.generator-ignore` entry. Fragments are Handlebars templates ([fragment overrides](../../agent-docs/deployment/build-process.md)). The documented worked example is for `app/pom.xml.extra-dependencies.fragment.hbs` on the backend side.
- The frontend override mechanism is the same: a template with the same name in `generator-overrides/` is used instead of the default, and the template name is shown in each generated file's header ([template override process](../../agent-docs/frontend/README.md)).
- Direct edits of a generated file fail the checksum unless the file is in `.generator-ignore` ([checksum protection](../../agent-docs/frontend/README.md)).

### Practice notes: a package.json dependencies fragment

Frontends name the fragment `package.json.dependencies.extra.fragment.hbs` and place it under `generator-overrides/ui-react/actor/` of the frontend application. The docs here do not list the frontend `package.json` fragment names, so confirm the name from the marker comment in your generated `package.json`.

The file holds only the extra entries, comma-separated:

```json
"@react-pdf-viewer/core": "^3.12.0",
"pdfjs-dist": "3.11.174",
```

- Pin versions that match each other (the PDF viewer packages and `pdfjs-dist` go together).
- Check conflicts with generated dependencies after regeneration; the fragment does not resolve version clashes.
- Keep a note of which custom component needs each package.

## Rationale

A fragment keeps generated and custom dependencies separate and needs no ignore entry, so `package.json` still receives generator updates.

## Example

- One app: three PDF viewer packages (`@react-pdf-viewer/core`, `@react-pdf-viewer/page-navigation`, `pdfjs-dist`) via the fragment, for inline PDF preview. `react-imask` is already in the generated dependencies.
- Another app instead lists `package.json` in `.generator-ignore` and edits it by hand to add `mermaid`, `svg-pan-zoom` and `react-syntax-highlighter` for its diagram and code-viewer elements. This works, but it loses generator updates to that file.

## When to avoid

- The package is already generated, check the generated `package.json` first.
- The fragment marker for your needed spot does not exist in your generated version: the file-ignore route is the fallback, see [[generator-ignore-app-theme]].

## Related

- [[pdf-preview-inline-display]] — the PDF viewer that needs these packages
- [[generator-ignore-app-theme]] — the ignore-file alternative
