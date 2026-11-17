---
id: masked-input-integration
title: Masked Input Field Integration (react-imask)
description: A frontend-only pattern that renders a group of text fields as a custom implementation element with react-imask masks, for structured identifiers such as VAT IDs; the model's own textMask is the first thing to try.
aliases: [input mask, masked text field]
keywords: [masked, input, field, integration, react, imask, mask, form]
tags: [domain:frontend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: []
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Structured identifiers (VAT IDs, tax numbers, phone numbers, postal codes) must match a fixed format while the user types. The platform already has a model-level answer: a string `DataField` with `textWidget=INPUT` and `textMultiLine=false` can carry a `textMask` pattern, and the generated form applies it. Use that first. When the mask needs behaviour the pattern string cannot give (placeholder handling, null for an empty mask, case normalization, a mix of masked and plain fields in one group), the group is built as a custom implementation element that renders masked text fields. The attributes stay the same; only the input control differs.

### Masks live in the frontend, validation stays in the model

The mask shapes what the user can type. Business validation still comes from the model and the backend. The custom element reads the validation messages for each field and shows them as helper text.

## Structure

The pattern has no model shape of its own beyond a UI element flagged as a custom implementation. The platform generates an extension point for such elements, and the frontend registers a React component for it (see the `frontend.md` and the platform's custom component replacement section). The element is not a replacement of an arbitrary generated component: the model has to expose it. In one project this is a group of VAT ID fields on an edit page. The element receives the stored data, the validation map, the edit mode, the store diff, the loading flag and the action helpers from the generated page. Each masked field is a text input with an input-mask component, a mask pattern and a placeholder character. The accepted (unmasked) value is written back to the store.

## Constraints

- The element must be marked as a custom implementation in the UI model. Its registration key is generated per element in the container's `customization.ts`, and the generated scaffold `register<Container>CustomImplementations.tsx.default` contains the register function with the correct props type. Take the key from there, not from another project.
- The props are those of the proxy props type in the scaffold. The names used here (`data`, `validation`, `editMode`, `storeDiff`, `isLoading`, `actions`) come from one project, so check them against the scaffold.
- The mask callback is used to capture the value. The change handler is not used, because it fires before the mask has settled.
- An empty mask (only placeholder characters) is stored as null, not as an empty string.
- Editability follows the generated flags: the field is read-only when the generated updateable flag is false or the field is disabled by the action helpers.

## Variations

- **Uppercase normalization.** Accepted values can be converted to upper case before they are stored, for identifiers that are case-insensitive.
- **Mixed masked and plain fields.** One group can contain masked fields and a plain text field with a maximum length, when only some identifiers have a fixed format.
- **Shared mask component.** Several pages can reuse one mask component, with the mask pattern passed in as a parameter.

## When to use

- A text attribute has a fixed, well-known format that users must follow while typing.
- The generated input is too permissive and validation messages alone are not enough.
- The page is a React frontend that already uses a mask library.

## When to avoid

- A model `textMask` pattern on the attribute is enough. It needs no custom code.
- The format is only checked on save. A validation rule in the model is enough.
- The attribute is free text, or its format varies by country in ways one mask cannot cover.
- The frontend is not React. The mask library and the element interface are framework specific.

## Related

- [[organization-entity]] — an organization page that often carries identifier fields such as VAT numbers
- [[partner-with-contact-details]] — contact fields that can use the same masked-input approach
