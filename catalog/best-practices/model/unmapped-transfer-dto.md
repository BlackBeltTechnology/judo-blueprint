---
id: "unmapped-transfer-dto"
title: "Unmapped Transfer Object (DTO) Pattern"
domain: "model"
category: "transfer"
score: 77.4
usage_count: 12
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
  - judo-demo-miniworkflow
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
---
## Description

Unmapped transfer objects have no entity mapping and serve as standalone data containers for operation inputs, outputs, and fault types. They are used when the data structure does not correspond to any persisted entity -- typically for API request/response payloads, error objects, and parameter wrappers.

## Structure

Common unmapped DTO categories:
- **Operation input**: Captures user input for an operation (e.g., `RegisterInput`, `Credential`)
- **Operation output**: Wraps operation results (e.g., `PromptList`)
- **Error/fault type**: Carries error information (e.g., `Error` with `message` + `code` enum)
- **Data container**: Holds binary or structured data (e.g., `JsonData` with a binary JSON field)
- **ID wrapper**: Simple wrapper for a single identifier (e.g., `TestId`)
- **Transient report row**: Denormalized data for report generation (no persistence)

Naming conventions for unmapped DTOs:
- `*Input` suffix for creation/operation inputs
- `*Update` suffix for modification inputs
- `*Data` suffix for read-only data containers
- `*Output` suffix for operation results

## Examples

### Trivia
Seven unmapped DTOs: `admin::JsonData` (JSON container for upload/download), `player::RegisterInput` (email + name), `player::Answer` (number + choice), `player::AnswerList` (transient answer collection), `player::Error` (message + ErrorCode enum), `player::TestId` (ID wrapper), `player::Credential` (email + code for activation).

### RackInspect
40+ unmapped DTOs across service packages following consistent suffixes: `FaultRegistryInput`, `ElementFaultInput`, `CostPriceInput` (creation), `CostPriceUpdate`, `OfferItemUpdate`, `PriceModifierInstanceUpdate` (modification), `CostPriceData`, `PriceModifierData` (read-only), `PreviewOutput` (results), `EmailInput`, `FaultRegistryEmailInfo` (email integration), `BusinessError` (fault type).

### itracker
Single unmapped DTO: `InititativeInput` for the `createInitiative` operation. Contains 8 required attributes (location, title, source, enum defaults, numeric defaults, date default) plus 2 transient relations (region, category with `!any()` defaults). Demonstrates a compact input DTO with comprehensive defaults for all fields.

### SkillMatrix
`report::Competence` is a transient/unmapped transfer object with all TRANSIENT attributes (`user`, `unit`, `competence`, `tag`, `score`, `level`). Used as an intermediate denormalized row during the report generation pipeline, populated in the `Definition.run` operation body and passed to the Excel generation custom implementation.

### ActionGroupTest
3 unmapped DTOs: `CreatureTemplate` (transient name + required id, plus transient signs relation for creature creation), `MatterCreator` (transient mass + shortNote for Galaxy matter creation operations), `Message` (transient message string for creature-God communication as both input and output).

### Alba
3 transient/unmapped DTOs: `ApprovalTaskInput` (transient relation `users` with derived range filtering active TEACHER/APPROVER users), `CloseTaskInput` (transient `result` attribute of type TaskState), `TeacherAccountFinalizationForm` (profile completion data). Also form-specific TOs: `AuthorProductForm` and `AdminProductForm` for product creation input.

### SkillMatrix-Model
Transient report DTO `report::Competence` confirmed with all-transient attributes for denormalized report rows. The `ResultHelper` transfer serves as a utility view for report result handling. The model uses minimal unmapped DTOs compared to its transfer object count (37 total), relying primarily on mapped transfers with selective attribute projection rather than standalone input/output DTOs.

### KozutEugyfelClient
5 unmapped operation input DTOs: `Lezaras` (szoveg + lezaroDokumentum for closing), `Megjegyzes` (szoveg for comments), `Tovabbitas` (mapped to TovabbitasAction with szoveg), `Megnyitas` (szoveg for reopening), `Resztvevo` (mapped to ResztvevoAction for adding participants). Also `EmailKuldo` and `Alkalmazas` as utility DTOs. Demonstrates minimal, purpose-built input DTOs per operation.

