---
id: masked-input-integration
title: Masked Input Field Integration (react-imask)
description: "A frontend-only pattern for integrating masked input fields (via `react-imask` / `IMaskInput`) into JUDO forms by replacing a generated group component with a custom visual element that renders MUI TextFields with input masks."
aliases: []
keywords: [masked, input, field, integration, react, imask]
tags: ["domain:model", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

A frontend-only pattern for integrating masked input fields (via `react-imask` / `IMaskInput`) into JUDO forms by replacing a generated group component with a custom visual element that renders MUI TextFields with input masks. Commonly used for structured identifiers like VAT IDs, tax numbers, phone numbers, or postal codes where the input must conform to a specific format pattern. The custom component registers via `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY` and uses `IMaskInput` as the `inputComponent` prop on MUI TextField. This is an implementation-only blueprint -- it does not correspond to a specific model-level entity.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
