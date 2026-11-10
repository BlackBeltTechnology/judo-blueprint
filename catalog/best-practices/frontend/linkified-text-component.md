---
id: linkified-text-component
title: Linkified Text Component for Long Text Fields
description: "A small custom React component that renders plain text with http and https URLs as safe external links, used in custom views for long description fields while the stored text stays plain."
aliases: [auto link text, clickable urls in text]
keywords: [linkify, url, link, text, typography, noopener, long text, custom view]
tags: ["domain:frontend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: component
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/src/custom/components/LinkifiedText.tsx"]
alternatives: []
related: [custom-component-directory, custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Make URLs inside long text attributes (descriptions, announcements) clickable without storing markup in the model. Users paste links as plain text; the view shows them as links.

## Practice

### Platform base

- Custom views and components belong in the project's custom directory and are wired in through the generated hook scaffolds ([extension points](../../agent-docs/frontend/extension-points.md)).

### Project practice: a presentational component, used by custom views (mlszksz-platform)

- It is not registered as a replacement of the generated text field. Custom detail views, registered through container hooks, import it and use it where they would otherwise print the text attribute. Generated forms keep the standard input. Whether a text-field visual element can be overridden the same way is *verify*.
- A pure `parseText` function splits the text into text and link parts with an `https?://` regex. It is exported so it can be unit tested apart from React.
- Trailing punctuation (`. , ) ! ?`) is moved out of the link. A match ending in `...` is left as text, because a server-side truncated URL would link to the wrong address.
- Links open with `target="_blank"` and `rel="noopener noreferrer"`, and the click handler stops propagation so a link inside a clickable card does not trigger the card's navigation.
- Text without a URL takes a fast path and renders as plain typography. Text is always rendered as React children, never as HTML, so no escaping step is needed.
- Wrapper styling (`whiteSpace: 'pre-wrap'`, word break) is passed in by the caller, so line breaks in the stored text survive.
- Only URLs are detected; mentions are not handled in the project.

## Rationale

Plain text storage stays simple and safe. The cost is a small regex that can mis-split unusual URLs, such as one ending in a parenthesis that belongs to it.

## Example

mlszksz-platform shows feed descriptions in four detail views and in the feed card with this component.

## When to avoid

- The text is rich text or markdown; use a renderer for that format.
- Only an editing form is needed; links in input fields are not useful.

## Related

- [[custom-component-directory]] — where custom components live
- [[custom-visual-element-override]] — replacing generated elements instead of using a component in a custom view
