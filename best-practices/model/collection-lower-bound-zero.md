---
id: "collection-lower-bound-zero"
title: "Collection Relations Always Use 0 Lower Bound"
domain: "model"
category: "relation"
score: 60.4
usage_count: 18
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - sanctuary-backend
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

All collection relations (multi-valued) in JUDO models use `0` as their lower bound, resulting in cardinality `0..*`. The cardinality `1..*` (required collection) is not used. This is a best practice because entities are created before their relations are populated, so requiring at least one element at creation time would cause validation failures.

## Structure

- All multi-valued relations use cardinality `0..*`
- Single-valued required relations use `1..1`
- Single-valued optional relations use `0..1`
- The `1..*` cardinality is avoided

## Examples

### Trivia
All 12+ collection relations use `0..*`: `User.tests`, `Contest.fixedQuestions`, `Contest.tests`, `Contest.categories`, `Contest.questions`, `Category.questions`, `Test.prompts`, `Upload.questions`, plus all access points. No `1..*` cardinality appears anywhere in the model.

### RackInspect
Across 72 entities with dozens of collection relations, all use `0..*`: `Partner.addresses`, `Partner.bankAccounts`, `FaultRegistry.faultHeaders`, `Offer.offerItems`, `Configuration.minimumOfferPrices`, `Rack.groups`, `User.roles`, etc. No `1..*` cardinality exists despite complex hierarchical data.

### itracker
All collection relations use `0..*`: `Initiative.forecastVersions`, `Initiative.monthlyForecasts`, `ForecastVersion.monthlyForecasts`, `User.initiatives`. No `1..*` cardinality despite monthly forecasts being logically required for an initiative.

### SkillMatrix
All collection relations across 21 entities use `0..*`: `User.skills`, `User.managedUnits`, `User.languageSkills`, `User.trainingPlans`, `Competence.skills`, `Competence.tags`, `TrainingPlan.skillTargets`, `TrainingPlan.notes`. Required single relations use `1..1` (e.g., `Skill.competence`, `SkillTarget.skillLevel`).

### ActionGroupTest
All 13 relations use `0..*` for collections: `God.galaxies`, `God.creatures`, `God.matter`, `Galaxy.stars`, `Galaxy.matter`, `Planet.creatures`, `Sign.creatures`, `CreatureTemplate.signs`. Single relations (God.earth, Galaxy.astronomer, Creature.planet) use `0..1`. No `1..*` cardinality found.

### Alba
All collection relations use `0..*`: `Product.audience`, `Product.curriculum`, `Product.resultTypes`, `Product.attachments`, `Product.events`, `User.products`, `User.tasks`, `Institution.teachers`. Single required relations use `1..1` (e.g., `ProductVersion.origin`, `Task.createdBy`, `Task.assignee`).

### SkillMatrix-Model
69 collection relations confirmed with `lower="0" upper="-1"` in the model source; zero instances of `lower="1" upper="-1"`. Collections span all domains: `User.skills [0..*]`, `Competence.skillTargets [0..*]`, `Definition.results [0..*]`, `Search.results [0..*]`. Required single relations (`1..1`) used for `Skill.competence`, `SkillTarget.competence`, `SkillTarget.skillLevel`.

### MLSZKSZPlatform
All collection relations use `0..*`: `Announcement.documents [0..*]`, `Invitation.recipients [0..*]`. Optional single relations use `0..1`: `Organization.address [0..1]`, `FeedEntry.post [0..1]`, `AuditLog.user [0..1]`. Required singles use `1..1`: `User.organization`, `City.region`, `Device.user`.

### Viterra Demo
All collection relations use `0..*`: `Period.reports [0..*]`, `Client.reports [0..*]`, `Report.stocks [0..*]` (composition). Required single relations use `1..1`: `Report.client`, `Report.period`, `Stock.silo`, `Stock.commodity`. The research explicitly calls out these `lower="0"` collections as a notable pattern.

### KozutEugyfelClient
All collection relations use `0..*`: `Bejelentes.kepek` (images, composition), `Bejelentes.resztvevok` (participants, two-way), `Bejelentes.esemenyek` (events, two-way). The research explicitly confirms these collections follow the standard 0 lower bound pattern.

### MJSZ
All 11 collection relations use `0..*`: `Player.licenses`, `Player.teams`, `Player.transfers`, `Season.tournaments`, `Tournament.teams`, `Tournament.matches`, `Club.players`, `Club.teams`, `Team.players`, `Team.homeMatches`, `Team.visitorMatches`. No `1..*` cardinality despite teams logically needing players.

### judo-demo-miniworkflow
All 5 collection relations use `0..*`: `Document.files`, `Document.documentHistoryEntries`, `User.documents`, `DocumentTransfer.files`, `DocumentTransfer.documentHistoryEntries`. Documents can exist without files, and the initial history entry is created atomically in the `createDocument` factory operation. The `+=` operator is used to append to these collections in workflow operations.

