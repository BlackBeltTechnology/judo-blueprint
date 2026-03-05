---
id: sports-league-entity-cluster
title: "Sports League Entity Cluster (Season-Tournament-Match-Club-Team-Player)"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mjsz
---

## Description

A comprehensive entity cluster for modeling a sports league management system. The structure consists of six core entities organized in a hierarchical and relational network:

- **Season**: A time-bounded competitive period (e.g., "2022/2023") that contains tournaments. Has a `year` attribute and a bidirectional relation to tournaments.
- **Tournament**: A named competition (e.g., "Erste Liga") within a season. Contains matches via composition and links to participating teams. Derives its `year` from the parent season.
- **Club**: An organization (e.g., "Ferencvarosi TC") that owns teams via composition and has bidirectional association to players.
- **Team**: A club's entry in a specific tournament. Derives its name from the parent club via `container()` expression. Carries derived statistics (points, matches, goalsFor, goalsAgainst, goalsDifference) computed from match results. Links to tournament (1..1), players (0..*), homeMatches (0..*), and visitorMatches (0..*).
- **Player**: An individual athlete with personal details (firstName, lastName, dateOfBirth), a derived fullName, a sequence-generated identifier, and computed age. Has relations to club (0..1), licenses (0..* COMPOSITION), teams (0..*), and transfers (0..* COMPOSITION).
- **Match**: A game between two teams at a venue, with date/time, homeScore/visitorScore, and a derived result string. Links to homeTeam (1..1), visitorTeam (1..1), and venue (0..1). Carries derived win/draw/loss integer flags (0 or 1) used for aggregation in Team statistics.

Supporting entities:
- **License**: Validity period (dateOfIssue, dateOfExpiration) for a player, owned via composition.
- **Transfer**: Records a player's move between clubs with startDate, endDate, and a club reference.
- **Venue**: A physical location (name, city, address) where matches are played.

Key modeling patterns within this cluster:
- Bidirectional many-to-many between Tournament and Team, and between Team and Player
- Dual-relation match pattern: Match references both homeTeam and visitorTeam (same target type, different relation names)
- Derived integer flags (homeWin, draw, visitorWin returning 0/1) used with `!sum()` aggregation on Team to compute standings
- Container-based derived attributes using `self!container(Type).field` expressions
- Sequence-generated identifier on Player with `getVariable("SEQUENCE", "MJSZID")`

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Tournament" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Match" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Team" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

Look for entities with homeTeam/visitorTeam relations on a Match entity, or Tournament/Season/Club/Team hierarchical relations.

## Creation Mutations

### Season entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Season",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Season", name: "year"
} }) { success fqn } }
```

### Tournament entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Tournament",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Tournament", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Tournament", name: "season",
  target: "{{NAMESPACE}}::Season", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Tournament", name: "matches",
  target: "{{NAMESPACE}}::Match", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### Club entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Club",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Club", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Club", name: "teams",
  target: "{{NAMESPACE}}::Team", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

### Team entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Team",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Team", name: "tournament",
  target: "{{NAMESPACE}}::Tournament", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Team", name: "players",
  target: "{{NAMESPACE}}::Player", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Player entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Player",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Player", name: "firstName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Player", name: "lastName"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Player", name: "dateOfBirth"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Player", name: "club",
  target: "{{NAMESPACE}}::Club", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Match entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Match",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Match", name: "date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Match", name: "time"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Match", name: "homeScore"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Match", name: "visitorScore"
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Match", name: "homeTeam",
  target: "{{NAMESPACE}}::Team", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { twoWayRelationMember: {
  container: "{{NAMESPACE}}::Match", name: "visitorTeam",
  target: "{{NAMESPACE}}::Team", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Match", name: "venue",
  target: "{{NAMESPACE}}::Venue", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Venue entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Venue",
  createable: true, updateable: true, deleteable: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Venue", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Venue", name: "city"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Venue", name: "address"
} }) { success fqn } }
```

## Examples

### mjsz
The Hungarian Ice Hockey Federation (MJSZ) management system models a complete league hierarchy:

