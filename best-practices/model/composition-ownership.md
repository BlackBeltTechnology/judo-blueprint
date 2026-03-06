---
id: "composition-ownership"
title: "Composition Ownership for Lifecycle-Bound Children"
domain: "model"
category: "relation"
score: 81.5
usage_count: 17
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
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

Composition relations are used sparingly and only when child entities are lifecycle-bound to their parent (cascade delete). All other entity relations use association. This pattern keeps the entity graph loosely coupled by default, reserving composition for true parent-child ownership.

## Structure

- COMPOSITION: child is owned by parent, destroyed when parent is deleted
- ASSOCIATION: entities exist independently, no cascade semantics
- Typical ratio: 1 composition for many associations
- Composition children can use `self!container(ParentType)` to navigate up to the parent

## Examples

### Trivia
Only one composition exists: `Test.prompts -> Prompt` (prompts are owned by their test). All other relations (User-Test, Contest-Test, Question-Category, Contest-Category, etc.) use ASSOCIATION, keeping entities independent.

### RackInspect
Composition used extensively for owned children: `Partner.addresses`, `Partner.bankAccounts`, `Partner.emailAddresses`, `FaultRegistry.faultHeaders`, `Offer.offerItems`, `Task.documents`, `Task.history`, `Rack.groups`, `DimensionGroup.parameters`. Associations used for cross-references: `Item.brand`, `Rack.rackType`, `ErrorCode.rackElements`.

### itracker
3 compositions form a two-level ownership hierarchy: `Initiative.monthlyForecasts -> MonthlyForecast`, `Initiative.forecastVersions -> ForecastVersion`, `ForecastVersion.monthlyForecasts -> MonthlyForecastVersion`. Associations for independent references: `Initiative.region`, `Initiative.category`, `Initiative.user`.

### SkillMatrix
7 compositions for owned children: `User.languageSkills -> LanguageSkill`, `User.resumes -> Resume`, `User.trainingPlans -> TrainingPlan`, `TrainingPlan.notes -> Note`, `TrainingPlan.skillTargets -> SkillTarget`, `Resume.works -> Work`, `report::Definition.results -> Result`. Associations for cross-references: `User.unit`, `Skill.competence`, `Tag.competences`.

### ActionGroupTest
2 compositions forming a celestial hierarchy: `Galaxy.stars -> Star` (stars cannot exist without a galaxy) and `Star.planets -> Planet` (planets cannot exist without a star). All other relations use AGGREGATION (`Planet.creatures`, `Galaxy.astronomer`, `Sign.creatures`) or STATIC ACCESS (`God.galaxies`, `God.creatures`).

### Alba
Single composition: `Product.attachments -> Attachment` (attachments are lifecycle-bound to products). All other relations (Product.author, Product.events, Product.audience, Task.assignee, User.institution, etc.) use ASSOCIATION for independent lifecycles.

### SkillMatrix-Model
7 COMPOSITION relations confirmed in model source, all with `lower="0"`: `User.languageSkills`, `User.resumes`, `User.trainingPlans`, `TrainingPlan.notes`, `TrainingPlan.skillTargets`, `Resume.works`, `Definition.results`. Container navigation used on children: `TrainingPlan.incompleteSkillTargets = self!container(User).incompleteSkillTargets`, `Result.reportName = self!container(Definition).name`.

### MLSZKSZPlatform
Single composition: `Organization.address -> Address [0..1]` (address is lifecycle-bound to organization, cascade delete). All other 20+ relations use ASSOCIATION (User->Organization, City->Region, Device<->User, Document<->Announcement, etc.) or AGGREGATION (City->Region, User->Organization). This confirms the sparse-composition pattern.

### Viterra Demo
Single composition: `Report.stocks -> Stock [0..*]` (stocks are lifecycle-bound to their report). All other relations use ASSOCIATION: `Report.client`, `Report.period` (bidirectional), `Stock.silo`, `Stock.commodity` (one-way). The composed stocks get full CRUD at the transfer level (`ReportTransfer.stocks: createable, updateable, deleteable`), while the report itself is non-deleteable.

### KozutEugyfelClient
`Bejelentes.kepek -> Kep` (images are lifecycle-bound to the complaint report via composition). Events (`esemenyek`) and participants (`resztvevok`) use two-way association since they may be referenced independently. Notifications (`Ertesites`) are composed within events, navigating back via `self!container(Esemeny)`.

### MJSZ
4 compositions for lifecycle-bound children: `Player.licenses -> License`, `Player.transfers -> Transfer`, `Tournament.matches -> Match`, `Club.teams -> Team`. All other relations use two-way ASSOCIATION (Player<->Club, Player<->Team, Season<->Tournament, Match<->Team). Container navigation used: `Team.name = self!container(Club).name`, `Match.season = self!container(Tournament).season.year`.

