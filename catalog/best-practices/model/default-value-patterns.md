---
id: "default-value-patterns"
title: "Default Value Conventions"
domain: "model"
category: "entity"
score: 81.7
usage_count: 16
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

Entities and transfer objects use consistent default value conventions. Boolean flags default to their "normal" state (`true` for active flags, `false` for computed flags). Enum status attributes default to their initial lifecycle state. Timestamps use `Timestamp!now()` for auto-population. Transfer objects may provide additional or overriding defaults not present on the entity.

## Structure

Common default value patterns:
- **Boolean active flags**: `active = true` (entity starts active)
- **Boolean computed flags**: `personalBest = false`, `correct = false` (start as not-yet)
- **Enum initial states**: `status = EnumType#INITIAL_STATE` (first lifecycle state)
- **Enum sentinel values**: `answer = Choice#NONE` (no selection yet)
- **Auto-timestamp**: `timestampOfUpload = Timestamp!now()`
- **Auto-sequence**: `identifier = Long!getVariable("SEQUENCE", "Entity")`
- **Transfer-level defaults**: Override or supplement entity defaults (e.g., `numberOfQuestions = 20`)
- **Numeric defaults**: `0` for costs, `1` for quantities, specific values for business rules
- **String defaults**: `"-"` or `" "` for required strings that may be computed later
- **Self-referencing defaults**: `self.priceModifier.scope` (copy from template)
- **Actor variable defaults**: `Email!getVariable('ACTOR', 'email')` (current user)
- **Date defaults**: `Date!now()` for current date on creation
- **Formatted sequence**: `"PREFIX" + Long!getVariable("SEQUENCE", "NAME")!asString()!lpad(N, "0")` for human-readable IDs
- **Time defaults**: `09:00`, `17:00` for business hours
- **Count-based ID**: `'PREFIX-' + ((Entity!count()+1)!asString())!lpad(N, "0")` for sequential prefixed IDs

## Examples

### Trivia
Entity defaults: `User.active = true`, `Question.status = QuestionStatus#REVIEW`, `Test.status = TestStatus#CREATED`, `Prompt.answer = Choice#NONE`. Transfer overrides: `admin::Contest.numberOfQuestions = 20`, `admin::Contest.responseTime = 15` (entity has no defaults for these).

### RackInspect
Extensive defaults: booleans (`active=true`, `offerCreated=false`, `internalUse=false`), enums (`FaultRegistryStatus#DRAFT`, `WorkStatus#IN_PROGRESS`, `RatingResult#A`), timestamps (`Timestamp!now()`), numerics (`netMarginPercent=40`, quantity=1, costs=0), strings (`"-"`, `" "`), self-references (`self.priceModifier.scope`), actor variables (`Email!getVariable('ACTOR', 'email')`).

### itracker
Entity defaults: `Initiative.status = InitiativeStatus#NEW`, `Initiative.inFcst = false`, `Initiative.version = 0`, `Initiative.id` via sequence. Transfer-level (InititativeInput): enum defaults `SavingType#FIXED`, `ActionType#USAGE`, numeric `annualSpend = 0`, `monthlySavingPotential = 0`, date `actionDueDate = Date!now()`, relation defaults `Region!any()` and `SRTCategory!any()`.

### SkillMatrix
Boolean role flags default to `false`: `isActiveAdmin`, `isActiveHREmployee`, `isActiveProfessional`. Active flags default to `true`: `Competence.active`. Date defaults use `Date!now()`: `TrainingPlan.date`, `Note.date`. State flags default to initial state: `TrainingPlan.closed = false`. Placeholder string: `User.email = 'info@bb.hu'`.

### Alba
Enum initial states: `Product.state = ProductState#DRAFT`, `User.role = UserRole#GUEST`. Boolean soft-delete flags: `Audience.isEnabled = true`, `Curriculum.isEnabled = true`, `ResultType.isEnabled = true`, `Institution.isEnabled = true`. Activity flag: `Task.isActive = false`. Integer default: `ProductVersion.version = 0`. Actor variable default: `Product.author` defaults to current user via `User!filter(...)!any()`.

### SkillMatrix-Model
Same patterns as SkillMatrix frontend research, confirmed in model source. `User.createTrainingPlan()` operation uses inline defaults: `new TrainingPlan(date = Date!now(), closed = False)`. The initializer seeds SkillLevels with explicit scores: `new SkillLevel(name = "JUNIOR", score = 1)`. `Competence.strategic` defaults to `false`, `Competence.active` defaults to `true`.

### MLSZKSZPlatform
Boolean visibility/classification defaults: `User.isVisible = true`, `Announcement.isSensitive = false`, `Announcement.isStrategic = false`. Empty string defaults for computed fields: `FeedEntry.contentId = ""`, `FeedEntry.capabilities = ""`, `FeedEntry.authorName = ""`. These defaults avoid NULL values in denormalized display fields, ensuring consistent rendering even before data is populated.

### Viterra Demo
Enum initial state: `Report.status = ReportStatus#PENDING`. Boolean active defaults: `SiloTransfer.active = true`, `ClientTransfer.active = true`. Date default: `Period.referenceDate = Date!now()`. The enum default ensures new reports start in PENDING state, ready for partner editing.

