---
id: sensitive-field-double-entry-verification
title: Sensitive Field Double-Entry Verification UI
description: A frontend-only pattern for preventing data entry errors on sensitive numeric fields by requiring the user to enter the value twice.
aliases: [confirm field, repeat entry, masked confirmation input]
keywords: [sensitive, field, double, entry, verification, ui, mask, confirm, password]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: none: frontend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Prevent typing errors on a sensitive numeric field by making the user enter the value twice. After the user leaves the first field its value is masked, and a second field must hold the same value. The pattern is a frontend safeguard only. It adds nothing to the model's shape.

### The first entry is masked after blur

The primary field is shown as plain text while focused and as a password-type field after it loses focus. A masked value cannot be checked by eye, so the user has to type it again. Masking also stops the user from copying the first value into the second field.

### The second field depends on the first

The repeat field is disabled while the primary field is empty. When the primary field is cleared, the repeat field is cleared too.

## Structure

The shape is a frontend component, not a model element.

- The form's transfer object carries the sensitive value as an ordinary attribute, plus a second attribute for the repeat value. In the source project the repeat attribute is a transient attribute on the input transfer object, so nothing is stored. Both are plain numeric attributes in the generated form.
- A custom visual element replaces the generated group that holds the two fields. The element renders both inputs together, so the masking and the enable rule stay in one place.
- A companion form action hook on the same dialog can add other checks, for example blocking future dates.

## Constraints

- The comparison is a UI convenience. The server must still validate the value: a client can send any pair of values. Where the two fields must match, a server-side check in the operation or its validation compares them (project practice). See [validation hooks](../../agent-docs/frontend/hooks/validation-hooks.md).
- The component is registered under the key the framework generates for the group's page and container. Never copy the key from another form. See [advanced patterns](../../agent-docs/frontend/advanced-patterns.md).
- The generated form marks fields read-only when the form is not updateable. A replacement component must handle that itself, because it no longer uses the generated field components.
- Masking uses the browser's password input type. Password managers may offer to save or fill the field, so turn their autofill off for it.

## Variations

- **Match check in a validation hook.** Report a field error on the repeat field when the values differ, before the form is submitted.
- **Reveal toggle.** Add a show/hide control on the primary field for users who want to check the value.
- **Other value types.** The same pattern works for an account number or an e-mail address; only the input component changes.

## When to use

- A wrong value has a significant business or financial effect and is hard to correct later.
- The value is entered rarely, so the extra step is acceptable.

## When to avoid

- The field is entered often or in bulk. The second entry becomes a burden.
- A mistake is easy to undo. Use an ordinary field.
- The data comes from an import or an API, not from a form.

## Related

- [[exchange-rate-entity]] — the entity whose rate entry uses this safeguard
