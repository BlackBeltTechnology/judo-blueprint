---
id: masked-input-integration
title: "Masked Input Field Integration (react-imask)"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
---

## Description

A frontend-only pattern for integrating masked input fields (via `react-imask` / `IMaskInput`) into JUDO forms by replacing a generated group component with a custom visual element that renders MUI TextFields with input masks. Commonly used for structured identifiers like VAT IDs, tax numbers, phone numbers, or postal codes where the input must conform to a specific format pattern. The custom component registers via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` and uses `IMaskInput` as the `inputComponent` prop on MUI TextField. This is an implementation-only blueprint -- it does not correspond to a specific model-level entity.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
