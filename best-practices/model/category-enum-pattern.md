---
id: "category-enum-pattern"
title: "Category/Classification Enumeration Pattern"
domain: "model"
category: "enum"
score: 71.7
usage_count: 13
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - mlszksz-platform
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

Simple enumerations are used to classify entities into fixed categories that do not have lifecycle transitions. Unlike state machine enums, category enums are set once at creation and rarely change. They serve as domain-specific classifiers for filtering, reporting, and grouping. Multiple category enums can coexist on the same entity, providing orthogonal classification dimensions.

## Structure

- Enum with a small number of fixed members (2-5 typically)
- Used as required or optional attributes on entities
- No associated operations for transitioning between members
- Often have a default value set in the input DTO for creation convenience
- Members represent domain categories, not lifecycle states
- May be used for filtering in access expressions or reporting views

## Examples

### itracker
Three category enums on `Initiative`: `SavingType` (FIXED, VARIABLE) classifies the nature of cost savings; `ActionType` (PRICING, USAGE, LABOR, OEE, SCRAP) classifies the action type; `RiskLevel` (LOW, MEDIUM, HIGH) optionally assesses risk. `InititativeInput` defaults `SavingType#FIXED` and `ActionType#USAGE` for creation.

### SkillMatrix
`LanguageSkillLevel` enum (BEGINNER, CONVERSATIONAL, FLUENT, NATIVE) classifies language proficiency on the `LanguageSkill` entity. This is the only enum in the model -- notably, skill levels (JUNIOR/MEDIOR/SENIOR/EXPERT) are entity instances rather than an enum, demonstrating the choice between fixed enum classification and runtime-extensible entity-based classification.

### ActionGroupTest
`MatterType` enum with 3 members (`dark`, `interstellarMedium`, `intergalacticDust`) classifies Matter entities. Used as a required attribute on `Matter.type`. Ordinals start at 1 (not 0). Each member maps to a dedicated Galaxy creation operation (e.g., `createDarkMatter`), demonstrating enum-to-operation correspondence.

### Alba
`EventType` enum with 4 members (PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED, PRODUCT_FINALIZED, PRODUCT_CREATED) classifies audit events. `TaskType` with single member APPROVAL classifies task types (extensible). `UserRole` with 4 members (GUEST, TEACHER, APPROVER, ADMIN) classifies user permissions as a hierarchical role enum.

### SkillMatrix-Model
Single enum `LanguageSkillLevel` confirmed in model source with 4 ordinal members (BEGINNER=1, CONVERSATIONAL=2, FLUENT=3, NATIVE=4). Used by `LanguageSkill.level` (required). The model's deliberate minimalism (1 enum, 21 entities) illustrates a preference for entity-based extensible classifications (SkillLevel entity) over fixed enums, reserving enums only for truly stable value sets.

### MLSZKSZPlatform
Multiple category enums for classification: `PostType` (NEWS, OFFER, REQUEST, ANNOUNCEMENT) classifies content types, mirrored by `FeedEntryType` for the denormalized feed. `DevicePlatform` (ANDROID, IOS, WEB) classifies device types for push notification routing. `AnnouncementTargetType` (ALL, SPECIFIC_REGION, SPECIFIC_MEMBERS) classifies announcement targeting. `UserRole` (COMPANY_ADMIN, COMPANY_READER, PLATFORM_ADMIN, ASSOCIATION_LEADERSHIP) serves as a hierarchical permission classifier. `NotificationType` (8 members) classifies notification event triggers.

### KozutEugyfelClient
Two category enums: `BejelentesTipus` (JAROKELO, ALTALANOS) classifies complaints by source -- road inspector system vs general e-government portal. `MunkakorEnum` (Ugyfelszolgalati_Munkatars, Szervezetiegyseg_Vezeto, Szervezetiegyseg_Munkatars) classifies user job roles. Both are set at creation and drive routing logic in operations.

### AMS-Model
`RequestType` enum with 3 members (ACCESS, REVOKE, CONFIRMATION) classifies confirmation/access requests by their purpose. Set at creation time on `Request.type` (inherited by ConfirmationRequest and AccessRequest via generalization). Used as a display field on transfer objects but does not drive state transitions -- the separate `Status` enum handles lifecycle.

