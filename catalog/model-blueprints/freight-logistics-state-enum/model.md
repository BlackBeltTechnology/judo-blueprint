## Detection Query

```graphql
{ esm { enumerationtypes(where: { name: { like: "%FreightState%" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members including SUBMITTED, APPROVED, ARRIVED, and FINISHED.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "FreightState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "NOT_SUBMITTED", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "SUBMITTED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "REJECTED", ordinal: 3
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "APPROVED", ordinal: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "SUSPENDED", ordinal: 5
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "ARRIVED", ordinal: 6
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "FINISHED", ordinal: 7
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "DELAYED_UNLOADING", ordinal: 8
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::FreightState", name: "DELAYED_ARRIVAL", ordinal: 9
} }) { success fqn } }
```

## Examples

### reserve-app
- **FreightState enum**: `ReserveApp::entities::FreightState`
  - Members: NOT_SUBMITTED(1), SUBMITTED(2), REJECTED(3), APPROVED(4), SUSPENDED(5), ARRIVED(6), FINISHED(7), DELAYED_UNLOADING(8), DELAYED_ARRIVAL(9)
  - Used by: FreightReservation entity (state attribute)
  - Workflow: Partner creates reservation (NOT_SUBMITTED) -> submits to logistician (SUBMITTED) -> logistician approves (APPROVED) or rejects (REJECTED) -> vehicle arrives (ARRIVED) -> unloading completes (FINISHED)
  - Either party can suspend a reservation (SUSPENDED), tracked via suspendedByPartner and suspendedByLogistician relations to User
  - Delay states (DELAYED_ARRIVAL, DELAYED_UNLOADING) track schedule deviations
- Supports 5 actor roles (AdminActor, PartnerActor, LogisticianActor, DoormanActor, Readonly) that participate in different stages of the freight lifecycle
