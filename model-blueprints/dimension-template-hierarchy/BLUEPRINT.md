---
id: "dimension-template-hierarchy"
title: "Dimension Template Hierarchy (Template/Instance Pattern)"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A template/instance pattern for configurable measurement dimensions. A DimensionTemplate defines the structure: it has a name, a type enum (RACK or RACK_ELEMENT), and composes DimensionTemplateGroup entities. Each group has parameters (DimensionTemplateParameter) with name, label, order, valueType (NUMERIC/STRING/ENUM/BOOLEAN), isRequired, and optional selectableValues for enum-typed parameters. When a template is instantiated (e.g., during fault inspection), DimensionGroup instances are created mirroring the template structure, with DimensionParameter instances holding actual values (numericValue, stringValue, booleanValue, selectedValue). The group/parameter instances link back to their template counterparts. This pattern enables dynamic, configurable forms without code changes.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
