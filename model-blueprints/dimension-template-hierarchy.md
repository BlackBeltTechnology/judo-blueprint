---
id: dimension-template-hierarchy
title: "Dimension Template Hierarchy (Template/Instance Pattern)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---

## Description

A template/instance pattern for configurable measurement dimensions. A DimensionTemplate defines the structure: it has a name, a type enum (RACK or RACK_ELEMENT), and composes DimensionTemplateGroup entities. Each group has parameters (DimensionTemplateParameter) with name, label, order, valueType (NUMERIC/STRING/ENUM/BOOLEAN), isRequired, and optional selectableValues for enum-typed parameters. When a template is instantiated (e.g., during fault inspection), DimensionGroup instances are created mirroring the template structure, with DimensionParameter instances holding actual values (numericValue, stringValue, booleanValue, selectedValue). The group/parameter instances link back to their template counterparts. This pattern enables dynamic, configurable forms without code changes.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%DimensionTemplate%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "DimensionTemplateType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DimensionTemplateType", name: "{{TYPE_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "ValueType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ValueType", name: "NUMERIC", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ValueType", name: "STRING", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ValueType", name: "ENUM", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::ValueType", name: "BOOLEAN", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "DimensionTemplate",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplate", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplate", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::DimensionTemplate", name: "groups",
  target: "{{NAMESPACE}}::DimensionTemplateGroup", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "DimensionTemplateGroup",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateGroup", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateGroup", name: "order"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::DimensionTemplateGroup", name: "parameters",
  target: "{{NAMESPACE}}::DimensionTemplateParameter", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "DimensionTemplateParameter",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateParameter", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateParameter", name: "valueType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateParameter", name: "order"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateParameter", name: "label"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::DimensionTemplateParameter", name: "isRequired"
} }) { success fqn } }
```

## Examples

### rackinspect
**Template layer:**
- `DimensionTemplate` -- name, type (DimensionTemplateType: RACK/RACK_ELEMENT); composes groups (0..*)
- `DimensionTemplateGroup` -- name (req), label (req), order (req), attributePerRow (default: 3), multiLine (default: false), isRequired (default: false); composes parameters (0..*)
- `DimensionTemplateParameter` -- name (req), label (req), order (req), valueType (req, ValueType enum), isRequired (default: false), isInSimpleReviewReport (default: false); relations: unit (0..1 ASSOC to Unit), selectableValues (0..* ASSOC to SelectableValue)

**Instance layer:**
- `DimensionGroup` -- name (req), label (req), order (req), attributePerRow (default: 3), multiLine (default: false), isRequired (default: false); composes parameters (0..*) and rows (0..*); relation: dimensionTemplateGroup (1..1 ASSOC back to template)
- `DimensionGroupRow` -- order (req); composes parameters (0..*)
- `DimensionParameter` -- name (req), label (req), order (req), valueType (req), numericValue, stringValue, booleanValue, unitName, isRequired (default: false), isInSimpleReviewReport (default: false); relations: dimensionTemplateParameter (1..1 ASSOC), selectedValue (0..1 ASSOC to SelectableValue)

**Supporting entities:**
- `SelectableValue` -- name (req), order (req) -- predefined dropdown options for ENUM-typed parameters
- `ValueType` enum -- NUMERIC(1), STRING(2), ENUM(3), BOOLEAN(4)
- `DimensionTemplateType` enum -- RACK(1), RACK_ELEMENT(2)