### judo-demo-miniworkflow
2 compositions on `Document`: `Document.files -> Files [0..*]` (file attachments lifecycle-bound to document) and `Document.documentHistoryEntries -> DocumentHistoryEntry [0..*]` (audit trail lifecycle-bound to document). The `owner -> User` relation uses association since users exist independently. History entries are immutable (no CRUD) and appended via `+=` in workflow operations.

### AMS-Model
Single composition: `Campaign.confirmationRequests -> ConfirmationRequest [0..*]` (confirmation requests are lifecycle-bound to their campaign). All other relations use ASSOCIATION: `Application.requests`, `User.requests`, `User.subordinates`, `User.applications`, `Request.application`, `Request.user`, `ConfirmationRequest.approver`, `AccessRequest.issuer`. The composed confirmation requests use `self!container(Campaign).status` for container navigation to derive campaignStatus.

### Sanctuary Backend
2 compositions for settings entities: `User.privacySettings -> UserPrivacySettings [0..1]` and `User.settings -> UserSettings [0..1]`. Both use `targetDefinedCRUD="true"` to delegate CRUD to the child entity. All other relations (User<->Role, User<->RoleGroup, User->PositionTitle) use ASSOCIATION for independent lifecycles.

### ParkHere
3 compositions: `User.cars -> Car [0..*]` (cars owned by user), `User.holidays -> Holiday [0..*]` (holidays bound to user), `Reservation.guest -> Guest [0..1]` (guest info bound to reservation). All other relations use ASSOCIATION: `Reservation->User`, `Reservation->ParkingSlot`, `User<->ParkingGarage`, `Doorman->ParkingGarage`. Composition children use `!container()` for back-references: `Car.carOwner`, `Holiday.holidayOwner`.

### InterfaceRegister
5 compositions for owned children: `Email.tos/ccs/bccs -> EmailRecipient [0..*]` (email recipients cascade-delete with their email specification) and `Server.ipv4Addresses/ipv6Addresses -> IPV4Address/IPV6Address [0..*]` (IP addresses cascade-delete with their server). All other 18 relations use ASSOCIATION for independent entities.

### judo-partner
4 compositions across domains: `Partner.addresses -> Address [0..*]`, `Partner.contacts -> Contact [0..*]` (contact info lifecycle-bound to partner), `Taxpayer.addresses -> TaxpayerAddress [0..*]` (NAV address data), `DocumentType.attributeTypes -> AttributeType [0..*]`. All other relations use ASSOCIATION or TWO-WAY, including `Import.partners` which is ASSOCIATION (not composition) allowing imported partners to be independently managed.

### KozutEugyfelModelTest
Single composition: `Bejelentes.kepek -> Kep [0..*]` (images lifecycle-bound to complaint reports). All other relations use ASSOCIATION (stored or two-way): `esemenyek`, `bejelentesTipus`, `ugyintezo`, `felelos` (derived), `kezdemenyezo`, `celFelhasznalo`, `ertesitesiLista`. Only `Kep` has full CRUD (createable/updateable/deleteable), reflecting its composed child status.

### workflow-poc
5 compositions forming a workflow definition hierarchy: `WorkflowVersion.states -> State [0..*]`, `WorkflowVersion.events -> Event [0..*]`, `State.transitions -> Transition [0..*]`, `Transition.guards -> Guard [0..*]`, `Context.attributes -> ContextAttribute [0..*]`. All other relations (Token->State, Token->User, Workflow->WorkflowVersion, Role->User, etc.) use ASSOCIATION. The composition hierarchy mirrors the YAML-based workflow definition structure.

### ReserveApp
Single composition: `FreightReservation.attachments -> Attachment [0..*]` (attachments are lifecycle-bound to their reservation). All other 11 relations on FreightReservation use ASSOCIATION (e.g., `partner`, `gate`, `project`, `spot`, `items`, `vehicleType`, `loadingType`, `recipient`). This confirms the sparse-composition pattern in a domain with 15 entities and 12 relations on the central aggregate.

### AMS-Frontend
Single composition: `Campaign.confirmationRequests -> ConfirmationRequest [0..*]`. Confirmation requests are lifecycle-bound to their campaign and use `self!container(Campaign).status` for upward navigation. `Campaign.applications` is a plain ASSOCIATION -- applications exist independently across campaigns.

## Trade-offs

- Pros: Clear ownership semantics, automatic cascade delete for dependent data, composition navigation via `!container()`
- Cons: Composition children cannot be shared across parents, must be created within parent context
- Prefer when: Child entities have no meaning outside their parent; prefer association for independent entities

## Related Patterns

- [conditional-visibility-getter](conditional-visibility-getter.md) (uses `!container()` for composition navigation)
- [container-back-reference](container-back-reference.md)