**Season** (`mjsz::Season`): createable/updateable/deleteable
- Attributes: year (String, required)
- Relations: tournaments (0..* ASSOCIATION to Tournament, bidirectional)

**Tournament** (`mjsz::Tournament`): createable/updateable/deleteable
- Attributes: name (String, required), year (String, DERIVED: `self.season.year`)
- Relations: teams (0..* ASSOCIATION to Team, bidirectional), matches (0..* COMPOSITION to Match), season (1..1 ASSOCIATION to Season, bidirectional)

**Club** (`mjsz::Club`): createable/updateable/deleteable
- Attributes: name (String, required)
- Relations: players (0..* ASSOCIATION to Player, bidirectional), teams (0..* COMPOSITION to Team)

**Team** (`mjsz::Team`): createable/updateable/deleteable
- Attributes: name (String, DERIVED: `self!container(mjsz::Club).name`), points (Integer, DERIVED), matches (Integer, DERIVED), goalsFor (Integer, DERIVED), goalsAgainst (Integer, DERIVED), goalsDifference (Integer, DERIVED: `self.goalsFor - self.goalsAgainst`)
- Relations: tournament (1..1 ASSOCIATION to Tournament), players (0..* ASSOCIATION to Player, bidirectional), homeMatches (0..* ASSOCIATION to Match, bidirectional), visitorMatches (0..* ASSOCIATION to Match, bidirectional)
- The `points` attribute uses: `3 * homeMatches!sum(m | m.homeWin) + homeMatches!sum(m | m.draw) + 3 * visitorMatches!sum(m | m.visitorWin) + visitorMatches!sum(m | m.draw)` (3 points for win, 1 for draw)

**Player** (`mjsz::Player`): createable/updateable/deleteable
- Attributes: firstName (String, required), lastName (String, required), fullName (String, DERIVED: `self.lastName + " " + self.firstName`), dateOfBirth (Date, required), age (Integer, DERIVED from dateOfBirth), identifier (String, required, identifier=true, default: sequence-generated "MJSZ" + padded sequence), licenseExpiration (Date, DERIVED: latest license expiration), clubName (String, DERIVED: `self.club.name`)
- Relations: club (0..1 ASSOCIATION to Club, bidirectional), licenses (0..* COMPOSITION to License), teams (0..* ASSOCIATION to Team, bidirectional), transfers (0..* COMPOSITION to Transfer)

**Match** (`mjsz::Match`): createable/updateable/deleteable
- Attributes: date (Date, required), time (Time, required), homeScore (Integer), visitorScore (Integer), result (String, DERIVED: `homeScore + ":" + visitorScore`), homeTeamName (String, DERIVED), visitorTeamName (String, DERIVED), venueName (String, DERIVED), venueAddress (String, DERIVED), season (String, DERIVED from container Tournament), tournament (String, DERIVED from container Tournament), homeWin (Integer, DERIVED: 1 if home wins else 0), draw (Integer, DERIVED: 1 if draw else 0), visitorWin (Integer, DERIVED: 1 if visitor wins else 0)
- Relations: homeTeam (1..1 ASSOCIATION to Team, bidirectional), visitorTeam (1..1 ASSOCIATION to Team, bidirectional), venue (0..1 ASSOCIATION to Venue)

**License** (`mjsz::License`): non-CRUD
- Attributes: dateOfIssue (Date, required), dateOfExpiration (Date, required), player (String, DERIVED from container Player)

**Transfer** (`mjsz::Transfer`): createable/updateable/deleteable
- Attributes: startDate (Date, required), endDate (Date), clubName (String, DERIVED: `self.club.name`)
- Relations: club (1..1 ASSOCIATION to Club)

**Venue** (`mjsz::Venue`): createable/updateable/deleteable
- Attributes: name (String, required), city (String, required), address (String, required)

**Transfer Objects**: Club, Player, Season, Tournament, Match, Team, Transfer -- all non-CRUD projections mapped to their respective entities, exposed via the Munkatars actor (anonymous, human).

**Actor**: Munkatars (anonymous human actor) with access to: season (0..*), tournament (0..*), player (0..*), club (0..*), match (0..*), transfer (0..*) -- all with full CRUD permissions.
