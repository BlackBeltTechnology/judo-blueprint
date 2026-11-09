---
id: address-field-auto-composition
title: "Address Field Auto-Composition from Components"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - rackinspect
---

## Description

A frontend-only pattern for automatically composing a summary address text field from individual address component fields (street name, public place category, number, building, staircase, floor, door, lot number) via blur event hooks. When any component field loses focus, the composed `addressInformation` field is recalculated by concatenating non-empty components with appropriate separators. A `manualAddressInformation` boolean flag allows users to override auto-composition and manually edit the summary field. The pattern is implemented via form/view action hooks that register `onFieldBlurAction` handlers for each address component field. This is an implementation-only blueprint -- it provides a frontend UX enhancement for address forms.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
