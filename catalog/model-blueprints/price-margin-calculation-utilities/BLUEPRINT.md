---
id: price-margin-calculation-utilities
title: Price/Margin Calculation Utility Library
description: A frontend-only shared utility library providing bidirectional price/margin/selling-price calculations using the gross margin formula.
aliases: []
keywords: [price, margin, calculation, utility, library, utilities]
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

A frontend-only shared utility library providing bidirectional price/margin/selling-price calculations using the gross margin formula. The library includes functions for computing selling price from cost price and margin, computing margin from cost price and selling price, and calculating standard selling price from time-based rates. All functions include null/zero guards and round results to configurable decimal places. The library is unit tested with comprehensive test coverage. It is consumed by multiple form action hooks (CostPrice creation, editing, and modification dialogs) to provide real-time price computation in form fields. This is an implementation-only blueprint -- it does not correspond to a specific model-level entity.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
