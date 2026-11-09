---
id: dimension-template-hierarchy
title: Dimension Template Hierarchy (Template/Instance Pattern)
description: A template/instance pattern for configurable measurement dimensions.
aliases: []
keywords: [dimension, template, hierarchy, instance]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A template/instance pattern for configurable measurement dimensions. A DimensionTemplate defines the structure: it has a name, a type enum (RACK or RACK_ELEMENT), and composes DimensionTemplateGroup entities. Each group has parameters (DimensionTemplateParameter) with name, label, order, valueType (NUMERIC/STRING/ENUM/BOOLEAN), isRequired, and optional selectableValues for enum-typed parameters. When a template is instantiated (e.g., during fault inspection), DimensionGroup instances are created mirroring the template structure, with DimensionParameter instances holding actual values (numericValue, stringValue, booleanValue, selectedValue). The group/parameter instances link back to their template counterparts. This pattern enables dynamic, configurable forms without code changes.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
