---
id: risk-level-enum
title: "Risk Level Enum (LOW/MEDIUM/HIGH)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - itracker
---

## Description

A three-level risk classification enumeration with members LOW, MEDIUM, and HIGH. This pattern models a simple ordinal risk assessment scale used as an attribute on domain entities to categorize items by their risk exposure. The enum is intentionally minimal -- three levels provide enough granularity for quick triage and dashboard filtering without overcomplicating the assessment process.

This pattern is suitable for project management, initiative tracking, issue triage, procurement risk assessment, compliance scoring, and any domain where items need a simple risk categorization for prioritization and reporting.

## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%Risk%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Also look for enumerations with exactly three members named LOW, MEDIUM, HIGH (or similar ordinal severity scales):

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "RiskLevel"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::RiskLevel", name: "LOW", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::RiskLevel", name: "MEDIUM", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::RiskLevel", name: "HIGH", ordinal: 3
} }) { success fqn } }
```

## Examples

### itracker
- **Enum**: `itracker::entities::RiskLevel` -- LOW(1), MEDIUM(2), HIGH(3)
- **Initiative entity** (`itracker::entities::Initiative`): uses `riskLevel` attribute to classify cost-saving initiatives by risk
  - The riskLevel attribute has no default value -- it must be set explicitly when creating an initiative
  - Used alongside other classification attributes: SavingType (FIXED/VARIABLE) and ActionType (PRICING/USAGE/LABOR/OEE/SCRAP)
- **User Initiative TO** (`itracker::actors::user::Initiative`): exposes `riskLevel` attribute for display and editing in the initiative form
