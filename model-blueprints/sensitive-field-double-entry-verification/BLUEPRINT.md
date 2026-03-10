---
id: sensitive-field-double-entry-verification
title: "Sensitive Field Double-Entry Verification UI"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
---

## Description

A frontend-only pattern for preventing data entry errors on sensitive numeric fields by requiring the user to enter the value twice. The primary field switches to password input type after losing focus (masking the entered value), and a secondary confirmation field must match before submission. Implemented as a custom visual element component that replaces a generated form group, using MUI TextField input type toggling (`'text'` on focus, `'password'` on blur) and conditional field enablement (the repeat field is disabled until the primary field has a value, and clears when the primary field is emptied). Used for exchange rate entry where incorrect values could have significant financial impact. This is an implementation-only blueprint -- it provides a frontend UX safeguard pattern.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
