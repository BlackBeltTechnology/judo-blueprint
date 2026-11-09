## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with exactly two members where one represents an active/enabled state and the other represents an inactive/archived/closed state.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{STATUS_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{STATUS_NAME}}", name: "{{ACTIVE_MEMBER}}", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{STATUS_NAME}}", name: "{{INACTIVE_MEMBER}}", ordinal: 2
} }) { success fqn } }
```

## Examples

### viterra_demo
- **Enum**: `viterra::Status` -- ACTIVE(1), INACTIVE(2)
- Not directly used as a status attribute on any entity in this model
- Instead, Client and Silo entities each have a boolean `active` attribute for the same purpose
- The enum exists alongside the boolean flags, suggesting it may be intended for future use or for expression-based filtering

### sanctuary-backend
- **Enum**: `Sanctuary::ActiveStatus` -- active(1), archived(2)
- Named "ActiveStatus" rather than "Status", with lowercase member names and "archived" instead of "inactive"
- Used as the `status` attribute on both the `User` entity and the `PositionTitle` entity
- The "archived" semantics suggest data is preserved for reference but no longer actively used, rather than simply being toggled off
- This is the first observed variant where the second state uses "archived" instead of "inactive"

### kozut-eugyfel-client
- **Enum**: `e_ugyfelszolgalat::entities::BejelentesAllapot` -- AKTIV(1), LEZART(2)
- Hungarian-language variant meaning "Report Status" with ACTIVE and CLOSED members
- Used as the `allapot` (status) required attribute on the Bejelentes (Report/Ticket) entity
- The AKTIV state represents an open ticket under processing; LEZART represents a resolved/closed ticket
- The Munkatars (Worker) actor separates active and closed tickets into two different access points: `aktivBejelentesek` (active reports) and `lezartBejelentesek` (closed reports)
- State transitions are controlled by operations: `lezaras` (closure) moves from AKTIV to LEZART, `megnyitas` (reopening) moves from LEZART to AKTIV
- Permission guard DERIVED booleans (lezarasEngedely, megnyitasEngedely) control which operations are available based on the current state
