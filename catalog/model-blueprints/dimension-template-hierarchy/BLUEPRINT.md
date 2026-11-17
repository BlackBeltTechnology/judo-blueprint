---
id: dimension-template-hierarchy
title: Dimension Template Hierarchy (Template/Instance Pattern)
description: A template hierarchy of groups and typed parameters that defines configurable measurement dimensions, instantiated later as value-holding instances.
aliases: [dimension template, template instance hierarchy]
keywords: [dimension, template, hierarchy, group, parameter, value type, instance, composition]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: [rackinspect:model/rackinspect.model]
alternatives: [credential-generalization-hierarchy]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let administrators define the measurements that a check records, as data rather than code. The template describes the structure once; each check later copies it and fills in values.

## Structure

The template layer has three elements. A template holds groups in composition. A group holds parameters in composition. A parameter has a name and a value type from a four-member enumeration: NUMERIC, STRING, ENUM and BOOLEAN. The template layer is the definition; the instance layer, which holds the entered values, is a separate set of entities outside this shape.

## Constraints

- A template is administered, not created by users. It is not createable, updateable or deleteable from the generated interface; administrators maintain it through the group and parameter pages.
- Each parameter has exactly one value type. A change of value type after values exist is a data migration, not an edit.
- ENUM parameters need selectable values. Without them the input has no choices.
- Instance groups link back to their template group, so the link must be kept when a template is copied.

## Variations

- **Template per object type.** One template per kind of object, so each kind has its own set of groups.
- **Multi-line groups.** A group flagged as multi-line holds several rows of the same parameters.
- **Selectable values as a list.** Predefined choices for ENUM parameters, kept as a separate entity with an order.

## When to use

- Users must define the fields of a form without a code change.
- The same structure is filled in many times, each time with values.
- Groups and parameters have a fixed order and a fixed value type.

## When to avoid

- The fields are fixed and never change. A plain entity with attributes is simpler.
- Only one value per object is needed. A single attribute is enough.
- The values need their own history or audit. Add the history on the instance layer.

## Related

- [[credential-generalization-hierarchy]]: another hierarchy, built from a base type and subtypes
- [[self-referencing-derived-relation]]: a self-referencing relation for hierarchical data
- [[category-enum-pattern]]: choosing an enumeration for the value type
