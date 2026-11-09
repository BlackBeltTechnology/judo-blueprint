---
id: masked-input-integration
title: Masked Input Field Integration (react-imask)
description: A frontend-only pattern that replaces a generated form group with a custom element of masked text fields built on react-imask, for structured identifiers such as VAT IDs.
aliases: [input mask, masked text field]
keywords: [masked, input, field, integration, react, imask, mask, form]
tags: [domain:frontend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-09
---
## Intent

Structured identifiers (VAT IDs, tax numbers, phone numbers, postal codes) must match a fixed format while the user types. A generated form group cannot express that, so the group is replaced by a custom element that renders masked text fields. The model does not change: the attributes stay the same and only the input control differs.

### Masks live in the frontend, validation stays in the model

The mask shapes what the user can type. Business validation still comes from the model and the backend. The custom element reads the validation messages for each field and shows them as helper text.

## Structure

The pattern has no model shape of its own. It is a frontend element that replaces one generated group of attributes on one page. The element receives the stored data, the validation map, the edit mode, the store diff, the loading flag and the action helpers from the generated page. Each masked field is a text input with an input-mask component, a mask pattern and a placeholder character. The accepted (unmasked) value is written back to the store.

## Constraints

- The replacement targets one generated group on one page. The registration key is generated per page and per container, so it must be looked up from the generated page definition, not copied from another project.
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

- The format is only checked on save. A validation rule in the model is enough.
- The attribute is free text, or its format varies by country in ways one mask cannot cover.
- The frontend is not React. The mask library and the element interface are framework specific.

## Related

- [[organization-entity]] — an organization page that often carries identifier fields such as VAT numbers
- [[partner-with-contact-details]] — contact fields that can use the same masked-input approach
