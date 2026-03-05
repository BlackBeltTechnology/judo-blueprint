---
id: "generalization-base-entity"
title: "Generalization Base Entity for Shared Infrastructure"
domain: "model"
category: "entity"
score: 144.9
usage_count: 8
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - mlszksz-platform
  - ams-model
  - indamedia-adtrack
  - InterfaceRegister
  - kozut-eugyfel-model-test
  - workflow-poc
  - ams-frontend
alternatives:
  - flat-entity-model
---
## Description

A base entity provides shared attributes and relations (timestamps, document management, user assignment, audit history) that are inherited by multiple concrete entity types via generalization. This avoids duplicating common infrastructure across entities that share the same workflow base. It is an alternative to the flat entity model where each entity defines its own attributes independently.

## Structure

- Base entity defines common attributes (e.g., `created`, `modified`, `registryNumber`)
- Base entity defines common relations (e.g., `documents [0..*]`, `assignedTo -> User`, `history [0..*]`)
- Concrete entities extend the base and add domain-specific attributes and relations
- Base entity may be abstract (`abstract: true`) or non-abstract
- Typically used for workflow/task entities that share lifecycle infrastructure

## Examples

### RackInspect
`Task` base entity (3 attributes: `created`, `modified`, `registryNumber`; 4 relations: `documents`, `lastDocument`, `assignedTo`, `history`) is extended by 6 concrete entities: `FaultRegistry` (status, facility, fault headers), `Offer` (costs, versioning, items), `JobSheet` (work status, items), `WorkReport` (start/end times, workers), `AssessmentSheet` (name, generated date), `ReviewReport` (expire date, pictures).

### MLSZKSZPlatform
`Post` abstract base entity (attributes: `title`, `description`, `status: PostStatus`, `createdAt: Timestamp`) is extended by 4 concrete entities: `News` (no additional attributes), `Offer` (`validFrom`, `validUntil` date range), `Request` (`deadline` date), `Announcement` (`isSensitive`, `isStrategic` boolean flags, `documents` relation). All subtypes share the common `publish`/`delete` operations and PostStatus lifecycle. The abstract base enables polymorphic feed queries via FeedEntry.post [0..1] -> Post.

### AMS-Model
`Request` (abstract) defines 12 shared attributes (`applicationName`, `userName`, `userEmail`, `responsibleName`, `roles`, `status`, `loginName`, `effectiveDate`, `isPending`, `creationTime`, `decisionTime`, `type`) and 2 relations (`application [1..1]`, `user [1..1]`), plus 3 operations (`approve`, `reject`, `reset`). Extended by `ConfirmationRequest` (adds `approver [1..1]` relation and derived `campaignStatus`) and `AccessRequest` (adds `issuer [1..1]` relation). The abstract base holds all common request workflow infrastructure.

### IndamediaAdTrack
`Credential` base entity (0 attributes, 1 relation: `account [1..1]`) is extended by `GoogleCredential` (4 platform-specific attributes: `customerId`, `delegatedAccount`, `jsonKeyFile`, `developerToken`) and `MetaCredential` (0 attributes -- incomplete). Demonstrates a strategy pattern where the base holds only the shared account association, and subtypes carry platform-specific credential data for multi-platform API integration.

### InterfaceRegister
`InterfaceSpecification` as a non-abstract base entity with 6 shared attributes (`id`, `name`, `description`, `linkToTheSpecification`, `specificationDocument`, `directionOfTransmission`). Extended via a 2-level hierarchy: first level `AsynchronCommunication` (extends InterfaceSpecification, no additional attributes), `DBLink`, `Rest` (adds `linkToOpenApiSpecification`, `openApiDocument`), `SOAP` (adds `WSDLDocument`, `linkToWSDLSpecification`). Second level: `Email`, `FileTransfer`, `MessageQueue` all extend `AsynchronCommunication`. This is the deepest generalization hierarchy observed across all projects (3 levels).

### KozutEugyfelModelTest
Three parallel generalization hierarchies: **Bejelentes** (base with 5 shared attributes) extended by `JarokeloBejelentes` and `EUgyfelszolgalatBejelentes`. **Esemeny** (abstract event base) extended via intermediate `UgyintezoBeallitas` (abstract, adds `celFelhasznalo`) into `Tovabbitas` and `Letrehozas`, plus direct children `Lezaras` and `Megjegyzes`. **Felhasznalo** (abstract user) with intermediate `FelelosFelhasznalo` (abstract) grouping `SzervezetiEgysegVezeto` and `UgyfelszolgalatiMunkatars`, plus a direct child `SzervezetiEgysegMunkatars`.

### workflow-poc
`Action` entity serves as a strategy/plugin base for the workflow engine. It defines a single `actionID` attribute and a `run(input: ActionInput)` instance operation. Three test subtypes extend it: `Action1`, `Action2`, and `InitDocumentWorkflow`, each overriding `run` with specific behavior (e.g., setting context labels). The `actionID` acts as a discriminator for looking up the correct Action implementation at runtime.

### AMS-Frontend
Abstract `Request` base entity with 12 attributes (including 5 derived), 2 mandatory relations, and 3 operations (`approve`, `reject`, `reset`). Extended by `ConfirmationRequest` (adds `approver [1..1]` and derived `campaignStatus` via container navigation) and `AccessRequest` (adds `issuer [1..1]`). Both subtypes inherit the full approval workflow from the base.

## Trade-offs

- Pros: DRY principle for common infrastructure, consistent audit trail across entities, single place to add shared fields
- Cons: Inheritance hierarchy adds complexity, all subtypes must conform to base contract, polymorphic queries may be needed
- Prefer when: Multiple entities share the same workflow infrastructure (timestamps, documents, user assignment)

## Related Patterns

- [flat-entity-model](flat-entity-model.md) (alternative: no inheritance)
- [enum-state-machine](enum-state-machine.md)
