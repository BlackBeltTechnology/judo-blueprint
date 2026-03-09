## Detection Query

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%Scoreboard%" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { transferobjecttypes(where: { name: { like: "%PersonalBest%" } }) {
  items { fqn name
    attributes { items { name } }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name defaultExpression } }
  }
} } }
```

Look for entities with a `personalBest` boolean attribute (default: false).

## Creation Mutations

### PersonalBest TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "PersonalBest"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::PersonalBest", name: "score"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::PersonalBest", name: "duration"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::PersonalBest", name: "playerName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::PersonalBest", name: "timestampOfFinished"
} }) { success fqn } }
```

### Scoreboard TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "Scoreboard"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::Scoreboard", name: "title"
} }) { success fqn } }
```

### personalBest flag on Test entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Test"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Test", name: "personalBest"
} }) { success fqn } }
```

## Examples

### trivia
- **PersonalBest TO** (`trivia::actors::player::PersonalBest`): mapped
  - Attributes: score, duration, playerName, timestampOfFinished -- all optional (display-only)
  - Projected from Test entity where personalBest=true, denormalizing the player's name from the User relation
- **Scoreboard TO** (`trivia::actors::player::Scoreboard`): mapped
  - Attributes: title (optional, the contest title)
  - Relations: personalBests (0..* AGGREGATION to PersonalBest)
  - Provides a ranked leaderboard for a contest
- **Player Contest TO** (`trivia::actors::player::Contest`):
  - Relations: scoreboard (0..1 ASSOC to Scoreboard), personalBests (0..* ASSOC to PersonalBest)
  - Players access the scoreboard and their personal bests from the contest view
- **Test entity** (`trivia::entities::Test`):
  - `personalBest` attribute (req, default: false) -- set to true when this test result is the player's best score for the contest
  - When a player submits a test, the backend compares the score against the player's previous best and updates the flag accordingly
- The personalBest flag acts as a materialized filter: rather than computing rankings on every query, the flag is updated on submission and the scoreboard simply queries tests where personalBest=true
