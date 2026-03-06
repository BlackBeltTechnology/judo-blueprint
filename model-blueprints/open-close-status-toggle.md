---
id: "open-close-status-toggle"
title: "Open/Close Two-State Status Toggle with Operations"
score: 36.7
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
  - ams-model
  - skillmatrix-model
---
## Description

A two-state status enumeration with OPEN and CLOSED members, paired with `open` and `close` instance operations on the entity for toggling between states. The entity starts in the CLOSED state (default) and can be opened to allow participation/access, then closed again to stop it. In some variants, the entity defaults to OPEN instead of CLOSED. In some variants, the toggle uses a boolean `closed` attribute (default: false) instead of a status enum. This pattern models time-bounded or admin-controlled availability windows -- contests, registration periods, enrollment windows, campaigns, training plans, or any entity that needs to be explicitly activated and deactivated.

Unlike the DRAFT/DONE pattern (which is linear and terminal), the OPEN/CLOSED pattern is cyclical: the entity can be opened and closed repeatedly. Unlike the ACTIVE/SUSPENDED pattern (which implies user account management), OPEN/CLOSED is typically used for event or period entities where availability is the primary concern.

The transfer object exposes the open and close operations as MAPPED operations, and may add derived boolean attributes (e.g., `isClosed`, `isOpen`) to control UI visibility of the operations. Some variants add a `load` operation for bulk data import when the entity is in an empty state.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with members OPEN and CLOSED.

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name defaultExpression } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities with `open` and `close` operations and a status attribute defaulting to a CLOSED or OPEN enum value, or a `closed` boolean attribute.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "OPEN", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}Status", name: "CLOSED", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{ENTITY_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "open",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}.open"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{ENTITY_NAME}}", name: "close",
  operationType: "INSTANCE", binding: "{{NAMESPACE}}::{{ENTITY_NAME}}.close"
} }) { success fqn } }
```

### Transfer object with guard attribute

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{ENTITY_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}", name: "isClosed"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}", name: "open",
  operationType: "INSTANCE", binding: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}.open"
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}", name: "close",
  operationType: "INSTANCE", binding: "{{SERVICE_NAMESPACE}}::{{ENTITY_NAME}}.close"
} }) { success fqn } }
```

## Examples

### trivia
- **ContestStatus enum**: `trivia::entities::ContestStatus` -- OPEN(1), CLOSED(2)
- **Contest entity**: `trivia::entities::Contest` (non-CRUD)
  - Attributes: status (req, default: ContestStatus#CLOSED), title (req), numberOfQuestions (req), responseTime (req), description (optional)
  - Relations: fixedQuestions (0..* ASSOC), tests (0..* ASSOC), categories (0..* ASSOC), questions (0..* DERIVED)
  - Operations: open (INSTANCE), close (INSTANCE), enter (INSTANCE)
  - The `enter` operation creates a new Test for a player joining the contest (only allowed when status is OPEN)
- **Admin Contest TO** (`trivia::actors::admin::Contest`):
  - Attributes: status (req), title (req), numberOfQuestions (req), isClosed (optional, derived guard), responseTime (req), description (optional)
  - Relations: categories (0..* ASSOC), fixedQuestions (0..* ASSOC)
  - Operations: open (MAPPED), close (MAPPED)
  - The `isClosed` guard attribute controls when the open/close operations are available in the UI
- **Player Contest TO** (`trivia::actors::player::Contest`):
  - Attributes: title, description -- read-only view for players
  - Relations: scoreboard (0..1 ASSOC), personalBests (0..* ASSOC)
  - Operations: enter (MAPPED) -- allows the player to join the contest

### ams-model
- **CampaignStatus enum**: `ams::entities::CampaignStatus` -- OPEN(1), CLOSED(2)
- **Campaign entity**: `ams::entities::Campaign` (non-CRUD)
  - Attributes: startDate (Date), finishDate (Date), status (CampaignStatus, req, default: CampaignStatus#OPEN)
  - Relations: confirmationRequests [0..*] COMPOSITION ConfirmationRequest, applications [0..*] ASSOC Application
  - Operations: open (INSTANCE), close (INSTANCE), load (INSTANCE)
  - The `open` operation sets `this.status = CampaignStatus#OPEN`
  - The `close` operation sets `this.status = CampaignStatus#CLOSED`
  - The `load` operation bulk-creates ConfirmationRequest entries for the campaign from user/application data
- **Admin Campaign TO** (`ams::actors::admin::Campaign`, maps Campaign):
  - Attributes: startDate (MAPPED), finishDate (MAPPED), status (MAPPED), download (DERIVED, CampaignDocument type), ratio (DERIVED: shows completed/total count as "X/Y" string), isOpen (DERIVED guard: `self.status == CampaignStatus#OPEN`), isClosed (DERIVED guard: `self.status == CampaignStatus#CLOSED`), isEmpty (DERIVED guard: `self.confirmationRequests!count() == 0`)
  - Relations: confirmationRequests [0..*] AGGREGATION ConfirmationRequest, applications [0..*] AGGREGATION Application
  - Operations: close (MAPPED, enabledBy: isOpen, with mandatory confirmation), open (MAPPED, enabledBy: isClosed, with mandatory confirmation), load (MAPPED, enabledBy: isEmpty)
  - Three derived guard attributes control operation availability: isOpen enables close, isClosed enables open, isEmpty enables load
- This variant defaults to OPEN (unlike trivia which defaults to CLOSED) since campaigns are created in an active state
- The Campaign entity uses COMPOSITION for confirmationRequests, making the campaign the lifecycle owner of its requests
- Adds a `load` operation for bulk data import, guarded by isEmpty so it can only be run on empty campaigns
- The ratio DERIVED attribute provides a progress summary string (e.g., "15/12" for 15 total, 12 decided)

### skillmatrix-model
- **No status enum** -- uses a `closed` boolean attribute (default: false) instead of an OPEN/CLOSED enum
- **TrainingPlan entity**: `SkillMatrix::TrainingPlan` (non-CRUD)
  - Attributes: date (Date, default: `SkillMatrix::types::Date!now()`), closed (Boolean, default: false), description (Text)
  - Relations: notes [0..*] COMPOSITION Note, skillTargets [0..*] COMPOSITION SkillTarget, incompleteSkillTargets [0..* DERIVED SkillTarget]
  - Operations: close (INSTANCE), open (INSTANCE)
  - The `close` operation sets the `closed` boolean to true
  - The `open` operation sets the `closed` boolean to false
- **Manager TrainingPlan TO** (`actor::manager::TrainingPlan`, maps TrainingPlan):
  - Attributes: closed (DERIVED), date (MAPPED), description (MAPPED), isOpen (DERIVED guard), subordinateName (DERIVED)
  - Relations: skillTargets [0..*] AGGREGATION SkillTarget, notes [0..*] AGGREGATION TrainingPlanNote, notesView [0..*] AGGREGATION TrainingPlanNote
  - Operations: close (MAPPED), open (MAPPED)
  - The `isOpen` derived attribute serves as a guard for toggling visibility of open/close buttons
- This variant is the boolean-flag approach to open/close toggle: uses a single `closed` boolean (default: false, meaning "open" by default) instead of a two-member enum
- The TrainingPlan owns its notes and skill targets via COMPOSITION, and the manager can create training plans for subordinates via User.createTrainingPlan
- Date defaults to `Date!now()` for automatic timestamping at creation
- The incompleteSkillTargets DERIVED relation provides a filtered view of only the unfulfilled skill targets
