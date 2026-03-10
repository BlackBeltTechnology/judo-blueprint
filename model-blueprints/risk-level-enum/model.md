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
