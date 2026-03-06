---
id: "builder-pattern-entity-creation"
title: "Builder Pattern for Entity Creation (ForCreate Types)"
domain: "backend"
category: "data-access"
score: 59.3
usage_count: 11
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - mlszksz-platform
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
---
## Description

All entity creation in JUDO uses generated `EntityForCreate` builder types that separate the creation contract from the read/update contract. The builder uses `withFieldName()` methods and supports setting relations (to existing entities) directly in the builder. The DAO's `create()` method accepts the built object and returns the persisted entity.

## Structure

```java
// Simple entity creation
Entity entity = entityDao.create(EntityForCreate.builder()
    .withField1(value1)
    .withField2(value2)
    .withRelation(existingEntity)
    .build());

// Entity creation with enum and timestamp
testDao.create(TestForCreate.builder()
    .withStatus(TestStatus.CREATED)
    .withPlayer(user.get())
    .withContest(contest)
    .withId(UUID.randomUUID().toString())
    .withTimestampOfCreation(LocalDateTime.now())
    .build());
```

## Examples

### Trivia
Used for creating Users, Tests, Prompts, Questions, Categories, and Upload records. For example, `TestForCreate.builder().withStatus(TestStatus.CREATED).withPlayer(user).withContest(contest).withId(UUID.randomUUID().toString()).withTimestampOfCreation(LocalDateTime.now()).build()` in EnterCustomImplementation.

### RackInspect
Used heavily across fault registry, offer, and item services. ExchangeRate creation: `ExchangeRateForCreate.builder().withCurrency(currency).withRate(rate).withRecordingMethod(RecordingMethod.AUTO).withSource("MNB").build()`. Also used in test infrastructure via `TestDataBuilder`.

### itracker
Model scripts use equivalent builder pattern: `new Initiative(title, source, location, ...)`, `new MonthlyForecast(month=0..11, savingPotential=input.monthlySavingPotential)`, `new ForecastVersion(timestamp=Timestamp!now(), ...)`. The model-script `new` keyword compiles to the same ForCreate builder under the hood.

### ALBA
Extensive builder usage for Products (15+ fields including relations to audiences, curriculums, result types), ProductVersions, Events, Tasks, and UserTransfer. Builders set collection relations inline: `.withResultTypes(resultTypes).withAudience(audiences).withCurriculum(curriculums).withAttachments(attachments)`.

### mlszksz-platform
Uses `.create()` static factory method instead of `.builder()`: `AuditLogForCreate.create()` then setter methods (`setActionType()`, `setEntityType()`, `setTimestamp()`). Also used in services: `OfferForCreate.create()` with setters for title, description, validFrom, validUntil, status, organization, author, capabilities. Both `.builder()` and `.create()` + setters patterns observed.

### judo-demo-miniworkflow
Model scripts use the `new` keyword for entity creation which compiles to builder pattern: `new DocumentTransfer(referenceNumber = input.referenceNumber, owner = owner)`, `new DocumentHistoryEntry(fromState = this.currentState, toState = DocumentState#ACCEPTED, eventTime = Timestamp!now(), user = currentUser, message = input.message)`, `new GenericUser(firstName = "Admin", email = "admin@example.org", approver = true, admin = true, active = true)`.

### Ubives
Builder used for all entity creation: `AccountForCreate.builder().withUserName(username).build()` in JIT provisioning, `AccountPrincipalForCreate.builder().withUserName("admin").withIsSuperAdmin(true).withEmail(mail).withIdentity(identity).build()` in init seeding, `InvitationEntityForCreate.builder().withInvitationType(type).withEmail(email).withExpiration(LocalDateTime.now().plusMonths(1)).build()` with nested relation creation. Nested builder: `withIdentity(identityDao.create(IdentityForCreate.builder().withEmail(email).build()))`.

### ParkHere
Builders used for all entity creation across 20+ operations: `CarForCreate.builder().withLicensePlate().withManufacturer().withModel().withIsFavorite().build()`, `ConfigurationForCreate.builder()` with 6 email template/email fields, `DoormanForCreate.builder().withEmail().withAssignedGarages(garageList)`, `ParkingSlotForCreate.builder().withParkingGarage().withFloor().withId().withIsExclusive().withFloorPlan()`. Also uses `FileType.builder()` for file references in Init seeding.

### Indamedia-AdTrack
Builders used for user creation in JIT provisioning: `UserForCreate.builder().withEmail(email).withName(name).withIsAdmin(isAdmin).build()`. Services use builders for campaign-related entities: `AvailableCampaignForCreate`, `AggregatedCampaignForCreate`, `TrackedCampaignForCreate`, `CostForCreate`, `FetchedDataForCreate`, `AggregatedCampaignHistoryForCreate`. Google credential creation: `GoogleCredentialForCreate.builder().withJsonKeyFile(fileType).withCustomerId().withDeveloperToken().build()`.

### judo-partner
Builders used for partner creation with 8+ fields: `PartnerForCreate.builder().withPartnerCode(code).withName(name).withNormalizedName(name).withTaxNumber(num).withTaxNumberType(type).withTaxIdentifier(id).withValidationStatus(OK).build()`. Also used for audit logs: `PartnerLogForCreate.builder().withPartner(partner).withType(LogType.CREATE).withUserEmail(email).build()`. Relation-based creation for addresses and contacts via `partnerDao.createAddresses()` and `partnerDao.createContacts()`.

### workflow-poc
Builders used extensively for workflow entities: `ContextForCreate.builder().withWorkflow(version).withType(contextType).withIdentifier(id).build()`, `TokenForCreate.builder().withContext(context).withTokenID(UUID.randomUUID().toString()).build()`, `WorkflowVersionForCreate.builder().withLabel(label).withWorkflow(workflow).withVersionNumber(num).withRole(role).build()`, `EventForCreate.builder().withEventID(eventID).withCorrelationID(correlationId).build()`, and `LogEntryForCreate.builder().withType(type).withLevel(level).withMessage(message).build()`.

## Trade-offs

- Pros: Immutable creation contract, compile-time field validation, clean fluent API, relations set declaratively
- Cons: Different type from the read/update entity type (cannot reuse), no partial creation support
- Alternative: None within JUDO -- this is the only supported creation pattern

## Related Patterns

- dao-fluent-query-filter
- relation-based-entity-creation
