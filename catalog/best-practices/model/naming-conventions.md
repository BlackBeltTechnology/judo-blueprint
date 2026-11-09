---
id: "naming-conventions"
title: "JUDO Model Naming Conventions"
domain: "model"
category: "namespace"
score: 84.2
usage_count: 19
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
  - bhs-global-operation
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

Consistent naming conventions across JUDO models for entities, attributes, relations, operations, enumerations, and packages. These conventions improve readability and maintain consistency across the model-driven architecture.

## Structure

| Element Type | Convention | Examples |
|---|---|---|
| Entities | PascalCase singular nouns | `User`, `Question`, `Contest`, `Application` |
| Attributes | camelCase | `email`, `choiceA`, `numberOfQuestions`, `timestampOfCreation` |
| Relations (collection) | camelCase plural | `tests`, `prompts`, `categories`, `fixedQuestions` |
| Relations (single) | camelCase singular | `contest`, `player`, `question`, `category` |
| Operations | camelCase verbs | `reset`, `approve`, `submit`, `approveAll`, `register` |
| Enums (type) | PascalCase | `ContestStatus`, `TestStatus`, `QuestionStatus` |
| Enums (members) | UPPER_SNAKE_CASE | `CREATED`, `STARTED`, `INVALID_CODE` |
| Packages | lowercase | `types`, `entities`, `actors`, `admin`, `player` |
| Actor transfers | Reuse entity name in actor package | `admin::Question` maps to `entities::Question` |

## Examples

### Trivia
Entities: `User`, `Question`, `Contest`, `Test`, `Category`, `Prompt`, `Application`, `Upload`, `Admin`. Relations: singular `contest`, `player` for 1..1; plural `tests`, `prompts`, `categories` for 0..*. Operations: verbs like `approve`, `reject`, `enter`, `submit`.

### RackInspect
Entities: `FaultRegistry`, `RegistryHeader`, `ElementFault`, `OfferItem`, `JobSheet`. Packages use snake_case: `fault_registry_services`, `job_task_services`, `offer_services`. Unmapped DTOs use suffixes: `*Input`, `*Update`, `*Data`, `*Panel`. Toggle operations: `toggleActive`, `togglePrimary`, `toggleBilling`.

### itracker
Entities: `Initiative`, `Region`, `SRTCategory`, `MonthlyForecast`, `ForecastVersion`, `User`, `Application`. Domain-specific compound names: `SRTCategory` (abbreviation prefix), `MonthlyForecastVersion`. Operations: `archiveForecast`, `sendForApproval`, `approve`, `reject`, `createInitiative`. Enums: `InitiativeStatus`, `SavingType`, `ActionType`, `RiskLevel`.

### SkillMatrix
Entities: `User`, `Competence`, `Skill`, `SkillLevel`, `TrainingPlan`, `SkillTarget`. Boolean flags use `is` prefix for role flags (`isActiveAdmin`, `isActiveProfessional`); other booleans use descriptive names (`strategic`, `active`, `approved`). Flattened derived attributes follow `{relation}Name` pattern: `competenceName`, `unitName`, `approvedLevelName`. Purpose-specific transfer names: `MyProfessional`, `Subordinate`, `UnapprovedSkillsView`.

### ActionGroupTest
Entities: PascalCase (`Galaxy`, `Star`, `Planet`, `Creature`, `Astronomer`). Template/input types suffixed: `CreatureTemplate`, `MatterCreator`. Relations: plural for collections (`galaxies`, `stars`, `planets`, `creatures`), singular for single (`astronomer`, `planet`, `earth`). Operations: verb-prefix (`createCreature`, `destroyLife`, `startWar`, `endWar`, `chooseTheMessiah`). Enum members: camelCase (`interstellarMedium`, `intergalacticDust`).

### Alba
Entities: PascalCase (`Product`, `ProductVersion`, `ProductVersions`, `User`, `Institution`, `Task`, `Event`). Role-based transfer prefixes: `AuthorProduct`, `AdminProduct`, `GuestProduct`, `ApproverProduct`. Suffix-based input DTOs: `ApprovalTaskInput`, `CloseTaskInput`, `AuthorProductForm`. Operations: lifecycle verbs (`finalize`, `approveVersion`, `revokeApproval`, `draftNewVersion`, `closeTask`). Enums: `ProductState`, `UserRole`, `TaskState`, `AccountStatus`.

### SkillMatrix-Model
Entities: PascalCase (`Competence`, `SkillTarget`, `TrainingPlan`, `ResumeList`, `ResumeTemplate`). Packages: `competence`, `user`, `report` for domain grouping; `types`, `measures` for infrastructure. Operations: `approveAllSkills`, `approveAllSubordinatesSkills`, `createTrainingPlan`, `completeAllTargets`, `deleteUser`. Derived boolean naming: `has*` (`hasApprovalRequest`, `hasSkills`) for existence checks, `is*` (`isInactiveUser`) for state checks.

