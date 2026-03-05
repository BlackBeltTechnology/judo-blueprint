---
id: "mapped-operation-delegation"
title: "Mapped Operation Delegation Pattern"
domain: "model"
category: "operation"
score: 185.0
usage_count: 13
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - itracker
  - skillmatrix-frontend
  - alba
  - skillmatrix-model
  - viterra_demo
  - kozut-eugyfel-client
  - judo-demo-miniworkflow
  - ams-model
  - kozut-eugyfel-model-test
  - workflow-poc
  - ams-frontend
---
## Description

Transfer-level operations use the MAPPED type to delegate to their corresponding entity-level operations. This creates a clean separation where the entity defines the business logic and the transfer layer defines the API contract visible to each actor, potentially with actor-specific input/output types.

## Structure

- Entity defines INSTANCE operations with business logic
- Transfer object defines MAPPED operations that bind to entity operations
- MAPPED operations may use different (actor-specific) input/output transfer types
- Static operations on transfers may have their own bodies or be custom-implemented

## Examples

### Trivia
`admin::Question.approve` (MAPPED) delegates to `Question.approve` (INSTANCE). `player::Contest.enter` (MAPPED) delegates to `Contest.enter` with actor-specific types: input `RegisterInput`, output `player::Test`, fault `player::Error`. 11 MAPPED operations total across admin and player actors.

### RackInspect
116 service-level transfer operations delegate to 40 entity-level operations. Toggle operations like `toggleActive`, `togglePrimary` on service TOs map to entity-level toggles. Complex operations like `generateAssessmentSheet`, `generateOffer` are exposed through `fault_registry_services::FaultRegistry` transfer.

### itracker
4 MAPPED operations on `user::Initiative`: `archiveForecast`, `sendForApproval`, `approve`, `reject` -- all delegate to corresponding entity-level operations with empty transfer-level bodies. Additionally, `createInitiative` is a STATIC operation with its own body (not MAPPED), constructing entities and pre-populating 12 monthly forecasts.

### SkillMatrix
9+ MAPPED operations across 3 actors: `Subordinate.approveAllSkills` -> `User.approveAllSkills`, `Skill.approve` -> `Skill.approve`, `TrainingPlan.close/open` -> `TrainingPlan.close/open`, `ReportDefinition.run` -> `Definition.run`. The same entity operation (e.g., `User.approveAllSkills`) is exposed to different actors through different transfer objects.

### Alba
15 service-level operations delegate to 9 entity operations. Same operation exposed to multiple roles: `Product.approveVersion()` mapped via `AdminProduct.approveVersion()`, `ApproverProduct.approveVersion()`, and `AuthorProduct.approve()` (renamed). `Task.closeTask()` mapped via both `AuthorTask.closeTask()` and `ApproverTask.closeTask()`. `Task.activate/deactivate()` mapped only to `AdminTask` (admin-restricted).

### SkillMatrix-Model
Model source confirms MAPPED operations including `deleteUser` (binding="deleteUser"), plus custom-implemented STATIC operations like `createTestData` (`customImplementation="true"`). Entity operations `approve`, `approveAllSkills`, `approveAllSubordinatesSkills`, `createTrainingPlan`, `completeAllTargets` all have corresponding MAPPED transfers across actor packages.

### Viterra Demo
3 MAPPED operations delegate to 3 entity operations: `ReportTransfer.accept()` -> `Report.accept()`, `ReportTransfer.review()` -> `Report.review()` (both admin), `PartnerOpenReportTransfer.submit()` -> `Report.submit()` (partner). The submit operation returns `PartnerClosedReportTransfer` enabling automatic UI navigation from open to closed report view after state change.

### KozutEugyfelClient
13 entity operations on `Bejelentes` delegate to transfer-level operations: `tovabbitas` (forward), `lezaras` (close), `megnyitas` (reopen), `megjegyzes` (comment), `hozzaadResztvevo` (add participant), `leiratkozas` (unsubscribe). Input DTOs like `Tovabbitas`, `Lezaras`, `Megjegyzes` wrap operation-specific parameters. The `Ertesites.elolvas` (mark-as-read) maps a simple parameterless entity operation.

### judo-demo-miniworkflow
4 MAPPED operations on `DocumentTransfer` delegate to `Document` entity operations: `accept`, `close`, `reject`, `requestReview`. All take `Message` as input (a transient DTO with optional message text). The mapped operations have empty bodies -- all business logic (creating `DocumentHistoryEntry`, resolving current user, setting state) lives in the entity operations.

### AMS-Model
6 MAPPED operations on manager transfer objects: `manager::Request.approve` and `manager::Request.reject` delegate to `Request.approve()` / `Request.reject()` entity operations (which set `status` and `decisionTime`). `manager::Campaign.open` / `manager::Campaign.close` delegate to `Campaign.open()` / `Campaign.close()` (toggle CampaignStatus). `User.approveAll` iterates `this.approvals!filter(r | r.status == Status#PENDING)` and calls `request.approve()` on each.

### KozutEugyfelModelTest
Each actor's `IntezendoBejelentes` TO exposes 3 MAPPED operations delegating to `Bejelentes` entity operations: `lezaras` (close complaint), `megjegyzes` (add comment), `tovabbitas` (forward complaint). All three actors share the same operation mappings, providing identical functionality through actor-scoped transfer objects with shared input DTOs from `KozosTransferObjectek`.

### workflow-poc
9 MAPPED operations on transfer objects delegate to entity operations: `TaskList.startWorkflow` -> `User.startWorkflow`, `Task.checkout/release/assign/execute/navigate` -> `Token.checkout/release/assign/execute/navigate`, `admin::Workflow.upload` -> `Workflow.upload`, `admin::WorkflowVersion.commit` -> `WorkflowVersion.commit`. The `upload` operation also exposes a fault type `DeclarationError` for invalid workflow definitions.

### AMS-Frontend
6 MAPPED operations: `manager::Request.approve/reject` delegate to `Request.approve()/reject()` (set status + decisionTime), `admin::Campaign.open/close/load` delegate to `Campaign.open()/close()/load()`, and `manager::ManagerApprovalList.approveAll` delegates to `User.approveAll()` (iterates pending approvals).

## Trade-offs

- Pros: Business logic centralized on entities, actors get tailored API signatures, clean layering
- Cons: Additional indirection layer, must keep entity and transfer operation signatures in sync
- Prefer when: Always for operations that have entity-level implementations -- this is the standard delegation pattern

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [custom-implementation-placeholder](custom-implementation-placeholder.md)