### AMS-Model
All collection relations use `0..*`: `Application.requests [0..*]`, `User.requests [0..*]`, `User.subordinates [0..*]`, `User.applications [0..*]`, `User.approvals [0..*]`, `User.issues [0..*]`, `Campaign.confirmationRequests [0..*]` (composition), `Campaign.applications [0..*]`. Required single relations use `1..1`: `Request.application`, `Request.user`, `ConfirmationRequest.approver`, `AccessRequest.issuer`.

### Sanctuary Backend
All collection relations use `0..*`: `User.roles [0..*]`, `User.roleGroups [0..*]`, `User.effectiveRoles [0..*]`, `Role.users [0..*]`, `RoleGroup.roles [0..*]`, `RoleGroup.users [0..*]`. Single relations use `0..1`: `User.privacySettings`, `User.settings`, `User.positionTitle`. No mandatory relations exist in the model.

### ParkHere
All collection relations use `0..*`: `User.cars`, `User.reservations`, `User.holidays`, `ParkingGarage.parkingSlots`, `ParkingGarage.accessedUsers`, `ParkingSlot.reservations`, `Configuration.doormans`, `Configuration.additionalDays`, `Doorman.assignedGarages`. Required single relations use `1..1` (Reservation.owner, ParkingSlot.parkingGarage). Research explicitly notes this as standard JUDO pattern.

### IndamediaAdTrack
All 8 collection relations use `0..*`: `Client.accounts`, `Client.aggregatedCampaigns`, `Account.trackedCampaigns`, `Account.availableCampaings`, `TrackedCampaign.costs`, `TrackedCampaign.fetchedData`, `AggregatedCampaign.trackedCampaigns`, `AggregatedCampaign.history`. Required singles use `1..1` for parent references (e.g., `Cost.trackedCampaign`, `Account.client`).

### InterfaceRegister
All 7 entity-level collection relations use `0..*`: `Email.tos/ccs/bccs -> EmailRecipient` (composition), `HighLevelConnection.businessDataTypes/brands` (association), `Server.ipv4Addresses/ipv6Addresses` (composition). Transfer-level collections also use `0..*`: `CreateHighLevelConnectionInput.businessDataTypes`, `CreateHighLevelConnectionInput.brands`.

### judo-partner
All 13 collection relations use `0..*` across both partner and registry domains: `Partner.addresses`, `Partner.contacts`, `Partner.participants` (TWO-WAY), `Taxpayer.addresses`, `ImportPartner.addresses`, `Import.partners`, `Case.records`, `Case.participants`, `Register.records`, `Register.documentTypes`, `DocumentType.attributeTypes`, `Record.versions`, `RecordVersion.attributes`. Required single relations use `1..1` (e.g., `PartnerLog.partner`, `Record.register`).

### KozutEugyfelModelTest
All 10+ collection relations use `0..*` across entities and transfers: `Bejelentes.kepek [0..*]` (composition), `Bejelentes.esemenyek [0..*]`, `Felhasznalo.esemenyek [0..*]`, `Felhasznalo.intezendok [0..*]`, `Megjegyzes.ertesitesiLista [0..*]`, plus all actor access points and transfer-level collections like `MegjegyzesInput.ertesitendok [0..*]`.

### workflow-poc
All 20+ collection relations use `0..*`: `WorkflowVersion.states`, `WorkflowVersion.events`, `WorkflowVersion.observers`, `State.transitions`, `State.incomingTransitions`, `Transition.guards`, `Transition.nextStates`, `Role.users`, `Role.transitions`, `User.roles`, `User.contexts`, `Context.attributes`, `Context.tokens`, `Context.assignables`, `Context.logs`, `ContextType.workflows`, `Workflow.versions`. Required singles use `1..1` only for `Token.context`, `WorkflowVersion.workflow`, `Context.workflow`, `Context.type`.

### ReserveApp
All collection relations across 15 entities use `0..*`: `FreightReservation.attachments`, `FreightReservation.items`, `Gate.freightReservations`, `Partner.freightReservations`, `Partner.contacts`, `Project.users`, `Project.spots`, `Project.freightReservations`, `Spot.projects`, `Spot.freightReservations`, `Company.contacts`, `User.projects`. Transfer-level collections also follow the pattern: `ManagedUser.projects [0..*]`, `Partner.contacts [0..*]`.

### AMS-Frontend
Same model as AMS-Model (frontend project shares the model). All 10 collection relations use `0..*`: `Application.requests`, `User.requests/subordinates/applications/approvals/issues`, `Campaign.confirmationRequests` (composition), `Campaign.applications`. Mandatory [1..1] only on child-side references: `Request.application`, `Request.user`, `ConfirmationRequest.approver`, `AccessRequest.issuer`.

## Trade-offs

- Pros: Entities can be created independently and populated later, avoids validation errors during creation
- Cons: Cannot express "must have at least one" at the model level (must enforce in operations)
- Prefer when: Always -- this is the standard JUDO best practice for collection cardinalities

## Related Patterns

- [composition-ownership](composition-ownership.md)