### MLSZKSZPlatform
Entities: PascalCase (`RegistrationRequest`, `FeedEntry`, `InvitationRecipient`, `UserInvitationRequest`). Boolean `is*` prefix: `isVisible`, `isSensitive`, `isStrategic`, `isActive`. Timestamp `*At` suffix: `createdAt`, `sentAt`, `verifiedAt`, `lastUsedAt`, `expiresAt`. Operations: lifecycle verbs (`publish`, `expired`, `accept`, `reject`), `edit*` prefix for edits (`editNews`, `editOffer`), `create*` for creation (`createCity`, `createCapability`), `activateToggle` for toggles. Packages: `admin`, `companyadmin`, `feed`, `registration` for service organization.

### Viterra Demo
Entities: PascalCase singular (`Period`, `Client`, `Silo`, `Stock`, `Commodity`, `Report`, `Application`). Transfer naming uses `EntityTransfer` suffix (`PeriodTransfer`, `ClientTransfer`, `StockTransfer`) plus actor-prefixed variants (`PartnerOpenReportTransfer`, `PartnerClosedReportTransfer`, `PartnerClientTransfer`). Operations: imperative verbs (`submit`, `accept`, `review`, `init`). Enums: PascalCase types (`ReportStatus`, `Status`), UPPER_CASE members (`PENDING`, `SUBMITTED`, `ACCEPTED`, `REVIEW`). Single flat `viterra` namespace with no sub-packages for entities.

### KozutEugyfelClient
Hungarian-language naming throughout: entities (`Bejelentes`, `Felhasznalo`, `Esemeny`, `Ertesites`), attributes (`azonosito`, `bejelentoNeve`, `letrehozasIdopont`), relations (`ugyintezo`, `felelos`, `resztvevok`), operations (`tovabbitas`, `lezaras`, `megnyitas`, `megjegyzes`). Permission booleans use `*Engedely` suffix (`tovabbitasEngedely`, `lezarasEngedely`). Demonstrates that JUDO conventions (PascalCase entities, camelCase attributes) are language-agnostic.

### BHS Global Operation
Skeleton project confirming baseline conventions. Model name: PascalCase with abbreviation (`BHSGlobalOperation`). Package names: camelCase (`types`, `measures`). Type names: PascalCase (`String`, `Long`, `Email`). Unit names: camelCase (`milligram`, `kilometrePerHour`, `squareMetre`). Access annotations: camelCase (`dashboard`, `profile`).

### MJSZ
Entities: PascalCase singular (`Player`, `Team`, `Match`, `Club`, `Season`, `Tournament`, `Transfer`, `License`, `Venue`, `Application`). Attributes: camelCase with full words (`dateOfBirth`, `visitorScore`, `licenseExpiration`, `goalsDifference`). Relations: plural for collections (`players`, `teams`, `licenses`, `transfers`), singular for single (`club`, `season`, `venue`). Role-based relation naming: `homeTeam`/`visitorTeam`, `homeMatches`/`visitorMatches` for dual-role relations to the same entity.

### judo-demo-miniworkflow
Entities: PascalCase (`Document`, `Files`, `DocumentHistoryEntry`, `User`). Transfer naming uses `EntityTransfer` suffix (`DocumentTransfer`, `FilesTransfer`, `DocumentHistoryEntryTransfer`). Operations: imperative verbs (`requestReview`, `accept`, `reject`, `close`, `createDocument`, `initUsers`). Enum: `DocumentState` with UPPER_SNAKE_CASE members (`IN_PROGRESS`, `REVIEW_REQUESTED`, `ACCEPTED`, `REJECTED`, `CLOSED`). Permission booleans use `is*` prefix: `isAcceptable`, `isClosable`. Negative attributes use `isNot*`: `isNotAdmin`, `isNotClosable`.

### AMS-Model
Entities: PascalCase (`User`, `Application`, `Request`, `Campaign`, `ConfirmationRequest`, `AccessRequest`, `Admin`). Enums use status/type suffixes: `CampaignStatus`, `RequestType`, `Status`. Relations: plural for collections (`requests`, `subordinates`, `approvals`, `applications`, `confirmationRequests`), singular for single (`manager`, `approver`, `issuer`, `application`). Operations: imperative verbs (`approve`, `reject`, `open`, `close`, `load`, `approveAll`, `reset`, `init`). Transfer objects reuse entity names in actor packages: `manager::Subordinate`, `manager::Request`.

### Sanctuary Backend
Entities: PascalCase (`User`, `UserPrivacySettings`, `UserSettings`, `PositionTitle`, `Role`, `RoleGroup`). Transfer objects use "TO" suffix: `UserTO`, `RoleTO`, `RoleGroupTO`, `PositionTitleTO`, `UserPrivacySettingsTO`, `UserSettingsTO`. Enums: PascalCase (`PrivacyVisibility`, `ActiveStatus`) with camelCase members (`publicForPeers`, `publicForTeam`, `active`, `archived`). Packages: `types`, `measures`, `user` for domain grouping.

### ParkHere
Entities: PascalCase (`ParkingGarage`, `ParkingSlot`, `Reservation`, `Doorman`, `DoormanNotified`, `AdditionalDay`). Transfer suffixes: `*Input` (CreateCarInput, HolidayInput, DoormanInput), `*Settings` (UserSettings, ConfigurationSettings, ParkingGarageSettings), `*Panel` (UserReservationPanel, ReservationsPanel, HolidayPanel). Enums: PascalCase types (ReservationStatus, ReservationType, DayType, ErrorCode), UPPER_SNAKE_CASE members (PERMISSION_DENIED, TOO_MANY_RESERVATION). Packages: `entities`, `services`, `measures`.