### Sanctuary Backend
`PrivacyVisibility` enum with 4 hierarchical members (`publicForPeers`, `publicForTeam`, `publicForUnit`, `publicForEveryone`) classifies data visibility levels on `UserPrivacySettings`. Applied to 4 attributes (phoneNumber, peerBadges, specialBadges, systemBadges) controlling who can view specific user information. Ordinals 1-4 represent increasing visibility scope.

### ParkHere
Two category enums: **ReservationType** (NORMAL, QUICK, GUEST, LONG) classifies reservations by booking rules -- each type has different time constraints, token limits, and permission requirements. **DayType** (WORK, HOLIDAY) classifies calendar overrides on AdditionalDay entity, allowing admins to designate weekends as workdays or weekdays as holidays. ReservationType is particularly notable for driving type-specific business rules (time windows, token quotas, required fields).

### IndamediaAdTrack
**Platform** enum with 2 members (META, GOOGLE) classifies advertising platform accounts. Set at creation time on `Account.platform` and determines which credential subtype is valid (`GoogleCredential` vs `MetaCredential`). Drives platform-specific API integration behavior in operations like `testConnection`, `fetchAvailableCampaigns`, and `syncData`.

### InterfaceRegister
8 category enums -- the highest count in any single project. `ApplicationCategory` (9 members: CRM, DMS, IMS, etc.) classifies application types. `BusinessDomain` (4 members: CRM, FINANCE, etc.) classifies business data domains. `CharacterEncoding` (ANSI, UTF8, UTF8_BOM), `FileTransferMethod` (FTP, SFTP, FTPS, SSH, FOLDER), `Environment` (DEV, TEST, PROD), `DirectionOfDataTransmission` (SERVER_TO_CLIENT, CLIENT_TO_SERVER), `HighLevelPeriodicity` (10 members from ADHOC to SOME_MONTHS). None are state machines; all are static classification enums.

### judo-partner
Multiple category enums: **TaxNumberType** (NA/HUN/EU/INT) classifies partner tax number jurisdiction. **Direction** (INCOMING/OUTGOING) classifies registry document flow direction. **LogType** (CREATE/UPDATE/DELETE) classifies audit log entries. **TaxpayerStatus** (VALID/INVALID_TAX_ID/UNDER_LIQUIDATION/UNDER_DISSOLUTION) classifies NAV taxpayer query results. **ValidationErrorCode** (9 members) classifies validation failure reasons.

### KozutEugyfelModelTest
Three category enums: **BejelentesTipusMegnevezes** (JAROKELO, ALTALANOS) classifies complaint type designation. **Megye** (VESZPREM, PEST) classifies counties for geographic routing. **SzervezetiEgyseg** (UFO, FFO) classifies organizational units. All are small fixed-member enums set at entity creation that drive forwarding/routing logic.

### workflow-poc
4 category enums for workflow engine classification: **ContextAttributeType** (BOOLEAN, STRING, NUMERIC) classifies workflow context variable types. **LogEntryType** (COMPLETION) classifies workflow log events by kind. **LogLevel** (TRACE, INFO) classifies log severity levels. **DeclarationErrorCode** (INVALID_REFERENCE) classifies workflow definition upload errors. All are small, stable classifiers without lifecycle transitions.

### ReserveApp
**Role** enum with 5 members (PARTNER, LOGISTICIAN, DOORMAN, READ_ONLY, ADMIN) classifies user roles. Used as an attribute on `User.role` to determine which actor the user authenticates as. Each member maps to a corresponding ActorType (PartnerActor, LogisticianActor, DoormanActor, Readonly, AdminActor). Ordinals start at 1.

### AMS-Frontend
`RequestType` enum (ACCESS, REVOKE, CONFIRMATION) classifies request purpose on the abstract `Request` entity. Set at creation, inherited by both `ConfirmationRequest` and `AccessRequest`. Orthogonal to the `Status` lifecycle enum -- RequestType is a static classifier while Status tracks workflow state.

## Trade-offs

- Pros: Fixed vocabulary prevents data inconsistency, supports filtering and reporting, simple to add members
- Cons: Adding new categories requires model changes, not suitable for frequently changing classifications (use reference entities instead)
- Prefer when: Classification values are stable and known at design time; prefer reference entities (like `Region`, `SRTCategory`) when values need to be managed at runtime

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (for lifecycle enums with transitions)
- [default-value-patterns](default-value-patterns.md)
