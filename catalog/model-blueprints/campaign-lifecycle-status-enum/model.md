## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%Status%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members including ONGOING, FINISHED, and DELETED.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "ONGOING", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "FINISHED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "DELETED", ordinal: 3
} }) { success fqn } }
```

## Examples

### indamedia-adtrack
- **CampaignStatus enum**: `AdTrack::entities::CampaignStatus` -- ONGOING(1), FINISHED(2), DELETED(3)
- Used by: `AggregatedCampaign` entity (status attribute, default: `AdTrack::entities::CampaignStatus#ONGOING`)
- AggregatedCampaign has time-bounded attributes: start, end, remainingDays
- Transfer object `AggregatedCampaignTransfer` exposes status for display
- `AggregatedCampaignUpdateInput` includes status field for state transitions
- `TrackedCampaignUpdateInput` also has a status field
- `deleteAggregatedCampaign` operation soft-deletes by setting status to DELETED