### IndamediaAdTrack
Entities: PascalCase (`TrackedCampaign`, `AggregatedCampaign`, `GoogleCredential`, `MetaCredential`, `AvailableCampaign`). Transfer suffixes: `*Transfer` (ClientTransfer, AccountTransfer), `*Input` (ClientInput, AccountInput, GoogleCredentialInput), `*UpdateInput` (ClientUpdateInput, AccountUpdateInput), `*Panel` (ClientPanel, CampaignPanel), `*Info` (CostInfo). Operations: `syncData`, `syncCosts`, `testConnection`, `fetchAvailableCampaigns`, `untrack`. Packages: `entities` and `services` for clear domain/service separation.

### InterfaceRegister
Entities: PascalCase singular (`Application`, `Vendor`, `InterfaceSpecification`, `ConcreteConnection`, `HighLevelConnection`). Transfer suffixes: `{Entity}Transfer` (ApplicationTransfer, VendorTransfer, HighLevelConnectionTransfer), `Create{Entity}Input` (CreateApplicationInput, CreateUserInput, CreateHighLevelConnectionInput). Enum naming: PascalCase types (ApplicationCategory, BusinessDomain, DirectionOfDataTransmission), UPPER_SNAKE_CASE members. Package: single `enterpriseArchitect` for all TOs and actor.

### judo-partner
Entities in `::database` sub-packages: `Partner::partner::database::Partner`, `Partner::registry::database::Case`. API transfer objects in parent packages reuse entity names: `Partner::partner::Partner` maps to `Partner::partner::database::Partner`. Unmapped input DTOs use descriptive suffixes: `CreatePartnerInput`, `PartnerImportInput`, `CountryImportInput`. Enums: PascalCase types (`PartnerStatus`, `TaxNumberType`, `ValidationErrorCode`), UPPER_SNAKE_CASE members (`INVALID_TAX_ID`, `NOT_VALIDATED`). Sub-view TOs use entity-purpose naming: `PartnerContacts`, `PartnerAddresses`.

### KozutEugyfelModelTest
Hungarian naming consistent with related KOZUT projects: entities (`Bejelentes`, `Felhasznalo`, `Esemeny`, `Inicializalo`), attributes (`targy`, `szoveg`, `allapot`, `helyszin`, `bejelentoNeve`), relations (`kepek`, `esemenyek`, `ugyintezo`, `felelos`), operations (`tovabbitas`, `lezaras`, `megjegyzes`, `szinkronizal`). Actor-specific packages mirror actor names: `UgyfelszolgalatiMunkatars`, `SzervezetiEgysegMunkatars`, `SzervezetiEgysegVezeto`. Shared TOs in `KozosTransferObjectek` package.

### workflow-poc
Entities: PascalCase (`Token`, `WorkflowVersion`, `State`, `Transition`, `Action`, `Guard`, `Context`, `ContextType`, `LogEntry`, `EventType`). Packages: hierarchical with `entities`, `transfers`, `transfers::admin`, `test`, `test::entities`. Transfers use purpose-based naming: `Task` (maps Token), `TaskList` (maps User), `Activity` (maps Transition). Admin TOs in separate `admin` sub-package. Unmapped DTOs use descriptive names: `Event`, `ContextInput`, `ActionInput`, `UploadInput`, `CommitInput`. Operations: imperative verbs (`trigger`, `checkout`, `release`, `execute`, `assign`, `navigate`, `commit`, `upload`, `publish`).

### ReserveApp
Entities: PascalCase singular (`FreightReservation`, `Partner`, `Gate`, `Spot`, `VehicleType`, `LoadingType`). Actor naming uses "Actor" suffix: `AdminActor`, `PartnerActor`, `LogisticianActor`, `DoormanActor`. Principal TOs use "User" suffix: `AdminUser`, `PartnerUser`, `LogisticianUser`, `DoormanUser`. Role-scoped TOs use `*ForPartner` suffix: `ReservationForPartner`, `GateForPartner`, `SpotForPartner`. Packages: `types`, `measures`, `entities`, `services`.

### AMS-Frontend
Hierarchical namespace: `ams::types`, `ams::measures`, `ams::entities`, `ams::actors::manager`, `ams::actors::admin`. Transfers named by actor perspective: `manager::Subordinate` (maps User), `manager::ManagerApprovalList` (maps User). Enums: `Status`, `CampaignStatus`, `RequestType` with UPPER_SNAKE_CASE members. Operations: imperative verbs (`approve`, `reject`, `open`, `close`, `load`, `approveAll`).

## Trade-offs

- Pros: Predictable naming across the entire model, generated code follows same conventions
- Cons: Some names may be verbose (e.g., `timestampOfCreation`), but clarity is preferred
- Prefer when: Always -- naming conventions should be applied uniformly

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md) (actor package naming)