### judo-demo-miniworkflow
2 unmapped DTOs: `Message` (single optional `message: Text` attribute, used by all 4 workflow operations as a comment container) and `NewDocument` (single optional `referenceNumber: String`, used by `createDocument` factory). Both are minimal transient types with no entity mapping, demonstrating the pattern of one shared input DTO reused across multiple operations.

### ParkHere
8+ unmapped input DTOs: `CreateCarInput`, `ModificationCarInput` (car CRUD), `ReservationInput`, `ReservationModificationInput` (reservation CRUD), `HolidayInput` (holiday creation with user selection and affected reservation preview), `ConfigurationInput` (global settings update), `DoormanInput` (doorman creation), `AdditionalDayInput` (calendar override). Also `BusinessError` as a fault DTO with `message` + `errorCode` enum. `QueryReservationsForHolidayOperationResult` as an output DTO for preview operations.

### IndamediaAdTrack
9 unmapped input DTOs: `ClientInput`, `ClientUpdateInput`, `AccountInput`, `AccountUpdateInput`, `GoogleCredentialInput`, `AggregatedCampaignCreateInput`, `AggregatedCampaignUpdateInput`, `TrackedCampaignUpdateInput`, `CostInput`. Plus `BusinessError` as the unified fault DTO and `CostInfo` as a summary data container. Demonstrates consistent `*Input`/`*UpdateInput`/`*CreateInput` naming for create vs update operations.

### InterfaceRegister
7+ unmapped input DTOs forming a nested hierarchy for complex creation operations: `CreateApplicationInput` (4 transient attributes + nested `CreateApplicationVendorInput`), `CreateHighLevelConnectionInput` (12 transient attributes + 6 nested input relations including `CreateHighLevelConnectionApplicationInput`, `CreateHighLevelConnectionBrandInput`, `CreateHighLevelConnectionBusinessDataTypeInput`, `CreateHighLevelConnectionVendorInput`), `CreateUserInput` (8 transient attributes with boolean access flags defaulting to false). Nested input DTOs use derived attributes with `self.*` getters for pre-populating from selected entities.

### judo-partner
3 unmapped input DTOs: `CreatePartnerInput` (flat fields combining partner + address + contact data for creation), `PartnerImportInput` (JSON payload field for bulk partner import), `CountryImportInput` (JSON payload field for country reference data import). The JSON-typed inputs demonstrate a pattern of accepting raw structured data for batch processing operations.

### KozutEugyfelModelTest
7 unmapped input DTOs in the shared `KozosTransferObjectek` and domain packages: `TovabbitasInput` (szoveg + felhasznalo relation for forwarding), `SzovegInput` (szoveg for closure), `MegjegyzesInput` (szoveg + ertesitendok notification list), `JarokeloBejelentesInput` (6 fields for pavement report creation), `EUgyfelszolgalatBejelentesInput` (7 fields for e-gov report creation), `EmailKuldesInput` (single-recipient email), `EmailKuldesTobbCimzettInput` (multi-recipient email with composed `Cimzett` list).

### workflow-poc
11 unmapped DTOs across public and admin namespaces: `Event` (eventID + correlationID for trigger input), `ContextInput` (context creation parameters), `ActionInput` (tokenID + correlationID for action execution), `Identifier` (simple value wrapper), `WorkflowDiagram` (diagram data), `YamlData` (YAML payload), `CreateURLInput` (address + workflow relation). Admin DTOs: `UploadInput` (YAML upload), `CommitInput` (comment for commit), `DeclarationError` (fault DTO with DeclarationErrorCode enum + message). Also `test::DocumentInfo` for test document creation.

## Trade-offs

- Pros: Clean operation signatures, no persistence overhead, purpose-built for each operation
- Cons: More transfer types to maintain, may proliferate for complex APIs
- Prefer when: Operation input/output does not map to a single entity, or for error/fault types

## Related Patterns

- [transient-relation-parameter](transient-relation-parameter.md)
- [actor-based-transfer-projection](actor-based-transfer-projection.md)