### MJSZ
`Player.identifier` uses a formatted sequence default: `"MJSZ" + mjsz::types::Long!getVariable("SEQUENCE", "MJSZID")!asString()!lpad(5, "0")`, producing human-readable IDs like "MJSZ00001". This is the only default value in the model, as no enums, booleans, or timestamps require defaults. Demonstrates the minimal-defaults approach for simple domain models.

### judo-demo-miniworkflow
Boolean defaults on `User`: `approver = false`, `active = true`, `admin = false`. No enum default on `Document.currentState` since it is derived from history rather than stored. The initial state (IN_PROGRESS) is set by the `createDocument` factory operation which creates the first `DocumentHistoryEntry` with `toState = DocumentState#IN_PROGRESS`.

### AMS-Model
Enum initial state: `Campaign.status` defaults to `CampaignStatus#OPEN` via `defaultExpression`. This ensures new campaigns are immediately active for confirmation request processing. No boolean role flags on User -- roles are determined by relations (manager hierarchy, approvals) rather than stored flags, contrasting with the SkillMatrix boolean-flag approach.

### ParkHere
Extensive defaults across entities: booleans (`Car.isFavorite=false`, `Car.isArchived=false`, `User.isActive=true`, `User.isAdministrator=false`, `User.isQuickReservation=true`, `ParkingGarage.isActive=true`, `ParkingSlot.isActive=true`, `ParkingSlot.nextToWall=false`, `ParkingSlot.isExclusive=false`, `Reservation.hasToNotify=true`, `Reservation.remindedBeforeStart=false`). Numeric quota defaults: `User.maxNormalReservation=5`, `User.maxGuestReservation=5`, `User.maxLongReservation=2`. Time defaults: `User.startOfWorkingTime=09:00`, `User.endOfWorkingTime=17:00`.

### IndamediaAdTrack
Numeric defaults to `0` for calculated/accumulated fields: `AggregatedCampaign.totalSpend=0`, `AggregatedCampaign.todaySumSpend=0`, `AggregatedCampaign.remainingBudget=0`, `AggregatedCampaign.remainingAverageDailySpend=0`. Boolean active flags: `Client.isActive=true`, `Account.isActive=true`. Enum initial state: `AggregatedCampaign.status=ONGOING`. Demonstrates the pattern of using zero defaults for fields that are recalculated by sync operations.

### InterfaceRegister
Count-based auto-generated IDs on transfer objects: `ApplicationTransfer.id = 'APP-' + ((Application!count()+1)!asString())!lpad(4, "0")`, `VendorTransfer.id = 'VND-' + ...`, `InterfaceSpecification.id = 'IFS-' + ...`, `ConnectionDefinition.id = 'CON-' + ...`. Boolean defaults on `CreateUserInput`: `hasAdminAccess=false`, `hasEnterpriseArchitectAccess=false`, `hasDeveloperAccess=false`, `hasOperatorAccess=false`. Demonstrates transfer-level count-based ID generation distinct from SEQUENCE-based patterns.

### judo-partner
Enum initial states: `ImportPartner.validationStatus = ValidationStatus#NOT_VALIDATED`, `ImportPartner.migrationStatus = MigrationStatus#DISABLED`. Boolean defaults: `Partner.isArchived = false` (entity starts as not-deleted), `Partner.isDuplicateName = false`, `ImportPartner.isDomesticTaxpayer = false`, `ImportPartner.isPrivateIndividual = false`. Timestamp: `Import.timestamp`, `PartnerLog.timestamp` likely use `Timestamp!now()`.

### workflow-poc
Boolean defaults on workflow entities: `WorkflowVersion.committed = false`, `State.autoAssign = false`, `State.joinState = false`, `EventType.showInTasklist = true`, `Event.processed = false`. Sequence-based default: `Event.sequence = Long!getVariable("SEQUENCE", "Event")` for auto-incrementing event ordering. Timestamp default: `LogEntry.timestamp = Timestamp!now()` for automatic log entry timestamping.

### ReserveApp
Boolean active defaults on 11 lookup entities: `Gate.active = true`, `Partner.active = true`, `Company.active = true`, `LoadingType.active = true`, `VehicleType.active = true`, `Project.active = true`, `Spot.active = true`, `LoadingTime.active = true`. This is the most extensive application of the `active = true` default pattern across reference data in a single project.

### AMS-Frontend
`Campaign.status` defaults to `CampaignStatus#OPEN`, ensuring newly created campaigns are immediately active for confirmation request processing. Transfer-level: `admin::Campaign.status` defaults to `CampaignStatus#CLOSED` (overriding the entity default for the admin creation form). No boolean defaults -- roles are relation-based rather than flag-based.

## Trade-offs

- Pros: Consistent initial state, reduces boilerplate in creation logic, transfer-level overrides provide UI-friendly defaults
- Cons: Transfer-level defaults may diverge from entity expectations if not coordinated
- Prefer when: Entities have predictable initial states; always set enum defaults to the starting lifecycle state

## Related Patterns

- [enum-state-machine](enum-state-machine.md)
- [sequence-based-identifier](sequence-based-identifier.md)
